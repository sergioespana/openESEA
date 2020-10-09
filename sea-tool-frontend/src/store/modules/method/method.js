import { debounce } from 'lodash';
import MethodService from '@/services/MethodService';

const baseMethod = { name: 'Untitled method', description: '...' };

export default {
	namespaced: true,
	state: {
		methods: [],
		method: { ...baseMethod },
		error: undefined,
		debouncer: debounce(
			async ({ id, oId, data, commit }) => {
				const { response, error } = await MethodService.put({
					id, oId, data,
				});
				if (error) {
					commit('setError', { error });
				} else {
					commit('updateMethodInList', { ...response, id });
					commit('setMethod', response);
				}
			}, 1000,
		),
	},
	mutations: {
		setMethods(state, { data }) {
			state.methods = data;
		},
		setMethod(state, { data }) {
			state.method = { ...data } || baseMethod;
		},
		updateMethod(state, data) {
			state.method = { ...state.method, ...data };
		},
		updateMethodInList(state, { id, data }) {
			state.methods = state.methods.map((item) => {
				if (item.id !== id) return item;
				return { ...item, ...data };
			});
		},
		addMethodInList(state, { data }) {
			state.methods.push(data);
		},
		deleteMethod(state, { id }) {
			state.methods = state.methods.filter(o => o.id !== id);
		},
		resetMethod(state) {
			state.method = { ...baseMethod };
		},
		setError(state, { error }) {
			state.error = error;
		},
	},
	actions: {
		async fetchMethods({ commit }, payload) {
			const { response, error } = await MethodService.get(payload);
			if (error) {
				commit('setError', { error });
				return;
			}
			commit('setMethods', response);
		},
		async fetchMethod({ commit }, payload) {
			const { response, error } = await MethodService.get(payload);
			if (error) {
				commit('setError', { error });
				return { error };
			}
			commit('addMethodInList', response);
			commit('setMethod', response);
			return { response };
		},
		async createMethod({ state, commit }, { oId }) {
			const { response, error } = await MethodService.post({
				oId, data: state.method,
			});
			if (error) {
				commit('setError', { error });
				return { error };
			}
			commit('addMethodInList', response);
			commit('setMethod', response);
			return { response };
		},
		async updateMethod({ state, commit }, payload) {
			const { id, organization: oId } = payload;
			state.debouncer({ id, oId, data: payload, commit });
		},
		async deleteMethod({ commit, dispatch }, payload) {
			const { response, error } = await MethodService.delete(payload);
			if (error) {
				commit('setError', { error });
				return { error };
			}
			commit('deleteMethod', payload);
			dispatch('setMethod', {});
			return { response };
		},
		saveMethod({ state, dispatch }, payload) {
			const action = state.method.id ? 'updateMethod'
				: 'createMethod';
			return dispatch(action, payload);
		},
		setMethod({ state, commit }, { id }) {
			let data = state.methods.find(m => m.id === id);
			if (!data) {
				[data] = state.methods;
			}
			commit('setMethod', { data });
		},
		updateMethodData({ commit }, payload) {
			commit('updateMethod', payload);
		},
		resetMethod({ commit }) {
			commit('resetMethod');
		},
		resetError({ commit }) {
			commit('setError', { error: undefined });
		},
	},
};
