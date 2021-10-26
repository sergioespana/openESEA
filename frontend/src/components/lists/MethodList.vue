<template>
    <list-bar v-model:tabledisplay="tableDisplay" v-model:allitems="allMethods" :includecheckbox="!networkmethods" v-model:search="customSearch" name="Methods">
        <slot></slot>
    </list-bar>
    <ProgressSpinner v-if="loading && !failedLoad" />
    <div v-else-if="loading && failedLoad" class="p-text-italic">Methods could not be retrieved</div>
    <div v-else-if="methods.length">
         <div v-if="tableDisplay" class="p-grid p-m-5" style="height: 500px;">
            <div v-for="method in filteredMethods" :key="method.id" class="p-col-12 p-md-6 p-lg-4" style="width: 300px; height: 200px; ">
                <div class="p-d-flex p-p-3" :class="method.hover ? 'p-shadow-2 p-m-1' : 'p-shadow-1 p-m-2'" style="height: 100%;" :style="(method.hover ? styleObject : '')" @mouseover="method.hover=true" @mouseleave="method.hover=false" @click.left="goTomethod(method)">
                    <!-- <img :src="method.image" alt="method Image" style="max-width: 150px; max-height: 150px; border-radius: 50%;" format="PNG" /> -->
                    <p class="p-as-center p-text-bold p-text-italic" style="width: 100%">{{method.name}}</p>
                </div>
            </div>
         </div>
        <DataTable v-else :value="filteredMethods"  dataKey="id" :loading="loading" selectionMode="single" @row-select="goTomethod" showGridlines autoLayout
        :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped"> <!-- p-datatable-sm -->

            <Column field="ispublic" header="Public" headerStyle="width: 5rem">
                <template #body="slotProps">
                    <i class="pi p-text-center p-text-bold" style="width:100%; font-size: 20px;" :class="{'true-icon pi-check': slotProps.data.ispublic, 'false-icon pi-times': !slotProps.data.ispublic}" :style="(slotProps.data.ispublic ? 'color: green;':'color: red;')"></i>
                </template>
            </Column>
            <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field" bodyStyle="" /> <!-- text-align: center; overflow: visible  contentStyle="width: 500px;" -->
            <Column field="created_by" header="Creator">
                <template #body="slotProps">
                    <div v-if="slotProps.data.created_by !== currentuser">{{slotProps.data.created_by}}</div> <div v-else class="p-text-bold">You</div>
                </template>
            </Column>

            <!-- <div v-if="networkmethods && permission"> -->
            <Column headerStyle="width: 15rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                <template #body="{data}">
                    <Button v-if="(data.created_by === this.currentuser && !networkmethods)" label="Update" class="p-button-sm p-mr-2" @click="updateMethod(data)"  style="width: 100px" />
                     <Button v-if="data.created_by === this.currentuser && !networkmethods" icon="pi pi-trash" class="p-button-danger p-button-sm" @click="(selectedMethod = data) && (destroyMethodDialog = true)" style="width: 50px" />
                    <div v-if="(networkmethods && permission)">
                        <Button v-if="importablemethods" label="Import Method" class="p-button-success p-button-sm" @click="importMethod(data)" />
                        <Button v-if="!importablemethods" label="Drop Method" class="p-button-danger p-button-sm" @click="dropMethod(data)" />
                    </div>
                </template>
            </Column>
            <!-- </div>
            <div v-else style="width: 0px;"><Column bodyStyle="width: 0rem;" /></div> -->
        </Datatable>
    </div>
    <div v-else class="p-text-italic">No methods to display!</div>
    <Dialog v-model:visible="destroyMethodDialog" :style="{width: '450px'}" header="Confirm Method Deletion" :modal="true">
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
    import { mapState, mapActions } from 'vuex'
    import ProgressSpinner from 'primevue/progressspinner'
    import ListBar from '@/components/lists/ListBar'

    export default {
        components: {
            ProgressSpinner,
            ListBar
        },
        props: {
            refresh: {
                type: Boolean,
                default: false
            },
            permission: {
                type: Boolean,
                default: false
            },
            importablemethods: {
                type: Boolean,
                default: false
            },
            networkmethods: {
                type: Boolean,
                default: false
            }
        },
        data () {
            return {
                customSearch: '',
                loading: true,
                failedLoad: false,
                tableDisplay: false,
                allMethods: false,
                destroyMethodDialog: false,
                selectedMethod: null,
                styleObject: { backgroundColor: '#EFEEEE', cursor: 'pointer' },
                columns: [
                    { field: 'name', header: 'Name' },
                    { field: 'description', header: 'Description' },
                    { field: 'surveys.length', header: 'Surveys' }
                ]
            }
        },
        computed: {
            ...mapState('authentication', ['currentuser']),
            ...mapState('method', ['methods', 'method']),
            filteredMethods () {
                return this.methods.filter(method => {
                    return (
                        method.name.toLowerCase().includes(this.customSearch.toLowerCase()) ||
                        method.description.toLowerCase().includes(this.customSearch.toLowerCase())
                    )
                })
            }
        },
        watch: {
            refresh: {
                immediate: true,
                handler () {
                    this.getMethods()
                }
            },
            allMethods () {
                this.getMethods()
            }
        },
        methods: {
            ...mapActions('method', ['fetchMethods', 'setMethod', 'deleteMethod']),
            async getMethods () {
                this.loading = true
                let query = ''
                setTimeout(() => { this.failedLoad = true }, 10000)
                if (this.networkmethods) {
                    if (this.importablemethods) {
                        query = `?excludenetwork=${this.$route.params.NetworkId}`
                    } else {
                        query = `?network=${this.$route.params.NetworkId}`
                    }
                } else {
                    if (this.allMethods) {
                    query = '?allmethods=1'
                    } else {
                        query = '?mymethods=1'
                    }
                }
                if (query.length) {
                    await this.fetchMethods({ query: query })
                }
                this.loading = false
                this.$emit('update: refresh', true)
            },
            async goTomethod (method) {
                if (method?.data) {
                    method = method.data
                }
                if (method.id) {
                    await this.setMethod(method)
                    this.$router.push({ name: 'newmethoddetails', params: { id: this.method.id } })
                }
            },
            importMethod (method) {
                this.$emit('import-method', method)
            },
            dropMethod (method) {
                this.$emit('drop-method', method)
            },
            async updateMethod (method) {
                await this.setMethod(method)
                this.$router.push({ name: 'method-general', params: { id: method.id } })
            },
            destroyMethod () {
                if (this.selectedMethod) {
                    this.deleteMethod({ id: this.selectedMethod?.id })
                }
                this.selectedMethod = null
                this.destroyMethodDialog = false
            }
        }
    }
</script>
