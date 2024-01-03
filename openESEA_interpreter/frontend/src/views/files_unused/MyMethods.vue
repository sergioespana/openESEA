<template>
    <Toolbar>
        <template #left>
            <div v-if="(networkMethods && permission)">
                <div v-if="!addingProcess">
                        <Button label="Create Method" icon="pi pi-plus" class="p-button-success p-mr-2" @click="importDialog = true" />
                        <ToggleButton v-if="selectionEnabled" v-model="selectionToggle" onLabel="Selecting: Enabled" offLabel="Selecting: Disabled" onIcon="pi pi-check" offIcon="pi pi-times" class="p-mr-2" />
                        <Button label="Add Methods" icon="pi pi-plus" class="p-button-success p-mr-2" @click="addableMethods()" />
                        <Button label="Remove Methods" icon="pi pi-trash" class="p-button-danger" @click="confirmationDialog = true" :disabled="!selectedRows.length" />
                </div>
                <div v-else>
                    <Button label="Show network methods" class="p-button-success p-mr-2" @click="initialize()" />
                    <Button label="Add selected Methods" class="p-button-primary p-mr-2" @click="confirmationDialog = true" :disabled="!selectedRows.length" />
                </div>
            </div>
            <div v-if="!networkMethods">
                <Button label="Create Method" icon="pi pi-plus" class="p-button-success p-mr-2" @click="importDialog = true" />
            </div>
        </template>

        <template #right>
            <span class="p-input-icon-left">
                <i class="pi pi-search" />
                <InputText v-model="filters['global']" placeholder="Search..." />
            </span>
        </template>
    </Toolbar>
    <div v-if="methods.length">
        <DataTable ref="dt" :value="methods" v-model:selection="selectedRows" :selectionMode="selectionToggle? 'multiple' : 'single'" dataKey="id" :metaKeySelection="false" @row-select="goToSelectedMethods"
            :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
            :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

            <Column field="ispublic" header="Public" headerStyle="width: 5rem">
                <template #body="slotProps">
                    <i class="pi p-text-center p-text-bold" style="width:100%; font-size: 20px;" :class="{'true-icon pi-check': slotProps.data.ispublic, 'false-icon pi-times': !slotProps.data.ispublic}" :style="(slotProps.data.ispublic ? 'color: green;':'color: red;')"></i>
                </template>
            </Column>
            <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field">
            </Column>
            <Column headerStyle="width: 8rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                <template #body="{data}">
                    <Button v-if="data.created_by === this.currentuser" label="Update" class="p-button-sm" @click="updateMethod(data)"  style="width: 100px" />
                </template>
            </Column>
            <Column headerStyle="width: 5rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                <template #body="{data}">
                    <Button v-if="data.created_by === this.currentuser" icon="pi pi-trash" class="p-button-danger p-button-sm" @click="(selectedMethod = data) && (destroyMethodDialog = true)" style="width: 50px" />
                </template>
            </Column>
        </DataTable>
    </div>
    <div v-else class="p-p-3 p-text-bold"> {{addingProcess? 'There are no methods to add, create one first!' : 'This network has no methods, add one!'}}</div>

    <Dialog v-model:visible="confirmationDialog" :style="{width: '450px'}" header="Confirm" :modal="true">
      <div class="confirmation-content">
          <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 2rem" />
            <span v-if="networkMethods">Are you sure you want to <b>{{addingProcess? 'add' : 'remove'}}</b> the following methods?</span>
            <span v-else>Are you sure you want to <b>delete</b> the following methods?</span>
            <br>
            <div class="p-shadow-2 p-m-3 p-p-3">
            <div v-for="item in selectedRows" :key=item.name>{{item.name}}</div>
            </div>
      </div>
      <template #footer>
        <Button label="No" icon="pi pi-times" class="p-button-text" @click="(confirmationDialog = false) && (selectedRows = [])"/>
        <Button v-if="networkMethods" label="Yes" icon="pi pi-check" class="p-button-text" @click="addingProcess? addMethods() : removeMethods()" />
        <Button v-else label="Yes" icon="pi pi-check" class="p-button-text" @click="deleteMethods()" />
      </template>
    </Dialog>

    <Dialog v-model:visible="importDialog" :style="{width: '1400px'}" header="Create New Method" :modal="true">
        <div class="p-grid p-text-center p-m-5">
        <div class="p-col-5 p-p-0" style="border: 1px solid lightgrey; border-radius: 5px;">
            <h3>Upload a model</h3>
            <p class="p-m-5 p-text-justify">Pick this option if you have a .yaml file which can be used as a model. You can modify this later through the editor.</p>
        <FileUpload name="myfile" :customUpload="true" @uploader="onUpload" :fileLimit="1" accept=".yaml" :maxFileSize="10000000">
            <template #empty>
                <p>Drag and drop your YAML file here to upload.</p>
            </template>
        </FileUpload>
        </div>
        <div class="p-col" />
        <div class="p-col-5 p-p-0" style="border: 1px solid lightgrey; border-radius: 5px;">
            <h3>Create a model</h3>
            <p class="p-p-5 p-text-justify ">Pick this option if you don't have a model that can be imported directly. You'll be able to create the method manually.</p>
            <Button label="Start Method Creation" @click="createNewMethod()" class="p-button-lg p-m-5" />
        </div>
        </div>
        <template #footer>
            <Button label="Remove window" icon="pi pi-times" class="p-button-text" @click="importDialog = false"/>
        </template>
    </Dialog>

    <Dialog v-model:visible="destroyMethodDialog" :style="{width: '450px'}" header="Confirm" :modal="true">
        <div class="confirmation-content">
            <i class="pi pi-exclamation-triangle p-mr-3" style="font-size:1.5rem" />
            <span>Are you sure you want to delete <b>{{selectedMethod.name}}</b>?</span>
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" class="p-button-text" @click="destroyMethodDialog = false"/>
            <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="destroyMethod()" />
        </template>
    </Dialog>
</template>

<script>
import { AxiosInstance } from '../../plugins/axios'
import { mapActions, mapState } from 'vuex'

export default {
    props: {
        columns: {
            type: Array,
            default: function () {
                return [
                    { field: 'name', header: 'Name' },
                    { field: 'description', header: 'Description' },
                    { field: '', header: '' }
                ]
            }
        },
        networkMethods: {
            type: Boolean,
            default: false
        },
        selectionEnabled: {
            type: Boolean,
            default: false
        }
    },
    data () {
        return {
            permission: false,
            filters: {},
            selectedRows: [],
            selectionToggle: false,
            addingProcess: false,
            confirmationDialog: false,
            destroyMethodDialog: false,
            importDialog: false,
            selectedMethod: {}
        }
    },
    computed: {
        ...mapState('method', ['methods', 'method']),
        ...mapState('network', ['network']),
        ...mapState('authentication', ['currentuser'])
    },
    created () {
        this.permission = this.network.created_by === this.currentuser
        this.initialize()
    },
    methods: {
        ...mapActions('method', ['fetchMethods', 'setMethod', 'createMethod', 'uploadMethod', 'deleteMethod']),
        ...mapActions('network', ['patchNetwork']),
        async initialize () {
            if (this.networkMethods) {
                console.log('eee')
                this.fetchMethods({ query: `?network=${this.network?.id || 0}` })
            } else {
                this.fetchMethods({})
            }
            this.selectedRows = []
            this.confirmationDialog = false
            this.addingProcess = false
        },
        addableMethods () {
            this.fetchMethods({ query: `?excludenetwork=${this.network?.id || 0}` })
            this.addingProcess = true
            this.selectionToggle = true
        },
        async addMethods () {
            if (this.selectedRows.length) {
                var newListOfMethods = []
                this.selectedRows.forEach(method => newListOfMethods.push(method.name))
                newListOfMethods = this.network.methods.concat(newListOfMethods)
                console.log('+++++', newListOfMethods)
                await this.patchNetwork({ methods: newListOfMethods })
            }
            this.initialize()
        },

        async removeMethods () {
            if (this.selectedRows.length) {
                var newListOfMethods = []
                this.selectedRows.forEach(method => newListOfMethods.push(method.name))

                newListOfMethods = this.network.methods.filter((item) => !this.newListOfMethods.includes(item))
                await this.patchNetwork({ methods: newListOfMethods })
                this.selectedRows.forEach((method, i) => {
                    this.$toast.add({ severity: 'success', summary: 'The following method was removed', detail: `${method.name}`, life: 3000 })
                })
            }
            this.initialize()
        },
        async deleteMethods () {
            await this.selectedRows.forEach((method, i) => {
                this.deleteOrganisation({ id: method?.id || 0 })
                this.$toast.add({ severity: 'success', summary: 'The following method was deleted', detail: `${method.name}`, life: 3000 })
            })
        },
        async destroyMethod () {
            await this.deleteMethod({ id: this.selectedMethod.id })
            this.destroyMethodDialog = false
            this.$toast.add({ severity: 'success', summary: 'The following method was deleted', detail: `${this.selectedMethod.name}`, life: 3000 })
            this.selectedMethod = {}
            this.initialize()
        },
        async onUpload (event) {
            // for (const file of event.files) {
            //     console.log(file)
            // }
            var formData = new FormData()
            formData.append('file', event.files[0])
            return new Promise((resolve, reject) => {
            AxiosInstance.post('/import-yaml/', formData)
            .then(response => {
                this.importDialog = false
                this.$toast.add({ severity: 'success', summary: 'Method created', detail: 'New method', life: 3000 })
                this.initialize()
            resolve()
            })
            .catch(err => { reject(err) })
            })
        },
        async goToSelectedMethods (event) {
            this.$toast.add({ severity: 'info', summary: 'Method Selected', detail: `${event.data.name}`, life: 3000 })
            if (!this.selectionToggle) {
                await this.setMethod({ ...event.data })
                this.$router.push({ name: 'newmethoddetails', params: { id: event.data.id } })
                // this.$router.push({ name: 'methoddetails', params: { id: event.data.id } })
                // this.$router.push({ name: 'networkmethod', params: { NetworkId: this.network.id, MethodId: this.method.id } })
            }
       },
       async updateMethod (method) {
           await this.setMethod(method)
            this.$router.push({ name: 'method-create', params: { id: method.id } })
       },
       async createNewMethod () {
           await this.createMethod({})
           this.$router.push({ name: 'method-create', params: { id: this.method.id } })
       }
    }
}
</script>
