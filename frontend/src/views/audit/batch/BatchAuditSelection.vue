<template>
    <div class="p-mx-3">
        <div class="p-d-flex p-ai-center p-jc-between">
            <h2 class="p-text-left">Organisation Selection</h2>
            <Button @click="(helpDialog = !helpDialog)" label="Help" class="p-button-sm p-button-warning" icon="pi pi-external-link" />
            <!-- <div>
                <Button @click="exportData()" label="Export Data" class="p-button-sm p-mr-2" />
                <Button @click="(helpDialog = !helpDialog)" label="Help" class="p-button-sm p-button-warning" icon="pi pi-external-link" />
            </div> -->
        </div>
        <!-- {{networkmembers}} {{ selectedAuditor }} --> {{networkAuditors}}
        <DataTable :value="campaign.organisation_accounts" dataKey="id" v-model:selection="selectedOrganisations" showGridlines autoLayout
            :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
            :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

            <Column selectionMode="multiple" headerStyle="width: 3em"></Column>
            <Column field="organisation_name" header="Organisation" />
            <Column header="Auditor">
                <template #body="{data}">
                    <Dropdown v-if="selectedOrganisations.includes(data)" v-model="data.auditor" :options="networkmembers"  optionLabel="user_name" optionValue="user" placeholder="Select an Auditor" />
                </template>
            </Column>
            <Column field="recommendations" header="Recommendations">
                <template #body="{data}">
                    <div v-if="permission">
                        <Button v-if="data.id===6" :label="`${nr_of_recommended} Recommendations`" class="p-button-sm p-button-rounded p-py-1 p-button-danger" :disabled="true" />
                    </div>
                </template>
            </Column>
        </Datatable>

        <div class="p-text-right p-col-12 p-as-end">
            <Button class="p-my-5" label="Start audit" @click="goToAudit" icon="pi pi-check" :disabled="!selectedOrganisations.length" />
        </div>
    </div>
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
                selectedOrganisations: []
            }
        },
        computed: {
            ...mapState('campaign', ['campaign']),
            ...mapState('networkTeam', ['networkmembers']),
            ...mapGetters('networkTeam', ['networkAuditors'])
        },
        methods: {
             ...mapActions('networkTeam', ['fetchNetworkMembers'])
        }
    }
</script>
