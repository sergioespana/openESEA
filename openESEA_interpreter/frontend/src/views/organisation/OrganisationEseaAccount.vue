http://localhost:8081/organisation/1/esea-accounts/1

<template>
    <router-view />

    <div v-if="eseaAccount.campaign" class="card p-mx-5 p-mb-5">
        <div class="p-d-flex p-jc-between p-m-2">
            <div>
                {{ dateFixer(campaign.open_survey_date, 'MMMM Do YYYY') }}
            </div>
            <div>
                {{ dateFixer(campaign.close_survey_date, 'MMMM Do YYYY') }}
            </div>
        </div>
        <ProgressBar :value="timeline" :showValue="true">
            <div v-if="campaigntimeleft > 0"> {{campaigntimeleft}} days left </div>
            <div v-else>This campaign has finished</div>
        </ProgressBar>
    </div>
    <br>
    <br>
    <div v-for="survey in eseaAccount.survey_response_by_survey" :key="survey.id" class="p-m-5">
        <ProgressBar :value="survey.current_response_rate + 1" :showValue="true">
            '{{survey.name}}' - Response Rate: {{survey.current_response_rate }}%
        </ProgressBar>
    </div>
    <TabView :activeIndex="0">
        <TabPanel header="Surveys">
            <DataTable :value="eseaAccount.survey_response_by_survey" datakey="id" :rows="10" :paginator="true" :rowHover="true" v-model:filters="filters" filterDisplay="Menu" selectionMode="single" @row-select="goToSurveyFill"
            paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown" :rowsPerPageOptions="[10,25,50]"
            currentPageReportTemplate="Showing {first} to {last} of {totalRecords} entries">
            <template #header>
                <div class="p-d-flex p-jc-between p-ai-center">
                    <h5 class="p-m-0">Surveys</h5>
                    <span class="p-input-icon-left">
                        <i class="pi pi-search" />
                        <InputText v-model="filters['global'].value" placeholder="Keyword Search" />
                    </span>
                </div>
            </template>
            <Column field="name" header="Name" sortable />
            <Column field="stakeholdergroup" header="Stakeholder Group" />
            <Column field="questions.length" header="Questions" sortable />
            <Column field="respondees.length" header="Stakeholders" sortable />
            <Column field="responses" header="Responses" sortable />
            <Column field="current_response_rate" header="Response Rate" sortable>
                <template #body="{data}">
                    <ProgressBar :value="(data.current_response_rate)" :showValue="true" />
                </template>
            </Column>
            <Column field="required_response_rate" header="Response Rate Threshold" sortable>
                <template #body='{data}'>
                    {{data.required_response_rate}}%
                </template>
            </Column>
            <Column header="Actions" headerStyle="width: 15rem; text-align: center" bodyStyle="text-align: center; overflow: visible" :style="permission ? '': 'display:none;'">
                <template #body="{data}">
                    <div v-if="permission">
                        <Button v-if="(data.type === 'single')" :label="data.responses ? 'Survey Results' : 'Fill in Survey'" type="button" icon="" class="p-button-success" @click="data.responses? goToResults(data) : goToSurveyFill(data)"  style="width: 200px" />
                        <Button v-else label="Import Employees" type="button" icon="pi pi-user-plus" @click="openEmployeesImportWindow(data)" style="width: 200px" />
                    </div>
                    <div v-else></div>
                </template>
            </Column>
            <Column header="Report" headerStyle="width: 6rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                <template #body="data">
                    <Button @click="goToReport(data)" icon="pi pi-file-pdf" :class="data.sufficient_responses? 'p-button-success' : 'p-button-danger'"></Button>
                </template>
            </Column>
            </DataTable>
        </TabPanel>
        <TabPanel header="Method">
            <h4>Method: <span class="p-text-light p-text-italic">'{{eseaAccount.method_name}}'</span></h4>
            <h4>Description: <span class="p-text-light p-text-italic">''</span></h4>
            <Button label="Go to Method" @click="goToMethod" />
        </TabPanel>
        <TabPanel header="Auditing">
            <div class="p-col-12 p-d-flex p-jc-end">
                <Button label="Reset for Demo" class="p-button-primary p-button-sm" @click="demoReset()" :disabled="false"/>
            </div>
             <Card v-if="(accountAudit.status === 'finished' && !accountAudit.assurance && !provideAssuranceCard && !declineAssuranceCard) || card1" class="p-text-left p-m-2">
                 <template #title>
                    Assurance
                 </template>
                 <template #subtitle>
                     Provide assurance?
                 </template>
                 <template #content>
                    Thank you for auditing {{organisation.name}}.

                    <p>Below you will find an overview of the audit status of all surveys.</p>

                    <p>Do you wish to provide assurance on this ESEA account?</p>
                 </template>
                 <template #footer>
                     <Button icon="pi pi-check" label="Provide Assurance" @click="provideAssuranceCard = true" />
                     <Button icon="pi pi-times" label="No Assurance" @click="declineAssuranceCard = true" class="p-button-secondary p-button-outlined" style="margin-left: .5em" />
                 </template>
             </Card>

            <Card v-if="(provideAssuranceCard && !accountAudit.assurance) || card2" class="p-text-left p-m-2">
                 <template #title>
                    Assurance
                 </template>
                 <template #subtitle class="p-col-12">
                    <div class="p-col-12 p-d-flex p-ai-center p-jc-between">
                        Please write your assurance declaration below
                        <Dropdown id="method"  v-model="chosenAssuranceLevel" placeholder="Assurance Level" :options="assuranceLevels" />
                    </div>
                 </template>
                 <template #content>
                    <Textarea v-model="assuranceDeclaration" :autoResize="true" rows="3" class="p-col-12" />
                 </template>
                 <template #footer>
                     <Button icon="pi pi-check" label="Provide Assurance Declaration" @click="confirmAssurance(chosenAssuranceLevel)" :disabled="!chosenAssuranceLevel" />
                 </template>
             </Card>

            <Card v-if="(declineAssuranceCard && !accountAudit.assurance) || card3" class="p-text-left p-m-2">
                 <template #title>
                    Assurance
                 </template>
                 <template #subtitle class="p-col-12">
                    Why do you not wish to provide assurance?
                 </template>
                 <template #content>
                    <Textarea v-model="assuranceDeclaration" :autoResize="true" rows="3" class="p-col-12" />
                 </template>
                 <template #footer>
                     <Button label="Decline Assurance" @click="confirmAssurance('assurance rejected')" />
                 </template>
             </Card>

            <Card v-if="accountAudit.assurance === 'limited' || accountAudit.assurance === 'reasonable' || card4" class="p-text-left p-m-2">
                 <template #title>
                    Assurance
                 </template>
                 <template #content class="p-col-12">
                    <div class="p-mr-5">
                        <div class="p-grid">
                            <div class="p-col-2 p-text-center"><i class="pi pi-check" style="font-size: 3rem; background-color: #689F38; color: white; border-radius: 50%; padding: 30px;"></i></div>
                            <div class="p-col-10">
                                <h3 class="p-mt-0 p-pt-0">Assurance Declaration</h3>
                                {{accountAudit.assurance_declaration}}
                            </div>
                        </div>
                        <h3 class="p-d-flex p-jc-end p-my-0 p-py-0">Assurance Level: {{accountAudit.assurance}}</h3>
                    </div>
                 </template>
             </Card>

            <Card v-if="accountAudit.assurance === 'assurance rejected' || card5" class="p-text-left p-m-2">
                 <template #title>
                    Assurance
                 </template>
                 <template #content class="p-col-12">
                    <div class="p-mr-5">
                        <div class="p-grid">
                            <div class="p-col-2 p-text-center"><i class="pi pi-times" style="font-size: 3rem; background-color: red; color: white; border-radius: 50%; padding: 30px;"></i></div>
                            <div class="p-col-10">
                                <h3 class="p-mt-0 p-pt-0">Assurance Declaration</h3>
                                {{accountAudit.assurance_declaration}}
                            </div>
                        </div>
                    </div>
                 </template>
             </Card>
            <!-- {{accountAudit}} -->
            <!-- <Button label="start Account Audit" @click="goToMethod" /> -->
            <!-- <div class="p-shadow-4" style="display: flex; justify-content: center; align-items: center; width: 80%; height: 400px; margin: auto; background-color: lightblue; border-radius: 10px"><h2>Start Account Audit</h2></div> -->
            <DataTable :value="eseaAccount.survey_response_by_survey" datakey="id" :rows="10" :paginator="true" v-model:filters="filters" filterDisplay="Menu"
            paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown" :rowsPerPageOptions="[10,25,50]"
            currentPageReportTemplate="Showing {first} to {last} of {totalRecords} entries">
                <template #header>
                    <div class="p-d-flex p-jc-between p-ai-center">
                        <h5 class="p-m-0">Surveys</h5>
                        <span class="p-input-icon-left">
                            <i class="pi pi-search" />
                            <InputText v-model="filters['global'].value" placeholder="Keyword Search" />
                        </span>
                        <div>
                            <Button label="Refresh Recommendations" class="p-mr-2" @click="refreshRecommendations()" />
                            <!-- <Button label="Auditors" class="p-mr-2" @click="something" :disabled="true" /> -->
                            <Button label="Finish Account Audit" @click="finishAuditDialog = true" :disabled="accountAudit.status === 'finished'" />

                        </div>
                    </div>
                </template>
                <Column field="name" header="Name" sortable />
                <Column field="auditor" header="Auditor" sortable />
                <Column field="recommendations" header="Recommendations">
                    <template #body="{data}">
                        <div v-if="permission">
                           <Button v-if="data.id===6" :label="`${nr_of_recommended} Recommendations`" class="p-button-sm p-button-rounded p-py-1 p-button-danger" :disabled="true" />
                        </div>
                    </template>
                </Column>
                <Column field="type" header="Type" />
                <Column header="Status" headerStyle="width: 15rem; text-align: center" bodyStyle="text-align: center; overflow: visible" :style="permission ? '': 'display:none;'">
                    <template #body="{data}">
                        <div v-if="permission">
                            <div v-if="eseaAccount.verified_surveys.includes(data.id)" class="p-d-flex p-ai-center p-jc-between p-px-1">
                                <div class="p-col-2 p-text-right"><i class="pi pi-check" style="font-size: 1rem; background-color: #689F38; color: white; border-radius: 50%; padding: 7px;"></i></div>
                            </div>
                            <div v-else class="p-text-left">
                                <Button :label="data.survey_audit? 'Continue Audit' : 'Start Audit'" type="button" class="p-button-sm" @click="startAudit(data)"  style="width: 150px" />
                            </div>
                        </div>
                    </template>
                </Column>
            </DataTable>
        </TabPanel>
        <TabPanel header="Settings" :disabled="!permission">
            <div class="p-col-8 p-fluid p-text-left p-p-5" style="width: 600px">
                    <div class="p-d-flex p-jc-between">
                        <Button label="Save ESEA Account Details" class="p-button-primary p-button-sm p-mr-5" @click="editEseaAccount" :disabled="false"/>
                        <Button label="Delete ESEA Account" class="p-button-danger p-button-sm p-ml-5" @click="deleteEseaAccountDialog = true" />
                    </div>
                </div>
        </TabPanel>
    </TabView>

        <Dialog v-model:visible="finishAuditDialog" style="width: 500px;" header="Finish Audit" :modal="true" dismissableMask="true">
        <p>Are you sure you wish to finish the audit for this complete ESEA account? </p>

        <p>You will not be able to start new survey audits for this ESEA account after clicking 'Yes'.</p>
        <template #footer>
            <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="finishAudit()" />
            <Button label="No" icon="pi pi-times" class="p-button-text" @click="finishAuditDialog = false" />
        </template>
    </Dialog>

    <Dialog v-model:visible="importEmployeesDialog" :style="{width: '900px'}" header="Import your stakeholders" :modal="true" class="p-fluid">
        <div class="p-d-flex p-jc-between p-ai-start p-p-5" style="border: 1px solid lightgrey;">
            <Listbox v-if="surveyy.respondees.length" v-model="s" :options="surveyy.respondees" :multiple="false"  optionLabel="name" :filter="true" listStyle="max-height:250px" style="width:15rem" filterPlaceholder="Search">
                <template #option="slotProps">
                    <div class="country-item">
                        <div>{{slotProps.option.name}}</div>
                    </div>
                </template>
            </Listbox>
            <div>
                <p>Import employees for the following survey: <span class="p-text-italic">'{{surveyy.name}}'</span>.</p>
                <FileUpload name="myfile" :customUpload="true" @uploader="onUpload" :fileLimit="1" accept=".csv" :maxFileSize="1000000">
                    <template #empty>
                        <p>Drag and drop your csv file here to upload.</p>
                    </template>
                </FileUpload>
                <div class="p-error p-text-italic" v-for="response in stakeholderupload" :key="response"><small>{{response}}</small></div>
            </div>
        </div>
        <template #footer>
            <Button label="Remove window" icon="pi pi-times" class="p-button-text" @click="importEmployeesDialog = false"/>
        </template>
    </Dialog>

    <Dialog v-if="eseaAccount" v-model:visible="deleteEseaAccountDialog" style="width: 450px;" header="Confirm" :modal="true" dismissableMask="true">
        <div class="confirmation-content">
            <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 1.5rem" />
            <span>Are you sure you want to delete this Esea Account?</span>
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" class="p-button-text" @click="deleteEseaAccountDialog = false" />
            <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="removeEseaAccount()" />
        </template>
    </Dialog>

    <Dialog v-model:visible="startAuditDialog" style="width: 500px" header="New Audit Process" :modal="true" :dismissableMask="true">
        <audit-form @closedialog="startAuditDialog=false" />
    </Dialog>
</template>

<script>
    import { mapActions, mapState } from 'vuex'
    import { AxiosInstance } from '../../plugins/axios'
    import { FilterMatchMode } from 'primevue/api'
    import ProgressBar from 'primevue/progressbar'
    import Listbox from 'primevue/listbox'
    import dateFixer from '../../utils/datefixer'
    import moment from 'moment'
    import Dropdown from 'primevue/dropdown'

    import AuditForm from '../../components/forms/AuditForm'

    export default {
        components: {
            ProgressBar,
            Listbox,
            AuditForm,
            Dropdown
        },
        data () {
            return {
                filters: {
                    global: { value: null, matchMode: FilterMatchMode.CONTAINS }
                },
                columns: [
                    { field: 'name', header: 'Name' },
                    { field: 'method', header: 'Method' },
                    { field: 'questions.length', header: 'Questions' },
                    { field: 'stakeholders', header: 'Stakeholder group' }
                ],
                deleteEseaAccountDialog: false,
                importEmployeesDialog: false,
                startAuditDialog: false,
                finishAuditDialog: false,
                surveyy: null,
                selected_survey: null,
                stakeholderupload: null,
                // Only used for Artur's Demo!
                card1: false,
                card2: false,
                card3: false,
                card4: false,
                card5: false,
                provideAssuranceCard: false,
                declineAssuranceCard: false,
                assuranceLevels: [
                    'limited',
                    'reasonable'
                ],
                chosenAssuranceLevel: null,
                assuranceDeclaration: '',
                items: [
                    {
                        label: '- Send Message',
                        command: () => {
                            this.$toast.add({ severity: 'warn', summary: 'Delete', detail: 'Data Deleted', life: 3000 })
                        }
                    },
                    {
                        label: '- Send Reminder',
                        command: () => {
                            this.$toast.add({ severity: 'warn', summary: 'Delete', detail: 'Data Deleted', life: 3000 })
                        }
                    }
                ],
                AssuranceDeclaration: 'Assurance Declaration',
                AssuranceDeclarationPlaceholder: 'Motivation for not providing assurance'
            }
        },
        computed: {
            ...mapState('eseaAccount', ['eseaAccount']),
            ...mapState('organisation', ['organisation']),
            ...mapState('survey', ['surveys', 'survey']),
            ...mapState('campaign', ['campaign']),
            ...mapState('auditIndicators', ['indicators']),
            ...mapState('accountAudit', ['accountAudit']),
            ...mapState('surveyAudit', ['surveyAudits']),
            nr_of_recommended () {
                var i = 0
                this.indicators.forEach((dict) => {
                    if (typeof dict === 'object') {
                        for (const [key] of Object.entries(dict)) {
                            // console.log(key)
                            if (key === 'critical_impact' | dict[key] === true) {
                                i++
                            }
                        }
                    }
                })
                console.log(i)
                return i
            },
            timeline () {
                const jsondate = new Date().toJSON()
                var currentdate = moment(jsondate, 'YYYY-MM-DD')
                var admission = moment(this.campaign.open_survey_date, 'YYYY-MM-DD')
                var discharge = moment(this.campaign.close_survey_date, 'YYYY-MM-DD')
                var progress = (admission.diff(currentdate, 'days') / admission.diff(discharge, 'days')) * 100
                return progress
            },
            campaigntimeleft () {
                const jsondate = new Date().toJSON()
                var currentdate = moment(jsondate, 'YYYY-MM-DD')
                var discharge = moment(this.campaign.close_survey_date, 'YYYY-MM-DD')
                var daysleft = (discharge.diff(currentdate, 'days'))
                return daysleft
            },
            permission () {
            if (this.organisation.accesLevel) {
                const accesLevel = this.organisation.accesLevel
                if (accesLevel === 'admin' || accesLevel === 'organisation admin' || accesLevel === 'esea accountant') {
                    return true
                }
            }
            return false
        }
        },
        created () {
            this.initialize()
        },
        methods: {
            ...mapActions('eseaAccount', ['deleteEseaAccount']),
            ...mapActions('survey', ['fetchSurveys', 'setSurvey']),
            ...mapActions('campaign', ['fetchCampaign']),
            ...mapActions('method', ['fetchMethod']),
            ...mapActions('auditIndicators', ['fetchIndicators']),
            ...mapActions('surveyAudit', ['fetchSurveyAudits', 'fetchSurveyAudit']),
            ...mapActions('accountAudit', ['fetchAccountAudit', 'updateAccountAudit']),
            dateFixer,
            async initialize () {
                this.fetchMethod({ id: this.eseaAccount.method })
                this.fetchSurveys({ mId: this.eseaAccount.method })
                if (this.eseaAccount.campaign) {
                    this.fetchCampaign({ nId: this.eseaAccount.network, id: this.eseaAccount.campaign })
                }
                this.refreshRecommendations()
                // this.fetchSurveyAudits({ oId: this.$route.params.OrganisationId, eaId: this.$route.params.EseaAccountId })
            },
            toggle (event) {
                this.$refs.menu.toggle(event)
            },
            openEmployeesImportWindow (data) {
                this.surveyy = data
                if (data.id) {
                    this.importEmployeesDialog = true
                    this.stakeholdergroup = null
                }
            },
            async onUpload (event) {
                var formData = new FormData()
                formData.append('file', event.files[0])
                return new Promise((resolve, reject) => {
                    AxiosInstance.post(`/import-employees/${this.$route.params.EseaAccountId || 0}/${this.surveyy.id}/`, formData) // esea account // survey
                    .then(response => {
                        this.stakeholderupload = response.data
                        console.log('...response:', response.data)
                        this.importDialog = false
                        this.$toast.add({ severity: 'success', summary: 'CSV uploaded', detail: 'Your csv was correctly uploaded.' })
                        this.initialize()
                    resolve()
                    })
                    .catch(err => { reject(err) })
                })
            },
            async goToSurveyFill (data) {
                // The retrieved object structure is dependent on whether the button was clicked or the full row
                if (data.data) {
                    data = data.data
                }
                if (data.responses) {
                    this.goToResults(data)
                    return
                }
                this.$router.push({ name: 'survey-fill-page', params: { uniquetoken: `survey=${data.id}` } })
            },
            // Right now this also goes to the report, but could be changed to show the summarized survey data to organisation members as well EseaAccountId
            goToResults (data) {
                console.log(data)
                if (data.type === 'single') {
                this.$router.push({ name: 'method-survey-result', params: { OrganisationId: this.$route.params.OrganisationId, EseaAccountId: this.$route.params.EseaAccountId, SurveyId: data.id } })
                } else {
                    this.$router.push({ name: 'survey-results', params: { OrganisationId: this.$route.params.OrganisationId, EseaAccountId: this.$route.params.EseaAccountId, SurveyId: data.id } })
                }
                // this.$router.push({ name: 'esea-account-report', params: { OrganisationId: this.$route.params.OrganisationId, EseaAccountId: this.eseaAccount.id } })
            },
            async goToReport (event) {
                this.$router.push({ name: 'esea-account-report', params: { OrganisationId: this.$route.params.OrganisationId, EseaAccountId: this.$route.params.EseaAccountId } })
            },
            async removeEseaAccount () {
                this.deleteEseaAccountDialog = false
                await this.deleteEseaAccount({ oId: this.$route.params.OrganisationId, id: this.eseaAccount?.id || 0 })
                this.$toast.add({ severity: 'success', summary: 'Succesful', detail: 'Esea Account Deleted', life: 3000 })
                this.$router.push({ name: 'organisationeseaaccounts' })
            },
            async goToMethod () {
                this.$router.push({ name: 'newmethoddetails', params: { id: this.eseaAccount.method } })
                /* this.$router.push({ name: 'methoddetails', params: { id: this.campaign.method } }) */
            },
            async startAudit (data) {
                console.log(data)
                this.selected_survey = data.id
                await this.setSurvey(data)
                if (!data.survey_audit) {
                    this.startAuditDialog = true
                } else {
                    await this.fetchSurveyAudit({ oId: this.$route.params.OrganisationId, eaId: this.$route.params.EseaAccountId, id: data.survey_audit })
                    if (data.type === 'single') {
                        await this.fetchIndicators({ id: this.$route.params.EseaAccountId }) //  oId: this.$route.params.OrganisationId, eaId: this.$route.params.EseaAccountId
                        this.$router.push({ name: 'questionselection', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.survey.id } })
                    } else if (data.type === 'multiple') {
                        this.$router.push({ name: 'multipleauditsampling', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.survey.id } })
                    }
                }
            },
            async finishAudit () {
                this.accountAudit.status = 'finished'
                await this.updateAccountAudit({ oId: this.$route.params.OrganisationId, eaId: this.$route.params.EseaAccountId, data: this.accountAudit })
                this.finishAuditDialog = false
                console.log('finish audit')
            },
            async confirmAssurance (choice) {
                console.log(choice)
                this.accountAudit.assurance = choice
                this.accountAudit.assurance_declaration = this.assuranceDeclaration
                await this.updateAccountAudit({ oId: this.$route.params.OrganisationId, eaId: this.$route.params.EseaAccountId, data: this.accountAudit })
            },
            async refreshRecommendations () {
                await this.fetchIndicators({ id: this.$route.params.EseaAccountId })
            },
            async demoReset () {
                this.accountAudit.status = 'in progress'
                this.accountAudit.assurance = ''
                this.accountAudit.assurance_declaration = ''
                this.provideAssuranceCard = false
                this.declineAssuranceCard = false
                await this.updateAccountAudit({ oId: this.$route.params.OrganisationId, eaId: this.$route.params.EseaAccountId, data: this.accountAudit })
            }
        }
    }
</script>

<style lang="scss" scoped>
    .p-splitbutton {
        width: 200px;
    }
</style>
