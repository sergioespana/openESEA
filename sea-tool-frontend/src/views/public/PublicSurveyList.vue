<template>
	<v-row justify="center" class="fill-height py-12">
		<v-col cols="12" lg="10" xl="8" class="fill-height">
			<v-data-table
				:headers="headers"
				:items="surveys"
				:loading="!surveys"
				loading-text="loading surveys..."
				class="elevation-1 fill-height"
				hide-default-footer
				@click:row="goToSurvey"
			>
				<template v-slot:item.questions="{ item }">
					{{ (item && item.questions && item.questions.length) || 0 }}
				</template>

				<template v-slot:no-data>
					<v-row justify="space-between" align="center" dense>
						<h3>No surveys</h3>
						<v-btn color="primary" class="ml-3" @click="initialize()">
							reload
						</v-btn>
					</v-row>
				</template>
			</v-data-table>
		</v-col>
	</v-row>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
	data() {
		return {
			headers: [
				{ text: 'Survey', value: 'name' },
				{ text: 'Description', value: 'description' },
				{ text: 'questions', value: 'questions' },
				{ text: 'Rate', value: 'rate' },
			],
		};
	},
	computed: {
		...mapState('publicSurvey', ['surveys', 'error']),
	},
	created() {
		this.initialize();
	},
	methods: {
		...mapActions('publicSurvey', ['fetchSurveys']),
		async initialize() {
			this.fetchSurveys();
		},
		goToSurvey(survey) {
			this.$router.push({
				name: 'survey-fill',
				params: { surveyId: survey.id },
			});
		},
	},
};
</script>
