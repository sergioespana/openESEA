<template>
	<v-app-bar
		:style="header"
		dense app clipped-left
		flat height="64" class="px-8"
	>
		<v-btn fab small depressed @click="goBack">
			<v-icon large>
				mdi-arrow-left
			</v-icon>
		</v-btn>

		<p class="title font-weight-bold ma-0 ml-6">
			{{ survey.name }}
		</p>

		<div class="d-flex justify-end align-center flex-grow-1">
			<user-menu />
		</div>
	</v-app-bar>
</template>

<script>
import { mapState } from 'vuex';
import UserMenu from '@/components/user/UserMenu';

export default {
	components: {
		UserMenu,
	},
	computed: {
		...mapState('survey', ['survey']),
		methodId() {
			return parseInt(this.$route.params.id, 10);
		},
		header() {
			return {
				'border-bottom': `1px solid ${
					this.$vuetify.theme.parsedTheme.secondary.lighten5}`,
			};
		},
	},
	methods: {
		goBack() {
			this.$router.push({
				name: 'method-surveys',
				params: { id: this.methodId },
			});
		},
	},
};
</script>
