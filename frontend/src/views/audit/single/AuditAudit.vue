<template>
    <div class="p-grid p-m-5">
        <div class="p-col-12 p-d-flex p-ai-center p-jc-between">
            <!-- <div class="p-col-12 p-d-flex p-ai-center p-jc-between"> -->
                <h2 class="p-text-left">Audit</h2>
                <Button @click="(helpDialog = !helpDialog)" label="Help" class="p-button-sm p-button-warning" icon="pi pi-external-link" />
        </div>
        <DataTable class="p-col-12" :value="selectedIndicators" rowGroupMode="rowspan" groupRowsBy="section.name" selectionMode="single" @row-select="goToQuestion" sortMode="single" sortField="section.name" :sortOrder="1" responsiveLayout="scroll"
        v-model:expandedRowGroups="expandedRowGroups" @rowgroupExpand="onRowGroupExpand" @rowgroupCollapse="onRowGroupCollapse" dataKey="name">
            <Column field="topic" header="Topic"></Column>
            <Column field="name" header="Name" sortable></Column>
            <Column field="value" header="Value" sortable></Column>
            <Column header="Status" headerStyle="width: 10rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                <template #body="data">
                    <div class="p-d-flex p-ai-center p-jc-between">
                        <div v-if="data.data.status">{{data.data.status}}</div>
                        <div v-else>open</div>
                        <Button v-if="data.data.status === 'verified'" icon="pi pi-check"  style="border-radius: 50%; background-color: green; border: none;" />
                        <Button v-else-if="data.data.status === 'rejected'" icon="pi pi-times" style="border-radius: 50%; background-color: red; border: none;" />
                        <Button v-else-if="data.data.status === 'awaiting correction'" style="border-radius: 50%; p-col-12; background-color: #FBC02D; border: none;" />
                        <Button v-else style="border-radius: 50%; background-color: #2196F3; border: none;" />
                    </div>
                </template>
            </Column>
            </DataTable>
        <!-- <div class="p-text-right p-col-12">
            <Button class="p-my-5" label="Finish" icon="pi pi-check" @click="finishAudit()" />
        </div> -->
        <div class="p-col-12 p-d-flex p-jc-end">
            <div class="p-py-3" style="width: 300px;">
                <Button @click="verifyAudit(true)" label="Verify" icon="pi pi-check" class="p-button-success p-button-sm p-mb-3" style="width: 100%;" />
                <Button @click="verifyAudit(false)" label="Reject" icon="pi pi-times" class="p-button-danger p-button-sm" style="width: 100%;" />
            </div>
        </div>
    </div>

    <Dialog v-model:visible="verificationDialog" style="width: 500px;" header="Confirmation" :modal="true" dismissableMask="true">
        <p>Are you sure you wish to {{verified ? 'verify': 'reject'}} this survey?</p>
        <template #footer>
            <Button label="Yes" class="p-button-sm" icon="pi pi-check" @click="verifySurveyAudit()" />
            <Button label="No" class="p-button-sm" icon="pi pi-times" @click="verificationDialog = false" />
        </template>
    </Dialog>

    <Dialog v-model:visible="helpDialog" style="width: 500px;" header="Help" :modal="true" dismissableMask="true">
        <p>Please audit the listed indicators. Click a question to see details and change its status.</p>

        <template #footer>
            <Button label="Ok" icon="pi pi-check" @click="(helpDialog = !helpDialog)" />
        </template>
    </Dialog>
</template>

<script>
    import { mapState, mapActions } from 'vuex'

    export default {
        data () {
            return {
                verified: null,
                verificationDialog: false,
                helpDialog: false,
                questions: [
                    {
                        name: 'What is the total number of men staff?',
                        response: 5,
                        status: 'Awaiting documentation',
                        section: { name: 'Gender' }
                    },
                    {
                        name: 'What is the total number of women staff?',
                        response: 7,
                        status: 'Open',
                        section: { name: 'Gender' }

                    },
                    {
                        name: 'What is the average monthly salary per employee?',
                        response: '$4000',
                        status: 'Verified',
                        section: { name: 'Salary' }
                    }
                ]
            }
        },
        computed: {
            ...mapState('auditIndicators', ['selectedIndicators', 'indicator']),
            ...mapState('surveyAudit', ['surveyAudit'])
        },
        methods: {
            ...mapActions('auditIndicators', ['setSelectedIndicator']),
            ...mapActions('surveyAudit', ['updateSurveyAudit']),
            async goToQuestion (question) {
                await this.setSelectedIndicator({ id: question.data.id })
                if (this.indicator.id) {
                    // await this.setQuestion(question)
                    this.$router.push({ name: 'singleauditquestion', params: { QuestionId: this.indicator.id } })
                }
            },
            verifyAudit (choice) {
                this.verified = choice
                this.verificationDialog = true
            },
            async verifySurveyAudit () {
                if (this.verified) {
                    this.surveyAudit.status = 'verified'
                } else if (this.verified === false) {
                    this.surveyAudit.status = 'rejected'
                }
                await this.updateSurveyAudit({ oId: this.$route.params.OrganisationId, eaId: this.$route.params.EseaAccountId, data: this.surveyAudit })
                // save survey_audit_object.verified = this.verified
                // async/await
                // this.surveyAudit.status = this.verified
                // await this.updateSurveyAudit({ oId: this.$route.params.OrganisationId, eaId: this.$route.params.EseaAccountId, id: this.surveyAudit.id, data: this.surveyAudit })
                this.$router.push({ name: 'singleauditresults', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } })
                // if this.verified === true, save survey to esea_account.verified_surveys
            }
        }
    }
</script>
