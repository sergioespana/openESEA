import Vue from 'vue';
import VueRouter from 'vue-router';
import AuthCheck from './auth-check';
import routes from './routes';

Vue.use(VueRouter);

const router = new VueRouter({
	routes,
});

router.beforeEach(AuthCheck);

export default router;
