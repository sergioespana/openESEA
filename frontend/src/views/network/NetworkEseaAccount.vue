// http://localhost:8081/network/2/campaigns/1/esea-account/1/

<template>
    <div v-for="survey in eseaAccount.survey_response_by_survey" :key="survey.id" class="p-m-5">
            <ProgressBar :value="survey.current_response_rate + 1" :showValue="true">
                '{{survey.name}}' - Response Rate: {{survey.current_response_rate}}%
            </ProgressBar>
            <Divider />
    </div>
    <TabView>
        <TabPanel header="Responses">
            <DataTable :value="eseaAccount.survey_response_by_survey" datakey="id" :rows="10" :paginator="true" :rowHover="true" selectionMode="single" @row-select="goToSummarizedResponses">
                <template #header>
                    <div class="p-d-flex p-jc-between p-ai-center">
                        <h5 class="p-m-0">Survey Responses</h5>
                        <span class="p-input-icon-left">
                            <i class="pi pi-search" />
                            <InputText v-model="filters" placeholder="Keyword Search" />
                        </span>
                    </div>
                </template>
                <Column field="name" header="Survey" sortable />
                <Column field="stakeholdergroup" header="Stakeholder Group" />
                <Column field="questions" header="Questions" sortable />
                <Column field="respondees.length" header="Stakeholders" sortable />
                <Column field="responses" header="Responses" sortable />
                <Column field="current_response_rate" header="Response Rate" sortable>
                    <template #body="{data}">
                        <ProgressBar :value="(data.current_response_rate)" :showValue="true" />
                    </template>
                </Column>
                <Column field="required_response_rate" header="Response Rate Threshold" sortable>
                    <template #body='{data}'>
                        {{data.required_response_rate}}%
                    </template>
                </Column>
                <Column headerStyle="width: 15rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                    <template #body="{data}">
                        <Button label="Survey Report" class="p-button-success" @click="data.responses? goToResults(data) : goToSurveyFill(data)"  style="width: 200px" />
                    </template>
                </Column>
            </DataTable>
        </TabPanel>
        <TabPanel header="Settings">
        </TabPanel>
    </TabView>
</template>

<script>
    import { mapState } from 'vuex'
    import ProgressBar from 'primevue/progressbar'

    export default {
        components: {
            ProgressBar
        },
        computed: {
            ...mapState('eseaAccount', ['eseaAccount'])
        },
        methods: {
            // Show Summarized Survey Results in charts
            goToSummarizedResponses (event) {
                this.$router.push({ name: 'survey-results', params: { OrganisationId: this.eseaAccount.organisation, methodId: this.eseaAccount.method, surveyId: event.data.id } })
            },
            // Show own Survey Results to the Survey if the user has filled it in
            goToSurveyResult (event) {
                this.$router.push({ name: 'method-survey-result', params: { OrganisationId: this.eseaAccount.organisation, methodId: this.eseaAccount.method, surveyId: event.data.id } })
            },
            // Go to report that shows the indicator values
            goToResults () {
                this.$router.push({ name: 'esea-account-report', params: { OrganisationId: this.eseaAccount.organisation, EseaAccountId: this.eseaAccount.id } })
            }
        }
    }
</script>

<style type="text/css">
    .memory-bar-style .ui-progressbar-value {
    background: #ffe600;
    }
    .cpu-bar-style .ui-progressbar-value {
    background: #7fb80e;
    }
</style>
