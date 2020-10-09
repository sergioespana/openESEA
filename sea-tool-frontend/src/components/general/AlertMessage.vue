<template>
	<v-alert
		prominent
		type="error"
	>
		<v-row justify="space-between" align="center">
			<v-col v-if="error.status === 400" class="grow">
				{{ firstError }}
			</v-col>
			<v-col v-else class="grow">
				{{ error.message }}
			</v-col>
			<div class="mr-5">
				<slot />
			</div>
		</v-row>
	</v-alert>
</template>

<script>
export default {
	props: {
		error: {
			type: Object,
			required: true,
		},
	},
	computed: {
		firstError() {
			if (!this.error || !this.error?.message) return undefined;
			const errors = Object.entries(this.error.message);
			return `${errors[0][0]}: ${errors[0][1]}`;
		},
	},
};
</script>
