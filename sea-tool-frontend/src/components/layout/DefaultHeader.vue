<template>
	<v-app-bar dense app clipped-left height="64" class="px-8">
		<organization-menu />

		<v-btn
			text
			class="text-capitalize text-subtitle-1 ml-12"
			@click="goToMethods"
		>
			Methods
		</v-btn>

		<v-btn
			text disabled
			class="text-capitalize text-subtitle-1 ml-12"
			@click="goToMethods"
		>
			Stakeholders
		</v-btn>

		<div class="d-flex justify-end flex-grow-1">
			<user-menu />
		</div>
	</v-app-bar>
</template>

<script>
import OrganizationMenu from '@/components/organization/OrganizationMenu';
import UserMenu from '@/components/user/UserMenu';

export default {
	components: {
		OrganizationMenu,
		UserMenu,
	},
	methods: {
		goToMethods() {
			this.$router.push({ name: 'methods' });
		},
	},
};
</script>

<style lang="scss" module>
.btn {
	text-transform: none;
	justify-content: left;
}
</style>
