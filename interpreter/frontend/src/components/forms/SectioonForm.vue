// used by SurveyCreation.vue

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
</script>
