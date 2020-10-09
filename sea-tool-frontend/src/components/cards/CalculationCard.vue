<template>
	<v-card :style="cssProps" width="100%" outlined>
		<div class="text-subtitle-2 font-weight-regular px-6 py-4">
			<p class="primary--text mb-1">
				<v-icon class="mr-2">
					mdi-calculator
				</v-icon>
				{{ calculation.name }}
			</p>

			<p class="text-subtitle-1 font-weight-medium mb-0">
				Calculation
			</p>

			<v-tooltip bottom>
				<template v-slot:activator="{ on, attrs }">
					<span v-bind="attrs" class="px-2 ml-n2" v-on="on">
						{{ calculation.calculation }} = {{ calculation.value }}
					</span>
				</template>
				<span>{{ formula }}</span>
			</v-tooltip>
		</div>
	</v-card>
</template>

<script>
export default {
	props: {
		calculation: {
			type: Object,
			required: true,
		},
		borderColor: {
			type: String,
			default: undefined,
		},
	},
	computed: {
		formula() {
			return this.calculation?.formula.replace(/\[|\]/g, '');
		},
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
