import { debounce } from 'lodash';
import PublicSurveyResponseService from
	'@/services/PublicSurveyResponseService';

const baseSurveyResponse = {
	question_responses: [],
};

export default {
	namespaced: true,
	state: {
		surveyResponse: {},
		error: undefined,
		debouncer: undefined,
		isSaved: false,
	},
	mutations: {
		setSurveyResponses(state, { data }) {
			state.surveyResponses = data;
		},
		setSurveyResponse(state, { commit, data }) {
			state.surveyResponse = data || {};
			state.isSaved = true;
			state.debouncer = debounce(
				async ({ surveyResponse }) => {
					const { response, error } = await PublicSurveyResponseService.put({
						sId: data.survey,
						id: data.id,
						token: data.token,
						data: surveyResponse,
					});
					if (error) {
						commit('setError', { error, id: surveyResponse.id });
						return;
					}
					commit('setError', { error: {}, id: surveyResponse.id });
					commit('setIsSaved', true);
					commit('updateSurveyResponse', { data: { id: response.data.id } });
				},
				1000,
			);
		},
		deleteSurveyResponse(state, { id }) {
			delete state.debouncers[id];
			delete state.errors[id];
			delete state.isSaved[id];
			state.surveyResponses = state.surveyResponses.filter(q => q.id !== id);
		},
		setError(state, { error, id }) {
			if (id && error?.response?.data) {
				state.errors = { ...state.errors, [id]: error?.response?.data };
				return;
			}
			state.error = error;
		},
		updateSurveyResponse(state, { data }) {
			state.surveyResponse = { ...state.surveyResponse, ...data };
		},
		setIsSaved(state, isSaved) {
			state.isSaved = isSaved;
		},
	},
	actions: {
		async fetchSurveyResponses({ commit }, payload = {}) {
			commit('setError', { error: undefined });
			const { response, error } = await PublicSurveyResponseService
				.get(payload);
			if (error) {
				commit('setError', { error });
				return;
			}

			if (response?.data instanceof Array) {
				commit('setSurveyResponse', { data: response.data[0], commit });
			} else {
				commit('setSurveyResponse', { ...response, commit });
			}
		},
		async createSurveyResponse({ commit }, { sId, token }) {
			const { response, error } = await PublicSurveyResponseService.post({
				sId, data: baseSurveyResponse, token,
			});
			if (error) {
				commit('setError', { error });
				return { error };
			}
			commit('setSurveyResponse', { ...response, commit });
			return { response };
		},
		updateSurveyResponse({ state, commit }, { sId, surveyResponse, token }) {
			if (!surveyResponse || !sId || !token) return;
			commit('updateSurveyResponse', { data: surveyResponse });
			commit('setIsSaved', false);
			state.debouncer({ sId, surveyResponse });
		},
		setSurveyResponse({ state, commit }, { id } = {}) {
			const data = state.surveyResponses.find(
				surveyResponses => surveyResponses.id === id,
			);
			if (!data) return;
			commit('setSurveyResponse', { data, commit });
		},
		resetError({ commit }) {
			commit('setError', { error: undefined });
		},
	},
};
