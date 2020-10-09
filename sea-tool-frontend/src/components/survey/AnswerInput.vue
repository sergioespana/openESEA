<template>
	<v-text-field
		v-if="type === questionTypes.TEXT
			|| type === questionTypes.NUMBER"
		v-model="lazyValue"
		:type="type"
		:rules="rules"
		:readonly="readonly"
		outlined
		hide-details="auto"
	/>
	<div
		v-else-if="type === questionTypes.CHECKBOX"
		class="d-flex flex-column mt-n6"
	>
		<v-checkbox
			v-for="(option, index) in options"
			:key="`${index}-option`"
			v-model="lazyValue"
			:label="option[optionTextKey]"
			:value="option[optionValueKey]"
			:rules="rules"
			:readonly="readonly"
			multiple hide-details="auto"
		/>
	</div>
	<v-radio-group
		v-else-if="type === questionTypes.RADIO"
		v-model="lazyValue"
		:rules="rules"
		:readonly="readonly"
		class="ma-0 mt-n4"
		hide-details="auto"
	>
		<v-radio
			v-for="(option, index) in options"
			:key="`${index}-option`"
			:label="option[optionTextKey]"
			:value="option[optionValueKey]"
			class="mt-2"
		/>
	</v-radio-group>
</template>

<script>
import { QUESTION_TYPES } from '@/utils/Constants';

export default {
	components: {
	},
	model: {
		prop: 'value',
		event: 'input',
	},
	props: {
		value: {
			type: [String, Number, Array],
			default: undefined,
		},
		required: {
			type: Boolean,
			default: false,
		},
		type: {
			type: String,
			default: 'text',
			validator: v => Object.values(QUESTION_TYPES).includes(v),
		},
		options: {
			type: Array,
			default: () => ([]),
		},
		optionTextKey: {
			type: String,
			default: 'text',
		},
		optionValueKey: {
			type: String,
			default: 'value',
		},
		readonly: {
			type: Boolean,
			default: false,
		},
	},
	data() {
		return {
			lazyValue: this.value,
			requiredRule: v => !!v || 'Input is required.',
			requiredMultipleRule: v => !!(v && v.length)
				|| 'One requires to be selected.',
			questionTypes: QUESTION_TYPES,
		};
	},
	computed: {
		parsedType() {
			return this.type.toLowerCase();
		},
		rules() {
			const rules = [];
			if (this.required) {
				const requiredType = this.options.length
					? this.requiredMultipleRule : this.requiredRule;
				rules.push(requiredType);
			}
			return rules;
		},
	},
	watch: {
		value(val) {
			if (val !== this.lazyValue) {
				this.lazyValue = this.type === this.questionTypes.CHECKBOX
					? this.splitValue(val) : val;
			}
		},
		lazyValue(val) {
			if (val === this.value) return;
			if (this.type === this.questionTypes.CHECKBOX) {
				const checked = this.splitValue(this.value);
				if (!val.length) {
					this.lazyValue = checked;
					return;
				}
				if (val === checked) return;
			}
			this.$emit('input', `${val}`);
		},
	},
	created() {
		if (this.parsedType === this.questionTypes.CHECKBOX) {
			this.lazyValue = this.splitValue(this.lazyValue);
		}
	},
	methods: {
		splitValue(value) {
			return value ? value.split(',') : value;
		},
	},
};
</script>
