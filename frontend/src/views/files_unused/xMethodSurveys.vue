<template>
    <div class="surveys">
        <h1>Survey Overview</h1>
        <div class="card p-m-4 p-shadow-2">
        <personalised-datatable table-name="surveys" :columns="SurveysColumns" :filters="filters"
        :custom-data="surveys" @item-redirect="goToSurvey" />
        </div>
    </div>
</template>
<script>
import { mapState, mapActions } from 'vuex'
import PersonalisedDatatable from '../components/PersonalisedDatatable'

export default {
    components: {
        PersonalisedDatatable
    },
    data () {
        return {
            SurveysColumns: [
                { field: 'name', header: 'Name' },
                { field: 'description', header: 'Description' },
                { field: 'questions.length', header: 'Questions' },
                { field: 'rate', header: 'Rate' },
                { field: 'respondents', header: 'Respondents' }
            ],
            filters: {}

        }
    },
    computed: {
        ...mapState('method', ['method']),
        ...mapState('survey', ['surveys']),
        ...mapState('survey_response', ['surveyResponses'])
    },
    created () {
        this.initialize()
    },
    methods: {
        ...mapActions('survey', ['fetchSurveys', 'setSurvey']),
        async initialize () {
            this.fetchSurveys({ mId: this.method.id })
        },
        goToSurvey (survey) {
            // this.$router.push({ name: 'method-survey-result', params: { id: this.method.id, surveyId: survey.id } })
            this.setSurvey(survey)
            this.$router.push({ name: 'survey-fill', params: { id: this.method.id, surveyId: survey.id } })
        }
    }
}
</script>
