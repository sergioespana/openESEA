<template>
	<v-row justify="center" class="fill-height">
		<v-col cols="12" lg="10" xl="8" class="fill-height">
			<alert-message v-if="error" :error="error">
				<v-btn @click="initialize()">
					Reset
				</v-btn>
			</alert-message>

			<v-btn fixed color="primary" left class="ml-12" @click="createMethod">
				new Method
			</v-btn>

			<v-data-table
				:headers="headers"
				:items="methods"
				:loading="!methods"
				loading-text="loading methods..."
				class="elevation-1 fill-height"
				hide-default-footer
				@click:row="goToMethod"
			>
				<template v-slot:item.actions="{ item }">
					<v-icon
						color="primary" class="mr-2"
						@click.stop="updateQuestionnaire(item)"
					>
						mdi-pencil
					</v-icon>
					<v-icon
						color="error"
						@click.stop="deleteItem(item)"
					>
						mdi-delete
					</v-icon>
				</template>

				<template v-slot:no-data>
					<v-row justify="space-between" align="center" dense>
						<h3>No methods</h3>
						<v-btn color="primary" class="ml-3" @click="initialize()">
							reload
						</v-btn>
					</v-row>
				</template>
			</v-data-table>
		</v-col>
	</v-row>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import AlertMessage from '@/components/general/AlertMessage';

export default {
	components: {
		AlertMessage,
	},
	data() {
		return {
			headers: [
				{ text: 'Method', value: 'name' },
				{ text: 'Description', value: 'description' },
				{
					text: 'Actions',
					value: 'actions',
					sortable: false,
					align: 'center',
					width: 150,
				},
			],
		};
	},
	computed: {
		...mapState('organization', ['organization']),
		...mapState('method', ['methods', 'error']),
	},
	created() {
		this.initialize();
	},
	methods: {
		...mapActions('method', [
			'fetchMethods', 'resetMethod', 'resetError', 'deleteMethod', 'setMethod',
		]),
		...mapActions('topic', ['resetTopics']),
		async initialize() {
			this.resetError();
			this.fetchMethods({ oId: this.organization.id });
		},
		goToMethod(method) {
			this.$router.push({ name: 'method-surveys', params: { id: method.id } });
		},
		createMethod() {
			this.resetMethod();
			this.resetTopics();
			this.$router.push({ name: 'method-create' });
		},
		updateQuestionnaire(method) {
			this.setMethod({ id: method.id });
			this.$router.push({
				name: 'method-design',
				params: { id: method.id },
			});
		},
		async deleteItem(method) {
			this.deleteMethod({ id: method.id, oId: this.organization.id });
		},
	},
};
</script>
