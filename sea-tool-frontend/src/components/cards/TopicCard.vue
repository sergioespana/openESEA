<template>
	<v-card :style="cssProps" width="100%" outlined>
		<div class="px-6 py-6 pb-5">
			<p :class="isSubTopic ? 'text-h5' : 'text-h4'" class="mb-0">
				{{ name }}
			</p>
			<p v-if="description" class="body-2 mt-5 mb-0">
				{{ description }}
			</p>
		</div>
	</v-card>
</template>

<script>
export default {
	props: {
		name: {
			type: String,
			required: true,
		},
		description: {
			type: String,
			default: undefined,
		},
		isSubTopic: {
			type: Boolean,
			default: false,
		},
		borderColor: {
			type: String,
			default: undefined,
		},
	},
	computed: {
		borderThemeColor() {
			return this.$vuetify.theme.currentTheme[this.borderColor];
		},
		cssProps() {
			const props = {};
			if (this.borderColor) {
				props['border-color'] = this.borderThemeColor || this.borderColor;
			}
			return props;
		},
	},
};
</script>

<style>

</style>
