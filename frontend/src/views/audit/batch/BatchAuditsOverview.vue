<template>
    <div class="p-mx-3">
        <div class="p-d-flex p-ai-center p-jc-between">
            <h2 class="p-text-left">Organisation Selection</h2>
            <Button @click="addOrganisation()" label="Add Organisation" class="p-button-sm" />
            <!-- <div>
                <Button @click="exportData()" label="Export Data" class="p-button-sm p-mr-2" />
                <Button @click="(helpDialog = !helpDialog)" label="Help" class="p-button-sm p-button-warning" icon="pi pi-external-link" />
            </div> -->
        </div>
        <!-- {{networkmembers}} {{ selectedAuditor }} -->
        <DataTable :value="campaign.organisation_accounts" dataKey="id" v-model:selection="selectedOrganisations" showGridlines autoLayout
            :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
            :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

            <Column selectionMode="multiple" headerStyle="width: 3em"></Column>
            <Column field="organisation_name" header="Organisation" />
            <Column header="Auditor" headerStyle="min-width: 250px;">
                <template #body="{data}">
                    {{data.auditor}}
                    <Dropdown v-if="selectedOrganisations.includes(data)" v-model="data.auditor" :options="networkAuditors"  optionLabel="user_name" optionValue="user_name" placeholder="Select an Auditor" class="p-m-0 p-p-0" style="width: 100%;" />
                </template>
            </Column>
            <Column field="recommendations" header="Status" headerStyle="width: 200px;">
                <template #body="{data}">
                    <Button :label="`${data.id} Recommendations`" class="p-button-sm p-button-rounded p-py-1 p-button-danger" style="width: 180px" :disabled="true" />
                </template>
            </Column>
        </Datatable>

        <div class="p-text-right p-col-12 p-as-end">
            <Button class="p-my-5" label="Start audit" @click="goToAudit" icon="pi pi-check" :disabled="!selectedOrganisations.length" />
        </div>
    </div>

    <Dialog v-model:visible="AddAuditorDialog" style="width: 500px;" header="Help" :modal="true" dismissableMask="true">
        <p>Make sure that all selected Organisations are assigned an auditor.</p>

        <template #footer>
            <Button label="Ok" icon="pi pi-check" @click="(AddAuditorDialog = !AddAuditorDialog)" />
        </template>
    </Dialog>
</template>

<script>
export default {
    methods: {
        addOrganisation () {
            print()
        }
    }
}
</script>
