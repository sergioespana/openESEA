<!-- used by OrganisationDashboards.vue -->

<template>
    <list-bar v-model:tabledisplay="tableDisplay" v-model:allitems="dashboards" :includecheckbox="false" v-model:search="customSearch" name="Dashboards">
        <slot></slot>
    </list-bar>
    <ProgressSpinner v-if="loading && !failedLoad" />
    <div v-else-if="loading && failedLoad" class="p-text-italic">Dashboards could not be retrieved!</div>
    <div v-else-if="dashboards.length">
        <div v-if="tableDisplay" class="p-grid p-m-5">
            <div v-for="dashboard in filteredDashboards" :key="dashboard.id" class="p-col-12 p-md-6 p-lg-4" style="width: 300px; height: auto;">
                <div class="p-p-3" :class="dashboard.hover ? 'p-shadow-2 p-m-1' : 'p-shadow-1 p-m-2'" :style="(dashboard.hover ? styleObject: '')" @mouseover="dashboard.hover = true" @mouseleave="dashboard.hover = false" @click="$event => goToDashboard(dashboard)">
                    <p class="p-text-bold">{{dashboard.specification.Name}}</p>
                    <p class="p-text-italic">{{dashboard.id}}</p>
                </div>
            </div>
        </div>
        <DataTable v-else :value="filteredDashboards" datakey="id" selectionMode="single" @row-select="$event => this.$emit('goToDashboard', $event.data)" showGridlines autoLayout
            :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
            :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

            <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field" bodyStyle="" />
        </Datatable>
    </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import ProgressSpinner from 'primevue/progressspinner'
import ListBar from '@/components/lists/ListBar/'

export default {
    components: {
        ProgressSpinner,
        ListBar
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
        ...mapState('dashboard', ['dashboards', 'dashboard']),
        filteredDashboards () {
            console.log('Dashboards:', this.dashboards)
            const search = this.customSearch.toLowerCase()
            return this.dashboards.filter((dashboard) => {
                const id = dashboard.id.toString()
                const name = dashboard.specification.Name?.toLowerCase()
                return (id ? id.includes(search) : false) ||
                    (name ? name.includes(search) : false)
                })
        }
    },
    created () {
        this.getDashboards()
        setTimeout(() => { this.failedLoad = true }, 10000)
    },
    methods: {
        ...mapActions('dashboard', ['fetchDashboards']),
        async getDashboards () {
            await this.fetchDashboards({})
            this.loading = false
        }
    }
}
</script>
