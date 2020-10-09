import Vue from 'vue';
import Vuex from 'vuex';
import VuexPersist from 'vuex-persist';
import auth from './modules/auth';
import organization from './modules/organization';
import method from './modules/method/method';
import topic from './modules/method/topic';
import question from './modules/method/question';
import indirectIndicator from './modules/method/indirect_indicator';
import survey from './modules/method/survey';
import surveyResponse from './modules/method/survey/survey_response';
import surveyResponseCalculation from
	'./modules/method/survey/survey_response_calculations';
import surveyResults from './modules/method/survey/survey_results';

import publicSurvey from './modules/public/public_survey';
import publicSurveyResponse from './modules/public/public_survey_response';

const debug = process.env.NODE_ENV !== 'production';

Vue.use(Vuex);

const vuexLocalStorage = new VuexPersist({
	key: 'vuex',
	storage: window.localStorage,
	reducer: state => ({
		organization: state.organization,
		indirectIndicator: state.indirectIndicator,
		question: state.question,
		method: state.method,
		topic: state.topic,
		survey: state.survey,
		surveyResponse: state.surveyResponse,
		surveyResponseCalculation: state.surveyResponseCalculation,
		surveyResults: state.surveyResults,

		publicSurvey: state.publicSurvey,
		publicSurveyResponse: state.publicSurveyResponse,
	}),
});

export default new Vuex.Store({
	modules: {
		auth,
		organization,
		indirectIndicator,
		question,
		method,
		topic,
		survey,
		surveyResponse,
		surveyResponseCalculation,
		surveyResults,

		publicSurvey,
		publicSurveyResponse,
	},
	strict: debug,
	plugins: [vuexLocalStorage.plugin],
});
