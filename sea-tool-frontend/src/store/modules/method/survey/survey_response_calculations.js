import SurveyResponseService from
	'@/services/SurveyResponseService';

export default {
	namespaced: true,
	state: {
		surveyResponseCalculations: [],
		error: undefined,
	},
	mutations: {
		setSurveyResponses(state, { data }) {
			state.surveyResponseCalculations = data;
			state.error = undefined;
		},
		setError(state, { error, id }) {
			if (id && error?.response?.data) {
				state.errors = { ...state.errors, [id]: error?.response?.data };
				return;
			}
			state.error = error;
		},
	},
	actions: {
		async fetchSurveyResponseCalculations({ commit }, payload) {
			const { response, error } = await SurveyResponseService.get({
				...payload,
				query: 'calculations/',
			});
			if (error) {
				commit('setError', { error });
				return;
			}
			commit('setSurveyResponses', response);
		},
		resetError({ commit }) {
			commit('setError', { error: undefined });
		},
	},
};
