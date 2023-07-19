export default {
    namespaced: true,
    state: {
        indicators: [], /*         */ // List of indicators
        indicatorData: [], /*      */ // Values from survey responses
        indicatorFields: [] /*     */ // Selected fields from survey responses
        // supplementaryData: [], /*  */ // Values from uploaded json
        // supplementaryFields: [] /* */ // Fields from uploaded json
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
        }
        // setSupplementaryData (state, data) {
        //     state.supplementaryData = data
        // },
        // setSupplementaryFields (state, fields) {
        //     state.supplementaryFields = fields
        // }
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
        }
        // getSupplementaryData: (state, getters) => () => {
        //     return state.supplementaryData
        // },
        // getSupplementaryFields: (state, getters) => () => {
        //     return state.supplementaryFields
        // }
    }
}
