import { cloneDeep } from 'lodash'

const elementPaths = {
    DashboardModel: { previousPath: null },
    DashboardName: { previousPath: 'DashboardModel', attribute: 'Name' },
    Overviews: { previousPath: 'DashboardModel', attribute: 'Overviews' },
    Overview: { previousPath: 'Overviews', id: 'overviewId' }
}

export default {
    namespaced: true,
    state: {
        dashboard: null,
        selectionConfig: null
    },
    getters: {
        get: (state, getters) => (name) => {
            const elementPath = elementPaths[name]
            const stateValue = elementPath.previousPath ? getters.get(elementPath.previousPath) : state.dashboard
            const element = elementPath.attribute ?? state.selectionConfig[elementPath.id]
            return stateValue[element]
        },

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
        getContainerPosition: (state, getters) => (payload) => {
            return getters.getContainer(payload)?.Position
        },
        getContainerStyle: (state, getters) => (payload) => {
            return getters.getContainer(payload)?.Style
        },

        getContainerBackgroundColor: (state, getters) => (payload) => {
            return getters.getContainerStyle(payload)?.['Background Color']
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
        getDataDisplay: (state, getters) => (payload) => {
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
            return getters.getDataDisplay(payload)?.Type
        },
        getDataConfiguration: (state, getters) => (payload) => {
            return getters.getDataDisplay(payload)?.DataConfiguration
        },

        getValueField: (state, getters) => (payload) => {
            return getters.getDataConfiguration(payload)?.['Value Field']
        },
        getFractionalValueField: (state, getters) => (payload) => {
            return getters.getDataConfiguration(payload)?.['Fractional Value Field']
        },
        getTotalValueField: (state, getters) => (payload) => {
            return getters.getDataConfiguration(payload)?.['Total Value Field']
        },
        getCurrentValueField: (state, getters) => (payload) => {
            return getters.getDataConfiguration(payload)?.['Current Value Field']
        },
        getTargetValueField: (state, getters) => (payload) => {
            return getters.getDataConfiguration(payload)?.['Target Value Field']
        },
        getCategoryField: (state, getters) => (payload) => {
            return getters.getDataConfiguration(payload)?.['Category Field']
        },
        getGroupingField: (state, getters) => (payload) => {
            return getters.getDataConfiguration(payload)?.['Grouping Field']
        },
        getStackingField: (state, getters) => (payload) => {
            return getters.getDataConfiguration(payload)?.['Stacking Field']
        },
        getValueFieldName: (state, getters) => (payload) => {
            return getters.getValueField(payload)?.Name
        },
        getFractionalValueFieldName: (state, getters) => (payload) => {
            return getters.getFractionalValueField(payload)?.Name
        },
        getTotalValueFieldName: (state, getters) => (payload) => {
            return getters.getTotalValueField(payload)?.Name
        },
        getCurrentValueFieldName: (state, getters) => (payload) => {
            return getters.getCurrentValueField(payload)?.Name
        },
        getTargetValueFieldName: (state, getters) => (payload) => {
            return getters.getTargetValueField(payload)?.Name
        },
        getCategoryFieldName: (state, getters) => (payload) => {
            return getters.getCategoryField(payload)?.Name
        },
        getGroupingFieldName: (state, getters) => (payload) => {
            return getters.getGroupingField(payload)?.Name
        },
        getStackingFieldName: (state, getters) => (payload) => {
            return getters.getStackingField(payload)?.Name
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

        setDashboardModel (state, payload) {
            const dashboard = payload?.value
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
            state.dashboard.Overviews.push(overview)
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

        setContainers (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containers = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers = containers
        },
        addContainer (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const container = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers.push(container)
        },

        setContainerTitle (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const title = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Title = title
        },
        setContainerStyle (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const style = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Style = style
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

        setContainerBackgroundColor: (state, payload) => {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const backgroundColor = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Style['Background Color'] = backgroundColor
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
        addVisualisation (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisation = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations.push(visualisation)
        },
        setVisualisations (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisations = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations = visualisations
        },

        setDataDisplay: (state, payload) => {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const dataDisplay = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay = dataDisplay
        },
        setDataConfiguration: (state, payload) => {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const dataConfiguration = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.DataConfiguration = dataConfiguration
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

        setValueField (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const valueField = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.DataConfiguration['Value Field'] = valueField
        },
        setFractionalValueField (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const fractionalValueField = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.DataConfiguration['Fractional Value Field'] = fractionalValueField
        },
        setTotalValueField (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const totalValueField = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.DataConfiguration['Total Value Field'] = totalValueField
        },
        setCurrentValueField (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const currentValueField = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.DataConfiguration['Current Value Field'] = currentValueField
        },
        setTargetValueField (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const targetValueField = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.DataConfiguration['Target Value Field'] = targetValueField
        },
        setCategoryField (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const categoryField = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.DataConfiguration['Category Field'] = categoryField
        },
        setGroupingField (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const groupingField = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.DataConfiguration['Grouping Field'] = groupingField
        },
        setStackingField (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const stackingField = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.DataConfiguration['Stacking Field'] = stackingField
        },
        setValueFieldName (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const name = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.DataConfiguration['Value Field'].Name = name
        },
        setFractionalValueFieldName (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const name = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.DataConfiguration['Fractional Value Field'].Name = name
        },
        setTotalValueFieldName (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const name = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.DataConfiguration['Total Value Field'].Name = name
        },
        setCurrentValueFieldName (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const name = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.DataConfiguration['Current Value Field'].Name = name
        },
        setTargetValueFieldName (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const name = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.DataConfiguration['Target Value Field'].Name = name
        },
        setCategoryFieldName (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const name = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.DataConfiguration['Category Field'].Name = name
        },
        setGroupingFieldName (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const name = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.DataConfiguration['Grouping Category Field'].Name = name
        },
        setStackingFieldName (state, payload) {
            const overviewId = payload?.overviewId ?? state.selectionConfig.overviewId
            const containerId = payload?.containerId ?? state.selectionConfig.containerId
            const visualisationId = payload?.visualisationId ?? state.selectionConfig.visualisationId
            const name = payload?.value
            state.dashboard.Overviews[overviewId].BodySection.Containers[containerId].Visualisations[visualisationId].DataDisplay.DataConfiguration['Stacking Category Field'].Name = name
        }
    },
    actions: {
        async updateSelectionConfig ({ commit }, payload) {
            await commit('setSelectionConfig', payload)
        },

        async createDashboardModel ({ commit, dispatch }, payload) {
            await commit('setDashboardModel', payload)
            const selection = { overviewId: 0 }
            await dispatch('updateSelectionConfig', selection)
        },

        async addOverview ({ commit, dispatch, getters }, payload) {
            // Add an overview with the following information
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
            // Get current overview id
            const overviewId = await getters.getOverviewId(payload)

            // Delete overview if id is present
            if (overviewId !== null) {
                // Get overviews and remove overview at overviewId
                const overviews = await getters.getOverviews()
                overviews.splice(overviewId, 1)

                // Update the overviews with the overview removed
                const payload = { value: overviews }
                await commit('setOverviews', payload)

                // Update the current selection to display the previous overview or otherwise the first overview
                var selection = null
                if (overviews.length === 0) {
                    selection[overviewId] = null
                } else if (overviewId === 0) {
                    selection[overviewId] = 0
                } else {
                    selection[overviewId] = overviewId - 1
                }
                await dispatch('updateSelectionConfig', selection)
            }
        },

        async addContainer ({ commit, dispatch, getters }, payload) {
            // Add an container with the following information
            const container = { Title: 'New Container', Position: { 'X Start': 40, 'X End': 60, 'Y Start': 45, 'Y End': 55 }, Visualisations: [], Images: [], TextParagraphs: [] }
            const containerPayload = { value: container }
            await commit('addContainer', containerPayload)

            // Set current selection to added container
            const containers = await getters.getContainers()
            const newContainerId = containers.length - 1
            const selection = { overviewId: await getters.getOverviewId(), containerId: newContainerId }
            await dispatch('updateSelectionConfig', selection)
        },

        async deleteContainer ({ commit, dispatch, getters }, payload) {
            // Get current overview id
            const containerId = await getters.getContainerId(payload)

            // Delete overview if id is present
            if (containerId !== null) {
                // Get overviews and remove overview at overviewId
                const containers = await getters.getContainers()
                containers.splice(containerId, 1)

                // Update the overviews with the overview removed
                const payload = { value: containers }
                await commit('setContainers', payload)

                // Update the current selection to display the previous overview or otherwise the first overview
                const selection = { overviewId: await getters.getOverviewId() }
                await dispatch('updateSelectionConfig', selection)
            }
        },

        async addVisualisation ({ commit, dispatch, getters }, payload) {
            // Add a container with the following information
            const visualisation = { Title: 'New Visualisation', Position: { 'X Start': 40, 'X End': 60, 'Y Start': 45, 'Y End': 55 }, DataDisplay: { Type: null } }
            const visualisationPayload = { value: visualisation }
            await commit('addVisualisation', visualisationPayload)

            // Set current selection to added container
            const visualisations = await getters.getVisualisations()
            const newVisualisationId = visualisations.length - 1
            const selection = { overviewId: await getters.getOverviewId(), containerId: await getters.getContainerId(), visualisationId: newVisualisationId }
            await dispatch('updateSelectionConfig', selection)
        },

        async deleteVisualisation ({ commit, dispatch, getters }, payload) {
            // Get current overview id
            const visualisationId = await getters.getVisualisationId(payload)

            // Delete overview if id is present
            if (visualisationId !== null) {
                // Get overviews and remove overview at overviewId
                const visualisations = await getters.getVisualisations()
                visualisations.splice(visualisationId, 1)

                // Update the overviews with the overview removed
                const payload = { value: visualisations }
                await commit('setVisualisations', payload)

                // Update the current selection to display the previous overview or otherwise the first overview
                const selection = { overviewId: await getters.getOverviewId(), containerId: await getters.getContainerId() }
                await dispatch('updateSelectionConfig', selection)
            }
        },

        async updateContainerBackgroundColor ({ commit, dispatch, getters }, payload) {
            // Initialize style object if not exists
            const style = getters.getContainerStyle(payload)
            if (!style) {
                var stylePayload = cloneDeep(payload)
                stylePayload.value = {}
                await commit('setContainerStyle', stylePayload)
            }
            // Set background color
            await commit('setContainerBackgroundColor', payload)
        },

        async updateDataConfiguration ({ commit, dispatch, getters }, payload) {
            // Initialize dataDisplay object if not exists
            const dataDisplay = getters.getDataDisplay(payload)
            if (!dataDisplay) {
                var dataDisplayPayload = cloneDeep(payload)
                dataDisplayPayload.value = {}
                await commit('setDataDisplay', dataDisplayPayload)
            }
            await commit('setDataConfiguration', payload)
        },
        async updateValueField ({ commit, dispatch, getters }, payload) {
            // Initialize dataConfiguration object if not exists
            const dataConfiguration = getters.getDataConfiguration(payload)
            if (!dataConfiguration) {
                var dataConfigurationPayload = cloneDeep(payload)
                dataConfigurationPayload.value = {}
                await dispatch('updateDataConfiguration', dataConfigurationPayload)
            }
            await commit('setValueField', payload)
        },
        async updateFractionalValueField ({ commit, dispatch, getters }, payload) {
            // Initialize dataConfiguration object if not exists
            const dataConfiguration = getters.getDataConfiguration(payload)
            if (!dataConfiguration) {
                var dataConfigurationPayload = cloneDeep(payload)
                dataConfigurationPayload.value = {}
                await dispatch('updateDataConfiguration', dataConfigurationPayload)
            }
            await commit('setFractionalValueField', payload)
        },
        async updateTotalValueField ({ commit, dispatch, getters }, payload) {
            // Initialize dataConfiguration object if not exists
            const dataConfiguration = getters.getDataConfiguration(payload)
            if (!dataConfiguration) {
                var dataConfigurationPayload = cloneDeep(payload)
                dataConfigurationPayload.value = {}
                await dispatch('updateDataConfiguration', dataConfigurationPayload)
            }
            await commit('setTotalValueField', payload)
        },
        async updateCurrentValueField ({ commit, dispatch, getters }, payload) {
            // Initialize dataConfiguration object if not exists
            const dataConfiguration = getters.getDataConfiguration(payload)
            if (!dataConfiguration) {
                var dataConfigurationPayload = cloneDeep(payload)
                dataConfigurationPayload.value = {}
                await dispatch('updateDataConfiguration', dataConfigurationPayload)
            }
            await commit('setCurrentValueField', payload)
        },
        async updateTargetValueField ({ commit, dispatch, getters }, payload) {
            // Initialize dataConfiguration object if not exists
            const dataConfiguration = getters.getDataConfiguration(payload)
            if (!dataConfiguration) {
                var dataConfigurationPayload = cloneDeep(payload)
                dataConfigurationPayload.value = {}
                await dispatch('updateDataConfiguration', dataConfigurationPayload)
            }
            await commit('setTargetValueField', payload)
        },
        async updateCategoryField ({ commit, dispatch, getters }, payload) {
            // Initialize dataConfiguration object if not exists
            const dataConfiguration = getters.getDataConfiguration(payload)
            if (!dataConfiguration) {
                var dataConfigurationPayload = cloneDeep(payload)
                dataConfigurationPayload.value = {}
                await dispatch('updateDataConfiguration', dataConfigurationPayload)
            }
            await commit('setCategoryField', payload)
        },
        async updateGroupingField ({ commit, dispatch, getters }, payload) {
            // Initialize dataConfiguration object if not exists
            const dataConfiguration = getters.getDataConfiguration(payload)
            if (!dataConfiguration) {
                var dataConfigurationPayload = cloneDeep(payload)
                dataConfigurationPayload.value = {}
                await dispatch('updateDataConfiguration', dataConfigurationPayload)
            }
            await commit('setGroupingField', payload)
        },
        async updateStackingField ({ commit, dispatch, getters }, payload) {
            // Initialize dataConfiguration object if not exists
            const dataConfiguration = getters.getDataConfiguration(payload)
            if (!dataConfiguration) {
                var dataConfigurationPayload = cloneDeep(payload)
                dataConfigurationPayload.value = {}
                await dispatch('updateDataConfiguration', dataConfigurationPayload)
            }
            await commit('setStackingField', payload)
        }
    }
}
