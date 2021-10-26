<template>
    <div class="p-d-flex p-grid p-nested-grid p-jc-center p-m-0">
        <div class="p-grid p-col-12 p-ai-center" style="background-color: #dcedc8;">
            <div class="p-col-4">
                <SelectButton v-model="amountDisplayButtonValue" :options="amountDisplayButtonOptions" optionLabel="name" />
            </div>
            <div class="p-col-8 p-text-left">
            <h1>{{survey.name}}</h1>
            <h3>{{survey.description}}</h3>
            <p>Respondents: {{ surveyResult.respondents }} of {{ surveyResult.responses }} </p>
            <!-- {{surveyResult}} -->
            <!-- {{survey.topics[0].sub_topics[0].questions}} -->
            </div>
        </div>
        <div class="p-grid p-col-6 p-p-3" style="min-width: 800px;">
            <div v-for="topic in survey.topics" :key="topic.id" class="p-grid p-col-12 p-p-5" style="background-color: #F5F5F5; border-radius: 10px;">
                <div class="p-col-12 p-text-left"><h3>Topic: '{{topic.name}}</h3></div>
                <survey-question-results
					v-for="question in topic.questions"
					:key="`question-${question.id}`"
					:question="question"
					:answers="answers[question.key]"
					:amountdisplaychoice="amountDisplayButtonValue"
					class="mt-6"
				/>

                <div v-for="subtopic in topic.sub_topics" :key="subtopic.id" class="p-col-12 p-p-3 p-my-3" style="background-color: white; border-radius: 10px;">
                    <div class="p-col-12 p-text-left"><h3>Topic: '{{subtopic.name}}</h3></div>
                    <survey-question-results
						v-for="question in subtopic.questions"
						:key="`question-${question.id}`"
						:question="question"
						:answers="answers[question.key]"
                        :amountdisplaychoice="amountDisplayButtonValue"
						class="mt-6"
					/>
                </div>
            </div>
            <Button label="Go to surveys" class="p-button-success p-mt-4" style="width: 100%" @click="goToSurveys"/>
        </div>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import SurveyQuestionResults from '../../components/survey/SurveyQuestionResults'
export default {
    components: {
        SurveyQuestionResults
    },
    data () {
        return {
            topicNumber: 0,
            amountDisplayButtonValue: { name: 'Percentages', value: 1 },
            amountDisplayButtonOptions: [
                { name: 'Percentages', value: 1 },
                { name: 'Numbers', value: 0 }
                ]
        }
    },
    computed: {
        ...mapState('organisation', ['organisation']),
        ...mapState('eseaAccount', ['eseaAccount']),
        ...mapState('survey', ['survey']),
        ...mapState('surveyResults', ['surveyResult']),
        answers () {
            console.log(this.surveyResult.indicators)
            return this.surveyResult.indicators || {}
        },
		calculations () {
			const calculations = {}
			if (this.surveyResult?.calculations.length) {
				this.surveyResult.calculations.forEach((calculation) => {
					calculations[calculation.topic] = !calculations[calculation.topic]
						? [calculation] : [...calculations[calculation.topic], calculation]
				})
			}
            return calculations
        },
        methodId () {
            return parseInt(this.$route.params.methodId, 10)
        }
    },
    beforeRouteUpdate (to, from, next) {
        this.initialize()
        next()
    },
    created () {
        this.initialize()
    },
    methods: {
        ...mapActions('survey', ['fetchSurvey']),
        ...mapActions('surveyResults', ['fetchSurveyResults']),
        async initialize () {
            const surveyId = parseInt(this.$route.params.surveyId, 10)
            await this.fetchSurvey({ mId: this.eseaAccount.method?.id, id: surveyId })
            // if (this.survey.method !== this.methodId) {
            //     this.$router.push({ name: 'methods' })
            // }
            this.fetchSurveyResults({ eaId: this.eseaAccount?.id })
        }
    }
}
</script>
