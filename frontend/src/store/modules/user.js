import UserService from '../../services/UserService'

export default {
    namespaced: true,
    state: {
        users: [],
        user: {},
        error: []
    },
    mutations: {
        setUsers (state, { data }) {
            state.users = data
        },
        setUser (state, { data }) {
            state.user = data || {}
        },
        updateUser (state, { id, data }) {
            state.users = state.users.map((item) => {
                if (item.id !== id) { return item }
                return { ...item, ...data }
            })
        },
        deleteUser (state, { id }) {
            state.users = state.users.filter(o => o.id !== id)
        },
        setError (state, { error }) {
            state.error = error
        }
    },
    actions: {
        async fetchUsers ({ commit }, payload) {
            const { response, error } = await UserService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setUsers', response)
        },
        async fetchUser ({ commit }, payload) {
            const { response, error } = await UserService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setUser', response)
        },
        async updateUser ({ state, commit }, payload) {
            const id = state.user.id
            const { response, error } = await UserService.put({ id, data: payload, headers: { 'Content-Type': 'multipart/form-data' } })
            if (error) {
                console.log(error.response.data)
                commit('setError', { error })
                return
            }
            commit('updateUser', { ...response, id })
            commit('setOrganisation', response)
        },
        async deleteUser ({ commit, dispatch }, payload) {
            const { error } = await UserService.delete(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('deleteUser', payload)
            dispatch('setUser', {})
        },
        setUser ({ state, commit }, { id }) {
            if (id) {
                const data = state.users.find(u => u.id === id)
                commit('setUser', { data: data })
            } else {
                commit('setUser', {})
            }
        }
    }
}
