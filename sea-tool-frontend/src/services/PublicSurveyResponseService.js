import apiCall from '@/utils/api';
import { API_URL } from '@/utils/Constants';

const createUrl = ({ sId, id, token }) => {
	let base = `${API_URL}/surveys/${sId}/responses/`;
	base = id ? `${base}${id}/` : base;
	return token ? `${base}?token=${token}` : base;
};

export default {
	get({ sId, id, token }) {
		const url = createUrl({ sId, id, token });
		return apiCall({ url });
	},
	post({ sId, data, token }) {
		const url = createUrl({ sId, token });
		return apiCall({ method: 'post', url, data });
	},
	put({ sId, id, data, token }) {
		const url = createUrl({ sId, id, token });
		return apiCall({ method: 'put', url, data });
	},
	delete({ sId, id, token }) {
		const url = createUrl({ sId, id, token });
		return apiCall({ method: 'delete', url });
	},
};
