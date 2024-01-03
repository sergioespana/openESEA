import SurveyResultService from '@/services/SurveyResultService'

export default {
	namespaced: true,
	state: {
		surveyResult: {},
		error: undefined
	},
	mutations: {
		setSurveyResult (state, { data }) {
			state.surveyResult = data || {}
		},
		setError (state, { error, id }) {
			if (id && error?.response?.data) {
				state.errors = { ...state.errors, [id]: error?.response?.data }
				return
			}
			state.error = error?.response?.data || error
		}
	},
	actions: {
		async fetchSurveyResults ({ commit }, payload) {
			const { response, error } = await SurveyResultService.get(
				{ ...payload, query: 'all/', id: undefined }
			)
			if (error) {
				commit('setError', { error })
				return { error }
			}
			commit('setSurveyResult', response)
			return { response }
		}
	}
}
