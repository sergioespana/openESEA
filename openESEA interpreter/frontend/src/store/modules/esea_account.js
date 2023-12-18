import EseaAccountService from '../../services/EseaAccountService'

export default {
    namespaced: true,
    state: {
        eseaAccounts: [],
        eseaAccount: {},
        error: []
    },
    getters: {
        getEseaAccounts: state => state.eseaAccounts
    },
    mutations: {
        setEseaAccounts (state, { data }) {
            state.eseaAccounts = data
        },
        setEseaAccount (state, { data }) {
            state.eseaAccount = data || {}
        },
        updateEseaAccount (state, { data, id }) {
            state.eseaAccounts = state.eseaAccounts.map((item) => {
                if (item.id !== id) { return item }
                return { ...item, ...data }
            })
        },
        deleteEseaAccount (state, { id }) {
            state.eseaAccounts = state.eseaAccounts.filter(e => e.id !== id)
        },
        setError (state, { error }) {
            console.log('my error:', error?.response.data)
            state.error = error?.response.data || []
        }
    },
    actions: {
        async fetchEseaAccounts ({ commit }, payload) {
            const { response, error } = await EseaAccountService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setEseaAccounts', response)
        },
        async fetchEseaAccount ({ commit }, payload) {
            const { response, error } = await EseaAccountService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setEseaAccount', response)
        },
        async createEseaAccount ({ commit, dispatch }, { oId, data }) {
            const { response, error } = await EseaAccountService.post({ oId, data: data })
            if (error) {
                commit('setError', { error })
                return
            }
            await dispatch('fetchEseaAccounts', { oId })
            await commit('setEseaAccount', response)
        },
        async updateEseaAccount ({ commit }, { oId, data }) {
            const { response, error } = await EseaAccountService.put({ oId, id: data.id, data, headers: { 'Content-Type': 'multipart/form-data' } })
            if (error) {
                commit('setError', { error })
                return
            }
            commit('updateEseaAccount', response)
            commit('setEseaAccount', response)
        },
        async deleteEseaAccount ({ commit, dispatch }, payload) {
            const { error } = await EseaAccountService.delete(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('deleteEseaAccount', payload)
            commit('setEseaAccount', {})
        },
        setEseaAccount ({ state, commit }, { id }) {
            if (id) {
                const data = state.eseaAccounts.find(e => e.id === id)
                commit('setEseaAccount', { data: data })
            } else {
                commit('setEseaAccount', {})
            }
        }
    }
}
