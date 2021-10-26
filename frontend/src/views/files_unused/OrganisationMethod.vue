<template>
    <div>
        <TabView v:model:activeIndex="active">
            <TabPanel header="Method Details">
                <p>"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
                    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."</p>
            </TabPanel>
            <TabPanel header="Surveys">
                <DataTable :value="surveys" :filters="filters" class="p-datatable-striped">
                    <template #header>
                        <div class="p-d-flex p-jc-between p-ai-center">
                            <h3 class="p-m-0">Surveys</h3>
                            <span class="p-input-icon-left"> <i class="pi pi-search" />
                                <InputText v-model="filters['global']" placeholder="Keyword Search" />
                            </span>
                        </div>
                    </template>
                    <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field" />
                    <Column>
                        <template #body="slotProps">
                            <Button type="button" label="Results" class="p-button-raised p-button secondary p-button-sm" @click="goToSurveyResults(slotProps.data)" />
                        </template>
                    </Column>
                </DataTable>
            </TabPanel>
            <TabPanel header="Responses">
                 <DataTable :value="surveyResponses" :filters="filters2" class="p-datatable-striped">
                    <template #header>
                        <div class="p-d-flex p-jc-between p-ai-center">
                            <h3 class="p-m-0">Responses</h3>
                            <span class="p-input-icon-left"> <i class="pi pi-search" />
                                <InputText v-model="filters2['global']" placeholder="Keyword Search" />
                            </span>
                        </div>
                    </template>
                    <Column v-for="col of responsescolumns" :field="col.field" :header="col.header" :key="col.field" />
                    <Column>
                        <template #body="slotProps">
                            <Button type="button" label="Results" class="p-button-raised p-button secondary p-button-sm" @click="goToSurveyResponse(slotProps.data)" />
                        </template>
                    </Column>
                </DataTable>

            </TabPanel>
            <TabPanel header="Report">
                    <p>"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."</p>
            </TabPanel>
        </TabView>
    </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
export default {
    data () {
        return {
            columns: [
                    { field: 'name', header: 'Name' },
                    { field: 'questions.length', header: 'Questions' },
                    { field: 'stakeholders', header: 'Stakeholder Group' },
                    { field: 'rate', header: 'Responserate' },
                    { field: 'anonymous', header: 'Anonymous' }
                ],
            responsescolumns: [
                { field: 'survey', header: 'Survey' },
                { field: 'user_organisation.user', header: 'Respondent' }
            ],
            filters: {},
            filters2: {},
            filters3: {},
            expandedRows: [],
            amountToggle: false,
            active: 0
        }
    },
    computed: {
        ...mapState('method', ['method']),
        ...mapState('survey', ['surveys']),
        ...mapState('surveyResponse', ['surveyResponses'])
    },
    created () {
        this.initialize()
    },
    methods: {
        ...mapActions('method', ['fetchMethod']),
        ...mapActions('survey', ['fetchSurveys']),
        ...mapActions('surveyResponse', ['fetchSurveyResponses']),
        async initialize () {
            this.fetchSurveys({ mId: this.method.id, query: `?organisation=${this.$route.params.OrganisationId}` })
            this.fetchSurveyResponses({ mId: this.method.id, sId: 0, oId: 0, query: `?organisation=${this.$route.params.OrganisationId}` })
        },
        async goToSurveyResults (survey) {
            // await this.setSurvey(survey.data)
            this.$router.push({ name: 'method-survey-results', params: { OrganisationId: this.$route.params.OrganisationId, methodId: this.method.id, surveyId: survey.id } })
            // this.$router.push({ name: 'survey-fill', params: { id: this.method.id, surveyId: survey.data.id } })
        },
        async goToSurveyResponse (surveyresponse) {
            this.$router.push({ name: 'method-survey-result', params: { OrganisationId: this.$route.params.OrganisationId, methodId: this.method.id, surveyId: surveyresponse.survey, id: surveyresponse.id } })
        }
    }
}
</script>
