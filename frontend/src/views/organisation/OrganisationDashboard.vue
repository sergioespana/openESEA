<template>
    <div class="organisationdashboard" id="dashboards">
        <!-- <DashboardFileOperations @modelIsUploaded="loadDashboardFromFile"></DashboardFileOperations> -->
        <EditDashboardElement></EditDashboardElement>
        <Dashboard v-if="modelUploaded"></Dashboard>
    </div>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from 'vuex'

import Dashboard from '../../components/dashboard/Dashboard.vue'
// import DashboardFileOperations from './DashboardFileOperations.vue'
import EditDashboardElement from '../../components/dashboard/EditDashboardElement.vue'

import EseaAccountService from '../../services/EseaAccountService.js'
import SurveyResponseService from '../../services/SurveyResponseService.js'
import DirectIndicatorService from '../../services/DirectIndicatorService.js'
import IndirectIndicatorService from '../../services/IndirectIndicatorService.js'

import { load as yamlLoad } from 'yaml'

export default {
    name: 'Dashboards',
    components: {
        // DashboardFileOperations,
        EditDashboardElement,
        Dashboard
    },
    data () {
        return {
            modelUploaded: false,
            organisationId: this.$route.params.OrganisationId,
            dashboardId: parseInt(this.$route.params.DashboardId)
        }
    },
    methods: {
        ...mapActions('dashboard', { setDashboard: 'setDashboard' }),
        ...mapGetters('dashboard', { getDashboardById: 'getDashboardById', getDashboards: 'getDashboards' }),
        ...mapGetters('dashboardData', { getIndicators: 'getIndicators', getIndicatorData: 'getIndicatorData', getIndicatorFields: 'getIndicatorFields' }),
        ...mapGetters('dashboardModel', { getMethods: 'getMethods' }),
        ...mapMutations('dashboardData', { setIndicators: 'setIndicators', setIndicatorData: 'setIndicatorData', setIndicatorFields: 'setIndicatorFields' }), //, setSupplementaryData: 'setSupplementaryData', setSupplementaryFields: 'setSupplementaryFields' }),
        ...mapMutations('dashboardModel', { setDashboard: 'setDashboard', setCurrentOverview: 'setCurrentOverview' }),
        async loadDashboard () {
            console.log('All Dashboards:', (await this.getDashboards()).filter((x) => x.id === this.dashboardId))
            const dashboard = await this.getDashboardById()(this.dashboardId)
            await this.setDashboard(dashboard)
            const model = dashboard.specification
            console.log('Loaded model:', model)
            this.loadDashboardModel(model)
        },
        async loadDashboardFromFile (fileContents, fileInfo) {
            // Parse dashboard model from file contents and file extension information
            const model = this.parseDashboardFromFileContents(fileContents, fileInfo)
            await this.loadDashboardModel(model)
        },
        parseDashboardFromFileContents (fileContents, fileInfo) {
            const fileExtension = fileInfo.name.split('.').pop()?.toLowerCase()
            var model = null
            if (fileExtension === 'yaml') model = yamlLoad(fileContents)
            if (fileExtension === 'json') model = JSON.parse(fileContents)
            return model
        },
        async loadDashboardModel (model) {
            // Save dashboard model
            await this.saveDashboard(model)
            // Load dashboard contents by setting uploaded to true
            this.modelUploaded = true

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
        async saveDashboard (model) {
            // Force reload by first setting model to null
            await this.setDashboard(null)
            await this.setDashboard(model)
            await this.setCurrentOverview(0)
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
            console.log('Names', indicatorNames)
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
    },
    async created () {
        console.log('Organisation Id', this.organisationId)
        console.log('Dashboard Id', this.dashboardId)
        console.log('This:', this.$route)
        await this.loadDashboard()
    }
}
</script>

<style>
.organisationdashboard {
    min-height: 600px;
    position: relative;

    font-family: Arial, Helvetica, sans-serif;

    /* Offset from top bar */
    height: 100%;

    /* Handle edit element */
    --edit-area-width: 200px;
    --edit-area-current-width: 0px;
    --edit-panel-width: 10px;
}
</style>
