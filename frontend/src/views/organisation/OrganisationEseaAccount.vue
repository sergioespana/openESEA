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
    <TabView :activeIndex="1">
        <TabPanel header="Method">
            <h4>Method: <span class="p-text-light p-text-italic">'{{eseaAccount.method_name}}'</span></h4>
            <h4>Description: <span class="p-text-light p-text-italic">''</span></h4>
            <Button label="Go to Method" @click="goToMethod" />

        </TabPanel>
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
                    <div>
                        <Button label="Tool Menu" @click="toggle" :disabled="false" />
                        <Menu id="overlay_menu" ref="menu" :model="items" :popup="true" />
                    </div>
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
                        <Button v-if="(data.type === 'single')" :label="data.responses? 'Survey Results' : 'Fill in Survey'" type="button" icon="" class="p-button-success" @click="data.responses? goToResults(data) : goToSurveyFill(data)"  style="width: 200px" />
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
        <TabPanel header="Report">
            d
        </TabPanel>
        <TabPanel header="Auditing">
            <Button label="Go to auditing page" @click="goToAuditingPage" />
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
</template>

<script>
    import { mapActions, mapState } from 'vuex'
    import { AxiosInstance } from '../../plugins/axios'
    import { FilterMatchMode } from 'primevue/api'
    import ProgressBar from 'primevue/progressbar'
    import Listbox from 'primevue/listbox'
    import dateFixer from '../../utils/datefixer'
    import moment from 'moment'

    export default {
        components: {
            ProgressBar,
            Listbox
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
                surveyy: null,
                stakeholderupload: null,
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
                ]
            }
        },
        computed: {
            ...mapState('eseaAccount', ['eseaAccount']),
            ...mapState('organisation', ['organisation']),
            ...mapState('survey', ['surveys']),
            ...mapState('campaign', ['campaign']),
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
            ...mapActions('survey', ['fetchSurveys']),
            ...mapActions('campaign', ['fetchCampaign']),
            dateFixer,
            async initialize () {
                this.fetchSurveys({ mId: this.eseaAccount.method })
                if (this.eseaAccount.campaign) {
                    this.fetchCampaign({ nId: this.eseaAccount.network, id: this.eseaAccount.campaign })
                }
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
                console.log('======>', data)
                this.$router.push({ name: 'survey-fill-page', params: { uniquetoken: `survey=${data.id}` } })
            },
            // Right now this also goes to the report, but could be changed to show the summarized survey data to organisation members as well
            goToResults (data) {
                this.$router.push({ name: 'esea-account-report', params: { OrganisationId: this.$route.params.OrganisationId, EseaAccountId: this.eseaAccount.id } })
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
            }
        }
    }
</script>

<style lang="scss" scoped>
    .p-splitbutton {
        width: 200px;
    }
</style>
