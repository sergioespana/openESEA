<template>
	<v-menu offset-y nudge-left="150px" nudge-bottom="5px">
		<template v-slot:activator="{ on }">
			<v-btn fab color="primary" small depressed v-on="on">
				J
			</v-btn>
		</template>
		<v-list>
			<v-list-item link @click="accountDetails">
				<v-list-item-action>
					<v-icon>mdi-account-details</v-icon>
				</v-list-item-action>
				<v-list-item-content>
					Personal details
				</v-list-item-content>
			</v-list-item>
			<v-list-item link @click="logout">
				<v-list-item-action>
					<v-icon>mdi-arrow-left</v-icon>
				</v-list-item-action>
				<v-list-item-content>
					Logout
				</v-list-item-content>
			</v-list-item>
		</v-list>
	</v-menu>
</template>

<script>
import { mapActions } from 'vuex';

export default {
	methods: {
		...mapActions('auth', ['removeToken']),
		accountDetails() {
			this.$router.push({ name: 'account-details' });
		},
		logout() {
			this.removeToken();
			this.$router.push({ name: 'login' });
		},
	},
};
</script>
