import NetworkService from '../../services/NetworkService'

export default {
    namespaced: true,
    state: {
        networks: [],
        network: {},
        error: []
    },
    mutations: {
        setNetworks (state, { data }) {
            state.networks = data
        },
        setNetwork (state, { data }) {
            state.network = data || {}
        },
        updateNetwork (state, { id, data }) {
            state.networks = state.networks.map((item) => {
                if (item.id !== id) { return item }
                return { ...item, ...data }
            })
        },
        deleteNetwork (state, { id }) {
            state.networks = state.networks.filter(n => n.id !== id)
        },
        setError (state, { error }) {
            console.log(error?.response?.data)
            state.error = error?.response?.data || []
        },
        clearError (state) {
            state.error = []
        }
    },
    actions: {
        async fetchNetworks ({ commit }, payload) {
            commit('clearError')
            const { response, error } = await NetworkService.get(payload)
            if (error) {
				commit('setError', { error })
                return
            }
            commit('setNetworks', response)
        },
        async fetchNetwork ({ commit }, payload) {
            const { response, error } = await NetworkService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setNetwork', response)
        },
        async createNetwork ({ commit, dispatch }, { data }) {
            const { response, error } = await NetworkService.post({ data: data, headers: { 'Content-Type': 'multipart/form-data' } })
            if (error) {
                commit('setError', { error })
                return
            }
            await dispatch('fetchNetworks', {})
            commit('setNetwork', response)
        },
        async updateNetwork ({ state, commit }, payload) {
            const id = state.network.id
            const { response, error } = await NetworkService.put({ id, data: payload, headers: { 'Content-Type': 'multipart/form-data' } })
            if (error) {
                commit('setError', { error })
                return
            }
            commit('updateNetwork', { ...response, id })
            commit('setNetwork', response)
        },
        async patchNetwork ({ state, commit }, payload) {
            const id = parseInt(state.network.id)
            const { response, error } = await NetworkService.patch({ id, data: payload, headers: { 'Content-Type': 'application/json' } })
            if (error) {
                commit('setError', { error })
                return
            }
            commit('updateNetwork', { ...response, id })
            commit('setNetwork', response)
        },
        async deleteNetwork ({ commit }, payload) {
            const { error } = await NetworkService.delete(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('deleteNetwork', payload)
            commit('setNetwork', {})
        },
        setNetwork ({ state, commit }, { id }) {
            if (id) {
                const data = state.networks.find(n => n.id === id)
                commit('setNetwork', { data: data })
            } else {
                commit('setNetwork', {})
            }
        }
    }
}
