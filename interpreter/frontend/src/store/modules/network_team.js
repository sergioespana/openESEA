import NetworkTeamService from '@/services/NetworkTeamService'

export default {
    namespaced: true,
    state: {
        networkmembers: [],
        networkmember: {},
        error: []
    },
    getters: {
        networkAuditors: (state) => { return state.networkmembers.filter(object => object.role_name === 'auditor') }
    },
    mutations: {
        setNetworkMembers (state, { data }) {
            state.networkmembers = data
        },
        setNetworkMember (state, { data }) {
            state.networkmember = data || {}
        },
        addNetworkMemberToList (state, { data }) {
            state.networkmembers.push(data)
        },
        updateNetworkMember (state, { id, data }) {
            state.networkmembers = state.networkmembers.map((item) => {
                if (item.id !== id) { return item }
                return { ...item, ...data }
            })
        },
        deleteNetworkMember (state, { id }) {
            state.networkmembers = state.networkmembers.filter(m => m.id !== id)
        },
        setError (state, { error }) {
            console.log(error?.response?.data)
            state.error = error?.response.data || []
        },
        clearError (state) {
            state.error = []
        }
    },
    actions: {
        async fetchNetworkMembers ({ commit }, payload) {
            commit('clearError')
            const { response, error } = await NetworkTeamService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setNetworkMembers', response)
        },
        async fetchNetworkMember ({ commit }, payload) {
            const { response, error } = await NetworkTeamService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setNetworkMember', response)
        },
        async createNetworkMember ({ commit, dispatch }, { nId, data }) {
            const { response, error } = await NetworkTeamService.post({ nId, data: data, headers: { 'Content-Type': 'multipart/form-data' } })
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setNetworkMember', response)
        },
        async updateNetworkMember ({ commit }, { nId, id, data }) {
            const { response, error } = await NetworkTeamService.put({ nId, id, data: data, headers: { 'Content-Type': 'multipart/form-data' } })
            if (error) {
                commit('setError', { error })
                return
            }
            commit('updateNetworkMember', response)
            commit('setNetworkMember', response)
        },
        async deleteNetworkMember ({ commit, dispatch }, payload) {
            const { error } = await NetworkTeamService.delete(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('deleteNetworkMember', payload)
            dispatch('setNetworkMember', {})
        },
        setNetworkMember ({ state, commit }, { id }) {
            if (id) {
                const data = state.networkmembers.find(m => m.id === id)
                commit('setNetworkMember', { data: data })
            } else {
                commit('setNetworkMember', {})
            }
        }
    }
}
