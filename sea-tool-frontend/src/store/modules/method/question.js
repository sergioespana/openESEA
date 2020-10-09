import { random, debounce, isInteger } from 'lodash';
import QuestionService from '@/services/QuestionService';

const baseQuestion = {
	key: '',
	name: '',
	prefix: '',
	default: '',
	suffix: '',
	type: 'NUMBER',
	options: [],
};

export default {
	namespaced: true,
	state: {
		questions: [],
		question: {},
		error: undefined,
		debouncers: {},
		errors: {},
		isSaved: {},
	},
	getters: {
		getById: state => id => state.questions.find(object => object.id === id),
		topicQuestions: (state) => {
			const filtered = {};
			state.questions.forEach((question) => {
				filtered[question.topic] = !filtered[question.topic]
					? [question] : [...filtered[question.topic], question];
			});
			return filtered;
		},
		getValidQuestionKeyNumber: (state) => {
			const indicators = state.questions
				.map(indicator => parseInt(indicator.key.match(/[^_]*$/), 10))
				.filter(indicator => isInteger(indicator));
			return indicators.length ? Math.max(...indicators) + 1 : 1;
		},
	},
	mutations: {
		setQuestions(state, { data }) {
			state.questions = data;
			state.debouncers = {};
			state.errors = {};
			state.isSaved = {};
		},
		setQuestion(state, { data }) {
			state.question = data || {};
		},
		deleteQuestion(state, { id }) {
			delete state.debouncers[id];
			delete state.errors[id];
			delete state.isSaved[id];
			state.questions = state.questions.filter(q => q.id !== id);
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

			state.questions = state.questions.map((item) => {
				if (item.id !== id) return item;
				return Object.assign(item, data);
			});
		},
		addNewQuestion(state, { topic }) {
			const question = { ...baseQuestion, id: random(-1000000, -1), topic };
			state.questions.push(question);
			state.question = question;
		},
		setDebouncer(state, { id, commit }) {
			state.debouncers[id] = debounce(
				async ({ oId, mId, question }) => {
					const method = question.id > 0 ? 'put' : 'post';
					const { response, error } = await QuestionService[method](
						{ oId, mId, id, data: question },
					);
					if (error) {
						commit('setError', { error, id: question.id });
						return;
					}
					commit('setError', { error: {}, id: question.id });
					commit('setIsSaved', { id: question.id, isSaved: true });
					commit('updateList', { id: question.id, data: response.data });
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
		async fetchQuestions({ commit }, payload) {
			const { response, error } = await QuestionService.get(payload);
			if (error) {
				commit('setError', { error });
				return;
			}
			commit('setQuestions', response);
		},
		async deleteQuestion({ commit }, payload) {
			if (payload.id > 0) {
				const { error } = await QuestionService.delete(payload);
				if (error) {
					commit('setError', { error });
					return;
				}
			}
			commit('deleteQuestion', payload);
		},
		updateQuestion({ state, commit }, { oId, mId, question }) {
			if (!question || !oId || !mId) return;
			if (!state.debouncers[question.id]) {
				commit('setDebouncer', { id: question.id, commit });
			}
			if (question.id < 0) {
				commit('updateList', { id: question.id, data: question });
			}
			commit('setIsSaved', { id: question.id });
			if (!question.name || !question.key) return;
			state.debouncers[question.id]({ oId, mId, question });
		},
		setQuestion({ state, commit }, { id } = {}) {
			const data = state.questions.find(questions => questions.id === id);
			if (data && data.id === state.question.id) return;
			commit('setQuestion', { data });
		},
		resetError({ commit }) {
			commit('setError', { error: undefined });
		},
		addNewQuestion({ commit }, payload) {
			commit('addNewQuestion', payload);
		},
	},
};
