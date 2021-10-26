<template>
<div class="p-shadow-10 p-d-flex p-jc-center">
    <div class="p-shadow-5 p-m-5 p-p-5" style="width: 80%">
        <div class="p-d-flex p-ai-center p-jc-between">
        <h1>Stakeholder Survey</h1> <Button label="Create Survey" class="p-button-info p-button-lg" @click="addSurvey()" />
        </div>
        <p class="p-text-left p-mb-5">Connect your question indicators to the desired stakeholder groups</p>
        <div v-for="survey in surveys" :key="survey.id">
        <Panel :header="survey.name" :toggleable="true" class="p-my-5">
            <template #icons>
                <!-- <Button class="p-panel-header-icon p-link p-mr-2" @click="toggle">
                    <span class="pi pi-cog"></span>
                </Button> -->
                <Button icon="pi pi-trash" class="p-panel-header-icon p-link" @click="removeSurvey(survey.id)" />    <!-- <Menu id="config_menu" ref="menu" :model="items" :popup="true" /> -->
            </template>
            <div class="p-col-12 p-d-flex p-jc-start">
            <Button type="button" :label="isSaved[survey?.id] ? 'Saved' : 'Unsaved'" icon="pi pi-check" :class="isSaved[survey?.id] ? '' : 'p-button-warning'" />
            </div>
            <survey-form :survey="survey" :items="items" :questions="questions" :stakeholders="stakeholders" :errors="errors[survey.id] || {}" @goodinput="saveSurvey" />
        </Panel>
        </div>
        <Button label="Add Survey" icon="pi pi-plus" class="p-col-12 p-button-text p-text-left p-p-5" @click="addSurvey()" />
    </div>
</div>
</template>

<script>
import Panel from 'primevue/panel'
import SurveyForm from '../../components/forms/SurveyForm'
import { mapActions, mapGetters, mapState } from 'vuex'
import getMethodItems from '../../utils/getMethodItems'

export default {
    components: {
        Panel,
        SurveyForm
    },
    data () {
        return {
        }
    },
    computed: {
        ...mapState('method', ['method']),
        ...mapState('survey', ['surveys', 'error', 'errors', 'isSaved']),
        ...mapState('question', ['questions']),
        ...mapGetters('topic', ['methodTopics', 'subTopics']),
        ...mapGetters('question', ['topicQuestions']),
        items () {
            return getMethodItems(
                this.methodTopics,
                this.subTopics,
                this.topicQuestions,
                []
            )
        },
        stakeholders () {
            return ['members', ...this.surveys.map(survey => survey.stakeholder).filter(stakeholder => stakeholder !== '' && stakeholder)]
        }
    },
    created () {
        this.initialize()
    },
    methods: {
        ...mapActions('method', ['fetchMethod']),
        ...mapActions('topic', ['fetchTopics']),
		...mapActions('question', ['fetchQuestions']),
		...mapActions('indirectIndicator', ['fetchIndirectIndicators']),
		...mapActions('survey', ['fetchSurveys', 'updateSurvey', 'addNewSurvey', 'deleteSurvey']),
        ...mapActions('section', ['fetchSections']),
        async initialize () {
            const methodId = parseInt(this.$route.params.id, 10)
            if (this.method.id !== methodId) {
                const { error } = await this.fetchMethod({ id: methodId })
                if (error) {
                    this.$router.push({ name: 'methods' })
                }
            }
            await this.fetchTopics({ mId: this.method.id })
            await this.fetchQuestions({ mId: this.method.id, SuId: 0, SeId: 0 })
            await this.fetchIndirectIndicators({ mId: this.method.id })
            await this.fetchSurveys({ mId: this.method.id })
            await this.fetchSections({ mId: parseInt(this.method.id), sId: 0 })
        },
        addSurvey () {
            this.addNewSurvey()
        },
        saveSurvey (survey) {
            this.updateSurvey({ mId: this.method.id, survey: survey })
        },
        removeSurvey (id) {
            this.deleteSurvey({ mId: this.method.id, id })
        }
    }
}
</script>
