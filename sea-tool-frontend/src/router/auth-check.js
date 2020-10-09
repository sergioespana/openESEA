import store from '@/store';

export default (to, from, next) => {
	if (to.matched.some(record => record.meta.guest)) {
		if (store.state.auth.jwt !== null) {
			next({ name: 'home' });
		} else {
			next();
		}
	} else {
		if (store.state.auth.jwt === null) {
			next({ name: 'login', params: { nextUrl: to.fullPath } });
		} else {
			next();
		}

		if (to.matched.some(record => record.meta.is_admin)) {
			const { user: admin } = store.state.auth;
			if (admin !== 1) {
				next({ name: 'home' });
			}
		}
	}
};
