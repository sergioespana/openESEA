<template>
    <form v-if="active" ref="form"  class="p-d-flex p-ai-center p-fluid p-input-filled p-text-center p-pt-1" @submit.prevent="!v$.$invalid"
    :style="[(active) ? 'border: 2px solid #9ecaed;':'border: 1px solid lightgrey;',
    (valid) ? '': 'border: 1px solid rgba(255, 0, 0, 0.5);']" style="width: 100%;">
        <div class="p-d-flex p-px-2 p-ai-center" style="width: 100%;">
            <div class="p-pl-2" style="width: 40px;">
                <ProgressSpinner v-if="(loading && !failedToUpDate)" style="width: 35px;"/>
                <i v-else-if="!valid" class="pi pi-refresh p-d-flex p-jc-center p-ai-center p-m-0 p-p-0" style="font-size: 30px; color: #ff6666; cursor: pointer;" @click="updateThisSection()" />
                <i v-if="valid" class="pi pi-check p-d-flex p-jc-center p-ai-center p-m-0 p-p-0" style="font-size: 30px; color: #9ecaed;" />
            </div>
            <div class="p-grid p-mx-5 p-pt-5" style="width: 100%;">
                <div style="width: 100%;">
                    <div class="p-field">
                        <span class="p-float-label">
                            <InputText id="sectiontitle" ref="input" v-model.lazy="lazySection.title" :class="{'p-invalid': v$.lazySection.title.$invalid}" @blur="v$.lazySection.title.$touch()" />
                            <label for="sectiontitle">Title</label>
                        </span>
                        <div class="p-error p-text-italic p-text-left" v-for="error in titleErrors" :key="error"><small>{{error}}</small></div>
                    </div>
                </div>
            </div>
            <i class="pi pi-trash p-d-flex p-jc-center p-ai-center p-pr-5" style="width: 40px; font-size: 30px; color: #ff6666; cursor: pointer;" @click="removeSection()" />
        </div>
    </form>
    <sectioon-card v-else :title="lazySection.title" :style="[(valid) ? 'border: 1px solid green;': 'border: 1px solid rgba(255, 0, 0, 0.3);']" />
</template>

<script>
import { mapActions } from 'vuex'
import { isEqual, cloneDeep } from 'lodash'
import HandleValidationErrors from '../../utils/HandleValidationErrors'
import useVuelidate from '@vuelidate/core'
import { required } from '../../utils/validators'
import SectioonCard from '@/components/cards/SectioonCard'
import ProgressSpinner from 'primevue/progressspinner'

export default {
    components: {
        SectioonCard,
        ProgressSpinner
    },
    props: {
        section: {
            type: Object,
            required: true
        },
        active: {
            type: Boolean,
            default: false
        },
        errors: {
            type: Object,
            default: () => ({})
        },
        checkSavingStatus: {
            type: Boolean
        }
    },
    setup: () => ({ v$: useVuelidate() }),
    validations: {
        lazySection: {
            title: { required }
        }
    },
    data () {
        return {
            lazySection: cloneDeep(this.section) || { },
            // selectedQuestions: this.section?.questions || [],
            loading: false,
            failedToUpDate: false
        }
    },
    computed: {
        titleErrors () {
            return HandleValidationErrors(
                this.v$.lazySection.title,
                this.errors.title
            )
        },
        valid () {
            return (!this.v$.lazySection.$invalid && (this.lazySection.id > 0) && this.uptodate)
        },
        uptodate () {
            return (isEqual(this.section, this.lazySection))
        }
    },
    watch: {
        section (val) {
            this.loading = false
            if (isEqual(this.lazySection, val)) { return }
            this.lazySection = cloneDeep(val)
        },
        lazySection: {
            handler (val) {
                this.failedToUpDate = false
                setTimeout(() => {
                    if (isEqual(this.section, this.lazySection)) { return }
                    this.v$.lazySection.$touch()
                    if (this.v$.lazySection.$invalid) { return }
                    this.updateThisSection()
                }, 200)
            },
            deep: true
        },
        checkSavingStatus () {
            this.$emit('savingstatus', this.v$.lazySection.$invalid)
        }
    },
    // created () {
    //     this.lazySection = cloneDeep(this.section)
    // },
    methods: {
        ...mapActions('section', ['updateSection', 'deleteSection']),
        async updateThisSection () {
            this.loading = true
            this.failedToUpDate = false
            setTimeout(() => { this.failedToUpDate = true }, 5000)
            await this.updateSection({
                mId: this.$route.params.id,
                sId: this.$route.params.SurveyId,
                section: this.lazySection
            })
        },
        async removeSection () {
            await this.deleteSection({ mId: this.$route.params.id, sId: this.$route.params.SurveyId, id: this.lazySection.id })
        }
    }
}
// <!-- <div class="p-grid p-m-0 p-pt-5" style="background-color: #F1F1F1; border: 1px solid #D8D8D8;"> -->
// <!-- <tree-select v-model="selectedQuestions" :options="goodItems" selectionMode="checkbox"  placeholder="Select Items" @blur="updateQuestions" class="p-col-12" :class="{'borderless': questionsErrors.length}" /> -->
// <!-- <MultiSelect v-model="selectedQuestions" :options="questions" optionLabel="name" placeholder="Select Questions" class="p-col-12 p-my-2" :class="{'p-invalid': v$.lazySection.questions.$invalid}" @blur="v$.lazySection.questions.$touch()" /> @blur="updateQuestions" :class="{'borderless': questionsErrors.length} -->
// <!--<Button label="Delete Section" class="p-col p-button-danger p-button-text" @click="deleteSection" /><div class="p-col-12 p-error p-text-italic p-pt-1" v-for="error in questionsErrors" :key="error">{{error}}</div> -->
// <!-- <div class="p-error p-text-italic p-pt-1" v-for="error in nameErrors" :key="error">{{error}}</div> -->

// <!-- <div style="width: 100%;">
//     <div v-if="active" class="p-d-flex p-m-0 p-p-5" style="width: 100%;">
//         <div style="width: 40px;">
//             <ProgressSpinner v-if="(loading && !failedToUpDate)" style="width: 35px;"/>
//             <i v-else-if="!valid" class="pi pi-refresh p-d-flex p-jc-center p-ai-center" style="font-size: 30px; height: 100%; color: #ff6666; cursor: pointer;" @click="updateThisTopic()" />
//             <i v-if="valid" class="pi pi-check p-d-flex p-jc-center p-ai-center p-p-0" style="font-size: 30px; height: 100%; color: #9ecaed;" />
//         </div>
//         <span class="p-float-label p-pl-3 p-m-0" style="width: 100%;">
//             <InputText id="sectiontitle" type="text" v-model.lazy="lazySection.title" :class="{'p-invalid': v$.lazySection.title.$invalid}" @blur="v$.lazySection.title.$touch()" />
//             <label for="sectiontitle">Title</label>
//         </span>
//         <i class="pi pi-trash" style="width: 10%; font-size: 30px; color: red;" @click="deleteSection()" />
//     </div>
//     <h2 v-else>{{lazySection.title}}</h2>
// </div> -->
// <!-- <div v-if="v$.lazySection.questions.$invalid" class="p-error p-text-left">Be sure to add atleast one question to keep this section!</div> -->  <!-- rgba(0, 153, 51, 1) -->

// ,
//         deleteSection () {
//             console.log('eeee')
//             this.$emit('delete', this.section)
//         }
// questions: {
//     required,
//     minLength: minLength(1)
// }
 // ,
// selectedQuestions (val) {
//     const templist = []
//     val.forEach((question) => templist.push(question.id))
//     console.log(templist)
//     this.lazySection.questions = templist
// }
// survey: {
//     type: Number,
//     required: true
// },
// questions: {
//     type: Object,
//     required: true
// },
// import MultiSelect from 'primevue/multiselect' border: 1px solid #00695C; !v$.lazySection.$invalid && lazySection.id > 0
</script>
