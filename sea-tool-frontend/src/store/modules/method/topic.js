import { debounce, random } from 'lodash';
import TopicService from '@/services/TopicService';

const baseTopic = { name: '', description: '' };

export default {
	namespaced: true,
	state: {
		topics: [],
		topic: {},
		error: undefined,
		debouncers: {},
		errors: {},
		isSaved: {},
	},
	getters: {
		getById: state => id => state.topics.filter(object => object.id === id),
		getErrorById: state => id => state.errors[id],
		methodTopics: state => state.topics.filter(topic => !topic.parent_topic),
		subTopics: (state) => {
			const subTopics = state.topics.filter(topic => topic.parent_topic);
			const filtered = {};
			subTopics.forEach((subTopic) => {
				if (!filtered[subTopic.parent_topic]) {
					filtered[subTopic.parent_topic] = [];
				}
				filtered[subTopic.parent_topic] = [
					...filtered[subTopic.parent_topic],
					subTopic,
				];
			});
			return filtered;
		},
	},
	mutations: {
		setTopics(state, { data }) {
			state.topics = data;
			state.debouncers = {};
			state.errors = {};
			state.isSaved = {};
		},
		setTopic(state, { data }) {
			state.topic = data || {};
		},
		deleteTopic(state, { id }) {
			delete state.debouncers[id];
			delete state.errors[id];
			delete state.isSaved[id];
			state.topics = state.topics.filter(o => o.id !== id);
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

			state.topics = state.topics.map((item) => {
				if (item.id !== id) return item;
				return Object.assign(item, data);
			});
		},
		addNewTopic(state, { parent } = {}) {
			const topic = { ...baseTopic, id: random(-1000000, -1) };
			topic.parent_topic = parent;
			state.topics.push(topic);
			state.topic = topic;
		},
		setDebouncer(state, { id, commit }) {
			state.debouncers[id] = debounce(
				async ({ oId, mId, topic }) => {
					const method = topic.id > 0 ? 'put' : 'post';
					const { response, error } = await TopicService[method](
						{ oId, mId, id, data: topic },
					);
					if (error) {
						commit('setError', { error, id: topic.id });
						return;
					}
					commit('setError', { error: {}, id: topic.id });
					commit('setIsSaved', { id: topic.id, isSaved: true });
					commit('updateList', { id: topic.id, data: response.data });
				},
				1000,
			);
		},
		resetTopics(state) {
			state.topics = [];
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
		async fetchTopics({ commit }, payload) {
			const { response, error } = await TopicService.get(payload);
			if (error) {
				commit('setError', { error });
				return;
			}
			commit('setTopics', response);
		},
		async deleteTopic({ commit }, payload) {
			if (payload.id > 0) {
				const { error } = await TopicService.delete(payload);
				if (error) {
					commit('setError', { error });
					return;
				}
			}
			commit('deleteTopic', payload);
		},
		updateTopic({ state, commit }, { oId, mId, topic }) {
			if (!topic || !oId || !mId) return;
			if (!state.debouncers[topic.id]) {
				commit('setDebouncer', { id: topic.id, commit });
			}
			commit('setIsSaved', { id: topic.id });
			if (!topic.name) return;
			state.debouncers[topic.id]({ oId, mId, topic });
		},
		setTopic({ state, commit }, { id } = {}) {
			const data = state.topics.find(topic => topic.id === id);
			if (data && data.id === state.topic.id) return;
			commit('setTopic', { data });
		},
		resetError({ commit }) {
			commit('setError', { error: undefined });
		},
		addNewTopic({ commit }, payload) {
			commit('addNewTopic', payload);
		},
		resetTopics({ commit }) {
			commit('resetTopics');
		},
	},
};
