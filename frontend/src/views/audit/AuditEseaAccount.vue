<template>
    <div style="background-color: white; height: 100%;">
        <div class="p-d-flex p-ai-center" style="background-color: #f7f7f7;" @click="goToEseaAccount()">
            <i class="pi pi-angle-left p-mx-3" style="fontSize: 2rem"></i>
            <h4>ESEA account</h4>
        </div>
        <h1>Workforce Survey audit</h1>
        <div class="p-grid p-mt-5">
            <div class="p-col-6">Organisation:</div>
            <div class="p-col-6">Auditor:</div>
            <div class="p-col-6">Type:</div>
            <div class="p-col-6">Deadline:</div>
        </div>
        <Steps :model="items" :readonly="false" class="p-m-5" />
        <Divider class="p-my-5" />
        <router-view class="p-m-5" />
    </div>
</template>

<script>
import Steps from 'primevue/steps'
import { mapState } from 'vuex'

export default {
    components: {
        Steps
    },
    data () {
        return {
            items: [{
                label: 'Question Selection',
                to: { name: 'questionselection', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } }
            },
            {
                label: 'Documentation request',
                to: { name: 'documentationrequest', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } }
            },
            {
                label: 'Documentation upload',
                to: { name: 'documentationupload', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } }
            },
            {
                label: 'Audit',
                to: { name: 'singleauditaudit', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } }
            },
            {
                label: 'Results',
                to: { name: 'singleauditresults', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } }
            }]
        }
    },
    computed: {
        ...mapState('eseaAccount', ['eseaAccount'])
    },
    methods: {
        goToPage () {
            this.$router.push({ name: 'questionselection', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } })
        },
        goToEseaAccount () {
            this.$router.push({ name: 'organisationeseaaccount', params: { OrganisationId: this.eseaAccount.organisation, EseaAccountId: this.$route.params.EseaAccountId } })
        }
    }
}
</script>

<style lang="scss">
    // Gives equal width to the Steps component items
    .p-steps-item {
        width: 100px;
    }
</style>
