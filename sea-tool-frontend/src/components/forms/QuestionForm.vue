<template>
	<v-card :style="cssProps" width="100%" outlined>
		<v-form v-if="active" ref="form" class="px-6 pt-6" @submit.prevent="save">
			<v-row>
				<v-col cols="3" class="py-0">
					<v-text-field
						ref="input"
						v-model="lazyQuestion.key"
						:error-messages="keyErrors"
						name="direct_indicator"
						label="Direct indicator"
						required filled
						@input="questionKeyFilter"
					/>
				</v-col>
				<v-col class="py-0">
					<v-text-field
						v-model="lazyQuestion.name"
						:error-messages="nameErrors"
						name="question"
						label="Question"
						required filled
						@input="updateName"
					/>
				</v-col>
			</v-row>
			<v-row>
				<v-col cols="3" class="py-0">
					<v-select
						:value="lazyQuestion.type"
						:items="questionTypesList"
						name="question_type"
						label="Question type"
						filled
						@input="changeQuestionType"
					/>
				</v-col>
				<v-col class="py-0">
					<v-text-field
						v-model="lazyQuestion.description"
						name="description"
						label="Description" filled
					/>
				</v-col>
			</v-row>
			<v-row v-if="lazyQuestion.type === 'NUMBER'">
				<v-col cols="3" class="py-0">
					<v-text-field
						v-model="lazyQuestion.prefix"
						name="prefix"
						label="Prefix"
						required filled
					/>
				</v-col>
				<v-col class="py-0">
					<v-text-field
						v-model="lazyQuestion.default"
						name="default"
						label="Default"
						required filled
					/>
				</v-col>
				<v-col cols="3" class="py-0">
					<v-text-field
						v-model="lazyQuestion.suffix"
						name="suffix"
						label="Suffix"
						required filled
					/>
				</v-col>
			</v-row>
			<template v-if="lazyQuestion.options && lazyQuestion.options.length">
				<option-fields
					v-for="(option, index) in lazyQuestion.options"
					:key="`option-${index}`"
					:option="option"
					@delete="deleteOption(option)"
				/>
				<v-btn class="text-capitalize my-6" @click="newOption">
					Add option
				</v-btn>
			</template>
		</v-form>
		<div v-else class="text-subtitle-2 font-weight-regular px-6 py-4">
			<p :style="{ color: primaryColor }" class="mb-1">
				{{ question.key }}
			</p>

			<p class="text-subtitle-1 font-weight-medium mb-0">
				{{ question.name }}
			</p>
			<p v-if="!question.options.length" class="mb-0">
				<span class="text-capitalize">
					{{ questionType }}
				</span>
				<span class="pl-1 text--grey">
					{{ question.prefix }}
				</span>
				<span class="pl-1 text--grey">
					{{ question.default }}
				</span>
				<span class="pl-1 text--grey">
					{{ question.suffix }}
				</span>
			</p>
			<template v-else>
				<v-checkbox
					v-for="(option, index) in question.options"
					:key="`option-${index}`"
					:label="option.text"
					:value="option.value"
					class="mt-2"
					hide-details
					readonly
				/>
			</template>
		</div>
	</v-card>
</template>

<script>
import { mapGetters } from 'vuex';
import { isEqual, cloneDeep } from 'lodash';
import HandleValidationErrors from '@/utils/HandleValidationErrors';
import { required, maxLength } from '@/utils/validators';
import OptionFields from '@/components/forms/OptionFields';
import { QUESTION_TYPES } from '@/utils/Constants';

export default {
	components: {
		OptionFields,
	},
	props: {
		question: {
			type: Object,
			required: true,
		},
		active: {
			type: Boolean,
			default: false,
		},
		errors: {
			type: Object,
			default: () => ({}),
		},
	},
	data() {
		return {
			lazyQuestion: cloneDeep(this.question),
			inputRules: [required],
			questionTypes: QUESTION_TYPES,
		};
	},
	computed: {
		...mapGetters('question', ['getValidQuestionKeyNumber']),
		questionTypesList() {
			return Object.entries(this.questionTypes)
				.map(([text, value]) => ({ text, value }));
		},
		questionType() {
			return this.questionTypesList.find(
				type => type.value === this.lazyQuestion.type,
			).text;
		},
		keyErrors() {
			return HandleValidationErrors(
				this.$v.lazyQuestion.key,
				this.errors.key,
			);
		},
		nameErrors() {
			return HandleValidationErrors(
				this.$v.lazyQuestion.name,
				this.errors.name,
			);
		},
		primaryColor() {
			return this.$vuetify.theme.currentTheme.primary;
		},
		cssProps() {
			const props = {};
			if (this.active) {
				props['border-color'] = this.primaryColor;
			}
			return props;
		},
	},
	watch: {
		question(val) {
			if (isEqual(this.lazyQuestion, val)) return;
			this.lazyQuestion = cloneDeep(val);
		},
		lazyQuestion: {
			deep: true,
			handler(val) {
				if (isEqual(this.question, val)) return;
				this.$emit('input', cloneDeep(val));
			},
		},
		active(val) {
			if (!val) {
				this.$v.$touch();
			} else {
				this.$nextTick(() => this.$refs.input && this.$refs.input.focus());
			}
		},
	},
	mounted() {
		if (!this.lazyQuestion.name) {
			this.$refs.input.focus();
		}
	},
	created() {
		this.initialize();
	},
	methods: {
		initialize() {
			if (!this.lazyQuestion.key && !this.lazyQuestion.name) {
				this.lazyQuestion.key = `direct_indicator_${
					this.getValidQuestionKeyNumber}`;
				this.lazyQuestion.name = `question ${this.getValidQuestionKeyNumber}`;
			}
		},
		updateName() {
			this.$v.lazyQuestion.name.$touch();
		},
		changeQuestionType(e) {
			this.lazyQuestion.type = e;
			const typesWithOptions = ['RADIO', 'CHECKBOX'];
			if (typesWithOptions.includes(e) && !this.lazyQuestion.options.length) {
				this.lazyQuestion.options = [
					{ text: 'option 1', value: '0' },
					{ text: 'option 2', value: '0' },
				];
			} else if (!typesWithOptions.includes(e)) {
				this.lazyQuestion.options = [];
			}
		},
		newOption() {
			this.lazyQuestion.options.push({
				text: `option ${this.lazyQuestion.options.length + 1}`,
				value: '',
			});
		},
		deleteOption(event) {
			if (this.lazyQuestion.options && this.lazyQuestion.options.length > 2) {
				this.lazyQuestion.options = this.lazyQuestion.options.filter(
					option => option !== event,
				);
			}
		},
		questionKeyFilter(val) {
			if (val.includes(' ')) {
				this.lazyQuestion.key = val.replace(' ', '_');
			}
		},
	},
	validations: {
		lazyQuestion: {
			key: { required },
			name: { required, maxLength: maxLength(120) },
		},
	},
};
</script>

<style lang="scss">
.lowercase {
  text-transform: lowercase;
}
.capitalize {
  text-transform: capitalize;
}
</style>
