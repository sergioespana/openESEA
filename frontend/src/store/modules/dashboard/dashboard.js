import DashboardService from '../../../services/DashboardService.js'

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
        getDashboardById: (state) => (id) => state.dashboards.find((dashboard) => dashboard.id === id)
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
            const { response, error } = await DashboardService.get(payload)
            if (error) {
                await commit('setError', { error })
                return
            }
            await commit('setDashboards', response)
        },
        async fetchDashboard ({ commit }, payload) {
            const { response, error } = await DashboardService.get(payload)
            if (error) {
                await commit('setError', { error })
                return
            }
            await commit('setDashboard', response)
        },
        async createDashboard ({ commit, dispatch }, { data }) {
            const { response, error } = await DashboardService.post({ data: data })
            if (error) {
                commit('setError', { error })
                return
            }
            await dispatch('fetchDashboards', { })
            await commit('setDashboard', response)
        },
        async updateDashboard ({ commit }, { id, data }) {
            const { response, error } = await DashboardService.put({ id: id, data, headers: { 'Content-Type': 'multipart/form-data' } })
            if (error) {
                commit('setError', { error })
                return
            }
            await commit('updateDashboard', response)
            await commit('setDashboard', response)
        },
        async deleteDashboard ({ commit, dispatch }, payload) {
            const { error } = await DashboardService.delete(payload)
            if (error) {
                await commit('setError', { error })
                return
            }
            await commit('deleteDashboard', payload)
            await commit('setDashboard', {})
        },
        async setDashboard ({ state, commit }, { id }) {
            if (id) {
                const data = state.dashboards.find(e => e.id === id)
                await commit('setDashboard', { id: id, data: data })
            } else {
                await commit('setDashboard', {})
            }
        }
    }
}
