import axios from 'axios';
import { STATUS, API_URL } from '@/utils/Constants';

const obtainJWT = `${API_URL}/auth/token`;

export default {
	namespaced: true,
	state: {
		jwt: localStorage.getItem('sea-token') || null,
		status: STATUS.IDLE,
		user: {},
		hasLoadedOnce: false,
	},
	mutations: {
		updateToken(state, { token, user }) {
			state.status = STATUS.SUCCESS;
			state.jwt = token;
			state.hasLoadedOnce = true;
			state.user = user;
		},
		loading(state) {
			state.status = STATUS.LOADING;
		},
		error(state) {
			state.status = STATUS.ERROR;
			state.hasLoadedOnce = true;
		},
		logout(state) {
			state.jwt = null;
			state.status = STATUS.IDLE;
			state.user = {};
		},
	},
	actions: {
		obtainToken({ commit }, userCredentials) {
			return new Promise((resolve, reject) => {
				commit('loading');
				axios.post(obtainJWT, userCredentials)
					.then((response) => {
						const { token, user } = response.data;
						localStorage.setItem('sea-token', token);
						commit('updateToken', { token, user });
						resolve(response);
					})
					.catch((err) => {
						commit('error');
						localStorage.removeItem('sea-token');
						reject(err);
					});
			});
		},
		setToken({ commit }, payload) {
			commit('updateToken', payload);
		},
		removeToken({ commit }) {
			return new Promise((resolve) => {
				commit('logout');
				localStorage.removeItem('sea-token');
				resolve();
			});
		},
	},
};
