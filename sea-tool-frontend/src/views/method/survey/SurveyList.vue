<template>
	<v-row justify="center" class="fill-height">
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

				<template v-slot:item.actions="{ item }">
					<v-btn
						class="text-capitalize text-subtitle-1"
						color="primary"
						@click.stop="goToSurveyResults(item)"
					>
						Results
					</v-btn>
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
import { mapActions, mapState } from 'vuex';

export default {
	data() {
		return {
			headers: [
				{ text: 'Survey', value: 'name' },
				{ text: 'Description', value: 'description' },
				{ text: 'questions', value: 'questions' },
				{ text: 'Rate', value: 'rate' },
				{
					text: 'Actions',
					value: 'actions',
					sortable: false,
					align: 'center',
					width: 150,
				},
			],
		};
	},
	computed: {
		...mapState('organization', ['organization']),
		...mapState('method', ['method']),
		...mapState('survey', ['surveys']),
	},
	watch: {
		organization() {
			if (this.method.organization !== this.organization.id) {
				this.$router.push({ name: 'methods' });
			}
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
		...mapActions('survey', ['fetchSurveys']),
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

			this.fetchSurveys({
				oId: this.organization.id,
				mId: this.method.id,
			});
		},
		goToSurvey(survey) {
			this.$router.push({
				name: 'method-survey-fill',
				params: { id: this.method.id, surveyId: survey.id },
			});
		},
		goToSurveyResults(survey) {
			this.$router.push({
				name: 'method-survey-results',
				params: { id: this.method.id, surveyId: survey.id },
			});
		},
	},
};
</script>
