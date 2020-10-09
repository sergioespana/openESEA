import store from '@/store';
import router from '@/router';
import { API_URL } from '@/utils/Constants';

export default [
	response => response,
	(error) => {
		if (
			error.response && error.response.status === 401
			&& store.state.auth.jwt
			&& error.config.url.startsWith(API_URL)
		) {
			store.dispatch('auth/removeToken');

			router.push({
				name: 'login',
				params: { nextUrl: router.currentRoute.fullPath },
			});
		}
		throw error;
	},
];
