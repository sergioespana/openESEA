<template>
	<v-expansion-panels v-model="panel" multiple>
		<v-expansion-panel>
			<v-expansion-panel-header
				class="flex-row-reverse py-0 pr-0"
				@keyup.space.prevent
			>
				<div class="d-flex align-center mx-6" @click.stop>
					<v-text-field
						v-model="lazySurvey.name"
						:error-messages="nameErrors"
						name="name"
						class="headline"
						height="45"
						required
						@input="updateName"
						@focus="$event.target.select()"
					/>
					<v-menu>
						<template v-slot:activator="{ on, attrs }">
							<v-btn
								color="grey"
								class="ml-4"
								dark
								icon
								v-bind="attrs"
								v-on="on"
							>
								<v-icon large>
									mdi-dots-vertical
								</v-icon>
							</v-btn>
						</template>
						<v-list>
							<v-list-item @click="deleteSurvey">
								<v-list-item-title>Delete</v-list-item-title>
							</v-list-item>
						</v-list>
					</v-menu>
				</div>
			</v-expansion-panel-header>
			<v-expansion-panel-content>
				<v-text-field
					v-model="lazySurvey.description"
					name="description"
					label="Survey description"
					filled
				/>
				<v-row>
					<v-col>
						<v-combobox
							v-model="lazySurvey.stakeholder"
							:error-messages="stakeholderErrors"
							:items="stakeholders"
							label="Select stakeholder"
							filled
							@input="updateStakeholder"
						>
							<template v-slot:append-item>
								<v-divider />
								<div class="pt-4 pb-2 px-3 d-flex align-center">
									<p class="ml-2 mb-0">
										or type to create new stakeholder
									</p>
								</div>
							</template>
						</v-combobox>
					</v-col>
					<v-col>
						<v-combobox
							v-model="lazySurvey.rate"
							:items="rates"
							label="Response rate"
							suffix="%"
							filled
						/>
					</v-col>
				</v-row>

				<v-treeview
					:value="selectedQuestions"
					:items="items"
					item-key="uniqueId"
					expand-icon="mdi-chevron-down"
					selected-color="primary"
					selectable
					@input="setSelected"
				/>
			</v-expansion-panel-content>
		</v-expansion-panel>
	</v-expansion-panels>
</template>

<script>
import { isEqual } from 'lodash';
import { required, maxLength } from '@/utils/validators';
import HandleValidationErrors from '@/utils/HandleValidationErrors';

export default {
	props: {
		survey: {
			type: Object,
			required: true,
		},
		items: {
			type: Array,
			required: true,
		},
		stakeholders: {
			type: Array,
			required: true,
		},
		errors: {
			type: Object,
			default: () => ({}),
		},
	},
	data() {
		return {
			lazySurvey: { ...this.survey },
			panel: [0],
			rates: Array.from(Array(21), (_, i) => i * 5),
		};
	},
	computed: {
		selectedQuestions() {
			return this.lazySurvey.questions.map(id => `question_${id}`);
		},
		nameErrors() {
			return HandleValidationErrors(
				this.$v.lazySurvey.name,
				this.errors.name,
			);
		},
		stakeholderErrors() {
			return HandleValidationErrors(
				this.$v.lazySurvey.stakeholder,
				this.errors.stakeholder,
			);
		},
	},
	watch: {
		survey(val) {
			if (isEqual(this.lazySurvey, val)) return;
			this.lazySurvey = { ...val };
		},
		lazySurvey: {
			deep: true,
			handler(val) {
				if (isEqual(this.survey, val)) return;
				this.$emit('input', { ...val });
			},
		},
	},
	created() {
		this.initialize();
	},
	methods: {
		initialize() {
			if (!this.lazySurvey.name && !this.lazySurvey.rate) {
				this.lazySurvey.name = 'Untitled Survey';
				this.lazySurvey.stakeholder = 'members';
			}
		},
		setSelected(selected) {
			const selectedQuestions = selected.map((item) => {
				const [type, id] = item.split('_');
				return { type, id };
			})
				.filter(item => item.type === 'question')
				.map(item => item.id);
			this.lazySurvey.questions = selectedQuestions;
		},
		deleteSurvey() {
			this.$emit('deleteSurvey', this.survey.id);
		},
		updateName() {
			this.$v.lazySurvey.name.$touch();
		},
		updateStakeholder() {
			this.$v.lazySurvey.stakeholder.$touch();
		},
	},
	validations: {
		lazySurvey: {
			name: { required, maxLength: maxLength(120) },
			stakeholder: { required },
		},
	},
};
</script>
