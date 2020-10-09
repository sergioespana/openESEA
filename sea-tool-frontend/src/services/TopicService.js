import { API_URL } from '@/utils/Constants';
import BaseApiService from './BaseApiService';

const createUrl = ({ id, oId, mId }) => {
	const base = `${API_URL}/organizations/${oId}/methods/${mId}/topics/`;
	return id ? `${base}${id}/` : base;
};

export default new BaseApiService(createUrl);
