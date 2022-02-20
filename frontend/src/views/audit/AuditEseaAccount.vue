<template>
    <div style="background-color: white; height: 100%;">
        <div class="p-d-flex p-ai-center" style="background-color: #f7f7f7;" @click="goToEseaAccount()">
            <i class="pi pi-angle-left p-mx-3" style="fontSize: 2rem"></i>
            <h4>ESEA account</h4>
        </div>
        <h1>Workforce Survey audit</h1>
        <div class="p-grid p-m-5">
            <div class="p-col-6">Organisation: {{this.eseaAccount.organisation_name}} </div>
            <div class="p-col-6">Auditor: {{this.surveyAudit.auditor}} </div>
            <div class="p-col-6">Type: {{this.survey.response_type}} </div>
            <div class="p-col-6">Deadline: {{ dateFixer(this.surveyAudit.deadline, 'MMMM Do YYYY') }} </div>
        </div>
        <Steps :model="steps" :readonly="false" @click="test">
            <template #item="{item}">
                {{item.label}} {{item.label}}
                <!-- <a :href="item.to">{{item.label}}--1</a> -->
            </template>
            <!--<router-link :to="item.to" custom v-slot="{href, navigate, activeIndex}"> :style="[activeIndex ? 'background-color: red;':'background-color: blue;']"
                <a :href="href" @click="navigate" style="background-color: blue;">{{activeIndex}}--{{item.label}}</a>
                {{activeIndex}}
            </router-link>-->
        </Steps>
        <Divider class="p-my-5" />
        <router-view class="p-m-5" />
    </div>
</template>

<script>
    import Steps from 'primevue/steps'
    import { mapState } from 'vuex'
    import dateFixer from '../../utils/datefixer'

    export default {
        components: {
            Steps
        },
        data () {
            return {
                styleObject: {
                    backgroundColor: 'red',
                    color: 'red',
                    fontSize: '13px'
                },
                single_audit_steps: [
                    {
                        label: 'Question Selection',
                        to: { name: 'questionselection', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } },
                        active: true
                    },
                    {
                        label: 'Documentation request',
                        to: { name: 'documentationrequest', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } },
                        active: false
                    },
                    {
                        label: 'Documentation upload',
                        to: { name: 'documentationupload', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } },
                        active: false
                    },
                    {
                        label: 'Audit',
                        to: { name: 'singleauditaudit', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } },
                        active: false
                    },
                    {
                        label: 'Results',
                        to: { name: 'singleauditresults', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } },
                        active: false
                    }
                ]
            }
        },
        computed: {
            ...mapState('eseaAccount', ['eseaAccount']),
            ...mapState('survey', ['survey']),
            ...mapState('surveyAudit', ['surveyAudit']),
            steps () {
                if (this.survey.response_type === 'single') {
                    return [
                    {
                        label: 'Question Selection',
                        to: { name: 'questionselection', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } },
                        active: true
                    },
                    {
                        label: 'Documentation request',
                        to: { name: 'documentationrequest', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } },
                        active: false
                    },
                    {
                        label: 'Documentation upload',
                        to: { name: 'documentationupload', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } },
                        active: false
                    },
                    {
                        label: 'Audit',
                        to: { name: 'singleauditaudit', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } },
                        active: false
                    },
                    {
                        label: 'Results',
                        to: { name: 'singleauditresults', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } },
                        active: false,
                        disabled: (this.surveyAudit.status !== 'verified' && this.surveyAudit.status !== 'rejected')
                    }
                ]
                } else {
                    return [
                    {
                        label: 'Response Sample',
                        to: { name: 'multipleauditsampling', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } },
                        active: true
                    },
                    {
                        label: 'Sample Overview',
                        to: { name: 'multiplesampleoverview', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } },
                        active: false
                        // disabled: !survey_audit.sample_size
                    },
                                    {
                        label: 'Audit',
                        to: { name: 'multipleaudit', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } },
                        active: true
                    },
                    {
                        label: 'Results',
                        to: { name: 'multipleauditresults', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } },
                        active: false,
                        disabled: (this.surveyAudit.status !== 'verified' && this.surveyAudit.status !== 'rejected')
                    }
                ]
                }
            }
        },
        methods: {
            dateFixer,
            goToPage () {
                this.$router.push({ name: 'questionselection', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } })
            },
            goToEseaAccount () {
                this.$router.push({ name: 'organisationeseaaccount', params: { OrganisationId: this.eseaAccount.organisation, EseaAccountId: this.$route.params.EseaAccountId } })
            },
            test ($event) {
                console.log($event.data)
            }
        }
    }
</script>

<style lang="scss">
    // Gives equal width to the Steps component items
    .p-steps-item {
        width: 100px;
    }
    .p-steps .p-steps-item .p-menuitem-link .p-steps-number {
        background-color: #f2f2f2;
    }
    // .p-steps .p-steps-item .p-highlight .p-steps-number {
    //     background-color: green;
    // }
</style>
