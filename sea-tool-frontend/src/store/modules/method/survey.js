import { random, debounce } from 'lodash';
import SurveyService from '@/services/SurveyService';

const baseSurvey = {
	name: '',
	description: '',
	stakeholder: '',
	rate: 0,
	questions: [],
	anonymous: false,
};

export default {
	namespaced: true,
	state: {
		surveys: [],
		survey: {},
		error: undefined,
		debouncers: {},
		errors: {},
		isSaved: {},
	},
	getters: {
		getById: state => id => state.surveys.find(object => object.id === id),
	},
	mutations: {
		setSurveys(state, { data }) {
			state.surveys = data;
			state.debouncers = {};
			state.errors = {};
			state.isSaved = {};
			state.error = undefined;
		},
		setSurvey(state, { data }) {
			state.survey = data || {};
		},
		deleteSurvey(state, { id }) {
			delete state.debouncers[id];
			delete state.errors[id];
			delete state.isSaved[id];
			state.surveys = state.surveys.filter(q => q.id !== id);
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
		updateList(state, { id, data }) {
			if (id !== data.id) {
				delete state.debouncers[id];
				delete state.errors[id];
				delete state.isSaved[id];
			}

			state.surveys = state.surveys.map((item) => {
				if (item.id !== id) return item;
				return Object.assign(item, data);
			});
		},
		addNewSurvey(state) {
			const survey = { ...baseSurvey, id: random(-1000000, -1) };
			state.surveys.push(survey);
		},
		setIsSaved(state, { id, isSaved = false }) {
			if (id) {
				state.isSaved = {
					...state.isSaved,
					[id]: isSaved,
				};
			}
		},
		setDebouncer(state, { id, commit }) {
			state.debouncers[id] = debounce(
				async ({ oId, mId, survey }) => {
					const method = survey.id > 0 ? 'put' : 'post';
					const { response, error } = await SurveyService[method](
						{ oId, mId, id, data: survey },
					);
					if (error) {
						commit('setError', { error, id: survey.id });
						return;
					}
					commit('setError', { error: {}, id: survey.id });
					commit('setIsSaved', { id: survey.id, isSaved: true });
					commit('updateList', { id: survey.id, data: response.data });
				},
				1000,
			);
		},
	},
	actions: {
		async fetchSurveys({ commit }, payload) {
			const { response, error } = await SurveyService.get(payload);
			if (error) {
				commit('setError', { error });
				return;
			}
			commit('setSurveys', response);
		},
		async fetchSurvey({ commit }, payload) {
			const { response, error } = await SurveyService.get(payload);
			if (error) {
				commit('setError', { error });
				return { error };
			}
			commit('updateList', response);
			commit('setSurvey', response);
			return { response };
		},
		async deleteSurvey({ commit }, payload) {
			if (payload.id > 0) {
				const { error } = await SurveyService.delete(payload);
				if (error) {
					commit('setError', { error });
					return;
				}
			}
			commit('deleteSurvey', payload);
		},
		updateSurvey({ state, commit }, { oId, mId, survey }) {
			if (!survey || !oId || !mId) return;
			if (!state.debouncers[survey.id]) {
				commit('setDebouncer', { id: survey.id, commit });
			}
			commit('setIsSaved', { id: survey.id });
			if (!survey.name && state.isSaved[survey.id]) return;
			state.debouncers[survey.id]({ oId, mId, survey });
		},
		setSurvey({ state, commit }, { id } = {}) {
			const data = state.surveys.find(surveys => surveys.id === id);
			if (data && data.id === state.survey.id) return;
			commit('setSurvey', { data });
		},
		resetError({ commit }) {
			commit('setError', { error: undefined });
		},
		addNewSurvey({ commit }) {
			commit('addNewSurvey');
		},
	},
};
