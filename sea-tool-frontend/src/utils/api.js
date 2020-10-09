import Vue from 'vue';

// TODO: API service needs to be cleaned and will be done in another story...
export default async ({ method = 'get', url, data }) => {
	try {
		const response = await Vue.axios[method](url, data);
		return { response };
	} catch (error) {
		return { error };
	}
};
