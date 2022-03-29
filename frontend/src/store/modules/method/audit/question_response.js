import QuestionResponseService from '@/services/QuestionResponseService'

export default {
    namespaced: true,
    state: {
        questionResponses: [],
        selectedQuestionResponses: [],
        questionResponse: {},
        error: undefined,
        debouncers: {}, //QUESTION: Do we need these?
        errors: {}
    },
    getters: {
    },
    mutations: {
        setQuestionResponses (state, { data }) {
            state.questionResponses = data || {}
            state.debouncers = {}
            state.errors = {}
        },
        setSelectedQuestionResponses (state, data) {
            state.selectedQuestionResponses = data
        },
        setQuestionResponse (state, { data }) {
            state.questionResponse = data || {}
        },
        updateQuestionResponse (state, data) {
            state.questionResponses = state.questionResponses.map((item) => {
                if (item.id !== data.id) { return item }
                return { ...item, ...data }
            })
            state.selectedQuestionResponses = state.selectedQuestionResponses.map((item) => {
                if (item.id !== data.id) { return item }
                return { ...item, ...data }
            })
        },
        setError (state, { error, id }) {
            console.log(id, '--', error?.response?.data)
            if (id && error?.response?.data) {
                state.errors = { ...state.errors, [id]: error?.response?.data }
                return
            }
            state.error = error
        },
        clearError (state) {
            state.error = []
        }
    },
    actions: {
        async fetchQuestionResponses ({ commit }, payload) {
            const { response, error } = await QuestionResponseService.get(payload) //QUESTION: New service?
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setQuestionResponses', response)
        },
        // only works in frontend
        async updateQuestionResponses ({ commit }, payload) {
            commit('updateQuestionResponse', payload)
        },
        async selectQuestionResponses ({ commit }, { indicators }) {
            await commit('setSelectedQuestionResponses', indicators)
        },
        setSelectedQuestionResponse ({ state, commit }, { id } = {}) {
            console.log(id)
            const data = state.selectedQuestionResponses.find(questionResponse => questionResponse.id === id)
            if (data && data.id === state.questionResponse.id) return
            commit('setQuestionResponse', { data })
        }
    }
}
