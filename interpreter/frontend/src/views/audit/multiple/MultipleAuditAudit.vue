<template>
    <div class="p-mx-3">
        <div class="p-d-flex p-ai-center p-jc-between">
            <h2 class="p-text-left">Audit</h2>
            <Button @click="resendMail()" label="Send verification mail" class="p-button-sm p-button-warning" icon="pi pi-envelope" />
        </div>
        <DataTable :value="respondents" dataKey="id" selectionMode="single" showGridlines autoLayout
            :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
            :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

            <Column header="Respondent" headerStyle="min-width: 250px;">
                <template #body="{data}">
                    {{ data.first_name}} {{ data.last_name_prefix }} {{ data.last_name}}
                </template>
            </Column>
            <Column header="Email adress" headerStyle="text-align: center" > <!-- bodyStyle="text-align: center; overflow: visible" -->
                <template #body="data">
                        <div class="p-d-flex p-ai-center p-jc-between">
                            {{data.data.email}}
                            <Button :icon="((sending_mails === data.data.email || sending_mails === true) ? 'pi pi-spin pi-spinner' : 'pi pi-replay')" class="p-button-warning p-button-sm" @click="resendMail(data)" />
                        </div>
                </template>
            </Column>
        </Datatable>
        <div class="p-d-flex p-jc-end">
            <div class="p-py-3" style="width: 300px;">
                <Button @click="verifyAudit('verified')" label="Verify" icon="pi pi-check" class="p-button-success p-button-sm p-mb-3" style="width: 100%;" />
                <Button @click="verifyAudit('rejected')" label="Reject" icon="pi pi-times" class="p-button-danger p-button-sm" style="width: 100%;" />
            </div>
        </div>
    </div>

    <Dialog v-model:visible="verificationDialog" style="width: 500px;" header="Help" :modal="true" dismissableMask="true">
        <p>Are you sure you wish to {{verified ? 'verify': 'reject'}} the survey responses?</p>
        <template #footer>
            <Button label="Yes" class="p-button-sm" icon="pi pi-check" @click="verifySurveyAudit()" />
            <Button label="No" class="p-button-sm" icon="pi pi-times" @click="verificationDialog = false" />
        </template>
    </Dialog>
</template>

<script>
    import { mapState, mapActions } from 'vuex'
    import { AxiosInstance } from '@/plugins/axios'

    export default {
        data () {
            return {
                verificationDialog: false,
                verified: null,
                sending_mails: false,
                tablevals: [
                    { id: 1, respondent: 'Henk', email: 'henk@mail.com' },
                    { id: 2, respondent: 'Henriette', email: 'henriette@mail.com' }
                    ]
            }
        },
        computed: {
            ...mapState('respondent', ['respondents']),
            ...mapState('surveyAudit', ['surveyAudit'])
        },
        methods: {
            ...mapActions('surveyAudit', ['updateSurveyAudit']),
            async verifySurveyAudit () {
                // save survey_audit_object.verified = this.verified
                // async/await
                this.surveyAudit.status = this.verified
                await this.updateSurveyAudit({ oId: this.$route.params.OrganisationId, eaId: this.$route.params.EseaAccountId, id: this.surveyAudit.id, data: this.surveyAudit })
                this.$router.push({ name: 'multipleauditresults', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } })
                // if this.verified === true, save survey to esea_account.verified_surveys
            },
            async resendMail (data) {
                var respondentIds = null
                if (data) {
                    this.sending_mails = data.data.email
                    respondentIds = [data.data.id]
                } else {
                    this.sending_mails = true
                    respondentIds = this.respondents.map(respondent => respondent.id)
                }
                console.log('-->', this.respondents, respondentIds)
                await AxiosInstance.post(`/esea-account/${this.$route.params.EseaAccountId}/survey-audit/${this.$route.params.SurveyId}/send-audit-emails/`, { respondents: respondentIds })
                .then(async (response) => {
                    console.log(response.data)
                    setTimeout(() => { this.sending_mails = false }, 2000)
                })
            },
            verifyAudit (choice) {
                this.verified = choice
                this.verificationDialog = true
            }
        }
    }
</script>
