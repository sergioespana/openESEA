http://localhost:8081/method-wizard/2/surveys/5/survey-design/

<template>
    <div class="p-d-flex" style="height: 100%; border-top: 1px solid lightgrey;">
        <div class="p-d-flex p-flex-column p-jc-between" style="height: calc(100vh - 190px;); width: 300px; border: 1px solid lightgrey;">
            <survey-tree-side-bar style="height: 100%;" :key="updateSidebar" />
        </div>
        <div class="p-col p-d-flex p-jc-center" style="height: calc(100vh - 195px); width: 100%; background-color: white; text-align: center; overflow-y: auto;">
            <div class="p-text-left p-fluid" style="width: 1200px;">
                <div v-for="(section, sectionIndex) in items" :key="sectionIndex" class="p-my-5" style="background-color: #f8f9fe; border: 1px solid lightgrey;">
                    <sectioon-form
                        :section="section"
                        :active="activeItem.objType === section.objType && activeItem.id === section.id"
                        :errors="errors[section.id]"
                        :check-saving-status="checkSavingStatus"
                        @savingstatus="savingStatus(section, $event)"
                        @click="toggleActive(section)" @delete="removeSection"
                    />
                    <div v-for="(sectionChild, index) in section.children" :key="index" class="p-my-1 p-ml-5">
                        <question-form ref="items"
                        :question="sectionChild"
                        :active="activeItem.objType === sectionChild.objType && activeItem.id === sectionChild.id"
                        :check-saving-status="checkSavingStatus"
                        @savingstatus="savingStatus(sectionChild, $event)"
                        @click="toggleActive(sectionChild)"
                        @delete="removeQuestion(section, question)" />
                    </div>
                    <div class="addQuestion" @click="addQuestion(section)"><i class="pi pi-plus" /> Add Question</div>
                </div>
                <div class="addQuestion p-mb-5" @click="addSection"><i class="pi pi-plus" /> Add Section</div>
            </div>
        </div>
    </div>

    <Dialog v-model:visible="unsavedChangesDialog" style="width: 600px;" header="Unsaved Changes" :modal="true" :dismissableMask="true">
        <div class="confirmation-content">
            This page contains unsaved changes, leaving the page now will destroy these. Do you still wish to leave the page?
        </div>
        <template #footer>
            <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="unsavedChangesChoice(true)" />
            <Button label="No" icon="pi pi-times" class="p-button-text" @click="unsavedChangesChoice(false)"/>
        </template>
    </Dialog>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex'
    import SurveyTreeSideBar from '@/components/SurveyTreeSideBar'
    import getSurveyItems from '@/utils/getSurveyItems'
    import SectioonForm from '../../components/forms/SectioonForm'
    import QuestionForm from '@/components/forms/QuestionForm'

    export default {
        components: {
            SurveyTreeSideBar,
            QuestionForm,
            SectioonForm
        },
        data () {
            return {
                checkSavingStatus: false,
                SectionAndQuestionSavingStatus: {},
                to: null,
                allowRouting: false,
                unsavedChangesDialog: false,
                discardUnsavedChanges: false,
                updateSidebar: 0
            }
        },
        computed: {
            ...mapState('method', ['method']),
            ...mapState('survey', ['survey']),
            ...mapState('section', ['sections', 'section', 'errors']),
            ...mapState('question', ['questions', 'question', 'updatedList']),
            ...mapGetters('question', ['sectionQuestions']),
            items () {
                return getSurveyItems(
                    this.sections,
                    this.sectionQuestions
                )
            },
            activeItem () {
                let objType = 'section'
                let { id } = this.section

                if (this.question.id) {
                    objType = 'question'
                    id = this.question.id
                }
                return { objType, id }
            },
            errors () {
                return {
                    section: this.sectionErrors,
                    question: this.questionErrors
                }
            }
        },
            beforeRouteLeave (to, from, next) {
            if (this.allowRouting || this.discardUnsavedChanges) { //  & !this.discardUnsavedChanges @input="saveActive('section', $event)"  @input="saveActive(sectionChild.objType, $event)"
                next(true)
            } else {
                this.to = to
                this.allowRouting = false
                this.checkSavingStatus = !this.checkSavingStatus
                next(false)
            }
        },
        watch: {
            SectionAndQuestionSavingStatus: {
                handler (val) {
                    if ((Object.keys(val).length === (this.questions.length + this.sections.length))) {
                        for (const key in val) {
                            if (val[key]) {
                                this.SectionAndQuestionSavingStatus = {}
                                console.log('...')
                                this.unsavedChangesDialog = true
                                return
                            }
                        }
                        this.allowRouting = true
                        this.$router.push(this.to)
                    }
                },
                deep: true
            },
            // Used to rerender the sidebar component
            updatedList (val) {
                if (val) {
                    this.updateSidebar += 1
                }
            }
        },
        created () {
            this.initialize()
        },
        methods: {
            ...mapActions('survey', ['fetchSurvey', 'updateSurvey', 'saveSurvey']),
            ...mapActions('section', ['fetchSections', 'createSection', 'setSection', 'updateSection', 'addNewSection', 'deleteSection']),
            ...mapActions('question', ['fetchQuestions', 'setQuestion', 'addNewQuestion', 'updateQuestion', 'deleteQuestion']),
            async initialize () {
                if (this.survey.id !== parseInt(this.$route.params.SurveyId)) {
                    this.$router.push({ name: 'method-wizard-surveys' })
                }

                await this.fetchSections({ mId: this.method.id, sId: this.survey.id })
                await this.fetchQuestions({ mId: this.method.id, SuId: this.survey.id, SeId: 0 })
            },
            addSection () {
                this.createSection({ mId: this.method.id, sId: this.survey.id }) //  this.addNewSection({ survey: this.survey.id })
                this.setQuestion()
            },
            addQuestion (section) {
                this.addNewQuestion({ section: section?.id })
            },
            toggleActive (item) {
                console.log('check', item.objType, item.id, this.question.id)
                const { objType } = item
                const section = { id: item.section || item.id }
                if (objType === 'section') {
                    this.setSection(section)
                    this.setQuestion()
                } else if (objType === 'question' && (item.id !== this.question.id)) {
                    this.setQuestion(item)
                }
            },
            savingStatus (object, status) {
                const key = object.objType + object.id
                this.SectionAndQuestionSavingStatus[key] = status
            },
            unsavedChangesChoice (choice) {
                this.unsavedChangesDialog = false
                this.discardUnsavedChanges = choice
                if (choice) {
                    this.$router.push(this.to)
                }
            }
        }
    }
</script>

<style lang="scss" scoped>
    .addQuestion {
        height: 50px;
        line-height: 50px;
        margin: 50px;
        text-align: center;
        background-color: #E2E2E2;
        border-radius: 5px;
        font-size: 22px;
        font-weight: bold;
        color: black;
    }
    .addQuestion:hover {
        background-color: #E9E9E9;
        border: 1px solid lightgrey;
        cursor: pointer;
    }
</style>
