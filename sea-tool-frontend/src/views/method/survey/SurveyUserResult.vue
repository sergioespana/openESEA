<template>
	<v-row class="ma-0 pa-0">
		<v-row
			:class="$style['full-width']"
			class="pt-7" justify="center"
		>
			<v-col cols="6">
				<h1 class="text-h3 ma-0">
					{{ survey.name }}
				</h1>
				<p class="mt-4 mb-0">
					{{ survey.description }}
				</p>
			</v-col>
		</v-row>
		<v-row :class="$style['full-width']" justify="center" class="pb-7">
			<v-col cols="6" class="white rounded-lg px-4">
				<template v-for="(topic, index) in survey.topics">
					<topic-card
						:key="`topic-${topic.id}`"
						:name="topic.name"
						:class="index !== 0 ? 'mt-12' : ''"
						border-color="primary"
					/>
					<survey-question
						v-for="question in topic.questions"
						:key="`question-${question.id}`"
						:question="question"
						:answer="answers[question.id]"
						readonly
						class="mt-6"
					/>
					<calculation-card
						v-for="calc in calculations[topic.id]"
						:key="`topic-${topic.id}-calc-${calc.id}`"
						:calculation="calc"
						class="mt-6"
						border-color="primary"
					/>
					<template v-for="subTopic in topic.sub_topics">
						<topic-card
							:key="`subtopic-${subTopic.id}`"
							:name="subTopic.name"
							class="mt-6"
							border-color="primary"
							is-sub-topic
						/>
						<survey-question
							v-for="question in subTopic.questions"
							:key="`question-${question.id}`"
							:question="question"
							:answer="answers[question.id]"
							readonly
							class="mt-6"
						/>
						<calculation-card
							v-for="calc in calculations[subTopic.id]"
							:key="`subtopic-${subTopic.id}-calc-${calc.id}`"
							:calculation="calc"
							class="mt-6"
							border-color="primary"
						/>
					</template>
				</template>
			</v-col>
		</v-row>
	</v-row>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import SurveyQuestion from '@/components/survey/SurveyQuestion';
import TopicCard from '@/components/cards/TopicCard';
import CalculationCard from '@/components/cards/CalculationCard';

export default {
	components: {
		SurveyQuestion,
		TopicCard,
		CalculationCard,
	},
	data() {
		return {
			topicNumber: 0,
		};
	},
	computed: {
		...mapState('organization', ['organization']),
		...mapState('survey', ['survey']),
		...mapState('surveyResponse', ['surveyResponses', 'surveyResponse']),
		...mapState('surveyResponseCalculation', ['surveyResponseCalculations']),
		answers() {
			const answers = {};
			if (this.surveyResponse && this.surveyResponse.question_responses) {
				this.surveyResponse.question_responses.forEach((answer) => {
					answers[answer.direct_indicator_id] = answer.value;
				});
			}
			return answers;
		},
		calculations() {
			const calculations = {};
			if (this.surveyResponseCalculations.length) {
				this.surveyResponseCalculations.forEach((calculation) => {
					calculations[calculation.topic] = !calculations[calculation.topic]
						? [calculation] : [...calculations[calculation.topic], calculation];
				});
			}
			return calculations;
		},
		methodId() {
			return parseInt(this.$route.params.id, 10);
		},
	},
	beforeRouteUpdate(to, from, next) {
		this.initialize();
		next();
	},
	created() {
		this.initialize();
	},
	methods: {
		...mapActions('survey', ['fetchSurvey']),
		...mapActions('surveyResponse', [
			'fetchSurveyResponses', 'setSurveyResponse',
		]),
		...mapActions('surveyResponseCalculation', [
			'fetchSurveyResponseCalculations',
		]),
		async initialize() {
			const surveyId = parseInt(this.$route.params.surveyId, 10);
			await this.fetchSurvey({
				oId: this.organization.id,
				mId: this.methodId,
				id: surveyId,
			});

			if (this.survey.method !== this.methodId) {
				this.$router.push({ name: 'methods' });
			}

			await this.fetchSurveyResponses({
				oId: this.organization.id,
				mId: this.methodId,
				sId: surveyId,
			});
			this.setSurveyResponse(this.surveyResponses[0]);

			await this.fetchSurveyResponseCalculations({
				oId: this.organization.id,
				mId: this.methodId,
				sId: surveyId,
				id: this.surveyResponse.id,
			});
		},
	},
};
</script>

<style lang="scss" module>
.full-width {
	width: 100%;
}
</style>
