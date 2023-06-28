export default {
    namespaced: true,
    state: {
        dashboard: null,
        currentOverviewIndex: null
    },
    mutations: {
        setDashboard (state, dashboard) {
            state.dashboard = { ...dashboard }
        },
        setCurrentOverview (state, index) {
            state.currentOverviewIndex = index
        }
    },
    getters: {
        getDashboard: (state, getters) => () => {
            return state.dashboard
        },
        getDashboardName: (state, getters) => () => {
            const dashboard = getters.getDashboard()
            if (!dashboard) return null
            return dashboard.Name
        },

        getSelectedOverviewIndex: (state, getters) => () => {
            return state.currentOverviewIndex
        },

        getOverviews: (state, getters) => () => {
            const dashboard = getters.getDashboard()
            if (!dashboard) return []
            return dashboard.Overviews ?? []
        },
        getOverviewsAmount: (state, getters) => () => {
            const overviews = getters.getOverviews()
            return overviews.length
        },
        getOverviewNames: (state, getters) => () => {
            const overviews = getters.getOverviews()
            return overviews.map(overview => overview.Name)
        },

        getOverview: (state, getters) => (overviewId) => {
            const overviews = getters.getOverviews()
            if (!overviews.length) return null
            return overviews[overviewId]
        },
        getOverviewName: (state, getters) => (overviewId) => {
            const overview = getters.getOverview(overviewId)
            if (!overview) return null
            return overview.Name
        },
        getHeadSection: (state, getters) => (overviewId) => {
            const overview = getters.getOverview(overviewId)
            if (!overview) return null
            return overview.HeadSection
        },
        getBodySection: (state, getters) => (overviewId) => {
            const overview = getters.getOverview(overviewId)
            if (!overview) return null
            return overview.BodySection
        },
        getSidePanel: (state, getters) => (overviewId) => {
            const overview = getters.getOverview(overviewId)
            if (!overview) return null
            return overview.SidePanel
        },

        getHeadSectionTitle: (state, getters) => (overviewId) => {
            const headsection = getters.getHeadSection(overviewId)
            if (!headsection) return null
            return headsection.Title
        },
        getHeadSectionText: (state, getters) => (overviewId) => {
            const headsection = getters.getHeadSection(overviewId)
            if (!headsection) return null
            return headsection.Text
        },
        getHeadSectionOverviewSelection: (state, getters) => (overviewId) => {
            const headsection = getters.getHeadSection(overviewId)
            if (!headsection) return null
            return headsection.OverviewSelection
        },
        getHeadSectionDataFilters: (state, getters) => (overviewId) => {
            const headsection = getters.getHeadSection(overviewId)
            if (!headsection) return null
            return headsection['Data Filters']
        },
        getHeadSectionVisualisation: (state, getters) => (overviewId) => {
            const headsection = getters.getHeadSection(overviewId)
            if (!headsection) return null
            return headsection.Visualisation
        },
        getHeadSectionDownloadButton: (state, getters) => (overviewId) => {
            const headsection = getters.getHeadSection(overviewId)
            if (!headsection) return null
            return headsection['Download Button']
        },

        getSidePanelOverviewSelection: (state, getters) => (overviewId) => {
            const sidepanel = getters.getSidePanel(overviewId)
            if (!sidepanel) return null
            return sidepanel.OverviewSelection
        },
        getSidePanelDataFilters: (state, getters) => (overviewId) => {
            const sidepanel = getters.getSidePanel(overviewId)
            if (!sidepanel) return null
            return sidepanel['Data Filters']
        },

        getContainers: (state, getters) => (overviewId) => {
            const bodysection = getters.getBodySection(overviewId)
            if (!bodysection) return []
            return bodysection.Containers
        },
        getContainer: (state, getters) => (overviewId, containerId) => {
            const containers = getters.getContainers(overviewId)
            if (!containers.length) return null
            return containers[containerId]
        },
        getContainerTitle: (state, getters) => (overviewId, containerId) => {
            const container = getters.getContainer(overviewId, containerId)
            if (!container) return null
            return container.Title
        },
        getContainerBackgroundColor: (state, getters) => (overviewId, containerId) => {
            const container = getters.getContainer(overviewId, containerId)
            if (!container) return null
            return container.Style['Background Color']
        },
        getContainerPosition: (state, getters) => (overviewId, containerId) => {
            const container = getters.getContainer(overviewId, containerId)
            if (!container) return null
            return container.Position
        },
        getVideo: (state, getters) => (overviewId, containerId) => {
            const container = getters.getContainer(overviewId, containerId)
            if (!container) return null
            return container.Video
        },
        getImages: (state, getters) => (overviewId, containerId) => {
            const container = getters.getContainer(overviewId, containerId)
            if (!container) return []
            return container.Images
        },
        getTextParagraphs: (state, getters) => (overviewId, containerId) => {
            const container = getters.getContainer(overviewId, containerId)
            if (!container) return []
            return container['Text Paragraphs']
        },

        getVisualisations: (state, getters) => (overviewId, containerId) => {
            const container = getters.getContainer(overviewId, containerId)
            if (!container) return []
            return container.Visualisations
        },
        getVisualisation: (state, getters) => (overviewId, containerId, visualisationId) => {
            const visualisations = getters.getVisualisations(overviewId, containerId)
            if (!visualisations) return null
            return visualisations[visualisationId]
        },
        getVisualisationPosition: (state, getters) => (overviewId, containerId, visualisationId) => {
            const visualisation = getters.getVisualisation(overviewId, containerId, visualisationId)
            if (!visualisation) return null
            return visualisation.Position
        },
        getVisualisationTitle: (state, getters) => (overviewId, containerId, visualisationId) => {
            const visualisation = getters.getVisualisation(overviewId, containerId, visualisationId)
            if (!visualisation) return null
            return visualisation.Title
        },
        getVisualisationDataDisplay: (state, getters) => (overviewId, containerId, visualisationId) => {
            const visualisation = getters.getVisualisation(overviewId, containerId, visualisationId)
            if (!visualisation) return null
            return visualisation.DataDisplay
        },
        getVisualisationType: (state, getters) => (overviewId, containerId, visualisationId) => {
            const visualisationDisplay = getters.getVisualisationDataDisplay(overviewId, containerId, visualisationId)
            if (!visualisationDisplay) return null
            return visualisationDisplay.Type
        },
        getVisualisationData: (state, getters) => (overviewId, containerId, visualisationId) => {
            const visualisationDisplay = getters.getVisualisationDataDisplay(overviewId, containerId, visualisationId)
            if (!visualisationDisplay) return null
            return visualisationDisplay.Data
        },
        getVisualisationField: (state, getters) => (overviewId, containerId, visualisationId) => {
            const visualisationDisplay = getters.getVisualisationDataDisplay(overviewId, containerId, visualisationId)
            if (!visualisationDisplay) return null
            return visualisationDisplay.Field
        },
        getVisualisationDataLabels: (state, getters) => (overviewId, containerId, visualisationId) => {
            const visualisationData = getters.getVisualisationData(overviewId, containerId, visualisationId)
            if (!visualisationData) return null
            return visualisationData.Labels
        },
        getVisualisationDataValues: (state, getters) => (overviewId, containerId, visualisationId) => {
            const visualisationData = getters.getVisualisationData(overviewId, containerId, visualisationId)
            if (!visualisationData) return null
            return visualisationData.Data
        }
    }
}
