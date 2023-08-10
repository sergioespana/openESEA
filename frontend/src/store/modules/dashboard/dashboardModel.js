export default {
    namespaced: true,
    state: {
        dashboard: null,
        selectionConfig: null
    },
    getters: {
        /* Get the given element ids from the payload or otherwise from the current selection */
        getOverviewId: (state, getters) => (payload) => {
            return payload?.overviewId ?? state.selectionConfig.overviewId
        },
        getContainerId: (state, getters) => (payload) => {
            return payload?.containerId ?? state.selectionConfig.containerId
        },
        getVisualisationId: (state, getters) => (payload) => {
            return payload?.visualisationId ?? state.selectionConfig.visualisationId
        },
        getImageId: (state, getters) => (payload) => {
            return payload?.imageId ?? state.selectionConfig.imageId
        },
        getTextParagraphId: (state, getters) => (payload) => {
            return payload?.textParagraphId ?? state.selectionConfig.textParagraphId
        },

        getDashboardModel: (state, getters) => () => {
            return state.dashboard
        },

        getDashboardName: (state, getters) => () => {
            return getters.getDashboardModel()?.Name
        },
        getMethods: (state, getters) => () => {
            return getters.getDashboardModel()?.Methods ?? []
        },
        getOverviews: (state, getters) => () => {
            return getters.getDashboardModel()?.Overviews ?? []
        },

        getOverview: (state, getters) => (payload) => {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            return getters.getOverviews()?.[overviewId]
        },

        getOverviewName: (state, getters) => (payload) => {
            return getters.getOverview(payload)?.Name
        },
        getHeadSection: (state, getters) => (payload) => {
            return getters.getOverview(payload)?.HeadSection
        },
        getBodySection: (state, getters) => (payload) => {
            return getters.getOverview(payload)?.BodySection
        },
        getSidePanel: (state, getters) => (payload) => {
            return getters.getOverview(payload)?.SidePanel
        },

        getHeadSectionTitle: (state, getters) => (payload) => {
            return getters.getHeadSection(payload)?.Title
        },
        getHeadSectionText: (state, getters) => (payload) => {
            return getters.getHeadSection(payload)?.Text
        },
        getHeadSectionOverviewSelection: (state, getters) => (payload) => {
            return getters.getHeadSection(payload)?.OverviewSelection
        },
        getHeadSectionDataFilters: (state, getters) => (payload) => {
            return getters.getHeadSection(payload)?.['Data Filters']
        },
        getHeadSectionVisualisation: (state, getters) => (payload) => {
            return getters.getHeadSection(payload)?.Visualisation
        },
        getHeadSectionDownloadButton: (state, getters) => (payload) => {
            return getters.getHeadSection(payload)?.['Download Button']
        },

        getSidePanelOverviewSelection: (state, getters) => (payload) => {
            return getters.getSidePanel(payload)?.OverviewSelection
        },
        getSidePanelDataFilters: (state, getters) => (payload) => {
            return getters.getSidePanel(payload)?.['Data Filters'] ?? []
        },

        getContainers: (state, getters) => (payload) => {
            return getters.getBodySection(payload)?.Containers ?? []
        },

        getContainer: (state, getters) => (payload) => {
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            return getters.getContainers(payload)?.[containerId]
        },

        getContainerTitle: (state, getters) => (payload) => {
            return getters.getContainer(payload)?.Title
        },
        getContainerBackgroundColor: (state, getters) => (payload) => {
            return getters.getContainer(payload)?.Style?.['Background Color']
        },
        getContainerPosition: (state, getters) => (payload) => {
            return getters.getContainer(payload)?.Position
        },

        getImages: (state, getters) => (payload) => {
            return getters.getContainer(payload)?.Images ?? []
        },
        getTextParagraphs: (state, getters) => (payload) => {
            return getters.getContainer(payload)?.['Text Paragraphs'] ?? []
        },
        getVisualisations: (state, getters) => (payload) => {
            return getters.getContainer(payload)?.Visualisations ?? []
        },

        getContainerXStart: (state, getters) => (payload) => {
            return getters.getContainerPosition(payload)?.['X Start']
        },
        getContainerXEnd: (state, getters) => (payload) => {
            return getters.getContainerPosition(payload)?.['X End']
        },
        getContainerYStart: (state, getters) => (payload) => {
            return getters.getContainerPosition(payload)?.['Y Start']
        },
        getContainerYEnd: (state, getters) => (payload) => {
            return getters.getContainerPosition(payload)?.['Y End']
        },

        getVisualisation: (state, getters) => (payload) => {
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            return getters.getVisualisations(payload)?.[visualisationId]
        },

        getVisualisationPosition: (state, getters) => (payload) => {
            return getters.getVisualisation(payload)?.Position
        },
        getVisualisationTitle: (state, getters) => (payload) => {
            return getters.getVisualisation(payload)?.Title
        },
        getVisualisationDataDisplay: (state, getters) => (payload) => {
            return getters.getVisualisation(payload)?.DataDisplay
        },

        getVisualisationXStart: (state, getters) => (payload) => {
            return getters.getVisualisationPosition(payload)?.['X Start']
        },
        getVisualisationXEnd: (state, getters) => (payload) => {
            return getters.getVisualisationPosition(payload)?.['X End']
        },
        getVisualisationYStart: (state, getters) => (payload) => {
            return getters.getVisualisationPosition(payload)?.['Y Start']
        },
        getVisualisationYEnd: (state, getters) => (payload) => {
            return getters.getVisualisationPosition(payload)?.['Y End']
        },

        getVisualisationType: (state, getters) => (payload) => {
            return getters.getVisualisationDataDisplay(payload)?.Type
        },
        getVisualisationIndicators: (state, getters) => (payload) => {
            return getters.getVisualisationDataDisplay(payload)?.DataConfiguration?.Indicators
        },
        getVisualisationCategories: (state, getters) => (payload) => {
            return getters.getVisualisationDataDisplay(payload)?.DataConfiguration?.Categories
        },
        getVisualisationGroupingField: (state, getters) => (payload) => {
            return getters.getVisualisationDataDisplay(payload)?.DataConfiguration?.['Grouping Field']
        },
        getVisualisationStackingField: (state, getters) => (payload) => {
            return getters.getVisualisationDataDisplay(payload)?.DataConfiguration?.['Stacking Field']
        }
    },
    mutations: {
        setSelectionConfig (state, payload) {
            state.selectionConfig = {
                overviewId: payload?.overviewId ?? null,
                containerId: payload?.containerId ?? null,
                visualisationId: payload?.visualisationId ?? null,
                imageId: payload?.imageId ?? null,
                textParagraphId: payload?.textParagraphId ?? null
            }
        },

        setDashboardModel (state, dashboard) {
            state.dashboard = dashboard
        },
        setDashboardName (state, payload) {
            const name = payload.value
            state.dashboard.Name = name
        },

        setOverviews (state, payload) {
            const overviews = payload?.value
            state.dashboard.Overviews = overviews
        },
        setOverviewName (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const name = payload.value
            state.dashboard.Overviews[overviewId].Name = name
        },
        addOverview (state, payload) {
            const overview = payload?.value
            const newOverviewId = state.dashboard.Overviews.push(overview)
            return newOverviewId
        },

        setHeadSectionTitle (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const title = payload?.value
            state.dashboard.Overviews[overviewId].HeadSection.Title = title
        },
        setHeadSectionText (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const text = payload?.value
            state.dashboard.Overviews[overviewId].HeadSection.Text = text
        },

        setContainerTitle (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const title = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Title = title
        },

        setContainerXStart: (state, payload) => {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const xStart = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Position['X Start'] = xStart
        },
        setContainerXEnd: (state, payload) => {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const xEnd = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Position['X End'] = xEnd
        },
        setContainerYStart: (state, payload) => {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const yStart = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Position['Y Start'] = yStart
        },
        setContainerYEnd: (state, payload) => {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const yEnd = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Position['Y End'] = yEnd
        },

        setVisualisationTitle (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const title = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].Title = title
        },
        setVisualisationType (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const type = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.Type = type
        },

        setVisualisationXStart: (state, payload) => {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const xStart = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].Position['X Start'] = xStart
        },
        setVisualisationXEnd: (state, payload) => {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const xEnd = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].Position['X End'] = xEnd
        },
        setVisualisationYStart: (state, payload) => {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const yStart = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].Position['Y Start'] = yStart
        },
        setVisualisationYEnd: (state, payload) => {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const yEnd = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].Position['Y End'] = yEnd
        },

        setVisualisationValueField (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const fieldInfo = {}
            fieldInfo[payload?.fieldType] = payload?.field
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.Configuration['Value Field'] = fieldInfo
        },
        setVisualisationCategoryField (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const fieldInfo = {}
            fieldInfo[payload?.fieldType] = payload?.field
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.Configuration['Category Field'] = fieldInfo
        },
        setVisualisationGroupingCategoryField (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const fieldInfo = {}
            fieldInfo[payload?.fieldType] = payload?.field
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.Configuration['Grouping Category Field'] = fieldInfo
        },
        setVisualisationStackingCategoryField (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const fieldInfo = {}
            fieldInfo[payload?.fieldType] = payload?.field
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.Configuration['Stacking Category Field'] = fieldInfo
        }
    },
    actions: {
        async createDashboardModel ({ commit, dispatch }, payload) {
            await commit('setDashboardModel', payload)
            const selection = { overviewId: 0 }
            await dispatch('updateSelectionConfig', selection)
        },
        async addOverview ({ commit, dispatch, getters }, payload) {
            const overview = { Name: 'New Overview', HeadSection: { Title: 'New Title', Text: null }, BodySection: { Containers: [] } }
            const overviewPayload = { value: overview }
            await commit('addOverview', overviewPayload)

            // Set current selection to added overview
            const overviews = await getters.getOverviews()
            const newOverviewId = overviews.length - 1
            const selection = { overviewId: newOverviewId }
            await dispatch('updateSelectionConfig', selection)
        },
        async deleteOverview ({ commit, dispatch, getters }, payload) {
            const overviewId = await getters.getOverviewId(payload)
            const overviews = await getters.getOverviews()
            if (overviewId !== null) {
                overviews.splice(overviewId, 1)
                const payload = { value: overviews }
                await commit('setOverviews', payload)
                var selection = null
                if (overviews.length === 0) {
                    selection = null
                } else if (overviewId === 0) {
                    selection = { overviewId: 0 }
                } else {
                    selection = { overviewId: overviewId - 1 }
                }
                await dispatch('updateSelectionConfig', selection)
            }
        },
        async updateSelectionConfig ({ commit }, payload) {
            await commit('setSelectionConfig', payload)
        }
    }
}
