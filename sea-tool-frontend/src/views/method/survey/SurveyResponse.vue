<template>
	<v-row v-if="survey.id === surveyId" class="ma-0 pa-0">
		<v-row
			:class="$style['full-width']"
			class="green lighten-5 py-7"
			justify="center"
		>
			<v-col cols="6">
				<h1 class="text-h3 ma-0">
					{{ survey.name }}
				</h1>
				<p class="mt-4">
					{{ survey.description }}
				</p>
			</v-col>
		</v-row>
		<v-row :class="$style['full-width']" justify="center">
			<v-col cols="6" class="white rounded-lg mt-n5 px-4">
				<v-row justify="space-between" dense>
					<v-col>Topic {{ topicNumber + 1 }} of {{ totalTopics }}</v-col>
					<v-col cols="4" class="my-auto">
						<v-progress-linear :value="surveyProgress" rounded color="green" />
					</v-col>
				</v-row>
				<v-row dense class="mb-2">
					<v-col class="text-h5">
						{{ currentTopic.name }}
					</v-col>
				</v-row>

				<v-form ref="form">
					<survey-question
						v-for="question in currentTopic.questions"
						:key="`question-${question.id}`"
						:question="question"
						:answer="answers[question.id]"
						class="mt-6"
						@input="updateAnswer(question.id, $event)"
					/>
					<template v-for="subTopic in currentTopic.sub_topics">
						<topic-card
							:key="`topic-${subTopic.id}`"
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
							class="mt-6"
							@input="updateAnswer(question.id, $event)"
						/>
					</template>
				</v-form>
				<v-row justify="space-between" class="mt-3">
					<v-col cols="auto">
						<v-btn
							:disabled="topicNumber === 0"
							color="primary"
							class="text-capitalize text-subtitle-1"
							@click="previousTopic"
						>
							Previous topic
						</v-btn>
					</v-col>
					<v-col cols="auto">
						<v-btn
							v-if="topicNumber + 1 < totalTopics"
							color="primary" class="text-capitalize text-subtitle-1"
							@click="nextTopic"
						>
							Next topic
						</v-btn>
						<v-btn
							v-else color="primary" class="text-capitalize text-subtitle-1"
							@click="finish"
						>
							Finish
						</v-btn>
					</v-col>
				</v-row>
			</v-col>
		</v-row>
	</v-row>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import SurveyQuestion from '@/components/survey/SurveyQuestion';
import TopicCard from '@/components/cards/TopicCard';

export default {
	components: {
		SurveyQuestion,
		TopicCard,
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
		surveyProgress() {
			return (this.totalTopics / 100) * (this.topicNumber + 1);
		},
		currentTopic() {
			return this.survey?.topics[this.topicNumber];
		},
		totalTopics() {
			return this.survey?.topics.length || 0;
		},
		answers() {
			const answers = {};
			if (
				this.surveyResponse?.id !== this.surveyId
				&& this.surveyResponse.question_responses
			) {
				this.surveyResponse.question_responses.forEach((answer) => {
					answers[answer.direct_indicator_id] = answer.value;
				});
			}
			return answers;
		},
		methodId() {
			return parseInt(this.$route.params.id, 10);
		},
		surveyId() {
			return parseInt(this.$route.params.surveyId, 10);
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
		...mapActions('method', ['fetchMethod']),
		...mapActions('survey', ['fetchSurvey']),
		...mapActions('surveyResponse', [
			'fetchSurveyResponses',
			'setSurveyResponse',
			'updateSurveyResponse',
			'createSurveyResponse',
		]),
		async initialize() {
			await this.fetchSurvey({
				oId: this.organization.id,
				mId: this.methodId,
				id: this.surveyId,
			});

			if (this.survey.method !== this.methodId) {
				this.$router.push({ name: 'methods' });
			}

			await this.fetchSurveyResponses({
				oId: this.organization.id,
				mId: this.methodId,
				sId: this.surveyId,
			});
			if (this.surveyResponses.length) {
				this.setSurveyResponse(this.surveyResponses[0]);
				return;
			}

			this.createSurveyResponse({
				oId: this.organization.id,
				mId: this.methodId,
				sId: this.surveyId,
			});
		},
		updateAnswer(id, answer) {
			this.updateSurveyResponse({
				oId: this.organization.id,
				mId: this.methodId,
				sId: this.survey.id,
				surveyResponse: {
					...this.surveyResponse,
					question_responses: [
						...this.surveyResponse.question_responses,
						{ direct_indicator_id: id, value: answer },
					],
				},
			});
		},
		nextTopic() {
			if (!this.$refs.form.validate()) {
				return;
			}
			this.topicNumber += 1;
		},
		previousTopic() {
			if (this.topicNumber > 0) {
				this.topicNumber -= 1;
			}
		},
		finish() {
			this.updateSurveyResponse({
				oId: this.organization.id,
				mId: this.methodId,
				sId: this.survey.id,
				surveyResponse: {
					...this.surveyResponse,
					finished: true,
				},
			});
			this.$router.push({
				name: 'method-survey-result',
				params: { id: this.methodId, surveyId: this.survey.id },
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
