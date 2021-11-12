import MembershipService from '../../services/MembershipService'

export default {
    namespaced: true,
    state: {
        memberships: [],
        membership: {},
        error: []
    },
    getters: {
        requestsByNetwork: (state) => {
            let requests = []
            requests = state.memberships.filter(m => m.requester === 'network')
            return requests
        },
        requestsByOrganisation: (state) => {
            let requests = []
            requests = state.memberships.filter(m => m.requester === 'organisation')
            return requests
        }
    },
    mutations: {
        setMemberships (state, { data }) {
            state.memberships = data
        },
        setMembership (state, { data }) {
            state.membership = data || {}
        },
        addMembershipToList (state, { data }) {
            state.memberships.push(data)
        },
        updateMembership (state, { id, data }) {
            state.memberships = state.memberships.map((item) => {
                if (item.id !== id) { return item }
                return { ...item, ...data }
            })
        },
        deleteMembership (state, { id }) {
            state.memberships = state.memberships.filter(m => m.id !== id)
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
        async fetchMemberships ({ commit }, payload) {
            commit('clearError')
            const { response, error } = await MembershipService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setMemberships', response)
        },
        async fetchMembership ({ commit }, payload) {
            const { response, error } = await MembershipService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setMembership', response)
        },
        async createMembership ({ commit, dispatch }, { data }) {
            const { response, error } = await MembershipService.post({ data: data, headers: { 'Content-Type': 'multipart/form-data' } })
            if (error) {
                commit('setError', { error })
                return
            }
            await dispatch('fetchMemberships', {})
            commit('setMembership', response)
        },
        async updateMembership ({ commit }, { id, data }) {
            const { response, error } = await MembershipService.put({ id: id, data: data, headers: { 'Content-Type': 'multipart/form-data' } })
            if (error) {
                commit('setError', { error })
                return
            }
            commit('updateMembership', response)
        },
        async deleteMembership ({ commit, dispatch }, payload) {
            const { error } = await MembershipService.delete(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('deleteMembership', payload)
            commit('setMembership', {})
        },

        setMembership ({ state, commit }, { id }) {
            if (id) {
                const data = state.memberships.find(m => m.id === id)
                commit('setMembership', { data: data })
            } else {
                commit('setMembership', {})
            }
        }
    }
}
