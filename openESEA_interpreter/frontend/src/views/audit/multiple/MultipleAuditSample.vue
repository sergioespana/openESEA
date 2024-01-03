<template>
    <div class="p-p-3">
        <h2 class="p-text-left">Sample Overview</h2>
        <Card class="p-text-left">
            <template #title>
            Survey Response Sample
            </template>
            <template #subtitle>
                Total number of responses:  {{responses}} <br>
                How many responses do you wish to audit?
            </template>
            <template #content class="p-col-12">
                <div class="field-radiobutton p-mb-2">
                    <RadioButton id="choice1" name="choice" value="fixed" class="p-mx-1" v-model="sampleChoice" />
                    <label for="city1">Fixed number</label>
                </div>
                <div class="field-radiobutton">
                    <RadioButton id="choice2" name="choice" value="percentage" class="p-mx-1" v-model="sampleChoice" />
                    <label for="city2">Percentage of Total Responses</label>
                </div>

                <div class="p-pt-5" style="width: 400px;">
                    <InputNumber v-if="sampleChoice ==='fixed'" class="p-col-12 p-m-0 p-p-0" v-model="surveyAudit.sample_size" :max="responses" />
                    <div v-if="sampleChoice ==='percentage'" class="p-inputgroup">
                        <span class="p-inputgroup-addon">%</span>
                        <InputNumber v-model="surveyAudit.sample_size" placeholder="Percentage" :min="0" :max="100" :maxFractionDigits="0" />
                    </div>
                </div>
                <Button class="p-mt-5" label="Sample Responses" @click="sampleResponses()" :disabled="!surveyAudit.sample_size" icon="pi pi-check" />
            </template>
        </Card>
    </div>
</template>

<script>
    import { AxiosInstance } from '@/plugins/axios'
    import { mapState, mapActions } from 'vuex'

    export default {
        data () {
            return {
                sampleChoice: null
            }
        },
        computed: {
            ...mapState('surveyAudit', ['surveyAudit']),
            ...mapState('eseaAccount', ['eseaAccount']),
            responses () {
                // this.eseaAccount.survey_response_by_survey.map(survey
                //     this.respondents.map(respondent => respondent.id)
                // )
                return this.eseaAccount.survey_response_by_survey.find(x => x.id === parseInt(this.$route.params.SurveyId)).responses
            }
        },
        methods: {
            ...mapActions('respondent', ['setRespondents']),
            ...mapActions('surveyAudit', ['fetchSurveyAudit']),
            async sampleResponses () {
                // Save sample_size to survey_audit object
                var data = {}
                if (this.sampleChoice === 'percentage') {
                    data = { sample_size_fixed: this.surveyAudit.sample_size }
                } else if (this.sampleChoice === 'fixed') {
                    data = { sample_size_fixed: this.surveyAudit.sample_size }
                }
                await AxiosInstance.post(`/esea-account/${this.$route.params.EseaAccountId}/survey-audit/${this.$route.params.SurveyId}/sample-survey-responses/`, data)
                .then(async (response) => {
                    await this.fetchSurveyAudit({ oId: this.$route.params.OrganisationId, eaId: this.$route.params.EseaAccountId, id: this.surveyAudit.id })
                    this.setRespondents(response)
                    console.log(response.data)
                    this.$router.push({ name: 'multiplesampleoverview', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } })
                })
                // Get number of sampled responses
            }
        }
    }
</script>
