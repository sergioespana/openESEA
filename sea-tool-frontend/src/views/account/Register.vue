<template>
	<v-row
		justify="center"
		align="center"
		class="fill-height"
	>
		<v-col xs="12" sm="8" md="6" lg="4">
			<v-card class="elevation-12 p-a-3">
				<h1 class="m-t-0">
					Create an account
				</h1>

				<v-form
					ref="form"
					v-model="valid"
					lazy-validation
					class="m-b-1"
					@submit.prevent="register"
				>
					<h4 class="m-b-1">
						Your login information
					</h4>

					<v-text-field
						v-model="user.email"
						:error-messages="emailErrors"
						label="Email address"
						name="email"
						type="text"
						filled
						@input="updateEmail"
						@blur="updateEmail"
					/>

					<p class="body-2 mb-1">
						At least 8 characters, one number and one special character
					</p>
					<v-text-field
						v-model="user.password"
						:error-messages="passwordErrors"
						label="Password"
						name="password"
						type="password"
						filled
						@input="$v.user.password.$touch()"
						@blur="$v.user.password.$touch()"
					/>

					<v-text-field
						v-model="user.password_confirm"
						:error-messages="passwordConfirmErrors"
						label="Confirm password"
						name="password_confirm"
						type="password"
						filled
						@input="$v.user.password_confirm.$touch()"
						@blur="$v.user.password_confirm.$touch()"
					/>

					<h4 class="m-b-1">
						Organization information
					</h4>
					<v-text-field
						v-model="user.organization"
						:error-messages="organizationErrors"
						label="Organization name"
						name="organization_name"
						type="text"
						filled
						@input="$v.user.organization.$touch()"
						@blur="$v.user.organization.$touch()"
					/>

					<v-row justify="end" dense>
						<v-col cols="auto">
							<v-btn
								:disabled="registerInProgress"
								color="primary"
								type="submit"
							>
								Create account
							</v-btn>
						</v-col>
					</v-row>
				</v-form>

				<v-divider class="m-b-3" />

				<div>
					<h2>
						Log in
					</h2>
					<p class="body-2">
						temporary...
					</p>

					<v-row justify="end" dense>
						<v-col cols="auto">
							<v-btn :to="{ name: 'login' }">
								Login
							</v-btn>
						</v-col>
					</v-row>
				</div>
			</v-card>
		</v-col>
	</v-row>
</template>

<script>
import { mapActions } from 'vuex';
import { required, email, sameAs } from '@/utils/validators';
import HandleValidationErrors from '@/utils/HandleValidationErrors';
import { STATUS } from '@/utils/Constants';

export default {
	data() {
		return {
			valid: true,
			user: {
				email: '',
				password: '',
				password_confirm: '',
				organization: '',
			},
			status: STATUS.IDLE,
			serverValidationErrors: {},
			error: false,
		};
	},
	computed: {
		registerUrl() {
			return `${this.$config.VUE_APP_BASE_API}/account/register/`;
		},
		registerInProgress() {
			return this.status === STATUS.IN_PROGRESS;
		},
		emailErrors() {
			return HandleValidationErrors(
				this.$v.user.email,
				this.serverValidationErrors?.email,
			);
		},
		passwordErrors() {
			return HandleValidationErrors(
				this.$v.user.password,
				this.serverValidationErrors?.password,
			);
		},
		passwordConfirmErrors() {
			return HandleValidationErrors(
				this.$v.user.password_confirm,
				// Disable eslint camelcase because it comes from the response.
				// eslint-disable-next-line camelcase
				this.serverValidationErrors?.password_confirm,
			);
		},
		organizationErrors() {
			return HandleValidationErrors(
				this.$v.user.organization,
				this.serverValidationErrors?.organization,
			);
		},
	},
	methods: {
		...mapActions('auth', ['setToken']),
		updateEmail() {
			this.$v.user.email.$touch();
			this.serverValidationErrors.email = false;
		},
		registerError(error) {
			this.serverValidationErrors = error?.response?.data;
			this.error = error;
		},
		async register() {
			this.error = false;
			if (this.$v.$invalid || this.status === STATUS.IN_PROGRESS) {
				return;
			}
			this.status = STATUS.IN_PROGRESS;

			const response = await this.apiHandler({
				method: 'post',
				url: this.registerUrl,
				data: this.user,
				errorHandler: this.registerError,
			});

			if (!response?.data) return;
			this.status = STATUS.SUCCESS;
			this.setToken(response.data);
			this.$router.push({ name: 'home' });
		},
		async apiHandler({
			method = 'get',
			url, data, errorHandler,
		}) {
			if (!url) {
				throw Error('url needs to be filled in');
			}

			try {
				return await this.$http[method](url, data);
			} catch (error) {
				if (errorHandler) {
					errorHandler(error);
				}
				return undefined;
			}
		},
	},
	validations: {
		user: {
			email: { required, email },
			password: {
				required,
				strongPassword(password) {
					return (
						/[a-z]/.test(password) // checks for a-z
						&& /[0-9]/.test(password) // checks for 0-9
						&& /\W|_/.test(password) // checks for special char
						&& password.length >= 8
					);
				},
			},
			password_confirm: {
				required,
				sameAsPassword: sameAs('password'),
			},
			organization: { required },
		},
	},
};
</script>
<style lang="scss" module>
.content-box {
	width: 40%;
	margin: auto;
}

.submit-box {
	display: flex;
}

.submit {
	width: 10rem;
	height: 3rem;
	margin-right: 1.5rem;
}

.error {
	color: $red;
}

.title {
	margin-top: 0;
}
</style>
