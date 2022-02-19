<template>
    <div class="p-p-3">
        <div class="p-d-flex p-ai-center p-jc-between">
            <h2 class="p-text-left">Audit</h2>
            <Button @click="resendBatchMail()" label="Send verification mail" class="p-button-sm p-button-warning" icon="pi pi-envelope" />
        </div>
        <DataTable :value="tablevals" dataKey="id" selectionMode="single" showGridlines autoLayout
            :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
            :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

            <Column field="respondent" header="Respondent" />
            <Column header="Email adress" headerStyle="text-align: center" > <!-- bodyStyle="text-align: center; overflow: visible" -->
                <template #body="data">
                        <div class="p-d-flex p-ai-center p-jc-between">
                            {{data.data.email}}
                            <Button :icon="((sending_mails === data.data.email || sending_mails === true) ? 'pi pi-spin pi-spinner' : 'pi pi-replay')" class="p-button-warning p-button-sm" @click="resendSingleMail(data)" />
                        </div>
                </template>
            </Column>
        </Datatable>

        <div class="p-d-flex p-jc-end">
                <div class="p-py-3" style="width: 300px;">
                    <Button @click="verifyAudit(true)" label="Verify" icon="pi pi-check" class="p-button-success p-button-sm p-mb-3" style="width: 100%;" />
                    <Button @click="verifyAudit(false)" label="Reject" icon="pi pi-times" class="p-button-danger p-button-sm" style="width: 100%;" />
                </div>
        </div>
    </div>

        <Dialog v-model:visible="verificationDialog" style="width: 500px;" header="Help" :modal="true" dismissableMask="true">
        <p>Are you sure you wish to {{verified ? 'verify': 'reject'}} the survey responses?</p>
        <template #footer>
            <Button label="Yes" class="p-button-sm" icon="pi pi-check" @click="goToResults()" />
            <Button label="No" class="p-button-sm" icon="pi pi-times" @click="verificationDialog = false" />
        </template>
    </Dialog>
</template>

<script>
    export default {
        data () {
            return {
                verificationDialog: false,
                verified: false,
                sending_mails: false,
                tablevals: [
                    { id: 1, respondent: 'Henk', email: 'henk@mail.com' },
                    { id: 2, respondent: 'Henriette', email: 'henriette@mail.com' }
                    ]
            }
        },
        methods: {
            goToResults () {
                this.$router.push({ name: 'multipleauditresults', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } })
                // if this.verified === true, save survey to esea_account.verified_surveys
                print()
            },
            resendSingleMail (data) {
                console.log(data.data.email)
                this.sending_mails = data.data.email
                // sending mails
                // this.sending_mails = false
                print()
            },
            resendBatchMail () {
                this.sending_mails = true
                print()
            },
            verifyAudit (choice) {
                this.verified = choice
                this.verificationDialog = true
            }
        }
    }
</script>
