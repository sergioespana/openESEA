
export default {
    namespaced: true,
    state: {
        respondents: [],
        respondent: {},
        error: []
    },
    mutations: {
        setRespondents (state, { data }) {
            state.respondents = data
        },
        setRespondent (state, { data }) {
            state.respondent = data || {}
        },
        updateRespondent (state, { id, data }) {
            state.respondents = state.respondents.map((item) => {
                if (item.id !== id) { return item }
                return { ...item, ...data }
            })
        },
        deleteRespondent (state, { id }) {
            state.Respondents = state.respondents.filter(o => o.id !== id)
        },
        setError (state, { error }) {
            state.error = error
        }
    },
    actions: {
        // async fetchUsers ({ commit }, payload) {
        //     const { response, error } = await UserService.get(payload)
        //     if (error) {
        //         commit('setError', { error })
        //         return
        //     }
        //     commit('setUsers', response)
        // },
        setRespondents ({ commit }, payload) {
            commit('setRespondents', payload)
        }
    }
}
