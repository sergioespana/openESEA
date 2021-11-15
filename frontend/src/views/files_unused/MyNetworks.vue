<template>
   <Toolbar>
        <template #left>
            <ToggleButton v-if="selectionEnabled" v-model="selectionToggle" onLabel="Selecting: Enabled" offLabel="Selecting: Disabled" onIcon="pi pi-check" offIcon="pi pi-times" class="p-mr-2" />
            <div v-if="!organisationNetworks">
                <Button label="Create Network" icon="pi pi-plus" class="p-button-success p-mr-2" @click="createDialog = true" />
                <Button label="Delete Network" icon="pi pi-trash" class="p-button-danger" @click="confirmationDialog = true" :disabled="!selectedRows.length" />
            </div>
            <div v-else>
                <div v-if="!addingProcess">
                <Button label="Join Network" icon="pi pi-plus" class="p-button-success p-mr-2" @click="addableNetworks()" />
                <Button label="Leave Network" icon="pi pi-plus" class="p-button-danger" @click="Dialog = true" :disabled="!selectedRows.length" />
                </div>
                <div v-else>
                    <Button label="Show owned networks" class="p-button-secondary p-mr-2" @click="initialize()" />
                    <Button label="request Network Participation" icon="pi pi-plus" class="p-button-success p-mr-2" @click="Dialog=true" :disabled="!selectedRows.length"/>

                </div>
            </div>
        </template>
        <template #right>
            <span class="p-input-icon-left">
                <i class="pi pi-search" />
                <InputText v-model="filters['global']" placeholder="Search..." />
            </span>
        </template>
    </Toolbar>
    <div v-if="networks.length">
        <DataTable ref="dt" :value="networks" v-model:selection="selectedRows" :selectionMode="selectionToggle? 'multiple' : 'single'" dataKey="id" :loading="loading" @row-select="goToSelectedNetwork"
        :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

        <template #loading>
            Loading records, please wait...
        </template>

        <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field" />
        </Datatable>
    </div>
    <div v-else class="p-p-3"><h3 class="p-text-light p-text-italic">There are no networks to display</h3></div>

    <Dialog v-model:visible="Dialog" :style="{width: '450px'}" header="Confirm" :modal="true">
        <div class="confirmation-content">
            <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 2rem" />
            <span>Are you sure you want to {{addingProcess? 'join': 'delete'}}: </span>
                <div v-for="network in selectedRows" :key="network.id">
                    <b>{{network.name}} </b>
                    </div>
        </div>?
        <template #footer>
            <Button label="No" icon="pi pi-times" class="p-button-text" @click="Dialog = false"/>
            <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="addOrRemoveNetworks()" />
      </template>
    </Dialog>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
    props: {
        columns: {
            type: Array,
            default: function () {
                return [
                    { field: 'ispublic', header: 'Public' },
                    { field: 'name', header: 'Name' },
                    { field: 'description', header: 'Description' },
                    { field: 'organisations.length', header: 'Organisations' },
                    { field: 'created_by.username', header: 'Created by' }
                ]
            }
        },
        organisationNetworks: {
            type: Boolean,
            default: false
        },
        query: {
            type: String,
            default: ''
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
            Dialog: false,
            loading: true
        }
    },
    computed: {
        ...mapState('network', ['networks', 'network']),
        ...mapState('organisation', ['organisation'])
    },
    created () {
        this.initialize()
    },
    methods: {
        ...mapActions('network', ['fetchNetworks', 'setNetwork', 'patchNetwork']),
        async initialize () {
            this.loading = true
            await this.fetchNetworks({ query: this.query })
            this.loading = false
            this.selectedRows = []
            this.addingProcess = false
            this.selectionToggle = false
        },
        async addableNetworks () {
            await this.fetchNetworks({ query: `?excludeorganisation=${this.$route.params.OrganisationId}` })
            this.addingProcess = true
            this.selectionToggle = true
            this.selectedRows = []
        },
        async addOrRemoveNetworks () {
            // const apicalls = new Promise((resolve, reject) => {
            //     this.selectedRows.forEach(async (network) => {
            //         const result = await this.patchNetwork({ id: network.id, data: [this.organisation] })
            //         resolve(result)
            //     })
            // })
            // await apicalls.then()
            // await this.selectedRows.forEach((network) => {
            //     this.patchNetwork({ id: network.id, data: [this.organisation] })
            //     console.log('check')
            // })
            for (const network of this.selectedRows) {
                await this.patchNetwork({ id: network.id, data: [this.organisation] })
                console.log(this.organisation)
            }
            this.Dialog = false
            this.initialize()
        },
        async goToSelectedNetwork (event) {
            if (!this.selectionToggle) {
                await this.setNetwork(event.data)
                this.$router.push({ name: 'networkdetails', params: { id: this.network?.id || 0 } })
            }
        }
    }
}
</script>
