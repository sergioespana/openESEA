<template>
    <div class="p-mx-3">
        <Card class="p-text-left p-m-2">
            <template #title>
            Audits Finished
            </template>
            <template #content class="p-col-12">
            <div class="p-mr-5">
                <div class="p-grid">
                    <div class="p-col-2 p-text-center"><i class="pi pi-check" style="font-size: 3rem; background-color: #689F38; color: white; border-radius: 50%; padding: 30px;"></i></div>
                    <div class="p-col-10">
                        <h3 class="p-mt-0 p-pt-0">All audits are finished</h3>
                        Information on the individual audit processes can be found below.
                    </div>
                </div>
            </div>
            </template>
        </Card>
        <DataTable :value="accountAudits" dataKey="id" v-model:selection="selectedOrganisations" showGridlines autoLayout
            :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
            :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">
            <Column field="organisation" header="Organisation" sortable />
            <Column field="auditor" header="Auditor" headerStyle="min-width: 250px;" sortable />
            <Column field="status" header="Status" headerStyle="width: 400px;" sortable />
        </Datatable>
    </div>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        computed: {
            ...mapState('accountAudit', ['accountAudits'])
        }
    }
</script>
