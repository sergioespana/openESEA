import { isEqual } from 'lodash'

export default {
    namespaced: true,
    state: {
        indicators: [], /*          */ // List of indicators
        indicatorData: [], /*       */ // Values from survey responses
        indicatorFields: [], /*     */ // Selected fields from survey responses
        indicatorDataSets: {}, /*   */ // Datasets for each indicator
        visualisationDatasets: []
    },
    getters: {
        getIndicators: (state, getters) => () => {
            return state.indicators
        },
        getIndicatorData: (state, getters) => () => {
            return state.indicatorData
        },
        getIndicatorFields: (state, getters) => () => {
            return state.indicatorFields
        },
        getIndicatorDataSets: (state, getters) => () => {
            return state.indicatorDataSets
        },
        getIndicatorDataSet: (state, getters) => (indicatorKey) => {
            return state.indicatorDataSets[indicatorKey]
        },
        getVisualisationDatasets: (state, getters) => () => {
            return state.visualisationDatasets
        }
    },
    mutations: {
        setIndicators (state, indicators) {
            state.indicators = indicators
        },
        setIndicatorData (state, data) {
            state.indicatorData = data
        },
        setIndicatorFields (state, fields) {
            state.indicatorFields = fields
        },
        setIndicatorDataSets (state, dataSets) {
            state.indicatorDataSets = dataSets
        },
        setVisualisationDatasets (state, visualisationDatasets) {
            state.visualisationDatasets = visualisationDatasets
        }
    },
    actions: {
        createIndicatorDataSets ({ commit, dispatch, getters }, payload) {
            const indicators = getters.getIndicators()
            const indicatorDataSets = {}
            for (const indicator of indicators) {
                const indicatorKey = indicator.key
                const indicatorName = indicator.name ?? indicator.key
                indicatorDataSets[indicatorKey] = { name: indicatorName, data: [] }
            }

            const indicatorsData = getters.getIndicatorData()
            for (const indicatorData of indicatorsData) {
                const indicatorKey = indicatorData['Indicator Key']
                const indicatorYear = indicatorData.Year
                const indicatorValue = indicatorData.Value

                const indicatorName = indicatorDataSets[indicatorKey].name

                var dataRecord = {}
                dataRecord.Year = indicatorYear
                dataRecord[indicatorName] = indicatorValue

                indicatorDataSets[indicatorKey].data.push(dataRecord)
            }
            commit('setIndicatorDataSets', indicatorDataSets)
        },
        saveVisualisationDataset ({ commit, dispatch, getters }, payload) {
            const visualisationDatasets = getters.getVisualisationDatasets()
            console.log(payload)
            const config = payload.config
            const dataset = payload.dataset
            var newDataset = true
            console.log(visualisationDatasets)
            for (var visualisationDataset of visualisationDatasets) {
                if (isEqual(visualisationDataset.config, config)) {
                    newDataset = false
                    visualisationDataset.dataset = dataset
                }
            }
            if (newDataset) visualisationDatasets.push(payload)
            commit('setVisualisationDatasets', visualisationDatasets)
        }
    }
}
