export default {
    namespaced: true,
    state: {
        dashboard: null,
        currentOverviewId: 0
    },
    mutations: {
        setDashboard (state, dashboard) {
            state.dashboard = dashboard
        },
        setCurrentOverview (state, index) {
            state.currentOverviewId = index
        },

        setHeadSectionTitle (state, payload) {
            state.dashboard.Overviews[payload.overviewId].HeadSection.Title = payload.title
        },
        setHeadSectionText (state, payload) {
            state.dashboard.Overviews[payload.overviewId].HeadSection.Text = payload.text
        },

        setVisualisationTitle (state, payload) {
            state.dashboard.Overviews[payload.overviewId].BodySection.Containers[payload.containerId].Visualisations[payload.visualisationId].Title = payload.title
        },
        setVisualisationValueField (state, payload) {
            const ding = {}
            ding[payload.fieldType] = payload.field
            state.dashboard.Overviews[payload.overviewId].BodySection.Containers[payload.containerId].Visualisations[payload.visualisationId].DataDisplay.Configuration['Value Field'] = ding
        },
        setVisualisationCategoryField (state, payload) {
            const ding = {}
            ding[payload.fieldType] = payload.field
            state.dashboard.Overviews[payload.overviewId].BodySection.Containers[payload.containerId].Visualisations[payload.visualisationId].DataDisplay.Configuration['Category Field'] = ding
        },
        setVisualisationGroupingCategoryField (state, payload) {
            const ding = {}
            ding[payload.fieldType] = payload.field
            state.dashboard.Overviews[payload.overviewId].BodySection.Containers[payload.containerId].Visualisations[payload.visualisationId].DataDisplay.Configuration['Grouping Category Field'] = ding
        },
        setVisualisationStackingCategoryField (state, payload) {
            const ding = {}
            ding[payload.fieldType] = payload.field
            state.dashboard.Overviews[payload.overviewId].BodySection.Containers[payload.containerId].Visualisations[payload.visualisationId].DataDisplay.Configuration['Stacking Category Field'] = ding
        },

        setContainerTitle (state, payload) {
            state.dashboard.Overviews[payload.overviewId].BodySection.Containers[payload.containerId].Title = payload.title
        }
    },
    getters: {
        getDashboard: (state, getters) => () => {
            return state.dashboard
        },
        getDashboardName: (state, getters) => () => {
            const dashboard = getters.getDashboard()
            return dashboard?.Name
        },

        getMethods: (state, getters) => () => {
            const dashboard = getters.getDashboard()
            return dashboard?.Methods
        },

        getSelectedOverviewId: (state, getters) => () => {
            return state.currentOverviewId
        },

        getOverviews: (state, getters) => () => {
            const dashboard = getters.getDashboard()
            return dashboard?.Overviews ?? []
        },
        getOverviewNames: (state, getters) => () => {
            const overviews = getters.getOverviews()
            return overviews?.map(overview => overview.Name)
        },

        getOverview: (state, getters) => (overviewId) => {
            const overviews = getters.getOverviews()
            return overviews?.[overviewId]
        },
        getOverviewName: (state, getters) => (overviewId) => {
            const overview = getters.getOverview(overviewId)
            return overview?.Name
        },
        getHeadSection: (state, getters) => (overviewId) => {
            const overview = getters.getOverview(overviewId)
            return overview?.HeadSection
        },
        getBodySection: (state, getters) => (overviewId) => {
            const overview = getters.getOverview(overviewId)
            return overview?.BodySection
        },
        getSidePanel: (state, getters) => (overviewId) => {
            const overview = getters.getOverview(overviewId)
            return overview?.SidePanel
        },

        getHeadSectionTitle: (state, getters) => (overviewId) => {
            const headsection = getters.getHeadSection(overviewId)
            return headsection?.Title
        },
        getHeadSectionText: (state, getters) => (overviewId) => {
            const headsection = getters.getHeadSection(overviewId)
            return headsection?.Text
        },
        getHeadSectionOverviewSelection: (state, getters) => (overviewId) => {
            const headsection = getters.getHeadSection(overviewId)
            return headsection?.OverviewSelection
        },
        getHeadSectionDataFilters: (state, getters) => (overviewId) => {
            const headsection = getters.getHeadSection(overviewId)
            return headsection?.['Data Filters']
        },
        getHeadSectionVisualisation: (state, getters) => (overviewId) => {
            const headsection = getters.getHeadSection(overviewId)
            return headsection?.Visualisation
        },
        getHeadSectionDownloadButton: (state, getters) => (overviewId) => {
            const headsection = getters.getHeadSection(overviewId)
            return headsection?.['Download Button']
        },

        getSidePanelOverviewSelection: (state, getters) => (overviewId) => {
            const sidepanel = getters.getSidePanel(overviewId)
            return sidepanel?.OverviewSelection
        },
        getSidePanelDataFilters: (state, getters) => (overviewId) => {
            const sidepanel = getters.getSidePanel(overviewId)
            return sidepanel?.['Data Filters']
        },

        getContainers: (state, getters) => (overviewId) => {
            const bodysection = getters.getBodySection(overviewId)
            return bodysection?.Containers
        },
        getContainer: (state, getters) => (overviewId, containerId) => {
            const containers = getters.getContainers(overviewId)
            return containers?.[containerId]
        },
        getContainerTitle: (state, getters) => (overviewId, containerId) => {
            const container = getters.getContainer(overviewId, containerId)
            return container?.Title
        },
        getContainerBackgroundColor: (state, getters) => (overviewId, containerId) => {
            const container = getters.getContainer(overviewId, containerId)
            return container?.Style?.['Background Color']
        },
        getContainerPosition: (state, getters) => (overviewId, containerId) => {
            const container = getters.getContainer(overviewId, containerId)
            return container?.Position
        },
        getVideo: (state, getters) => (overviewId, containerId) => {
            const container = getters.getContainer(overviewId, containerId)
            return container?.Video
        },
        getImages: (state, getters) => (overviewId, containerId) => {
            const container = getters.getContainer(overviewId, containerId)
            return container?.Images
        },
        getTextParagraphs: (state, getters) => (overviewId, containerId) => {
            const container = getters.getContainer(overviewId, containerId)
            return container?.['Text Paragraphs']
        },

        getVisualisations: (state, getters) => (overviewId, containerId) => {
            const container = getters.getContainer(overviewId, containerId)
            return container?.Visualisations
        },
        getVisualisation: (state, getters) => (overviewId, containerId, visualisationId) => {
            const visualisations = getters.getVisualisations(overviewId, containerId)
            return visualisations?.[visualisationId]
        },
        getVisualisationPosition: (state, getters) => (overviewId, containerId, visualisationId) => {
            const visualisation = getters.getVisualisation(overviewId, containerId, visualisationId)
            return visualisation?.Position
        },
        getVisualisationTitle: (state, getters) => (overviewId, containerId, visualisationId) => {
            const visualisation = getters.getVisualisation(overviewId, containerId, visualisationId)
            return visualisation?.Title
        },
        getVisualisationDataDisplay: (state, getters) => (overviewId, containerId, visualisationId) => {
            const visualisation = getters.getVisualisation(overviewId, containerId, visualisationId)
            return visualisation?.DataDisplay
        },
        getVisualisationType: (state, getters) => (overviewId, containerId, visualisationId) => {
            const visualisationDisplay = getters.getVisualisationDataDisplay(overviewId, containerId, visualisationId)
            return visualisationDisplay?.Type
        },
        getVisualisationIndicators: (state, getters) => (overviewId, containerId, visualisationId) => {
            const visualisationDisplay = getters.getVisualisationDataDisplay(overviewId, containerId, visualisationId)
            return visualisationDisplay?.DataConfiguration?.Indicators
        },
        getVisualisationCategories: (state, getters) => (overviewId, containerId, visualisationId) => {
            const visualisationDisplay = getters.getVisualisationDataDisplay(overviewId, containerId, visualisationId)
            return visualisationDisplay?.DataConfiguration?.Categories
        },
        getVisualisationGroupingField: (state, getters) => (overviewId, containerId, visualisationId) => {
            const visualisationDisplay = getters.getVisualisationDataDisplay(overviewId, containerId, visualisationId)
            return visualisationDisplay?.DataConfiguration?.['Grouping Field']
        },
        getVisualisationStackingField: (state, getters) => (overviewId, containerId, visualisationId) => {
            const visualisationDisplay = getters.getVisualisationDataDisplay(overviewId, containerId, visualisationId)
            return visualisationDisplay?.DataConfiguration?.['Stacking Field']
        }
    }
}
