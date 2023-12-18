<template>
    <Toolbar>
        <template #left>
            <div v-if="networkOrganisations">
                <div v-if="!addingProcess">
                    <ToggleButton v-if="selectionEnabled" v-model="selectionToggle" onLabel="Selecting: Enabled" offLabel="Selecting: Disabled" onIcon="pi pi-check" offIcon="pi pi-times" class="p-mr-2" />
                    <Button label="Invite Organisations" icon="pi pi-plus" class="p-button-success p-mr-2" @click="addableOrganisations()" />
                    <Button label="Remove Organisations" icon="pi pi-trash" class="p-button-danger" @click="confirmationDialog = true" :disabled="!selectedRows.length" />
                </div>
                <div v-else>
                    <Button label="Show network organisations" class="p-button-success p-mr-2" @click="initialize()" />
                    <Button label="Add selected Organisations" class="p-button-primary p-mr-2" @click="confirmationDialog = true" :disabled="!selectedRows.length" />
                </div>
            </div>
            <div v-else>
                <Button label="Create Organisation" icon="pi pi-plus" class="p-button-success p-mr-2" @click="createDialog = true" />
                <!-- <Button label="Delete Organisation" icon="pi pi-trash" class="p-button-danger" @click="confirmationDialog = true" :disabled="!selectedRows.length" /> -->
            </div>
        </template>
        <template #right>
            <span class="p-input-icon-left">
                <i class="pi pi-search" />
                <InputText v-model="filters['global']" placeholder="Search..." />
            </span>
        </template>
    </Toolbar>
    <div v-if="organisations.length">
        <DataTable ref="dt" :value="organisations" v-model:selection="selectedRows" :selectionMode="selectionToggle? 'multiple' : 'single'" dataKey="id" :metaKeySelection="false" @row-select="goToSelectedOrganisation"
        :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

        <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field">
            <template v-if="col.field === 'ispublic'" #body="slotProps">
            <i class="pi" :class="{'true-icon pi-check-circle': slotProps.data.ispublic, 'false-icon pi-times-circle': !slotProps.data.ispublic}"></i>
            </template>
        </Column>
        </Datatable>
    </div>
    <div v-else class="p-p-3 p-text-bold"> {{addingProcess? 'There are no organisations to add!' : 'This network has no organisations, add some!'}}</div>
    <Dialog v-model:visible="confirmationDialog" :style="{width: '450px'}" header="Confirm" :modal="true">
      <div class="confirmation-content">
          <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 2rem" />
            <span v-if="networkOrganisations">Are you sure you want to <b>{{addingProcess? 'add' : 'remove'}}</b> the following organisations?</span>
            <span v-else>Are you sure you want to <b>delete</b> the following organisations?</span>
            <br>
            <div class="p-shadow-2 p-m-3 p-p-3">
            <div v-for="item in selectedRows" :key=item.name>{{item.name}}</div>
            </div>
      </div>
      <template #footer>
        <Button label="No" icon="pi pi-times" class="p-button-text" @click="(confirmationDialog = false) && (selectedRows = [])"/>
        <Button v-if="networkOrganisations" label="Yes" icon="pi pi-check" class="p-button-text" @click="addingProcess? addOrganisations() : removeOrganisations()" />
        <Button v-else label="Yes" icon="pi pi-check" class="p-button-text" @click="deleteOrganisations()" />
      </template>
    </Dialog>

    <Dialog v-model:visible="createDialog" :style="{width: '450px'}" header="Organisation Details" modal="true" dismissableMask="true" class="p-fluid">
        <div class="p-field">
            <label for="name">Name</label>
            <InputText id="name" v-model.trim="organisationForm.name" required="true" autofocus :class="{'p-invalid': submitted && !organisationForm.name}" />
            <small class="p-error" v-if="submitted && !organisationForm.name">Name is required.</small>
        </div>
        <div class="p-field">
            <label for="description">Description</label>
            <Textarea id="description" v-model="organisationForm.description" required="true" rows="3" cols="20" />
        </div>
        <div class="p-field">
            <label for="ispublic">Should this organisation be public? </label>
            <SelectButton id="ispublic" v-model="organisationForm.ispublic" required="true" :options="ispublicbool" />
        </div>
        <template #footer>
            <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="createDialog = false" />
            <Button label="Save" icon="pi pi-check" class="p-button-text" @click="createNewOrganisation" :disabled="!organisationForm.name" />
        </template>
    </Dialog>

</template>
<script>
import { mapActions, mapState } from 'vuex'
export default {
    props: {
        columns: {
            type: Array,
            default: function () {
                return [
                    { field: 'ispublic', header: 'Public' },
                    { field: 'name', header: 'Name' },
                    { field: 'description', header: 'Description' },
                    { field: 'networks.length', header: 'Networks' },
                    { field: 'created_by', header: 'Created by' }
                ]
            }
        },
        networkOrganisations: {
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
            filters: {},
            selectedRows: [],
            selectionToggle: false,
            addingProcess: false,
            confirmationDialog: false,
            createDialog: false,
            submitted: false,
            ispublicbool: [true, false],
            boolChoice: null,
            organisationForm: {
                name: null,
                description: '',
                ispublic: true
            }
        }
    },
    computed: {
        ...mapState('organisation', ['organisations', 'organisation']),
        ...mapState('network', ['network'])
    },
    created () {
        this.initialize()
    },
    methods: {
        ...mapActions('organisation', ['fetchOrganisations', 'setOrganisation', 'createOrganisation', 'deleteOrganisation']),
        ...mapActions('network', ['patchNetwork']),
        async initialize () {
            if (this.networkOrganisations) {
                this.fetchOrganisations({ query: `?network=${this.network?.id || 0}` })
            } else {
                this.fetchOrganisations({})
            }
            this.selectedRows = []
            this.confirmationDialog = false
            this.addingProcess = false
        },
        addableOrganisations () {
            this.fetchOrganisations({ query: `?excludenetwork=${this.network?.id || 0}` })
            this.addingProcess = true
            this.selectionToggle = true
        },
        async addOrganisations () {
            await this.patchNetwork(this.selectedRows)
            this.initialize()
        },
        async removeOrganisations () {
            await this.patchNetwork(this.selectedRows)
            this.initialize()
        },
        async deleteOrganisations () {
            await this.selectedRows.forEach((organisation, i) => {
                this.deleteOrganisation({ id: organisation?.id || 0 })
            })
            this.$toast.add({ severity: 'success', summary: 'success', detail: 'organisations deleted', life: 3000 })
            this.initialize()
        },
        // async openCreateNetworkDialog () {
        //     await this.setOrganisation({})
        //     this.submitted = false
        //     this.createDialog = true
        // },
        async createNewOrganisation () {
            this.submitted = false
            if (this.organisationForm.name.trim()) {
                await this.createOrganisation({ data: this.organisationForm })
                this.$toast.add({ severity: 'success', summary: 'Organisation created', detail: `organisation: ${this.organisation.name}`, life: 3000 })
            this.createDialog = false
            this.submitted = true
            this.$router.push({ name: 'organisationoverview', params: { OrganisationId: this.organisation.id } })
            }
        },
        async goToSelectedOrganisation (event) {
            this.$toast.add({ severity: 'info', summary: 'Organisation Selected', detail: `${event.data.name}`, life: 3000 })
            if (!this.selectionToggle) {
                console.log(event.data)
                await this.setOrganisation({ ...event.data })
                console.log(this.organisation)
                this.$router.push({ name: 'organisationoverview', params: { OrganisationId: this.organisation.id } })
            }
        }
    }
}
</script>
