import apiCall from '@/utils/api';
import { API_URL } from '@/utils/Constants';

const createUrl = ({ id }) => {
	const base = `${API_URL}/surveys/`;
	return id ? `${base}${id}/` : base;
};

export default {
	get({ id }) {
		const url = createUrl({ id });
		return apiCall({ url });
	},
};
