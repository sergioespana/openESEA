import PublicSurveyService from '@/services/PublicSurveyService';

export default {
	namespaced: true,
	state: {
		surveys: [],
		survey: {},
		error: undefined,
	},
	getters: {
		getById: state => id => state.surveys.find(object => object.id === id),
	},
	mutations: {
		setSurveys(state, { data }) {
			state.surveys = data;
		},
		setSurvey(state, { data }) {
			state.survey = data || {};
		},
		setError(state, { error, id }) {
			if (id) {
				state.errors = {
					...state.errors,
					[id]: error?.response?.data || error,
				};
				return;
			}
			state.error = error;
		},
	},
	actions: {
		async fetchSurveys({ commit }, payload = {}) {
			commit('setError', { error: undefined });
			const { response, error } = await PublicSurveyService.get(payload);
			if (error) {
				commit('setError', { error });
				return;
			}

			if (response?.data instanceof Array) {
				commit('setSurveys', response);
			} else {
				commit('setSurvey', response);
			}
		},
		resetError({ commit }) {
			commit('setError', { error: undefined });
		},
	},
};
