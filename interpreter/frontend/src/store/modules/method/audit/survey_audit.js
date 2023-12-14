import SurveyAuditService from '@/services/SurveyAuditService'

export default {
    namespaced: true,
    state: {
        surveyAudits: [],
        surveyAudit: {},
        error: []
    },
    mutations: {
        setSurveyAudits (state, { data }) {
            console.log(data)
            state.surveyAudits = data
        },
        setSurveyAudit (state, { data }) {
            state.surveyAudit = data || {}
        },
        updateSurveyAudit (state, { data, id }) {
            state.surveyAudits = state.surveyAudits.map((item) => {
                if (item.id !== id) { return item }
                return { ...item, ...data }
            })
        },
        setError (state, { error }) {
            console.log('my error:', error?.response.data)
            state.error = error?.response.data || []
        }
    },
    actions: {
        async fetchSurveyAudits ({ commit }, payload) {
            const { response, error } = await SurveyAuditService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setSurveyAudits', response)
        },
        async fetchSurveyAudit ({ commit }, payload) {
            const { response, error } = await SurveyAuditService.get(payload)
            if (error) {
                commit('setError', { error })
                return
            }
            commit('setSurveyAudit', response)
        },
        async createSurveyAudit ({ commit, dispatch }, { oId, eaId, data }) {
            const { response, error } = await SurveyAuditService.post({ oId, eaId, data: data })
            if (error) {
                commit('setError', { error })
                return
            }
            await dispatch('fetchSurveyAudits', { oId, eaId })
            await commit('setSurveyAudit', response)
        },
        async updateSurveyAudit ({ commit }, { oId, eaId, data }) {
            const { response, error } = await SurveyAuditService.put({ oId, eaId, id: data.id, data, headers: { 'Content-Type': 'multipart/form-data' } })
            if (error) {
                commit('setError', { error })
                return
            }
            // console.log('account audit:', response.data)
            commit('updateSurveyAudit', response)
            commit('setSurveyAudit', response)
        },
        setSurveyAudit ({ state, commit }, { id }) {
            if (id) {
                const data = state.surveyAudit.find(s => s.id === id)
                commit('setSurveyAudit', { data: data })
            } else {
                commit('setSurveyAudit', {})
            }
        }
    }
}
