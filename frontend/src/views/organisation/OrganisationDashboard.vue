<template>
    <div class="organisation-dashboard">
        <div v-if="!dashboardLoaded" class="spinner-div">
            <ProgressSpinner class="center-spinner"></ProgressSpinner>
        </div>
        <div v-else>
            <DashboardFileOperations v-if="false" @modelIsUploaded="loadDashboardFromFile"></DashboardFileOperations>
            <DashboardEditingSection @saveButtonClicked="saveDashboardToDatabase" @discardButtonClicked="discardChanges"></DashboardEditingSection>
            <Dashboard></Dashboard>
        </div>
    </div>
    <Dialog ref="dialog" v-model:visible="showDialog" modal :header="'There are unsaved changes to the dashboard. Do you want to save these changes?'">
        <!-- Footer for cancel or save buttons -->
        <template #footer>
            <Button label="Cancel" icon="pi pi-times"
                @click="closeDialog" text>
            </Button>
            <Button label="Discard Changes" icon="pi pi-trash" class="p-button-danger p-button-sm"
                @click="discardChanges" text>
            </Button>
            <Button label="Save Changes" icon="pi pi-check" class="p-button-success p-button-sm"
                @click="saveChanges" autofocus>
            </Button>
        </template>
    </Dialog>
</template>

<script>
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'

import Dashboard from '../../components/dashboard/Dashboard.vue'
import DashboardFileOperations from '../../components/dashboard/DashboardFileOperations.vue'
import DashboardEditingSection from '../../components/dashboard/DashboardEditingSection.vue'

import EseaAccountService from '../../services/EseaAccountService.js'
import SurveyResponseService from '../../services/SurveyResponseService.js'
import DirectIndicatorService from '../../services/DirectIndicatorService.js'
import IndirectIndicatorService from '../../services/IndirectIndicatorService.js'

import ProgressSpinner from 'primevue/progressspinner'
import Dialog from 'primevue/dialog'

import { isEqual, cloneDeep } from 'lodash'

export default {
    components: {
        DashboardFileOperations,
        DashboardEditingSection,
        Dashboard,

        ProgressSpinner,
        Dialog
    },
    data () {
        return {
            organisationId: this.$route.params.OrganisationId,
            dashboardId: this.$route.params.DashboardId,

            dashboardLoaded: false,

            initialDashboard: null,

            showDialog: false,
            unloader: null
        }
    },
    computed: {
        ...mapState('dashboardModel', ['dashboard'])
    },
    mounted () {
        // For showing unsaved changes message before unloading
        this.unloader = window.addEventListener('beforeunload', this.unload)
    },
    unmounted () {
        window.removeEventListener(this.unloader)
    },
    async created () {
        // Fetch latest version of dashboard
        await this.fetchDashboard({ id: parseInt(this.dashboardId) })
        // Load dashboard from fetched dashboard
        await this.loadDashboardFromDatabase()
        await this.setInitialDashboard()
    },
    async beforeRouteLeave (to, from, next) {
        if (!this.dashboardSaved()) {
            this.showDialog = true
            next(false)
        } else {
            next(true)
        }
    },
    methods: {
        ...mapGetters('dashboard', ['getDashboard', 'getDashboards']),
        ...mapActions('dashboard', ['setDashboard', 'updateDashboard', 'fetchDashboard']),

        ...mapGetters('dashboardData', ['getIndicators', 'getIndicatorData', 'getIndicatorFields']),
        ...mapMutations('dashboardData', ['setIndicators', 'setIndicatorData', 'setIndicatorFields']),

        ...mapGetters('dashboardModel', ['getDashboardModel', 'getMethods']),
        ...mapActions('dashboardModel', ['createDashboardModel']),

        setInitialDashboard () {
            this.initialDashboard = cloneDeep(this.dashboard)
        },
        dashboardSaved () {
            return isEqual(this.dashboard, this.initialDashboard)
        },

        unload (event) {
            if (!this.dashboardSaved()) {
                event.preventDefault()
                event.returnValue = '' // Required for older browsers
            }
        },
        async saveChanges () {
            await this.saveDashboardToDatabase()
            this.closeDialog()
        },
        async discardChanges () {
            console.log(this.initialDashboard)
            const oldDashboard = cloneDeep(this.initialDashboard)
            await this.loadDashboardModel(oldDashboard)
            console.log(this.dashboard)
            this.closeDialog()
        },
        closeDialog () {
            this.showDialog = false
        },

        async loadDashboardFromDatabase () {
            // Load dashboard from database
            const dashboard = await this.getDashboard()
            // Set as current dashboard
            await this.setDashboard(dashboard)

            // Get dashboard model specification
            const model = dashboard.specification
            // Load dashboard model
            await this.loadDashboardModel(model)
            // Load dashboard data
            await this.loadDashboardData(model)
            // When everything is ready show dashboard
            this.dashboardLoaded = true
        },
        async saveDashboardToDatabase () {
            // Get current dashboard model
            const dashboardModel = await this.getDashboardModel()()
            // Combine dashboard id with dashboard model specification
            const dashboardId = parseInt(this.dashboardId)
            const data = { id: dashboardId, data: dashboardModel }
            // Send this data to update the dashboard in the database
            await this.updateDashboard(data)
            // Signal that changes are saved
            await this.setInitialDashboard()
        },
        async loadDashboardModel (model) {
            // Force reload by first setting model to null
            await this.createDashboardModel(null)
            // Then set dashboard model
            await this.createDashboardModel(model)
        },
        async loadDashboardData () {
            // Retrieve and save all indicators of the given methods
            const indicators = await this.retrieveIndicators()
            await this.setIndicators(indicators)

            // Retrieve and save all data for the indicators of the given methods
            const indicatorData = await this.retrieveIndicatorData()
            await this.setIndicatorData(indicatorData)

            // Get the metadata fields for the indicators
            var indicatorMetaDataFields = []
            if (indicatorData.length) indicatorMetaDataFields = Object.keys(indicatorData[0])
            await this.setIndicatorFields(indicatorMetaDataFields)
        },
        async retrieveIndicators () {
            const methodIds = await this.getMethods()()
            var indicators = []
            for (var methodId of methodIds) {
                const directIndicators = await DirectIndicatorService.get({ mId: methodId })
                // console.log('Direct', directIndicators)
                if (!directIndicators?.error || directIndicators?.error?.response?.status === 404) {
                    for (var directIndicator of directIndicators?.response?.data) {
                        indicators.push(directIndicator)
                    }
                }
                const indirectIndicators = await IndirectIndicatorService.get({ mId: methodId })
                // console.log('Indirect', indirectIndicators)
                if (!indirectIndicators?.error || indirectIndicators?.error?.response?.status === 404) {
                    for (var indirectIndicator of (indirectIndicators?.response?.data || [])) {
                        indicators.push(indirectIndicator)
                    }
                }
            }
            // console.log(indicators)
            const indicatorNames = indicators?.map(el => el.name)
            return indicatorNames
        },
        async retrieveIndicatorData () {
            // Determine current organisation and targeted methods
            const methodIds = await this.getMethods()()
            const organisationId = this.organisationId

            /* Get the data from the esea accounts of the current organisation (by looking at the question responses in the survey responses) */
            var eseaData = []

            // Get esea accounts for this organisation
            const eseaAccountsRequest = await EseaAccountService.get({ oId: organisationId })
            if (eseaAccountsRequest.error) return
            const eseaAccounts = eseaAccountsRequest.response.data

            // Loop over esea accounts
            for (var eseaAccount of eseaAccounts) {
                const eseaAccountId = eseaAccount.id
                const eseaAccountYear = eseaAccount.year
                const eseaMethod = eseaAccount.method

                // If this esea account is not for a targeted method, skip this esea account
                if (!methodIds.includes(eseaMethod)) continue

                // Get all survey responses for this esea account
                const surveyResponseRequest = await SurveyResponseService.get({ oId: organisationId, eaId: eseaAccountId })
                if (surveyResponseRequest.error) continue
                const surveyResponses = surveyResponseRequest.response.data

                // Loop over survey responses
                for (var surveyResponse of surveyResponses) {
                    // Get responses to questions
                    const questionResponses = surveyResponse.question_responses

                    // Loop over all questions
                    for (var questionResponse of questionResponses) {
                        // Retrieve indicator data and the given values
                        // const directIndicatorId = questionResponse.direct_indicator_id
                        const directIndicatorKey = questionResponse.direct_indicator_key
                        const directIndicatorValue = questionResponse.value ?? questionResponse.values

                        // Store indicator data
                        eseaData.push({
                            'Indicator Key': directIndicatorKey,
                            Value: directIndicatorValue,
                            Year: eseaAccountYear
                            // 'Esea Account Id': eseaAccountId,
                            // 'Method Id': eseaMethod,
                            // 'Indicator Id': directIndicatorId
                        })
                    }
                }
            }

            // Return the data for all indicators
            return eseaData
        }
    }
}
</script>

<style>
.organisation-dashboard {
    min-height: 600px;
    position: relative;

    font-family: Arial, Helvetica, sans-serif;

    height: 100%;

    /* Handle edit area element */
    --edit-area-width: 200px;
    --edit-area-current-width: 0px;
    --edit-sidebar-width: 20px;
}
.spinner-div {
    position: absolute;
    width: 100%;
    height: 100%;
}
</style>
