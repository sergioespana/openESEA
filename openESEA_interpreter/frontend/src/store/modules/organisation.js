import OrganisationService from '../../services/OrganisationService'

export default {
    namespaced: true,
    state: {
        organisations: [],
        organisation: {},
        error: []
    },
    mutations: {
        setOrganisations (state, { data }) {
            state.organisations = data
        },
        setOrganisation (state, { data }) {
            state.organisation = data || {}
        },
        addOrganisationToList (state, { data }) {
            state.organisations.push(data)
        },
        updateOrganisation (state, { id, data }) {
            state.organisations = state.organisations.map((item) => {
                if (item.id !== id) { return item }
                return { ...item, ...data }
            })
        },
        deleteOrganisation (state, { id }) {
            state.organisations = state.organisations.filter(o => o.id !== id)
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
        async fetchOrganisations ({ commit }, payload) {
            commit('clearError')
            const { response, error } = await OrganisationService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setOrganisations', response)
        },
        async fetchOrganisation ({ commit }, payload) {
            const { response, error } = await OrganisationService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setOrganisation', response)
        },
        async createOrganisation ({ commit, dispatch }, { data }) {
            const { response, error } = await OrganisationService.post({ data: data, headers: { 'Content-Type': 'multipart/form-data' } })
            if (error) {
                commit('setError', { error })
                return
            }
            await dispatch('fetchOrganisations', {})
            commit('setOrganisation', response)
        },
        async updateOrganisation ({ state, commit }, payload) {
            const id = state.organisation.id
            const { response, error } = await OrganisationService.put({ id, data: payload, headers: { 'Content-Type': 'multipart/form-data' } })
            if (error) {
                commit('setError', { error })
                return
            }
            commit('updateOrganisation', response)
            commit('setOrganisation', response)
        },
        async patchOrganisation ({ state, commit }, payload) {
            const id = state.organisation.id
            const { response, error } = await OrganisationService.patch({ id, data: payload, headers: { 'Content-Type': 'application/json' } })
            if (error) {
                commit('setError', { error })
                return
            }
            commit('updateOrganisation', { ...response, id })
            commit('setOrganisation', response)
        },
        async deleteOrganisation ({ commit, dispatch }, payload) {
            const { error } = await OrganisationService.delete(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('deleteOrganisation', payload)
            commit('setOrganisation', {})
        },
        setOrganisation ({ state, commit }, { id }) {
            if (id) {
                const data = state.organisations.find(o => o.id === id)
                commit('setOrganisation', { data: data })
            } else {
                commit('setOrganisation', {})
            }
        }
    }
}
