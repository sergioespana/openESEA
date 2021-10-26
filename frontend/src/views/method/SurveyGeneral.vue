<template>
    <form ref="form" class="p-text-left p-fluid p-m-5 p-p-5 p-inputtext-lg" style="width: 1000px; height: 70vh">
        <!-- {{unsavedChangesDialog}}{{lazySurvey}} <hr> {{survey}} -->
        <div class="p-field p-m-3">
            <label for="surveyname">Survey Name</label>
            <InputText ref="surveyname" id="surveyname" type="text" v-model.lazy="lazySurvey.name" @blur="v$.lazySurvey.name.$touch()" :class="{'borderless': nameErrors.length}" lazy />
            <div class="p-error p-text-italic p-pt-1" v-for="error in nameErrors" :key="error">{{error}}</div>
        </div>
        <div class="p-field p-m-3">
            <label for="surveyresponsetype">Response Type</label>
            <Dropdown id="surveyresponsetype" v-model="lazySurvey.response_type" :options="responseTypeList"  optionLabel="value" optionValue="value" placeholder="Select response type"  @blur="v$.lazySurvey.response_type.$touch()" :class="{'p-invalid': v$.lazySurvey.response_type.$invalid}"/>
        </div>
        <div class="p-field p-m-3">
            <label for="surveyminthreshold">Minimal Response Threshold</label>
            <InputNumber id="surveyminthreshold" suffix="%" :min="0" :max="100" v-model.lazy="lazySurvey.min_threshold" lazy  @blur="v$.lazySurvey.min_threshold.$touch()" :class="{'borderless': v$.lazySurvey.min_threshold.$invalid}" />
        </div>
        <div class="p-field p-m-3">
            <label for="welcomingtext">Welcoming Text</label>
            <Textarea id="welcomingtext" v-model="lazySurvey.welcome_text" :autoResize="true" />
            <!-- <div class="p-error p-text-italic" v-for="error in descriptionErrors" :key="error">{{ error }}</div> -->
        </div>
        <div class="p-field p-m-3">
            <label for="closingtext">Closing Text</label>
            <Textarea id="closingtext" v-model="lazySurvey.closing_text" :autoResize="true" />
            <!-- <div class="p-error p-text-italic" v-for="error in descriptionErrors" :key="error">{{ error }}</div> -->
        </div>
    </form>
    <Dialog v-model:visible="unsavedChangesDialog" header="Unsaved Changes" :modal="true" :dismissableMask="true">
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
import { mapState, mapActions } from 'vuex'
import Dropdown from 'primevue/dropdown'
import { RESPONSE_TYPE } from '../../utils/constants'
import { isEqual, cloneDeep } from 'lodash'
import { required, maxLength, between } from '../../utils/validators'
import HandleValidationErrors from '../../utils/HandleValidationErrors'
import useVuelidate from '@vuelidate/core'

    export default {
        components: {
            Dropdown
        },
        setup: () => ({ v$: useVuelidate() }),
        validations: {
            lazySurvey: {
                name: { required, maxLength: maxLength(120) },
                min_threshold: { required, between: between(0, 100) },
                response_type: { required }
            }
        },
        data () {
            return {
                lazySurvey: cloneDeep(this.survey) || {},
                response_type: RESPONSE_TYPE,
                unsavedChangesDialog: false,
                discardUnsavedChanges: false,
                to: null
            }
        },
        computed: {
            ...mapState('survey', ['survey', 'errors', 'isSaved']),
            responseTypeList () {
                return Object.entries(this.response_type).map(([text, value]) => ({ text, value }))
            },
            nameErrors () {
                return HandleValidationErrors(
                    this.v$.lazySurvey.name,
                    this.errors.name
                )
            }
        },
        watch: {
            survey (val) {
                if (isEqual(this.lazySurvey, val)) { return }
                this.lazySurvey = cloneDeep(val)
            },
            lazySurvey: {
                handler (val) {
                    setTimeout(() => {
                        if (this.v$.$invalid) { return }
                        if (isEqual(this.survey, val)) { return }
                        this.updateSurvey({ mId: this.$route.params.id, survey: val })
                    }, 200)
                },
                deep: true
            }
        },
        beforeRouteLeave (to, from, next) {
        if ((this.v$.$invalid || !this.isSaved) & !this.discardUnsavedChanges) {
            this.unsavedChangesDialog = true
            this.to = to
        } else {
            next(true)
        }
    },
        mounted () {
            this.lazySurvey = cloneDeep(this.survey)
            if (!this.lazySurvey.name.length) {
                this.$refs.surveyname.$el.focus()
            }
        },
        methods: {
            ...mapActions('survey', ['updateSurvey']),
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
    .p-inputtext {
        border: none;
        border-bottom: 1px solid lightgrey;
    }
    .borderless {
        border-bottom: 1px solid red;
    }
</style>
