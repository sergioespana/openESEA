<template>
    <div class="p-mx-3">
        <div class="p-d-flex p-ai-center p-jc-between">
            <h2 class="p-text-left">Organisation Selection</h2>
            <Button @click="(helpDialog = !helpDialog)" label="Help" class="p-button-sm p-button-warning" icon="pi pi-external-link" />
        </div>
        <DataTable :value="eseaAccounts" dataKey="id" v-model:selection="selectedOrganisations" showGridlines autoLayout
            :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
            :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

            <Column selectionMode="multiple" headerStyle="width: 3em"></Column>
            <Column field="organisation_name" header="Organisation" />
            <Column header="Auditor" headerStyle="min-width: 250px;">
                <template #body="{data}">
                    <Dropdown v-if="selectedOrganisations.includes(data)" v-model="data.account_audit.auditor" :options="networkAuditors"  optionLabel="user_name" optionValue="user_name" placeholder="Select an Auditor" class="p-m-0 p-p-0" style="width: 100%;" />
                    <span v-else>{{data.account_audit.auditor}}</span>
                </template>
            </Column>
            <Column field="account_audit.status" header="status" />
            <Column field="recommendations" header="Recommendations" headerStyle="width: 200px;">
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
    import { mapState, mapActions, mapGetters } from 'vuex'
    import Dropdown from 'primevue/dropdown'

    export default {
        components: {
            Dropdown
        },
        data () {
            return {
                helpDialog: false,
                selectedOrganisations: [],
                AddAuditorDialog: false
            }
        },
        computed: {
            ...mapState('eseaAccount', ['eseaAccounts', 'eseaAccount']),
            ...mapState('campaign', ['campaign']),
            ...mapState('networkTeam', ['networkmembers']),
            ...mapGetters('networkTeam', ['networkAuditors'])
        },
        async created () {
            await this.fetchEseaAccounts({ query: `?campaign=${this.$route.params.CampaignId}` })
            this.selectedOrganisations = this.eseaAccounts.filter(eseaAccount => (eseaAccount.account_audit.status === 'in progress' || eseaAccount.account_audit.status === 'finished'))
    },
        methods: {
            ...mapActions('eseaAccount', ['fetchEseaAccounts']),
            ...mapActions('networkTeam', ['fetchNetworkMembers']),
            ...mapActions('accountAudit', ['updateAccountAudit', 'fetchAccountAudits', 'changeStartedAudit']),
            ...mapActions('campaign', ['updateCampaign']),
            async goToAudit () {
                if (this.selectedOrganisations.some(item => item.account_audit.auditor === null)) {
                    this.AddAuditorDialog = true
                } else {
                    await this.updateDatabase()
                    this.campaign.auditstatus = 'Audits in Progress'
                    delete this.campaign.image
                    await this.updateCampaign({ nId: this.$route.params.NetworkId, data: this.campaign })
                    await this.fetchAccountAudits({ query: `?campaign=${this.$route.params.CampaignId}&audit-selection=true` })
                    this.changeStartedAudit(true)
                    this.$router.push({ name: 'batchauditoverview', params: { NetworkId: this.$route.params.NetworkId, CampaignId: this.$route.params.CampaignId } })
                }
            },
            updateDatabase () {
                this.selectedOrganisations.forEach((eseaAccount) => {
                    const data = eseaAccount.account_audit
                    if (data.status === 'not started') {
                        data.status = 'in progress'
                        console.log('-->', data)
                        eseaAccount.account_audit = data
                        this.updateAccountAudit({ oId: eseaAccount.organisation, eaId: eseaAccount.id, data: eseaAccount.account_audit })
                    }
                    // ListOfIds.push({ id: organisation.id, organisation: organisation.organisation
                    // })
                })
            }
        }
    }
</script>
