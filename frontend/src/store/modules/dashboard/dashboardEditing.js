export default {
    namespaced: true,
    state: {
        selectedOverviewId: null,
        selectedContainerId: null,
        selectedVisualisationId: null
    },
    mutations: {
        setSelectedVisualisation (state, payload) {
            state.selectedOverviewId = payload.overviewId
            state.selectedContainerId = payload.containerId
            state.selectedVisualisationId = payload.visualisationId
        }
    },
    getters: {
        getSelectedVisualisation: (state, getters) => () => {
            return { overviewId: state.selectedOverviewId, containerId: state.selectedContainerId, visualisationId: state.selectedVisualisationId }
        }
    }
}
