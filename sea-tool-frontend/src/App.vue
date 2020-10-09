<template>
	<v-app>
		<component :is="header" v-if="header" />

		<component :is="sidebar" v-if="sidebar" />

		<v-main>
			<v-container class="fill-height pa-0" align-content-start fluid>
				<router-view />
			</v-container>
		</v-main>
	</v-app>
</template>

<script>
import { mapState } from 'vuex';
import DefaultHeader from '@/components/layout/DefaultHeader';

export default {
	components: {
		DefaultHeader,
	},
	props: {
		source: {
			type: String,
			default: '',
		},
	},
	data: () => ({
		drawer: true,
	}),
	computed: {
		...mapState('auth', ['jwt']),
		header() {
			const header = this.$route.meta.header || DefaultHeader;
			return !this.$route.meta.noHeader ? header : false;
		},
		sidebar() {
			return this.$route.meta.sidebar;
		},
	},
	beforeRouteUpdate(to, from, next) {
		this.$route.params.id = to.params.id;
		this.$route.params.surveyId = to.params.surveyId;
		next();
	},
};
</script>

<style lang="scss">
@import "@/assets/sass/default/app.scss";
</style>
