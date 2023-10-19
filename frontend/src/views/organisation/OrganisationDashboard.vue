<template>

    <!-- Dashboard -->
    <div class="organisation-dashboard">

        <!-- Show spinner while loading dashboard -->
        <div v-if="!dashboardLoaded" class="spinner-div">
            <ProgressSpinner class="center-spinner"></ProgressSpinner>
        </div>

        <!-- If dashboard is loaded, show dashboard and editing section -->
        <div v-else>
            <!-- Editing Section -->
            <DashboardEditingSection @saveButtonClicked="saveDashboardToDatabase" @discardButtonClicked="discardChanges"></DashboardEditingSection>
            <!-- Actual dashboard -->
            <Dashboard></Dashboard>

            <!-- Dialog showing that there are unsaved changes -->
            <Dialog ref="dialog" v-model:visible="showDialog" modal
                :header="'There are unsaved changes to the dashboard. Do you want to save these changes?'">

                <!-- Footer with buttons for options: Cancel, Discard Changes, Save Changes -->
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

        </div>

    </div>

</template>

<script>
import { isEqual, cloneDeep } from 'lodash'

import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'

import EseaAccountService from '../../services/EseaAccountService.js'
import SurveyResponseService from '../../services/SurveyResponseService.js'
import DirectIndicatorService from '../../services/DirectIndicatorService.js'
import IndirectIndicatorService from '../../services/IndirectIndicatorService.js'

import Dashboard from '../../components/dashboard/Dashboard.vue'
import DashboardEditingSection from '../../components/dashboard/DashboardEditingSection.vue'

import ProgressSpinner from 'primevue/progressspinner'
import Dialog from 'primevue/dialog'

export default {
    components: {
        DashboardEditingSection,
        Dashboard,

        ProgressSpinner,
        Dialog
    },
    data () {
        return {
            // Route parameters for organisation and dashboard ids
            organisationId: this.$route.params.OrganisationId,
            dashboardId: this.$route.params.DashboardId,

            dashboardLoaded: false,

            initialDashboard: null,

            showDialog: false,

            fetchSuggestionsTimer: null
        }
    },
    computed: {
        ...mapState('dashboardModel', ['dashboard', 'selectionConfig'])
    },
    watch: {
        dashboard: {
            handler: 'updateRLModel',
            deep: true
        }
    },
    async mounted () {
        this.fetchSuggestionsTimer = setInterval(this.fetchDashboardSuggestions, 10000)
    },
    async unmounted () {
        clearInterval(this.fetchSuggestionsTimer)
    },
    async beforeUnmount () {
        window.removeEventListener('beforeunload', this.unload)
    },
    async created () {
        window.addEventListener('beforeunload', this.unload)

        // Fetch latest version of dashboard
        await this.fetchDashboard({ id: parseInt(this.dashboardId) })
        // Load dashboard from fetched dashboard
        await this.loadDashboardFromDatabase()
        await this.setInitialDashboard()

        // Initialize RL model
        await this.initializeRLModel()
    },
    async beforeRouteLeave (to, from, next) {
        console.log('Leaving route')
        if (!this.dashboardLoaded) next(true)
        if (!this.dashboardSaved()) {
            this.showDialog = true
            next(false)
        } else {
            await this.stopRLModel()
            next(true)
        }
    },
    methods: {
        ...mapGetters('dashboard', ['getDashboard', 'getDashboards']),
        ...mapActions('dashboard', ['setDashboard', 'updateDashboard', 'fetchDashboard']),

        ...mapGetters('dashboardData', ['getIndicatorDataSets', 'getIndicatorFields', 'getIndicators', 'getVisualisationDatasets']),
        ...mapMutations('dashboardData', ['setIndicators', 'setIndicatorData', 'setIndicatorFields']),
        ...mapActions('dashboardData', ['createIndicatorDataSets']),

        ...mapGetters('dashboardModel', ['getDashboardModel', 'getMethods', 'getOverview', 'getContainers', 'getVisualisations', 'getVisualisationTitle', 'getVisualisationType', 'getCategoryLimit']),
        ...mapActions('dashboardModel', ['createDashboardModel']),

        ...mapActions('dashboardSuggestions', ['buildDashboardRLModel', 'updateDashboardRLModel', 'deleteDashboardRLModel', 'fetchDashboardSuggestions']),

        setInitialDashboard () {
            this.initialDashboard = cloneDeep(this.dashboard)
        },
        dashboardSaved () {
            return isEqual(this.dashboard, this.initialDashboard)
        },

        async unload (event) {
            console.log('Unloading page')
            if (!this.dashboardLoaded) return
            // Prevent page unloading if dashboard is not saved
            if (!this.dashboardSaved()) {
                event.preventDefault()
                event.returnValue = '' // Required for older browsers
            }
        },
        async initializeRLModel () {
            // Wait 2 seconds before visualisations are loaded
            const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))
            await sleep(2000)
            // Build new RL Model and set interval for fetching suggestions
            const dashboard = await this.collectDashboardInfo()
            console.log(dashboard)
            await this.buildDashboardRLModel({ data: { dashboard: dashboard } })
        },
        async collectDashboardInfo () {
            // Initialize list with info for all visualisations
            var visualisationInfoList = []

            // Select current overview
            const overviewId = this.selectionConfig?.overviewId
            var selectionConfigCurrent = { overviewId: overviewId }

            // Get all containers with possible visualisations, if no containers, return
            const containers = await this.getContainers()(selectionConfigCurrent)
            if (!containers) return visualisationInfoList

            // Dashboard size
            const dashboardWidth = this.$refs.dashboard.clientWidth
            const dashboardHeight = this.$refs.dashboard.clientHeight
            const dashboardDisplayArea = dashboardWidth * dashboardHeight

            // Get visualisation datasets
            var visualisationDatasets = await this.getVisualisationDatasets()()
            // Collect visualisations for each container
            for (let containerId = 0; containerId < containers.length; containerId++) {
                const containerPosition = containers[containerId].Position
                const containerWidth = (containerPosition['X End'] - containerPosition['X Start']) * dashboardWidth / 100
                const containerHeight = (containerPosition['Y End'] - containerPosition['Y Start']) * dashboardHeight / 100

                // Update selection to current conainer
                selectionConfigCurrent.containerId = containerId
                // Get all visualisation for this container
                const visualisations = await this.getVisualisations()(selectionConfigCurrent)
                // Get info for each visualisation
                for (let visualisationId = 0; visualisationId < visualisations.length; visualisationId++) {
                    const visualisationPosition = visualisations[visualisationId].Position
                    const xStartPixels = dashboardWidth * containerPosition['X Start'] + containerWidth * visualisationPosition['X Start']
                    const xEndPixels = dashboardWidth * containerPosition['X End'] + containerWidth * visualisationPosition['X End']
                    const yStartPixels = dashboardHeight * containerPosition['Y Start'] + containerHeight * visualisationPosition['Y Start']
                    const yEndPixels = dashboardHeight * containerPosition['Y End'] + containerHeight * visualisationPosition['Y End']
                    const visualisationDisplayArea = (xEndPixels - xStartPixels) * (yEndPixels - yStartPixels)

                    // Update selection to current visualisation
                    selectionConfigCurrent.visualisationId = visualisationId

                    // Get dataset for this visualisation
                    var visualisationData = null

                    for (const visualisationDataset of visualisationDatasets) {
                        const config = visualisationDataset.config
                        const dataset = visualisationDataset.dataset
                        if (isEqual(config, selectionConfigCurrent)) {
                            visualisationData = dataset
                            break
                        }
                    }

                    // Get visualisation type
                    const visualisationType = await this.getVisualisationType()(selectionConfigCurrent)
                    const visualisationTitle = await this.getVisualisationTitle()(selectionConfigCurrent)
                    const categoryLimit = await this.getCategoryLimit()(selectionConfigCurrent)

                    const numberOfDataPoints = visualisationData?.data?.length ?? 0
                    const amountOfValueFields = Object.keys(visualisationData?.mapping).filter(fieldKey => fieldKey.includes('Value Field')).length

                    // Gather all visualisation information into one object
                    var visualisationInfo = {}
                    visualisationInfo['Selection Configuration'] = cloneDeep(selectionConfigCurrent) // For applying this to the correct visualisation
                    visualisationInfo['Visualisation Type'] = visualisationType
                    visualisationInfo['Visualisation Title'] = visualisationTitle
                    visualisationInfo['Data Items'] = numberOfDataPoints * amountOfValueFields
                    visualisationInfo['Item Limit Enabled'] = categoryLimit > 0
                    visualisationInfo['Item Limit'] = categoryLimit ?? 0
                    visualisationInfo['Display Area'] = visualisationDisplayArea
                    visualisationInfo.Position = { 'X Start': xStartPixels, 'X End': xEndPixels, 'Y Start': yStartPixels, 'Y End': yEndPixels }
                    visualisationInfoList.push(visualisationInfo)
                }
            }
            return { Visualisations: visualisationInfoList, 'Display Area': dashboardDisplayArea }
        },
        async updateRLModel () {
            // Update RL Model and set interval for fetching suggestions
            const dashboard = await this.collectDashboardInfo()
            await this.updateDashboardRLModel({ data: { dashboard: dashboard } })
            // Reset timer for fetching suggestions
            clearInterval(this.fetchSuggestionsTimer)
            this.fetchSuggestionsTimer = setInterval(this.fetchDashboardSuggestions, 10000)
        },
        async stopRLModel () {
            // Delete RL model and clear timer
            await this.deleteDashboardRLModel({ data: {} })
            clearInterval(this.fetchSuggestionsTimer)
        },
        async saveChanges () {
            await this.saveDashboardToDatabase()
            this.closeDialog()
        },
        async discardChanges () {
            const oldDashboard = cloneDeep(this.initialDashboard)
            await this.loadDashboardModel(oldDashboard)
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
            await this.loadDashboardData()
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
            const payload = { value: model }
            await this.createDashboardModel(payload)
        },
        async loadDashboardData () {
            // Retrieve and save all indicators of the given methods
            const indicators = await this.retrieveIndicators()
            await this.setIndicators(indicators)

            // Retrieve and save all data for the indicators of the given methods
            const indicatorData = await this.retrieveIndicatorData()
            await this.setIndicatorData(indicatorData)

            // Create data sets for each indicator
            await this.createIndicatorDataSets()
        },
        async retrieveIndicators () {
            const methodIds = await this.getMethods()()
            var indicators = []
            for (var methodId of methodIds) {
                const directIndicators = await DirectIndicatorService.get({ mId: methodId })
                console.log(directIndicators)
                if (!directIndicators?.error || directIndicators?.error?.response?.status === 404) {
                    for (var directIndicator of (directIndicators?.response?.data || [])) {
                        indicators.push(directIndicator)
                    }
                }
                const indirectIndicators = await IndirectIndicatorService.get({ mId: methodId })
                console.log(indirectIndicators)
                if (!indirectIndicators?.error || indirectIndicators?.error?.response?.status === 404) {
                    for (var indirectIndicator of (indirectIndicators?.response?.data || [])) {
                        indicators.push(indirectIndicator)
                    }
                }
            }
            // console.log(indicators)
            indicators = indicators?.map(el => ({ name: el.name, key: el.key }))
            return indicators
        },
        async retrieveIndicatorData () {
            // Determine current organisation and targeted methods for dashboard
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
                // Get year and method of this esea account
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
                        const directIndicatorKey = questionResponse.direct_indicator_key
                        const directIndicatorValue = questionResponse.value ?? questionResponse.values
                        const multipleChoice = questionResponse.value === null

                        // Store indicator data
                        eseaData.push({
                            'Indicator Key': directIndicatorKey,
                            Value: directIndicatorValue,
                            Year: eseaAccountYear,
                            'Multiple Choice': multipleChoice
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
    background-color: white;
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
