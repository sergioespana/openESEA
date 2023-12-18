<template>
    <form ref="form" class="p-grid p-fluid p-input-filled p-text-left p-py-5">
        <div class="p-col-6 p-field">
            <span class="p-float-label">
            <InputText id="surveyname" type="text" v-model.lazy="lazySurvey.name" @blur="updateName" :class="{'borderless': nameErrors.length}" lazy />
            <label for="surveyname">Survey Name</label>
            </span>
            <div class="p-error p-text-italic p-pt-1" v-for="error in nameErrors" :key="error">{{error}}</div>
        </div>
        <div class="p-col-3">
        <Dropdown v-model="lazySurvey.response_type" :options="responseTypeList"  optionLabel="text" optionValue="value" placeholder="Select response type" :class="{'p-invalid': v$.lazySurvey.response_type.$error}"/>
        </div>
        <!-- <div class="p-col-8">
            <span class="p-float-label">
            <InputText id="surveystakeholders" type="text" v-model.lazy="lazySurvey.stakeholdergroup" @blur="updateStakeholder" :class="{'borderless': stakeholderErrors.length}" lazy />
            <label for="surveystakeholders">Stakeholder Group</label>
            </span>
            <div class="p-error p-text-italic p-pt-1" v-for="error in stakeholderErrors" :key="error">{{error}}</div>
        </div> -->
        <div class="p-col-3">
            <span class="p-float-label">
                <InputNumber id="surveyminthreshold" suffix="%" :min="0" :max="100" v-model.lazy="lazySurvey.min_threshold" lazy :class="{'borderless': v$.lazySurvey.min_threshold.$error}" />
                <label for="surveyresponserate">Minimal Response Threshold</label>
            </span>
        </div>
        <div class="p-col-6 p-field">
            <label for="description">Welcoming Text</label>
            <Textarea id="description" v-model="lazySurvey.welcome_text" :autoResize="true" />
            <!-- <div class="p-error p-text-italic" v-for="error in descriptionErrors" :key="error">{{ error }}</div> -->
        </div>
        <div class="p-col-6 p-field">
            <label for="description">Closing Text</label>
            <Textarea id="description" v-model="lazySurvey.closing_text" :autoResize="true" />
            <!-- <div class="p-error p-text-italic" v-for="error in descriptionErrors" :key="error">{{ error }}</div> -->
        </div>
        <div class="p-col-12">
            <section-form v-for="section in surveySections[survey.id]" :key="section.id" :section="section" :questions="questions" @input="saveSection" @delete="removeSection" class="p-m-2" />
             <Button label="Add New Section" icon="pi pi-plus" class="p-col-12 p-button-text p-text-left p-p-5" @click="addSection" :disabled="(lazySurvey?.id < 0)" />
        </div>
        <Divider />

        <Button label="Save Survey" class="p-m-2" @click="saveSurvey" :loading="loading" />
    </form>
</template>
<script>
import { mapGetters, mapActions, mapState } from 'vuex'
import useVuelidate from '@vuelidate/core'
import { RESPONSE_TYPE } from '../../utils/constants'
import { required, maxLength, between } from '../../utils/validators'
import HandleValidationErrors from '../../utils/HandleValidationErrors'
import SectionForm from '../../components/forms/sectionForm'
// import getMethodItems from '../../utils/getMethodItems'
import { isEqual } from 'lodash'
import Dropdown from 'primevue/dropdown'

export default {
    components: {
        SectionForm,
        Dropdown
    },
    props: {
        survey: {
            type: Object,
            required: true
        },
        items: {
            type: Array,
            required: true
        },
        questions: {
            type: Array,
            required: true
        },
        stakeholders: {
            type: Array,
            required: true
        },
        errors: {
            type: Object,
            required: true
        }
    },
    data () {
        return {
            loading: false,
            lazySurvey: { ...this.survey },
            response_type: RESPONSE_TYPE
        }
    },
    computed: {
        ...mapState('section', ['sections']),
        ...mapState('method', ['method']),
        ...mapGetters('topic', ['methodTopics', 'subTopics']),
		...mapGetters('question', { topicQuestions: 'topicQuestions' }),
        ...mapGetters('section', ['surveySections']),
        responseTypeList () {
            return Object.entries(this.response_type).map(([text, value]) => ({ text, value }))
        },
        nameErrors () {
            return HandleValidationErrors(
                this.v$.lazySurvey.name,
                this.errors.name
            )
        },
        questionsErrors () {
            return HandleValidationErrors(
                this.v$.lazySurvey.questions,
                this.errors.questions
            )
        }
    },
    watch: {
        survey (val) {
            if (!isEqual(this.lazySurvey, val)) {
                console.log('not the same')
                this.lazySurvey = { ...val }
            }
        },
        lazySurvey: {
            handler (val) {
                setTimeout(() => {
                    if (this.v$.$invalid) { return }
                    // this.lazySurvey.questions.sort()
                    if (isEqual(this.survey, val)) { return }
                    this.$emit('goodinput', this.lazySurvey)
                }, 5000)
            },
            deep: true
        }
    },
    setup: () => ({ v$: useVuelidate() }),
    validations: {
        lazySurvey: {
            name: { required, maxLength: maxLength(120) },
            // stakeholdergroup: { required, minLength: minLength(4) },
            min_threshold: { required, between: between(0, 100) },
            response_type: { required }
            // questions: { required, minLength: minLength(1) }
        }
    },
    methods: {
        ...mapActions('section', ['addNewSection', 'createSection', 'updateSection', 'deleteSection']),
        updateName () {
            this.v$.lazySurvey.name.$touch()
        },
        updateQuestions () {
            // this.lazySurvey.questions = this.selectedQuestions
            this.v$.lazySurvey.questions.$touch()
        },
        saveSurvey () {
            this.loading = true
            // this.lazySurvey.questions = this.selectedQuestions
            this.v$.lazySurvey.$touch()
            setTimeout(() => { this.loading = false }, 500)
        },
        async addSection () {
            await this.createSection({ mId: this.survey.method, sId: this.survey.id })
            // await this.addNewSection({ survey: this.survey.id })
        },
        async saveSection (section) {
            if (section.id) {
                await this.updateSection({ mId: this.method.id, sId: this.survey.id, id: section?.id, data: section })
            }
        },
        async removeSection (section) {
            await this.deleteSection({ mId: this.method.id, sId: this.survey.id, id: section.id })
        }
    }
}
// goodItems () {
//     const data = getMethodItems(this.methodTopics,
//         this.subTopics,
//         this.topicQuestions,
//         this.topicIndirectIndicators)

//     for (const topic of data) {
//         topic.label = topic.name
//         for (const subtopic of topic.children) {
//             subtopic.label = subtopic.name
//             for (const indicator of subtopic.children) {
//                 indicator.label = indicator.name
//             }
//         }
//     }
//     return data
// }
// this.lazySurvey.stakeholders = []
// if (this.surveystakeholder !== undefined) {
// this.lazySurvey.stakeholders.push(this.surveystakeholder)
// }
// console.log('==', this.lazySurvey.questions, this.lazySurvey.stakeholdergroup)
// console.log(this.v$.lazySurvey.questions)
// <div class="p-grid p-col-12 p-mx-0 p-px-0 p-field">
// <div class="p-col-4">
// <!-- <span class="p-float-label">
//     <InputText id="questionkey" type="text" v-model="dd"  :class="{'borderless': keyErrors.length}"  @blur="questionKeyFilter" :disabled="!active" />
//     <label for="questionkey">Question Key</label>
// </span>
// <div class="p-error p-text-italic" v-for="error in keyErrors" :key="error"><small>{{error}}</small></div> -->
// </div>
// </div>
</script>

<style lang="scss" scoped>
.p-inputtext {
    border: none;
    border-bottom: 1px solid lightgrey;
}
.borderless {
    border-bottom: 1px solid red;

}
</style>
