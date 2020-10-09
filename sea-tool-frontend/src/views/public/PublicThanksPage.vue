<template>
	<v-row class="fill-height ma-0 pa-0">
		<v-row
			:class="$style['full-width']"
			class="primary pt-7 pb-10"
			justify="center"
		>
			<v-col cols="6">
				<h1 class="text-h3 ma-0 white--text">
					{{ survey.name }}
				</h1>
			</v-col>
		</v-row>
		<v-row
			:class="$style['full-width']"
			class="fill-height light-blue lighten-5"
			justify="center"
		>
			<v-col cols="6" class="white rounded-lg mt-n5 px-4 ma-auto">
				<h1 class="pa-4 ma-0">
					Thanks for filling in the survey!
				</h1>
				<div class="pa-4 pt-0">
					<p>Your reponse has been recorded.</p>

					<div class="d-flex justify-space-between">
						<v-btn color="primary" @click="goToSurvey">
							Fill survey in again
						</v-btn>
						<v-btn color="primary" @click="goToSurveys">
							Survey list
						</v-btn>
					</div>
				</div>
			</v-col>
		</v-row>
	</v-row>
</template>

<script>
import { mapActions, mapState } from 'vuex';

export default {
	computed: {
		...mapState('publicSurvey', ['survey']),
		surveyId() {
			return parseInt(this.$route.params.surveyId, 10);
		},
	},
	created() {
		this.initialize();
	},
	methods: {
		...mapActions('publicSurvey', ['fetchSurveys']),
		async initialize() {
			const surveyId = parseInt(this.$route.params.surveyId, 10);
			await this.fetchSurveys({ id: surveyId });
		},
		goToSurvey() {
			this.$router.push({
				name: 'survey-fill',
				params: { surveyId: this.surveyId },
			});
		},
		goToSurveys() {
			this.$router.push({ name: 'surveys' });
		},
	},
};
</script>

<style lang="scss" module>
.full-width {
	width: 100%;
}
</style>
