import { API_URL } from '@/utils/Constants';
import BaseApiService from './BaseApiService';

const createUrl = ({
	oId, mId, sId, id, query = '',
}) => {
	let base = `${API_URL}/organizations/${oId}/methods/${
		mId}/surveys/${sId}/responses`;
	base = id ? `${base}/${id}` : base;
	return `${base}/${query}`;
};

export default new BaseApiService(createUrl);
