<template>
	<v-row justify="center" class="fill-height">
		<v-col cols="12" lg="10" xl="6" class="fill-height">
			<v-row justify="center" class="mb-12">
				<h1>Create a new method</h1>
				<v-item-group v-model="selected" mandatory>
					<v-row justify="center" class="mb-9">
						<v-col
							v-for="(item, i) in items"
							:key="i"
							cols="12"
							md="6"
						>
							<v-item v-slot:default="{ active, toggle }">
								<v-card
									:style="active ? activeCard : greyBorder"
									:class="$style.card"
									:disabled="item.disabled"
									class="d-flex flex-column align-center text-center pa-12"
									outlined
									@click="toggle"
								>
									<v-icon x-large>
										{{ item.icon }}
									</v-icon>
									<p class="title font-weight-bold my-7">
										{{ item.title }}
									</p>
									<p class="body-1 mb-8">
										{{ item.text }}
									</p>
									<v-icon :class="{ 'primary--text': active }">
										{{
											active ? 'mdi-checkbox-marked-circle-outline'
											: 'mdi-checkbox-blank-circle-outline'
										}}
									</v-icon>
								</v-card>
							</v-item>
						</v-col>
					</v-row>
				</v-item-group>

				<v-card
					v-if="!selected"
					:style="greyBorder"
					:class="$style.card"
					class="d-flex flex-column align-center pa-12"
					color="blue lighten-5"
					outlined
					width="100%"
					@drop.prevent="addFile"
					@dragover.prevent
				>
					<v-snackbar v-model="wrongFileType" :timeout="6000" color="error" top>
						Incorrect file type
						<v-btn
							text
							@click="wrongFileType = false"
						>
							Close
						</v-btn>
					</v-snackbar>
					<p class="body-1">
						<span class="font-weight-bold">Drag and Drop file here</span>
						<span class="mx-4">or</span>
						<v-btn color="primary">
							Add file
						</v-btn>
					</p>
					<p class="body-1 ma-0 grey--text">
						Accepted File Type: .yml file
					</p>
					{{ file && file.name }}
				</v-card>

				<v-btn color="primary" class="mt-12" @click="goToNext">
					Start method
				</v-btn>
			</v-row>
		</v-col>
	</v-row>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
	data() {
		return {
			items: [{
				icon: 'mdi-cloud-upload-outline',
				title: 'Upload a model',
				text: `Pick this option if you have a .yml file which can be used as
					a model. You can modify this later through the editor.`,
				disabled: true,
			}, {
				icon: 'mdi-file-edit-outline',
				title: 'Create a model from scratch',
				text: `Pick this option if you don’t have a model that can be imported
					directly. You’ll be able to create the method manually.`,
			}],
			selected: 1,
			file: undefined,
			wrongFileType: false,
		};
	},
	computed: {
		...mapState('organization', ['organization']),
		activeCard() {
			return {
				'border-color': this.$vuetify.theme.currentTheme.primary,
			};
		},
		greyBorder() {
			return {
				'border-color':
					`${this.$vuetify.theme.parsedTheme.secondary.lighten5} !important`,
			};
		},
	},
	methods: {
		...mapActions('method', ['saveMethod']),
		async goToNext() {
			if (!this.file && !this.selected) {
				return;
			}
			const { response, error } = await this.saveMethod({
				oId: this.organization.id,
			});
			if (error) return;
			this.$router.push({
				name: 'method-design',
				params: { id: response.data.id },
			});
		},
		addFile(e) {
			const droppedFiles = e.dataTransfer.files;
			if (!droppedFiles) return;
			const [droppedFile] = [...droppedFiles];

			if (droppedFile.name.toLowerCase().endsWith('.yml')) {
				this.file = droppedFile;
				this.wrongFileType = false;
				return;
			}
			this.wrongFileType = true;
		},
	},
};
</script>

<style lang="scss" module>
.card {
  border-radius: 8px !important;
  border-width: 2px !important;
	border-style: solid;
}
</style>
