import { API_URL } from '@/utils/Constants';
import BaseApiService from './BaseApiService';

const createUrl = ({ id }) => {
	const base = `${API_URL}/organizations/`;
	return id ? `${base}${id}/` : base;
};

export default new BaseApiService(createUrl);
