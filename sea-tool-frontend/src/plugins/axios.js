import Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import requestAuthInterceptor from '@/utils/requestAuthInterceptor';
import responseAuthInterceptor from '@/utils/responseAuthInterceptor';

// Full config:  https://github.com/axios/axios#request-config
// axios.defaults.baseURL = process.env.baseURL || process.env.apiUrl ||
// axios.defaults.headers.common['Authorization'] = AUTH_TOKEN;
// axios.defaults.headers.post['Content-Type'] =
// 'application/x-www-form-urlencoded';

const config = {
	// baseURL: process.env.baseURL || process.env.apiUrl || ""
	// timeout: 60 * 1000, // Timeout
	// withCredentials: true, // Check cross-site Access-Control
};

const axioInstance = axios.create(config);

axioInstance.interceptors.request.use(
	...requestAuthInterceptor,
);

// Add a response interceptor
axioInstance.interceptors.response.use(
	...responseAuthInterceptor,
);

Vue.use(VueAxios, axioInstance);

export default axioInstance;
