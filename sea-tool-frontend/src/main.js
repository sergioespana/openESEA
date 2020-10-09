import Vue from 'vue';
import './plugins/axios';
import './plugins/vuelidate';
import App from '@/App';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false;
Vue.prototype.$config = process.env;

new Vue({
	router,
	store,
	vuetify,
	render: h => h(App),
}).$mount('#app');
