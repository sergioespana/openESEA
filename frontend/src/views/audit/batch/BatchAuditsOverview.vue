<template>
    <div class="p-mx-3">
        <div class="p-d-flex p-ai-center p-jc-between">
            <h2 class="p-text-left">Audits in Progress</h2>
            <!-- <div>
                <Button @click="exportData()" label="Export Data" class="p-button-sm p-mr-2" />
                <Button @click="(helpDialog = !helpDialog)" label="Help" class="p-button-sm p-button-warning" icon="pi pi-external-link" />
            </div> -->
        </div>
        <!-- {{networkmembers}} {{ selectedAuditor }} -->
        <DataTable :value="eseaAccounts" dataKey="id" v-model:selection="selectedOrganisations" showGridlines autoLayout
            :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
            :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">
            <Column field="organisation_name" header="Organisation" sortable />
            <Column field="account_audit.auditor" header="Auditor" headerStyle="min-width: 250px;" sortable />
            <Column field="account_audit.status" header="Status" headerStyle="width: 400px;" sortable />
        </Datatable>

        <div class="p-text-right p-col-12 p-as-end">
            <Button class="p-my-5" label="Finish audit" @click="goToResult" icon="pi pi-check" />
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
    import { mapState, mapActions } from 'vuex'

    export default {
        computed: {
            ...mapState('eseaAccount', ['eseaAccounts', 'eseaAccount']),
            ...mapState('accountAudit', ['accountAudits']),
            ...mapState('campaign', ['campaign'])
        },
        methods: {
            ...mapActions('campaign', ['updateCampaign']),
            async goToResult () {
                this.campaign.auditstatus = 'All Audits Finished'
                delete this.campaign.image
                await this.updateCampaign({ nId: this.$route.params.NetworkId, data: this.campaign })
                this.$router.push({ name: 'batchauditresults', params: { NetworkId: this.$route.params.NetworkId, CampaignId: this.$route.params.CampaignId } })
            }
        }
    }
</script>
