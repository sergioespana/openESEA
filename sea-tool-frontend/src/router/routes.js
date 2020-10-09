import Home from '@/views/Home';
import Login from '@/views/account/Login';
import Register from '@/views/account/Register';
import Details from '@/views/account/Details';
import MethodList from '@/views/method/MethodList';
import CreateMethod from '@/views/method/CreateMethod';
import DesignMethod from '@/views/method/DesignMethod';
import SurveyMethod from '@/views/method/SurveyMethod';
import SurveyList from '@/views/method/survey/SurveyList';
import SurveyResponse from '@/views/method/survey/SurveyResponse';
import SurveyUserResult from '@/views/method/survey/SurveyUserResult';
import SurveyResults from '@/views/method/survey/SurveyResults';

import PublicSurveyList from '@/views/public/PublicSurveyList';
import PublicSurveyResponse from '@/views/public/PublicSurveyResponse';
import PublicThanksPage from '@/views/public/PublicThanksPage';

import MethodHeader from '@/components/method/MethodHeader';
import MethodTreeSidebar from '@/components/method/MethodTreeSidebar';
import SurveyHeader from '@/components/survey/SurveyHeader';

const routes = [
	{
		path: '/login',
		name: 'login',
		component: Login,
		meta: {
			guest: true,
			noHeader: true,
		},
	},
	{
		path: '/register',
		name: 'register',
		component: Register,
		meta: {
			guest: true,
			noHeader: true,
		},
	},
	{
		path: '/surveys',
		name: 'surveys',
		component: PublicSurveyList,
		meta: {
			guest: true,
			noHeader: true,
		},
	},
	{
		path: '/surveys/:surveyId',
		name: 'survey-fill',
		component: PublicSurveyResponse,
		meta: {
			guest: true,
			noHeader: true,
		},
	},
	{
		path: '/surveys/:surveyId/thank-you',
		name: 'survey-thanks',
		component: PublicThanksPage,
		meta: {
			guest: true,
			noHeader: true,
		},
	},
	{
		path: '/home',
		name: 'home',
		component: Home,
	},
	{
		path: '/account-details',
		name: 'account-details',
		component: Details,
	},
	{
		path: '/methods',
		name: 'methods',
		component: MethodList,
	},
	{
		path: '/methods/create',
		name: 'method-create',
		component: CreateMethod,
		meta: {
			header: MethodHeader,
		},
	},
	{
		path: '/methods/:id/design',
		name: 'method-design',
		component: DesignMethod,
		meta: {
			header: MethodHeader,
			sidebar: MethodTreeSidebar,
		},
	},
	{
		path: '/methods/:id/surveys-builder',
		name: 'method-surveys-builder',
		component: SurveyMethod,
		meta: {
			header: MethodHeader,
		},
	},
	{
		path: '/methods/:id/surveys',
		name: 'method-surveys',
		component: SurveyList,
	},
	{
		path: '/methods/:id/surveys/:surveyId',
		name: 'method-survey-fill',
		component: SurveyResponse,
		meta: {
			header: SurveyHeader,
		},
	},
	{
		path: '/methods/:id/surveys/:surveyId/result',
		name: 'method-survey-result',
		component: SurveyUserResult,
		meta: {
			header: SurveyHeader,
		},
	},
	{
		path: '/methods/:id/surveys/:surveyId/results',
		name: 'method-survey-results',
		component: SurveyResults,
		meta: {
			header: SurveyHeader,
		},
	},
];

export default routes;
