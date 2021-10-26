import NetworkTeamService from '@/services/NetworkTeamService'

export default {
    namespaced: true,
    state: {
        networkmembers: [],
        networkmember: {},
        error: []
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
            // await dispatch('fetchMemberships', {})
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
// async patchMembership ({ state, commit }, payload) {
//     const id = state.organisation.id
//     const data = payload.data
//     const { response, error } = await OrganisationService.patch({ id, data, headers: { 'Content-Type': 'application/json' } })
//     if (error) {
//         commit('setError', { error })
//         return
//     }
//     commit('updateNetwork', { ...response, id })
//     commit('setNetwork', response)
// },
// resetError ({ commit }) {
//     commit('setError', { error: undefined })
// }
// }
// async fetchOrganisations({ commit }, payload) {
//     const { response, error } =  AxiosInstance.get(`http://127.0.0.1:8000/organisations/${this.$route.params.id}/`)
//     //     .then(response => {
//     //         console.log(response.data)
//     //         this.post = response.data
//     //     })
//     await OrganisationService.get(payload)
//     console.log(response)
//     if (error) {
//         commit('setError', { error })
//         return
//     }
//     commit('setOrganisations', response)
//
    // async fetchOrganisations () {
//     await TestService.get()
//     .then(response => {
//         this.organisations = response.data
//         console.log(this.organisations)
//     })
//     .catch(err => {
//     console.log(err)
// AxiosInstance.get('/organisations/', { headers: { Authorization: `Bearer ${this.$store.state.accessToken}` } })
// .then(response => {
//   commit('setOrganisations', response)
// })
// .catch(err => {
//   console.log(err)
//  })
// async fetchOrganisationUsers ({ commit }, payload) {
//     const query = `organisation=${payload.id}`
//     const { response, error } = await UserService.get({ query: query })
//     if (error) {
// 		commit('setError', { error })
//         return
//     }
//     console.log(response)
// var config = { headers: { Authorization: 'Bearer ' + getters.AuthenticationToken } }
// const response = await axios.get(`http://localhost:8000/users/?network=${payload.id}`, config)
//     commit('setNetworkUsers', response)
// },
// setOrganisationParticipants (state, { data }) {
//     state.organisationParticipants = data.participants || {}
// },
// deleteOrganisationUsers (state, { id }) {
//     state.organisationParticipants = state.organisationParticipants.filter(o => o.id !== id)
// },
