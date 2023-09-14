<!-- used by OrganisationDashboards.vue -->

<template>
    <list-bar v-model:tabledisplay="tableDisplay" :includecheckbox="false" name="Dashboards">
        <slot></slot>
    </list-bar>
    <ProgressSpinner v-if="loading && !failedLoad" />
    <div v-else-if="loading && failedLoad" class="p-text-italic">Dashboards could not be retrieved!</div>
    <div v-else-if="dashboards.length">
        <div v-if="tableDisplay" class="p-grid p-m-5">
            <div v-for="dashboard in filteredDashboards" :key="dashboard.id" class="p-col-12 p-md-6 p-lg-4" style="width: 300px; height: auto;">
                <div class="p-p-3" :class="dashboard.hover ? 'p-shadow-2 p-m-1' : 'p-shadow-1 p-m-2'" :style="(dashboard.hover ? styleObject: '')" @mouseover="dashboard.hover = true" @mouseleave="dashboard.hover = false" @click="this.$emit('goToSelectedDashboard', dashboard)">
                    <p class="p-text-bold">{{dashboard.specification.Name}}</p>
                    <p class="p-text-italic">{{dashboard.id}}</p>
                </div>
            </div>
        </div>
        <DataTable v-else :value="filteredDashboards" datakey="id" selectionMode="single" @row-select="$event => this.$emit('goToSelectedDashboard', $event.data)" showGridlines autoLayout
            :paginator="true" :rows="10" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
            :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

            <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field" bodyStyle="">
            </Column>
            <Column v-if="(organisation?.accesLevel === 'organisation admin' || organisation?.accesLevel === 'admin')" header="Actions" headerStyle="width: 10rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
            <template #body="{data}">
                <div class="p-d-flex">
                    <Button label="Delete" icon="pi pi-trash" class="p-button-danger p-button-sm" @click="removeOrganisationDashboard(data)">
                    </Button>
                </div>
            </template>
        </Column>
        </Datatable>
    </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

import ProgressSpinner from 'primevue/progressspinner'
import ListBar from '@/components/lists/ListBar/'
import Button from 'primevue/button'

export default {
    components: {
        ProgressSpinner,
        ListBar,
        Button
    },
    data () {
        return {
            tableDisplay: false,
            loading: true,
            failedLoad: false,
            customSearch: '',
            styleObject: { backgroundColor: '#EFEEEE', cursor: 'pointer' },
            columns: [
                { field: 'id', header: 'Id' },
                { field: 'specification.Name', header: 'Name' }
            ]
        }
    },
    computed: {
        ...mapState('organisation', ['organisation']),
        ...mapState('dashboard', ['dashboards', 'dashboard']),
        filteredDashboards () {
            const search = this.customSearch.toLowerCase()
            return this.dashboards.filter((dashboard) => {
                const id = dashboard.id.toString()
                const name = dashboard.specification.Name?.toLowerCase()
                return (id ? id.includes(search) : false) ||
                    (name ? name.includes(search) : false)
                }).sort((a, b) => { return a.id > b.id ? 1 : -1 })
        }
    },
    created () {
        this.getDashboards()
        setTimeout(() => { this.failedLoad = true }, 10000)
    },
    methods: {
        ...mapActions('dashboard', ['fetchDashboards', 'deleteDashboard']),
        async getDashboards () {
            await this.fetchDashboards({})
            this.loading = false
        },
        async removeOrganisationDashboard (data) {
            console.log(data)
            await this.deleteDashboard({ oId: this.$route.params.OrganisationId, id: data.id })
        }
    }
}
</script>
