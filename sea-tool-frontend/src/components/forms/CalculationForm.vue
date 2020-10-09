<template>
	<v-card :style="cssProps" width="100%" outlined>
		<v-form v-if="active" ref="form" class="px-6 pt-6" @submit.prevent="save">
			<v-row>
				<v-col cols="4" class="py-0">
					<v-text-field
						ref="input"
						v-model="lazyIndirectIndicator.name"
						:error-messages="nameErrors"
						max="255"
						name="indirect_indicator"
						label="Indirect indicator"
						filled
						@input="updateName"
						@blur="updateName"
					/>
				</v-col>
				<v-col class="py-0">
					<v-text-field
						v-model="lazyIndirectIndicator.description"
						name="description"
						label="description"
						filled
					/>
				</v-col>
			</v-row>
			<v-row dense>
				<v-col class="py-0">
					<v-text-field
						ref="calculationInput"
						v-model="lazyIndirectIndicator.formula"
						:error-messages="formulaErrors"
						name="calculation"
						label="Calculation"
						filled
						@input="updateFormula"
						@blur="updateFormula"
					/>
				</v-col>
			</v-row>
		</v-form>
		<div v-else class="text-subtitle-2 font-weight-regular px-6 py-4">
			<p :style="{ color: primaryColor }" class="mb-1">
				<v-icon class="mr-2">
					mdi-calculator
				</v-icon>
				{{ lazyIndirectIndicator.name }}
			</p>

			<p class="text-subtitle-1 font-weight-medium mb-0">
				Calculation
			</p>
			<p class="mb-0">
				{{ lazyIndirectIndicator.formula }}
			</p>
		</div>
	</v-card>
</template>

<script>
import { mapGetters } from 'vuex';
import { isEqual } from 'lodash';
import HandleValidationErrors from '@/utils/HandleValidationErrors';
import { required, maxLength } from '@/utils/validators';

export default {
	props: {
		indirectIndicator: {
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
			tab: null,
			lazyIndirectIndicator: { ...this.indirectIndicator },
		};
	},
	computed: {
		...mapGetters('indirectIndicator', ['getValidIndirectIndicatorNumber']),
		nameErrors() {
			return HandleValidationErrors(
				this.$v.lazyIndirectIndicator.name,
				this.errors.name,
			);
		},
		formulaErrors() {
			return HandleValidationErrors(
				this.$v.lazyIndirectIndicator.formula,
				this.errors.formula,
			);
		},
		primaryColor() {
			return this.$vuetify.theme.currentTheme.primary;
		},
		cssProps() {
			const props = {};
			if (this.active) {
				props['border-color'] = this.$vuetify.theme.currentTheme.primary;
			}
			return props;
		},
	},
	watch: {
		indirectIndicator(val) {
			if (!isEqual(this.lazyIndirectIndicator, val)) {
				if (this.lazyIndirectIndicator.formula !== val.formula) {
					this.$refs.calculationInput.focus();
				}
				this.lazyIndirectIndicator = { ...val };
			}
		},
		lazyIndirectIndicator: {
			deep: true,
			handler(val) {
				if (isEqual(this.indirectIndicator, val)) return;
				this.$emit('input', val);
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
	created() {
		this.initialize();
	},
	methods: {
		initialize() {
			if (!this.lazyIndirectIndicator.name) {
				this.lazyIndirectIndicator.name = `indirect_indicator_${
					this.getValidIndirectIndicatorNumber}`;
			}
		},
		updateName() {
			this.$v.lazyIndirectIndicator.name.$touch();
		},
		updateFormula() {
			this.$v.lazyIndirectIndicator.formula.$touch();
		},
	},
	validations: {
		lazyIndirectIndicator: {
			name: { required, maxLength: maxLength(255) },
			formula: { required },
		},
	},
};
</script>
