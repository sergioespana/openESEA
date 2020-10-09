<template>
	<v-card
		:style="primaryBorder"
		class="pa-8 rounded-lg" outlined
	>
		<v-card-title primary-title class="pa-0 mb-6">
			{{ question.name }}
		</v-card-title>

		<v-card-text class="pa-0">
			<answer-input
				:value="answer || question.default"
				:type="question.type"
				:options="question.options"
				:readonly="readonly"
				option-value-key="text"
				required
				@input="changeAnswer"
			/>
		</v-card-text>
	</v-card>
</template>

<script>
import AnswerInput from '@/components/survey/AnswerInput';

export default {
	components: {
		AnswerInput,
	},
	props: {
		question: {
			type: Object,
			required: true,
		},
		answer: {
			type: String,
			default: undefined,
		},
		readonly: {
			type: Boolean,
			default: false,
		},
	},
	computed: {
		primaryColor() {
			return this.$vuetify.theme.currentTheme.primary;
		},
		primaryBorder() {
			return { 'border-color': this.primaryColor };
		},
	},
	methods: {
		changeAnswer(answer) {
			this.$emit('input', answer);
		},
	},
};
</script>
