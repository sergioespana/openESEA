<template>
	<v-row justify="center" class="fill-height">
		<v-col
			cols="12" sm="10" md="8"
			lg="8" xl="6" class="fill-height"
		>
			<div class="d-flex justify-space-between mb-2">
				<h1 class="ma-0 text-h4">
					Stakeholder surveys
				</h1>
				<v-btn
					color="primary text-lowercase text-subtitle-1" depressed
					@click="addSurvey"
				>
					<span class="text-capitalize mr-1">Create</span> survey
				</v-btn>
			</div>
			<p class="ma-0 mb-8">
				select here which question indicators are for which stakeholders
			</p>

			<survey-form
				v-for="survey in surveys"
				v-show="survey.id > 0"
				:key="survey.id"
				:survey="survey"
				:items="items"
				:stakeholders="stakeholders"
				:errors="errors[survey.id]"
				class="mb-4"
				@input="saveSurvey"
				@deleteSurvey="removeSurvey"
			/>
		</v-col>
	</v-row>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex';
import getMethodItems from '@/utils/getMethodItems';
import SurveyForm from '@/components/forms/SurveyForm';

export default {
	components: {
		SurveyForm,
	},
	computed: {
		...mapState('organization', ['organization']),
		...mapState('method', ['method']),
		...mapState('survey', ['surveys', 'error', 'errors']),
		...mapGetters('topic', ['methodTopics', 'subTopics']),
		...mapGetters('question', ['topicQuestions']),
		items() {
			return getMethodItems(
				this.methodTopics,
				this.subTopics,
				this.topicQuestions,
				[],
			);
		},
		stakeholders() {
			return [
				'members',
				...this.surveys.map(survey => survey.stakeholder)
					.filter(stakeholder => stakeholder !== '' && stakeholder),
			];
		},
	},
	beforeRouteUpdate(to, from, next) {
		this.$route.params.id = to.params.id;
		this.initialize();
		next();
	},
	created() {
		this.initialize();
	},
	methods: {
		...mapActions('method', ['fetchMethod']),
		...mapActions('topic', ['fetchTopics']),
		...mapActions('question', ['fetchQuestions']),
		...mapActions('indirectIndicator', ['fetchIndirectIndicators']),
		...mapActions('survey', [
			'fetchSurveys', 'updateSurvey', 'addNewSurvey', 'deleteSurvey',
		]),
		async initialize() {
			const methodId = parseInt(this.$route.params.id, 10);
			if (this.method.id !== methodId) {
				const { error } = await this.fetchMethod({
					id: methodId,
					oId: this.organization.id,
				});
				if (error) {
					this.$router.push({ name: 'methods' });
				}
			}
			await this.fetchTopics({
				oId: this.organization.id,
				mId: this.method.id,
			});
			await this.fetchQuestions({
				oId: this.organization.id,
				mId: this.method.id,
			});
			await this.fetchIndirectIndicators({
				oId: this.organization.id,
				mId: this.method.id,
			});
			await this.fetchSurveys({
				oId: this.organization.id,
				mId: this.method.id,
			});
		},
		addSurvey() {
			this.addNewSurvey();
		},
		saveSurvey(survey) {
			this.updateSurvey({
				oId: this.organization.id,
				mId: this.method.id,
				survey,
			});
		},
		removeSurvey(id) {
			this.deleteSurvey({
				oId: this.organization.id,
				mId: this.method.id,
				id,
			});
		},
	},
};
</script>

<style lang="scss" module>
.card {
  border-radius: 8px !important; // important used to overwrite vuetify
  border-width: 2px !important; // important used to overwrite vuetify
	border-style: solid;
}

.content {
	overflow-y: auto;
}

.list {
	position: relative;
}

.toolbar {
	transition: all 0.5s ease 0s;
}

.divider {
	margin: 64px 0;
}
</style>
