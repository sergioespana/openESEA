import store from '@/store';
import { API_URL } from '@/utils/Constants';

export default [
	(config) => {
		if (
			config.url.startsWith(API_URL)
			&& !(config.url.includes('register') || config.url.includes('token'))
		) {
			// eslint-disable-next-line no-param-reassign
			config.headers.Authorization = `Bearer ${store.state.auth.jwt}`;
		}
		return config;
	},
	error => Promise.reject(error),
];
