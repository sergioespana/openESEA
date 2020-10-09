<template>
	<v-menu
		v-model="isMenuOpen"
		:close-on-content-click="false"
		offset-y
		max-width="280px"
	>
		<template v-slot:activator="{ on }">
			<v-btn
				v-if="organizations.length"
				text
				justify="space-between"
				min-width="150px"
				class="px-2"
				v-on="on"
			>
				<v-avatar color="grey lighten-2" size="30" tile class="mr-3">
					<img :src="organization.image">
				</v-avatar>
				<span class="text-capitalize text-subtitle-1">
					{{ organization.name }}
				</span>
				<v-icon large>
					mdi-menu-down
				</v-icon>
			</v-btn>
			<v-btn
				v-else
				text
				justify="space-between"
				min-width="150px"
				class="pr-2"
				@click="changeIsCreateFormOpen(true)"
			>
				<v-icon>
					mdi-plus
				</v-icon>
				<span>Create organization</span>
			</v-btn>
		</template>
		<v-card min-width="280px">
			<div class="py-2">
				<organization-details />
			</div>

			<v-divider class="mx-auto" width="90%" />

			<div class="py-2">
				<v-btn
					v-for="organization in filteredOrganizations"
					:key="organization.id"
					:class="$style.btn" text block
					@click="selectOrganization(organization)"
				>
					{{ organization.name }}
				</v-btn>
			</div>

			<v-divider class="mx-auto" width="90%" />

			<v-card-actions class="px-0 py-2">
				<create-organization />
			</v-card-actions>
		</v-card>
	</v-menu>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import CreateOrganization from '@/components/organization/CreateOrganization';
import OrganizationDetails from '@/components/organization/OrganizationDetails';

export default {
	components: {
		OrganizationDetails,
		CreateOrganization,
	},
	data() {
		return {
			isMenuOpen: false,
		};
	},
	computed: {
		...mapState('organization', [
			'organizations',
			'organization',
			'isCreateFormOpen',
			'isUpdateFormOpen',
			'error',
		]),
		baseUrl() {
			return `${this.$config.VUE_APP_BASE_API}/organizations/`;
		},
		formTitle() {
			return this.organization.id ? 'Edit Organization' : 'New Organization';
		},
		filteredOrganizations() {
			return this.organizations.filter(o => o.id !== this.organization.id);
		},
	},
	created() {
		this.initialize();
	},
	methods: {
		...mapActions('organization', [
			'fetchOrganizations',
			'setOrganization',
			'resetError',
			'changeIsCreateFormOpen',
		]),
		async initialize() {
			this.resetError();
			await this.fetchOrganizations({});
			this.setOrganization({ id: this.organization?.id || 0 });
			this.isMenuOpen = !!(this.isCreateFormOpen || this.isUpdateFormOpen);
		},
		selectOrganization(organization) {
			this.setOrganization({ id: organization.id });
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
