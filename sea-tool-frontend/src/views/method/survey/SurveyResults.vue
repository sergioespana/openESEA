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
				<p class="mt-2 mb-0 gray--text">
					Respondents: {{ surveyResult.respondents }}
					of {{ surveyResult.all_respondents }}
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
					/>
					<survey-question-results
						v-for="question in topic.questions"
						:key="`question-${question.id}`"
						:question="question"
						:answers="answers[question.id]"
						readonly
						class="mt-6"
					/>
					<calculation-card
						v-for="calc in calculations[topic.id]"
						:key="`topic-${topic.id}-calc-${calc.id}`"
						:calculation="calc"
						class="mt-6"
					/>
					<template v-for="subTopic in topic.sub_topics">
						<topic-card
							:key="`subtopic-${subTopic.id}`"
							:name="subTopic.name"
							class="mt-6"
							is-sub-topic
						/>
						<survey-question-results
							v-for="question in subTopic.questions"
							:key="`question-${question.id}`"
							:question="question"
							:answers="answers[question.id]"
							readonly
							class="mt-6"
						/>
						<calculation-card
							v-for="calc in calculations[subTopic.id]"
							:key="`subtopic-${subTopic.id}-calc-${calc.id}`"
							:calculation="calc"
							class="mt-6"
						/>
					</template>
				</template>
			</v-col>
		</v-row>
	</v-row>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import SurveyQuestionResults from '@/components/survey/SurveyQuestionResults';
import TopicCard from '@/components/cards/TopicCard';
import CalculationCard from '@/components/cards/CalculationCard';

export default {
	components: {
		SurveyQuestionResults,
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
		...mapState('surveyResults', ['surveyResult']),
		answers() {
			return this.surveyResult.question_responses || {};
		},
		calculations() {
			const calculations = {};
			if (this.surveyResult?.calculations.length) {
				this.surveyResult.calculations.forEach((calculation) => {
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
		...mapActions('surveyResults', ['fetchSurveyResults']),
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

			this.fetchSurveyResults({
				oId: this.organization.id,
				mId: this.methodId,
				sId: surveyId,
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
