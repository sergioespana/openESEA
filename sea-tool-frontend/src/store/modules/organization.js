import OrganizationService from '@/services/OrganizationService';
import { getRequestData } from '@/utils/helpers';
import { MEDIA_URL } from '@/utils/Constants';

const baseOrganization = {
	name: '',
	description: '',
	image: `${MEDIA_URL}/organization/default.png`,
};

export default {
	namespaced: true,
	state: {
		organizations: [],
		organization: {},
		form: { ...baseOrganization },
		isCreateFormOpen: false,
		isUpdateFormOpen: false,
	},
	mutations: {
		setOrganizations(state, { data }) {
			state.organizations = data;
		},
		setOrganization(state, { data }) {
			state.organization = data || {};
		},
		updateOrganization(state, { id, data }) {
			state.organizations = state.organizations.map((item) => {
				if (item.id !== id) return item;
				return { ...item, ...data };
			});
		},
		setError(state, { error }) {
			state.error = error;
		},
		addOrganizationInList(state, { data }) {
			state.organizations.push(data);
		},
		deleteOrganization(state, { id }) {
			state.organizations = state.organizations.filter(o => o.id !== id);
		},
		updateOrganizationForm(state, data) {
			state.form = { ...state.form, ...data };
		},
		resetOrganizationForm(state) {
			state.form = { ...baseOrganization };
			state.isCreateFormOpen = false;
			state.isUpdateFormOpen = false;
		},
		changeIsCreateFormOpen(state, data) {
			state.isCreateFormOpen = data;
		},
		changeIsUpdateFormOpen(state, data) {
			state.isUpdateFormOpen = data;
		},
		copyOrganizationToForm(state) {
			state.form = { ...state.organization };
		},
	},
	actions: {
		async fetchOrganizations({ commit }, payload) {
			const { response, error } = await OrganizationService.get(payload);
			if (error) {
				commit('setError', { error });
				return;
			}
			commit('setOrganizations', response);
		},
		async createOrganization({ state, commit }) {
			const data = getRequestData(state.form);
			const { response, error } = await OrganizationService.post({
				data,
				headers: { 'Content-Type': 'multipart/form-data' },
			});
			if (error) {
				commit('setError', { error });
				return;
			}
			commit('addOrganizationInList', response);
			commit('setOrganization', response);
			commit('resetOrganizationForm');
		},
		async updateOrganization({ state, commit }) {
			const { id } = state.form;
			const data = getRequestData(state.form);
			const { response, error } = await OrganizationService.put({
				id,
				data,
				headers: { 'Content-Type': 'multipart/form-data' },
			});
			if (error) {
				commit('setError', { error });
				return;
			}
			commit('updateOrganization', { ...response, id });
			commit('setOrganization', response);
			commit('resetOrganizationForm');
		},
		saveOrganization({ state, dispatch }) {
			const action = state.form.id ? 'updateOrganization'
				: 'createOrganization';
			dispatch(action);
		},
		async deleteOrganization({ commit, dispatch }, payload) {
			const { error } = await OrganizationService.delete(payload);
			if (error) {
				commit('setError', { error });
				return;
			}
			commit('deleteOrganization', payload);
			dispatch('setOrganization', {});
			commit('resetOrganizationForm');
		},
		setOrganization({ state, commit }, { id }) {
			let data = state.organizations.find(o => o.id === id);
			if (!data) {
				[data] = state.organizations;
			}
			commit('setOrganization', { data });
		},
		resetError({ commit }) {
			commit('setError', { error: undefined });
		},
		updateOrganizationForm({ commit }, payload) {
			commit('updateOrganizationForm', payload);
		},
		resetOrganizationForm({ commit }) {
			commit('resetOrganizationForm');
		},
		changeIsCreateFormOpen({ commit }, payload) {
			commit('changeIsCreateFormOpen', payload);
		},
		changeIsUpdateFormOpen({ commit }, payload) {
			commit('changeIsUpdateFormOpen', payload);
			if (payload) {
				commit('copyOrganizationToForm');
			}
		},
	},
};
