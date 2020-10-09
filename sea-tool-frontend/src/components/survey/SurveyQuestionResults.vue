<template>
	<v-card class="pa-8 rounded-lg" outlined>
		<p v-if="question.key" class="primary--text mb-0 mt-n6">
			{{ question.key }}
		</p>
		<v-card-title primary-title class="pa-0 mb-4">
			{{ question.name }}
		</v-card-title>

		<v-card-text class="pa-0">
			<template
				v-if="type === questionTypes.RADIO || type === questionTypes.CHECKBOX"
			>
				<div
					v-for="(mappedAnswer, index) in optionMappedAnswers"
					:key="index"
				>
					<v-divider v-if="index !== 0" />
					<div class="d-flex justify-space-between py-3">
						<p class="mb-0">
							{{ mappedAnswer[0] }}
						</p>
						<p class="mb-0">
							<span class="mr-6">
								{{ Math.round(mappedAnswer[1] / answers.length * 100) }}%
							</span>
							{{ mappedAnswer[1] }}
						</p>
					</div>
				</div>
			</template>
			<template v-else>
				<div class="d-flex flex-column">
					<div v-for="(answer, index) in answers" :key="index">
						<v-divider v-if="index !== 0" />
						<p class="py-3 mb-0">
							{{ answer }}
						</p>
					</div>
					<p class="rounded-lg mb-0 pa-2 blue lighten-4 align-self-start">
						average: {{ average }}
					</p>
				</div>
			</template>
		</v-card-text>
	</v-card>
</template>

<script>
import { QUESTION_TYPES } from '@/utils/Constants';

export default {
	components: {
	},
	props: {
		question: {
			type: Object,
			required: true,
		},
		answers: {
			type: Array,
			default: () => [],
		},
	},
	data() {
		return {
			questionTypes: QUESTION_TYPES,
		};
	},
	computed: {
		type() {
			return this.question.type;
		},
		average() {
			if (!this.answers.length || this.type !== this.questionTypes.NUMBER) {
				return 0;
			}

			const total = this.answers.reduce(
				(a, b) => parseInt(a, 10) + parseInt(b, 10), 0,
			);
			return total / this.answers.length;
		},
		optionMappedAnswers() {
			const optionMappedAnswers = {};
			if (!this.question.options.length || !this.answers.length) {
				return optionMappedAnswers;
			}

			this.question.options.forEach(
				option => optionMappedAnswers[option.text] = 0,
			);

			let allAnswers = [];
			if (this.type === this.questionTypes.CHECKBOX) {
				this.answers.forEach((answer) => {
					const list = answer.split(',');
					allAnswers = [...allAnswers, ...list];
				});
			} else if (this.type === this.questionTypes.RADIO) {
				allAnswers = this.answers;
			}

			allAnswers.forEach(answer => optionMappedAnswers[answer] += 1);
			return Object.entries(optionMappedAnswers);
		},
	},
	methods: {
		changeAnswer(answer) {
			this.$emit('input', answer);
		},
	},
};
</script>
