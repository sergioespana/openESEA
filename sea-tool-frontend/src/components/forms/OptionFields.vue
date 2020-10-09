<template>
	<v-row align="center" dense>
		<v-col cols="auto">
			<v-checkbox
				hide-details
				readonly
			/>
		</v-col>
		<v-col>
			<v-text-field
				v-model="option.text"
				:rules="rules"
				label="Option label"
				single-line
				hide-details
				required
			/>
		</v-col>
		<v-col cols="2">
			<div class="d-flex align-center">
				<v-text-field
					v-model="option.value"
					:rules="rules"
					class="ml-4"
					hide-details
					required
				/>
				<p class="text-capitalize mt-4 mb-0 ml-4 mr-12">
					points
				</p>
			</div>
		</v-col>
		<v-col cols="auto" offset-md="1" class="ml-auto">
			<v-btn color="error" class="mt-3" fab x-small @click="deleteOption">
				<v-icon>mdi-close</v-icon>
			</v-btn>
		</v-col>
	</v-row>
</template>

<script>
import { required } from '@/utils/inputValidations';

export default {
	props: {
		option: {
			type: Object,
			required: true,
		},
	},
	data() {
		return {
			rules: [required],
			lazyOption: this.option,
		};
	},
	watch: {
		option(val) {
			this.lazyOption = val;
		},
		lazyOption(val) {
			if (val !== this.option) {
				this.update();
			}
		},
	},
	methods: {
		update() {
			this.$emit('update', this.lazyOption);
		},
		deleteOption() {
			this.$emit('delete');
		},
	},
};
</script>
