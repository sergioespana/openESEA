<template>
    <div style="width: 100%;">
        <ProgressSpinner v-if="loading && !failedLoad" />
        <div v-else-if="loading && failedLoad" class="p-text-italic">THe Survey could not be loaded!</div> <!-- style="background-color: #ddedc8;" -->
        <div v-else-if="!surveyResponse.finished" class="p-d-flex p-grid p-jc-center p-m-0" >
            <div class="p-col-12 p-grid p-jc-center p-p-3">
                <h1 class="p-col-12 p-m-0">{{survey.name}}</h1>
                <h3 class="p-col-12 p-m-0">{{survey.description}}</h3>
                <div class="p-col-4 p-text-left">
                    <p><span class="p-text-bold">Respondent:</span> {{surveyResponse.respondent}} <br> <span class="p-text-bold">Organisation:</span> {{surveyResponse.organisation}} </p>
                </div>
            </div>
            <div v-if="this.survey.sections.length" class="p-grid p-col-6 p-m-5" style="border-radius: 10px">
                <div v-if="sectionNumber === 0" class="p-col-12 p-text-left p-p-5" style="border-radius: 10px; background-color: #F1F1F1;"><h3>{{survey.welcome_text}}</h3></div>
                <Divider />
                <div class="p-col-6 p-text-left p-text-bold">Section {{ sectionNumber + 1 }} of {{ totalSections.length }}</div>
                <div class="p-col-6 p-text-right">
                    <ProgressBar :value="progress + 0.1">{{progress}}% completed</ProgressBar></div>
                <div class="p-col-12 p-text-left"><h3>Section: '{{currentSection.title}}'</h3></div>
                <section-component class="p-col-12 p-my-2"
                    v-for="item, index in currentSection.mergedQuestionsAndTextFragments"
                    tabindex="0"
                    :key="item.id"
                    :item="item"
                    :answer="answers[item.id]"
                    :active="activeQuestion === (index)"
                    :refresh="refresh"
                    @input="updateAnswer(item.direct_indicator[0].id, item.id, $event)"
                    @focus="toggleActive(index)"
                    @focuschecking="toggleActive(index)"
                    @blur="toggleActive"
                />
                <div v-if="(sectionNumber + 1) === totalSections.length" class="p-col-12 p-text-left p-p-5" style="border-radius: 10px; background-color: #F1F1F1;"><h3>{{survey.closing_text}}</h3></div>
                <div class="p-grid p-col-12 p-m-0 p-px-0">
                    <div class="p-col-6 p-text-left p-pl-0">
                        <Button label="Previous Section" class="p-button-raised" :disabled="sectionNumber === 0" @click="previousSection" />
                    </div>
                    <div class="p-col-3 p-text-right">
                        <Button label="Save for Now" class="p-button-primary p-button-raised" @click="saveSurvey" :disabled="true" />
                    </div>
                    <div class="p-col-3 p-text-right p-pr-0">
                        <Button v-if="sectionNumber + 1 < totalSections.length" label="Next Section" class="p-button-raised" style="width: 100%;" @click="nextSection" />
                        <Button v-else label="Finish Survey" class="p-col p-button-success p-button-raised p-button-sm" style="width: 100%;" @click="finishSurvey" />
                    </div>
                </div>
            </div>
            <h1 v-else>This survey has no sections to display!</h1>
        </div>

        <Dialog v-model:visible="missedQuestionsDialog" :style="{width: '450px'}" header="Missing Answers" :modal="true">
            <i class="pi pi-star p-mr-3" style="font-size: 1.5rem" />
            <span class="p-text-left">You need to fill in the following answers to be able to send your survey response:</span>
            <div class="p-grid p-m-2">
                <div v-for="question in missedQuestions" :key="question" class="p-col-12">
                    <Button :label="`Question: '${question.name}'`" style="width: 100%;" @click="goToQuestion(question)"> </Button>
                </div>
            </div>
            <template #footer>
                <Button label="Ok" class="p-button-text" @click="missedQuestionsDialog = false"/>
            </template>
        </Dialog>
    </div>
</template>
<script>
import { mapActions, mapState } from 'vuex'
import SectionComponent from '../../components/survey/SectionComponent'
import ProgressBar from 'primevue/progressbar'
import ProgressSpinner from 'primevue/progressspinner'

export default {
    components: {
        SectionComponent,
        ProgressBar,
        ProgressSpinner
    },
    data () {
        return {
            loading: true,
            failedload: false,
            sectionNumber: 0,
            progressBarValue: 0,
            activeQuestion: null,
            missedQuestions: [],
            missedQuestionsDialog: false,
            refresh: false

        }
    },
    computed: {
        ...mapState('survey', ['survey']),
        ...mapState('surveyResponse', ['surveyResponse', 'surveyResponses']),
        ...mapState('eseaAccount', ['eseaAccount']),
        ...mapState('question', ['questions']),
        currentSection () {
            const section = this.survey.sections[this.sectionNumber]
            const mergedQuestionsAndTextFragments = section?.questions.concat(section.text_fragments)
            const sortedComponents = mergedQuestionsAndTextFragments?.sort((a, b) => (a.order > b.order) ? 1 : -1)
            section.mergedQuestionsAndTextFragments = sortedComponents
            return section
        },
        totalSections () {
            const sectionList = []
            for (let i = 0; i < this.survey.sections.length; i++) {
                sectionList.push(this.survey.sections[i].id)
            }
            // for (const section in this.survey?.sections) { totalSections = totalSections + this.survey?.topics[topic].sub_topics.length }

            return sectionList
        },
        answers () {
            const answers = {}
            if (this.surveyResponse.question_responses) {
                this.surveyResponse.question_responses.forEach((answer) => {
                    answers[answer.question] = [answer.values, answer.value]
                })
            }
            return answers
        },
        progress () {
            var progress
            if (this.sectionNumber === 0) { return 0 }
            progress = ((this.sectionNumber + 1) / this.totalSections.length) * 100
            return progress
        }

    },
    watch: {
        surveyResponse: {
            handler: function (newValue) {
                this.refresh = !this.refresh
            },
            deep: true
        }
    },
    created () {
        console.log('eee')
        setTimeout(() => { this.failedLoad = true }, 10000)
        this.initialize()
    },
    methods: {
        ...mapActions('survey', ['fetchSurvey']),
        ...mapActions('surveyResponse', ['fetchSurveyResponse', 'setSurveyResponse', 'updateSurveyResponse', 'createSurveyResponse', 'setSurveyResponse']),
        ...mapActions('question', ['fetchQuestions']),
        async initialize () {
            await this.fetchSurveyResponse({ oId: this.eseaAccount?.organisation || 0, eaId: this.eseaAccount?.id || 0, id: this.$route.params.uniquetoken })
            console.log('++++', this.surveyResponse.question_responses)
            await this.fetchSurvey({ mId: this.surveyResponse.method, id: this.surveyResponse.survey })
            await this.fetchQuestions({ mId: this.surveyResponse.method, SuId: this.surveyResponse.survey, SeId: 0 })
            this.loading = false
            if (this.surveyResponse.finished) {
                this.$router.push({ name: 'survey-thank-you' })
            }
        },
        previousSection () {
            if (this.sectionNumber > 0) {
                this.sectionNumber--
                this.activeQuestion = null
            }
        },
        nextSection () {
            if (this.sectionNumber + 1 < this.totalSections.length) {
                this.sectionNumber++
                this.activeQuestion = null
            }
        },
        toggleActive (question) {
            if (Number.isInteger(question)) {
                this.activeQuestion = question
            } else {
                this.activeQuestion = null
                }
        },
        goToQuestion (question) {
            this.sectionNumber = this.totalSections.indexOf(question.section)
            console.log(this.sectionNumber)
            this.missedQuestionsDialog = false
        },
        saveSurvey () {
            // TODO // popup Dialog: Survey is automatically saved.
        },
        async finishSurvey () {
            console.log('cc')
            await this.fetchSurveyResponse({ oId: this.eseaAccount?.organisation || 0, eaId: this.eseaAccount?.id || 0, id: this.$route.params.uniquetoken })

            console.log('eee')
            this.checkRequiredQuestions = true
            this.missedQuestions = []
            await this.checkMandatoryFields()
            console.log('reee')
            if (!this.missedQuestions.length) {
            this.surveyResponse.finished = true
            await this.updateResponse()
            this.$router.push({ name: 'survey-thank-you' })
            } else {
                this.missedQuestionsDialog = true
            }
        },
        updateAnswer (id, questionId, answer) {
            console.log(answer, id, questionId)
            let questionResponse = this.surveyResponse.question_responses.find(response => response.question === questionId)
            if (!questionResponse) {
                questionResponse = { question: questionId, direct_indicator_id: id, values: [], value: null }
            }
            // if (!questionResponse) { return }
            const relevantquestion = this.questions.find(q => q.id === questionId)
            if (relevantquestion.uiComponent === 'checkbox') {
                console.log('------->', answer.answer)
                questionResponse.values = answer.answer
            } else {
                questionResponse.value = answer.answer?.[0] || ''
            }
            this.surveyResponse.question_responses = [questionResponse]

            if (parseInt(this.$route.params.uniquetoken) !== this.surveyResponse.survey) {
                console.log('clearly not the same')
            }
            if ((this.$route.params.uniquetoken !== this.surveyResponse.token) && (this.$route.params.uniquetoken !== 'accountant') && (parseInt(this.$route.params.uniquetoken) !== this.surveyResponse.survey)) {
                console.log('Not possible')
                return
            }
            this.updateResponse()
        },
        async updateResponse () {
            console.log('dddd')
            await this.updateSurveyResponse({
                oId: this.eseaAccount?.organisation,
                eaId: this.eseaAccount?.id,
                token: this.$route.params.uniquetoken,
                surveyResponse: {
                    ...this.surveyResponse
                }
            })
        },
        checkMandatoryFields () {
            for (let i = 0; i < this.survey.sections.length; i++) {
                for (let j = 0; j < this.survey.sections[i].questions.length; j++) {
                    if (this.survey.sections[i].questions[j].isMandatory) {
                        const answer = this.surveyResponse.question_responses.find(response => response.question === this.survey.sections[i].questions[j].id)

                        if (!answer || (!answer.values.length && !answer.value)) {
                            this.survey.sections[i].questions[j].required = true
                            this.missedQuestions.push(this.survey.sections[i].questions[j])
                        }
                    }
                }
            }
        }
    }
}
// this.survey.sections.forEach(Section => { mandatorydict[Section.questions[0].id] = Section.questions[0].isMandatory })
// this.survey.topics[0].sub_topics.forEach(SubTopic => { mandatorydict[SubTopic.questions[0].id] = SubTopic.questions[0].isMandatory })
// this.surveyResponse.question_responses.forEach(response => { if (mandatorydict[response.direct_indicator_id]) { if (!response.values.length && !response.value) { this.missedQuestions.push(response.direct_indicator_id) } } })
//   axios.get('http://127.0.0.1:8000/methods/27/surveys/13/organisations/1/responses/')
//   .then(response => (console.log(response)))
//    AxiosInstance.get('/methods/27/surveys/13/organisations/1/responses/GhjrpoLc/', {}).then(response => (console.log(response)))
// await this.setSurveyResponse({})
// <!-- <survey-question class="p-col-12 p-my-2" style="background-color: white;"
// v-for="question in currentSection"
// :key="question.id"
// :question="question"
// :active="activeQuestion?.id === question.id"
// :answer="answers[question?.direct_indicator[0]?.id] || 0"
// :checkanswerrequired="question.isMandatory"
// :checkrequiredfields="checkRequiredQuestions"
// @input="updateAnswer(question.direct_indicator[0].id, $event)"
// @click="toggleActive(question)"

// /> -->
// console.log('sss', this.surveyResponse)
// this.surveyResponse.question_responses.forEach(response => { if (response.direct_indicator_id === id) { if (answer.answer[0] != null) { if (answer.answertype === ('RADIO' || 'CHECKBOX')) { response.values = answer.answer } else { response.value = answer.answer[0] } } } })
// this.surveyResponse.question_responses.forEach(response => { if (response.direct_indicator_id === id) { response.value = toString(answer.answer[0]) } }) //  console.log(response.value, answer.answer[0])
// this.surveyResponse.question_responses.forEach(response => { if (response.direct_indicator_id === id) { response.value = answer?.answer[0] } else { console.log(response) } }) // response.value = toString(answer?.answer[0] || response.value console.log(response, id)
// <!-- <div v-if="!surveyResponse.finished" class="p-d-flex p-grid p-jc-center p-m-0">
//     <div class="p-col-12 p-p-3" style="background-color: #dcedc8;">
//         <h1>{{survey.name}}</h1>
//         <h3>{{survey.description}}</h3>
//         <p><span class="p-text-bold">Respondent:</span> {{surveyResponse.respondent}} <br> <span class="p-text-bold">Organisation:</span>{{surveyResponse.organisation}} </p>
//     </div>
//     <div class="p-grid p-col-6 p-p-3" style="background-color: white; border-radius: 10px;">
//         <div class="p-col-6 p-text-left">Topic {{ topicNumber + 1}} of {{totalTopics}}</div>
//         <div class="p-col-6 p-text-right"><ProgressBar :value="progress">{{progress}}% completed</ProgressBar></div>
//         <div class="p-col-12 p-text-left"><h3>Topic: '{{currentTopic.name}}'</h3></div>
//         <survey-question class="p-col-12"
//         v-for="question in currentTopic.questions"
//         :key="question.id"
//         :question="question"
//         :answer="answers[question.id]"
//         :checkanswerrequired="question.isMandatory"
//         @input="updateAnswer(question.id, $event)"
//         />
//     <div class="p-col-6 p-text-left">
//         <Button label="Previous Topic" class="p-button-raised p-button-sm" :disabled="topicNumber === 0" @click="previousTopic"/>
//     </div>
//     <div class="p-col-3 p-text-right">
//         <Button label="Save for Now" class="p-button-primary p-button-raised p-button-sm" @click="saveSurvey" />
//     </div>
//     <div class="p-col-3 p-text-right">
//         <Button v-if="topicNumber + 1 < totalTopics" label="Next Topic" class="p-button-raised p-button-sm" style="width: 100%" @click="nextTopic" />
//         <Button v-else label="Finish Survey" class="p-col p-button-success p-button-raised p-button-sm" style="width: 100%" @click="finishSurvey" />
//     </div>
//     </div>
// </div> -->
</script>
