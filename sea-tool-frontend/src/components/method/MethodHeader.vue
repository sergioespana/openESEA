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
			{{ title }}
			<span v-if="showSavedChanges" class="ml-2 text-caption">
				<template v-if="isUpToDate">
					All changes saved
				</template>
				<template v-else>
					...
				</template>
			</span>
		</p>

		<div class="d-flex justify-end align-center flex-grow-1">
			<v-breadcrumbs :items="methodPages" large class="mr-6">
				<template v-slot:divider>
					<v-icon>mdi-chevron-right</v-icon>
				</template>
				<template v-slot:item="{ item }">
					<v-breadcrumbs-item
						:to="item.to"
						:disabled="false"
						exact-active-class="light-blue lighten-4 rounded"
					>
						<span class="black--text py-2 px-3">
							{{ item.text }}
						</span>
					</v-breadcrumbs-item>
				</template>
			</v-breadcrumbs>

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
	data() {
		return {
			steps: [{
				text: 'Design method',
				to: { name: 'method-design' },
				back: { name: 'methods' },
			}, {
				text: 'Survey',
				to: { name: 'method-surveys-builder' },
				back: { name: 'method-design' },
			}],
		};
	},
	computed: {
		...mapState('method', ['method']),
		...mapState('topic', { topicsSaved: 'isSaved' }),
		...mapState('question', { questionsSaved: 'isSaved' }),
		...mapState('indirectIndicator', { IndirectIndicatorsSaved: 'isSaved' }),
		...mapState('survey', { SurveysSaved: 'isSaved' }),
		header() {
			return {
				'border-bottom': `1px solid ${
					this.$vuetify.theme.parsedTheme.secondary.lighten5}`,
			};
		},
		title() {
			return this.method.id ? this.method.name : 'New method';
		},
		isUpToDate() {
			const all = {
				...this.topicsSaved,
				...this.questionsSaved,
				...this.IndirectIndicatorsSaved,
				...this.SurveysSaved,
			};
			const found = Object.values(all).find(value => value === false);
			return found === undefined;
		},
		methodPages() {
			return this.steps.map(item => ({
				...item,
				to: {
					...item.to,
					params: { id: this.$route.params.id },
				},
			}));
		},
		showSavedChanges() {
			return this.method.id;
		},
	},
	methods: {
		goBack() {
			this.$router.push(this.backRoute() || { name: 'methods' });
		},
		backRoute() {
			return this.methodPages.find(
				item => item.to?.name === this.$router.currentRoute?.name,
			)?.back;
		},
	},
};
</script>

<style lang="scss" module>
.active-breadcrumb {
	background-color: lightblue;
}
</style>
