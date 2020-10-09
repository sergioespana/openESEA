import { API_URL } from '@/utils/Constants';
import BaseApiService from './BaseApiService';

const createUrl = ({ oId, mId, id }) => {
	const base = `${API_URL}/organizations/${oId}/methods/${mId}/questions/`;
	return id ? `${base}${id}/` : base;
};

export default new BaseApiService(createUrl);
