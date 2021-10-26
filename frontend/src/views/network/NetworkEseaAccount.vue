<template>
    <div v-for="survey in eseaAccount.survey_response_by_survey" :key="survey.id" class="p-m-5">
            <ProgressBar :value="survey.current_response_rate + 1" :showValue="true">
                '{{survey.name}}' - Response Rate: {{survey.current_response_rate}}%
            </ProgressBar>
            <Divider />
            <!-- <ProgressBar :value="value.rate + 30" :showValue="true">
                '{{key}}' - Response Rate: {{value.rate + 30}}%
            </ProgressBar> -->
    </div>

    <div>Esea Account</div>
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
                <Column field="name" header="Survey" />
                <Column field="name" header="Name" sortable />
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
                    <Button label="Survey Results" class="p-button-success" @click="data.responses? goToResults(data) : goToSurveyFill(data)"  style="width: 200px" />
                </template>
            </Column>
                <!-- <Column field="stakeholdergroup" header="Stakeholder Group"
                <Column field="sufficient_responses" header="Sufficient Responses" />
                <Column field="responses" header="Responses" />
                <Column field="response_rate" header="Response Rate" /> -->
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
    data () {
        return {

        }
    },
    computed: {
        ...mapState('eseaAccount', ['eseaAccount'])
    },
    methods: {
        goToSummarizedResponses (event) {
            this.$router.push({ name: 'method-survey-results', params: { OrganisationId: 1, methodId: 1, surveyId: 1 } })
        }
    }
}
</script>

<style type="text/css">
/* .p-progressbar {
background: #f42020;
} */
.memory-bar-style .ui-progressbar-value {
background: #ffe600;
}
.cpu-bar-style .ui-progressbar-value {
background: #7fb80e;
}
</style>
