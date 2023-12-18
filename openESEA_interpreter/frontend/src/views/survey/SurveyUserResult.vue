// http://localhost:8080/organisations/1/esea-accounts/20/surveys/6/result/
// Shows results of a single Survey Response

<template>
    <div class="p-d-flex p-grid p-jc-center p-m-0">
        <div class="p-col-12 p-p-3" style="background-color: #dcedc8;">
            <h1>{{survey.name}}</h1>
            <h3>{{survey.description}}</h3>
            <div class="p-jc-center">
                <span class="p-text-left p-text-bold">Respondent:</span> '{{surveyResponse.respondent}}' <br>
                <span class="p-text-left p-text-bold">organisation:</span> '{{surveyResponse.organisation}}'
            </div>
        </div>
        <ProgressSpinner v-if="loading && !failedLoad" />
        <div v-else class="p-grid p-col-6 p-p-3" style="min-width: 800px;">
            <div v-for="section in survey.sections" :key="section.id" class="p-grid p-col-12 p-p-3" style="background-color: #F5F5F5; border-radius: 10px;">
                <div class="p-col-12 p-text-left"><h3>Section: '{{section.title}}'</h3></div>
                <survey-question class="p-col-12 p-m-2"
                v-for="question in section.questions"
                :key="question.id"
                :question="question"
                :answer="answers[question.id]"
                :readonly="true"
                />
            </div>
        </div>
    </div>
</template>

<script>
    import { mapState, mapActions } from 'vuex'
    import SurveyQuestion from '../../components/survey/SurveyQuestion'
    import ProgressSpinner from 'primevue/progressspinner'

    export default {
        components: {
            SurveyQuestion,
            ProgressSpinner
        },
        data () {
            return {
                loading: true,
                failedLoad: false
            }
        },
        computed: {
            ...mapState('method', ['method']),
            ...mapState('survey', ['survey']),
            ...mapState('surveyResponse', ['surveyResponses', 'surveyResponse']),
            answers () {
                const answers = {}
                if (this.surveyResponse && this.surveyResponse.question_responses) {
                    this.surveyResponse.question_responses.forEach((answer) => {
                        console.log(answer)
                        answers[answer.question] = answer.value
                    })
                }
                return answers
            }
        },
        created () {
            this.setSurveyResponse()
            this.initialize()
        },
        methods: {
            ...mapActions('survey', ['fetchSurvey']),
            ...mapActions('surveyResponse', ['fetchSurveyResponse', 'setSurveyResponse']),
            // ...mapActions('surveyResponseCalculation', ['fetchSurveyResponseCalculations']),
            async initialize () {
                await this.fetchSurvey({ mId: this.method.id, id: parseInt(this.$route.params.SurveyId) })
                await this.fetchSurveyResponse({ oId: this.$route.params.OrganisationId, eaId: this.$route.params.EseaAccountId, id: `survey=${this.survey.id}` })
                setTimeout(() => { this.failedLoad = true }, 10000)
                this.loading = false
            }
        }
    }
</script>
