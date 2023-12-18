<template>
    <!-- Show all responses of the survey and account-->
    <div class="p-mx-3">
        <div class="p-d-flex p-ai-center p-jc-between">
            <h2 class="p-text-left">Sample Overview</h2>
            <div>
            <Button @click="exportData()" label="Export Data" disabled="true" class="p-button-sm p-mr-2" />
            <Button @click="(helpDialog = !helpDialog)" label="Help" class="p-button-sm p-button-warning" icon="pi pi-external-link" />
            </div>
        </div>
        <DataTable :value="respondents" dataKey="id" selectionMode="single" showGridlines autoLayout
            :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
            :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

            <Column header="Respondent" headerStyle="min-width: 250px;">
                <template #body="{data}">
                    {{ data.first_name}} {{ data.last_name_prefix }} {{ data.last_name}}
                </template>
            </Column>
            <Column field="email" header="Email adress" sortable />
        </Datatable>

        <div class="p-text-right p-col-12 p-as-end">
            <Button class="p-my-5" label="Start audit" @click="goToAudit" icon="pi pi-check" />
        </div>
    </div>

     <Dialog v-model:visible="helpDialog" style="width: 500px;" header="Help" :modal="true" dismissableMask="true">
        <p>Please provide the list of sampled responses to the audited organisation. When you are ready to verify the
            responses (e.g. on location), click 'Start audit'.</p>
        <template #footer>
            <Button label="Ok" icon="pi pi-check" @click="(helpDialog = !helpDialog)" />
        </template>
    </Dialog>
</template>

<script>
import { mapState } from 'vuex'

export default {
    data () {
        return {
            helpDialog: false,
            tablevals: [
                { id: 1, respondent: 'Henk', email: 'henk@mail.com' },
                { id: 2, respondent: 'Henk', email: 'henk@mail.com' }
                ]
        }
    },
    computed: {
        ...mapState('respondent', ['respondents'])
    },
    methods: {
        goToAudit () {
            if (this.respondents.length) {
                this.$router.push({ name: 'multipleaudit', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } })
            }
        },
        exportData () {
            // Export data to csv file
            print()
        }
    }
}
</script>
