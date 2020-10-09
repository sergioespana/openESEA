<template>
	<v-dialog v-model="dialog" persistent max-width="500px">
		<template v-slot:activator="{ on }">
			<v-btn :class="$style.btn" text block v-on="on">
				Organization details
			</v-btn>
		</template>

		<alert-message v-if="error && error.status === 400" :error="error" />

		<v-card>
			<v-card-title class="justify-space-between">
				<span class="headline">
					Organization details
				</span>
				<v-btn icon @click="closeDialog">
					<v-icon color="black">
						mdi-close
					</v-icon>
				</v-btn>
			</v-card-title>

			<v-card-text class="px-0">
				<organization-form class="px-6 pb-4" />

				<v-divider />

				<div class="px-6 pt-8 pb-4">
					<h2 class="mb-4">
						Delete organization
					</h2>
					<p class="body-2">
						By deleting your organization you will lose all your assessments
						and collected data of the organization.
					</p>

					<v-row justify="end" dense>
						<v-col cols="auto">
							<v-btn
								color="error"
								@click="remove"
							>
								Delete organization
							</v-btn>
						</v-col>
					</v-row>
				</div>
			</v-card-text>
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
			organization: 'form',
			isDialogOpen: 'isUpdateFormOpen',
		}),
		dialog: {
			get() {
				return this.isDialogOpen;
			},
			set(val) {
				this.changeIsUpdateFormOpen(val);
			},
		},
	},
	methods: {
		...mapActions('organization', [
			'resetOrganizationForm',
			'changeIsUpdateFormOpen',
			'deleteOrganization',
		]),
		closeDialog() {
			this.dialog = false;
			this.resetOrganizationForm();
		},
		remove() {
			this.deleteOrganization({ id: this.organization.id });
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
