import OrganisationTeamService from '@/services/OrganisationTeamService'

export default {
    namespaced: true,
    state: {
        organisationmembers: [],
        organisationmember: {},
        error: []
    },
    mutations: {
        setOrganisationMembers (state, { data }) {
            state.organisationmembers = data
        },
        setOrganisationMember (state, { data }) {
            state.organisationmember = data || {}
        },
        addOrganisationMemberToList (state, { data }) {
            state.organisationmembers.push(data)
        },
        updateOrganisationMember (state, { id, data }) {
            state.organisationmembers = state.organisationmembers.map((item) => {
                if (item.id !== id) { return item }
                return { ...item, ...data }
            })
        },
        deleteOrganisationMember (state, { id }) {
            state.organisationmembers = state.organisationmembers.filter(m => m.id !== id)
        },
        setError (state, { error }) {
            console.log(error?.response?.data)
            state.error = error.response.data || []
        },
        clearError (state) {
            state.error = []
        }
    },
    actions: {
        async fetchOrganisationMembers ({ commit }, payload) {
            commit('clearError')
            const { response, error } = await OrganisationTeamService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setOrganisationMembers', response)
        },
        async fetchOrganisationMember ({ commit }, payload) {
            const { response, error } = await OrganisationTeamService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setOrganisationMember', response)
        },
        async createOrganisationMember ({ commit, dispatch }, { oId, data }) {
            const { response, error } = await OrganisationTeamService.post({ oId, data: data, headers: { 'Content-Type': 'multipart/form-data' } })
            if (error) {
                commit('setError', { error })
                return
            }
            dispatch('setOrganisationMember', response)
        },
        async updateOrganisationMember ({ commit }, { oId, id, data }) {
            const { response, error } = await OrganisationTeamService.put({ oId, id, data: data, headers: { 'Content-Type': 'multipart/form-data' } })
            if (error) {
                commit('setError', { error })
                return
            }
            commit('updateOrganisationMember', response)
            commit('setOrganisationMember', response)
        },
        async deleteOrganisationMember ({ commit, dispatch }, payload) {
            const { error } = await OrganisationTeamService.delete(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('deleteOrganisationMember', payload)
            dispatch('setOrganisationMember', {})
        },
        setOrganisationMember ({ state, commit }, { id }) {
            if (id) {
                const data = state.organisationmembers.find(m => m.id === id)
                commit('setOrganisationMember', { data: data })
            } else {
                commit('setOrganisationMember', {})
            }
        }
    }
}
