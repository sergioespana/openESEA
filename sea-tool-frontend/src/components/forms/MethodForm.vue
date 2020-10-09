<template>
	<v-form ref="form" width="100%" @submit.prevent="save">
		<v-row dense>
			<v-col>
				<v-text-field
					ref="input"
					v-model="lazyMethod.name"
					:error-messages="nameErrors"
					name="name"
					label="Method name"
					class="headline"
					height="45"
					single-line
					@blur="updateName"
					@focus="$event.target.select()"
				/>
			</v-col>
		</v-row>
		<v-row dense>
			<v-col>
				<v-text-field
					v-model="lazyMethod.description"
					:error-messages="descriptionErrors"
					name="description"
					label="Method description"
					single-line
					@blur="updateDescription"
				/>
			</v-col>
		</v-row>
	</v-form>
</template>

<script>
import { isEqual } from 'lodash';
import HandleValidationErrors from '@/utils/HandleValidationErrors';
import { required, maxLength } from '@/utils/validators';

export default {
	props: {
		method: {
			type: Object,
			required: true,
		},
		errors: {
			type: Object,
			default: () => ({}),
		},
	},
	data() {
		return {
			lazyMethod: { ...this.method },
		};
	},
	computed: {
		nameErrors() {
			return HandleValidationErrors(
				this.$v.lazyMethod.name,
				this.errors.name,
			);
		},
		descriptionErrors() {
			return HandleValidationErrors(
				this.$v.lazyMethod.description,
				this.errors.description,
			);
		},
	},
	watch: {
		method(val) {
			if (!isEqual(this.lazyMethod, val)) {
				this.lazyMethod = { ...val };
			}
		},
		lazyMethod: {
			deep: true,
			handler(val) {
				if (this.$v.$invalid) return;
				if (isEqual(this.method, val)) return;
				this.$emit('input', val);
			},
		},
	},
	mounted() {
		if (!this.lazyMethod.name) {
			this.$refs.input.focus();
		}
	},
	methods: {
		updateName() {
			this.$v.lazyMethod.name.$touch();
		},
		updateDescription() {
			this.$v.lazyMethod.description.$touch();
		},
	},
	validations: {
		lazyMethod: {
			name: { required, maxLength: maxLength(255) },
			description: { required },
		},
	},
};
</script>
