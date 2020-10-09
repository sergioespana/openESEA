<template>
	<v-dialog v-model="dialog" persistent max-width="500px">
		<template v-slot:activator="{ on }">
			<v-btn :class="$style.btn" text block v-on="on">
				<v-icon>mdi-plus</v-icon>
				Add organization
			</v-btn>
		</template>

		<alert-message v-if="error && error.status === 400" :error="error" />
		<v-card class="pa-8">
			<div class="d-flex justify-space-between">
				<span class="headline">
					Create organization
				</span>
				<v-btn icon @click="closeDialog">
					<v-icon color="black">
						mdi-close
					</v-icon>
				</v-btn>
			</div>

			<div class="mt-12">
				<organization-form />
			</div>
		</v-card>
	</v-dialog>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import AlertMessage from '@/components/general/AlertMessage';
import OrganizationForm from '@/components/forms/OrganizationForm';

export default {
	components: {
		AlertMessage,
		OrganizationForm,
	},
	model: {
		prop: 'dialog',
		event: 'closeDialog',
	},
	data() {
		return {
			error: undefined,
		};
	},
	computed: {
		...mapState('organization', {
			isDialogOpen: 'isCreateFormOpen',
		}),
		dialog: {
			get() {
				return this.isDialogOpen;
			},
			set(val) {
				this.changeIsCreateFormOpen(val);
			},
		},
	},
	methods: {
		...mapActions('organization', [
			'resetOrganizationForm',
			'changeIsCreateFormOpen',
		]),
		closeDialog() {
			this.dialog = false;
			this.resetOrganizationForm();
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
