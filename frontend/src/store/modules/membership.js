import MembershipService from '../../services/MembershipService'

export default {
    namespaced: true,
    state: {
        memberships: [],
        membership: {},
        // organisationParticipants: [],
        error: []
    },
    getters: {
        requestsByNetwork: (state) => {
            let requests = []
            requests = state.memberships.filter(m => m.requester === 'network')
            console.log('net:', requests)
            return requests
        },
        requestsByOrganisation: (state) => {
            let requests = []
            requests = state.memberships.filter(m => m.requester === 'organisation')
            console.log('org:', requests)
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
