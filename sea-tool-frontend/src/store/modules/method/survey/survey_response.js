import { debounce } from 'lodash';
import SurveyResponseService from '@/services/SurveyResponseService';

const baseSurveyResponse = {
	question_responses: [],
};

export default {
	namespaced: true,
	state: {
		surveyResponses: [],
		surveyResponse: {},
		error: undefined,
		debouncers: {},
		errors: {},
		isSaved: {},
	},
	getters: {
		getById: state => id => state.surveyResponses.find(
			object => object.id === id,
		),
	},
	mutations: {
		setSurveyResponses(state, { data }) {
			state.surveyResponses = data;
			state.debouncers = {};
			state.errors = {};
			state.isSaved = {};
		},
		setSurveyResponse(state, { data }) {
			state.surveyResponse = data || {};
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
		updateList(state, { id, data }) {
			if (id !== data.id) {
				delete state.debouncers[id];
				delete state.errors[id];
				delete state.isSaved[id];
			}

			state.surveyResponses = state.surveyResponses.map((item) => {
				if (item.id !== id) return item;
				return Object.assign(item, data);
			});
		},
		addSurveyResponse(state, { data: surveyResponse }) {
			state.surveyResponses.push(surveyResponse);
			state.surveyResponse = surveyResponse;
		},
		setDebouncer(state, { id, commit }) {
			state.debouncers[id] = debounce(
				async ({ oId, mId, sId, surveyResponse }) => {
					const { response, error } = await SurveyResponseService.put(
						{ oId, mId, sId, id, data: surveyResponse },
					);
					if (error) {
						commit('setError', { error, id: surveyResponse.id });
						return;
					}
					commit('setError', { error: {}, id: surveyResponse.id });
					commit('setIsSaved', { id: surveyResponse.id, isSaved: true });
					commit('updateList', {
						id: surveyResponse.id, data: { id: response.data.id },
					});
				},
				1000,
			);
		},
		setIsSaved(state, { id, isSaved = false }) {
			if (id) {
				state.isSaved = {
					...state.isSaved,
					[id]: isSaved,
				};
			}
		},
	},
	actions: {
		async fetchSurveyResponses({ commit }, payload) {
			const { response, error } = await SurveyResponseService.get(payload);
			if (error) {
				commit('setError', { error });
				return;
			}
			commit('setSurveyResponses', response);
		},
		async deleteSurveyResponse({ commit }, payload) {
			if (payload.id > 0) {
				const { error } = await SurveyResponseService.delete(payload);
				if (error) {
					commit('setError', { error });
					return;
				}
			}
			commit('deleteSurveyResponse', payload);
		},
		async createSurveyResponse({ commit }, { oId, mId, sId }) {
			const { response, error } = await SurveyResponseService.post({
				oId, mId, sId, data: baseSurveyResponse,
			});
			if (error) {
				commit('setError', { error });
				return { error };
			}
			commit('addSurveyResponse', response);
			commit('setSurveyResponse', response);
			return { response };
		},
		updateSurveyResponse({ state, commit }, { oId, mId, sId, surveyResponse }) {
			if (!surveyResponse || !oId || !mId || !sId) return;
			if (!state.debouncers[surveyResponse.id]) {
				commit('setDebouncer', { id: surveyResponse.id, commit });
			}
			commit('updateList', { id: surveyResponse.id, data: surveyResponse });
			commit('setIsSaved', { id: surveyResponse.id });
			state.debouncers[surveyResponse.id]({ oId, mId, sId, surveyResponse });
		},
		setSurveyResponse({ state, commit }, { id } = {}) {
			const data = state.surveyResponses.find(
				surveyResponses => surveyResponses.id === id,
			);
			if (!data) return;
			commit('setSurveyResponse', { data });
		},
		resetError({ commit }) {
			commit('setError', { error: undefined });
		},
	},
};
