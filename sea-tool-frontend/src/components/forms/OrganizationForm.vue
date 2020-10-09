<template>
	<v-form ref="form" @submit.prevent="save">
		<div class="mb-4">
			<v-snackbar v-model="wrongFile" :timeout="6000" color="error" top>
				{{ errorMessage }}
				<v-btn
					text
					@click="wrongFile = false"
				>
					Close
				</v-btn>
			</v-snackbar>

			<div class="d-flex align-center">
				<v-avatar color="grey lighten-2" size="80" tile>
					<img :src="image">
				</v-avatar>

				<div class="ml-4 flex-grow-1">
					<div class="d-flex mb-3">
						<v-btn color="primary" @click="chooseFile">
							Upload picture
						</v-btn>
						<input
							v-show="false"
							ref="imageInput"
							type="file"
							@change="fileChange"
						>
					</div>
					<p class="ma-0">
						JPG, GIF or PNG. Max size of 800K
					</p>
				</div>
			</div>
		</div>

		<v-text-field
			:value="organization.name"
			:rules="[required]"
			name="name"
			label="Organization name"
			autofocus
			@blur="updateOrganizationForm({ name: $event.target.value })"
		/>

		<v-text-field
			:value="organization.description"
			:rules="[required]"
			name="description"
			label="Organization description"
			@blur="updateOrganizationForm({ description: $event.target.value })"
		/>

		<v-row justify="end" dense>
			<v-col cols="auto">
				<v-btn v-if="organization.id" type="submit" color="primary">
					Save changes
				</v-btn>
				<v-btn v-else type="submit" color="primary">
					Create organization
				</v-btn>
			</v-col>
		</v-row>
	</v-form>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
	data() {
		return {
			imageUrl: undefined,
			wrongFile: false,
			errorMessage: '',
			imageTypes: [
				'image/jpeg',
				'image/png',
				'image/gif',
			],
			required: v => !!v || 'Input required',
		};
	},
	computed: {
		...mapState('organization', {
			organization: 'form',
			isUpdateFormOpen: 'isUpdateFormOpen',
			currentOrganization: 'organization',
		}),
		image() {
			return this.imageUrl || this.organization.image;
		},
	},
	methods: {
		...mapActions('organization', [
			'updateOrganizationForm',
			'saveOrganization',
		]),
		chooseFile() {
			this.$refs.imageInput.click();
		},
		fileChange(e) {
			const file = e.target.files[0];
			if (!this.validateFile(file)) return;
			this.imageUrl = URL.createObjectURL(file);
			this.updateOrganizationForm({ image: file });
		},
		validateFile(file) {
			if (!file) return false;
			if (!this.imageTypes.includes(file.type)) {
				this.errorMessage = 'Incorrect file type';
				this.wrongFile = true;
				return false;
			}
			if (file.size > 800000) {
				this.errorMessage = 'File too large';
				this.wrongFile = true;
				return false;
			}
			return true;
		},
		save() {
			if (!this.$refs.form.validate()) {
				return;
			}
			this.saveOrganization();
		},
	},
};
</script>
