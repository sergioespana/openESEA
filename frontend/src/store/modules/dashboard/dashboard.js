import DashboardService from '../../../services/DashboardService'

export default {
    namespaced: true,
    state: {
        dashboards: [],
        dashboard: {},
        error: []
    },
    getters: {
        getDashboards: state => state.dashboards,
        getDashboard: state => state.dashboard,
        getDashboardById: (state) => (id) => state.dashboards.filter((dashboard) => dashboard.id === id)[0]
    },
    mutations: {
        setDashboards (state, { data }) {
            state.dashboards = data
        },
        setDashboard (state, { data }) {
            state.dashboard = data || {}
        },
        updateDashboard (state, { data, id }) {
            state.dashboards = state.dashboards.map((item) => {
                if (item.id !== id) { return item }
                return { ...item, ...data }
            })
        },
        deleteDashboard (state, { id }) {
            state.dashboards = state.dashboards.filter(e => e.id !== id)
        },
        setError (state, { error }) {
            console.log('my error:', error?.response.data)
            state.error = error?.response.data || []
        }
    },
    actions: {
        async fetchDashboards ({ commit }, payload) {
            console.log('Payload', payload)
            const { response, error } = await DashboardService.get(payload)
            console.log('Response:', response)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setDashboards', response)
        },
        async fetchDashboard ({ commit }, payload) {
            const { response, error } = await DashboardService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setDashboard', response)
        },
        async createDashboard ({ commit, dispatch }, { data }) {
            console.log('Creating dashboard with: ', data)
            const { response, error } = await DashboardService.post({ data: data })
            console.log('Created dashboard: ', response)
            if (error) {
                commit('setError', { error })
                return
            }
            await dispatch('fetchDashboards', { })
            await commit('setDashboard', response)
        },
        async updateDashboard ({ commit }, { data }) {
            const { response, error } = await DashboardService.put({ id: data.id, data, headers: { 'Content-Type': 'multipart/form-data' } })
            if (error) {
                commit('setError', { error })
                return
            }
            commit('updateDashboard', response)
            commit('setDashboard', response)
        },
        async deleteDashboard ({ commit, dispatch }, payload) {
            const { error } = await DashboardService.delete(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('deleteDashboard', payload)
            commit('setDashboard', {})
        },
        setDashboard ({ state, commit }, { id }) {
            if (id) {
                const data = state.dashboards.find(e => e.id === id)
                commit('setDashboard', { data: data })
            } else {
                commit('setDashboard', {})
            }
        }
    }
}
