<template>
	<v-row
		justify="center"
		align="center"
		class="fill-height"
	>
		<v-col xs="12" sm="8" md="6" lg="4">
			<v-card class="elevation-12">
				<div class="p-x-3 p-t-3 p-b-1">
					<h1 class="m-t-0">
						Login
					</h1>

					<p v-if="responseError" class="error-msg">
						{{ responseError }}
					</p>

					<v-form
						id="login-form"
						ref="form"
						v-model="valid"
						lazy-validation
						@submit.prevent="login"
					>
						<v-text-field
							v-model="user.email"
							:error-messages="emailErrors"
							label="email address"
							name="email"
							type="text"
							filled
							@input="$v.user.email.$touch()"
							@blur="$v.user.email.$touch()"
						/>

						<v-text-field
							v-model="user.password"
							:error-messages="passwordErrors"
							label="password"
							name="password"
							type="password"
							filled
							@input="$v.user.password.$touch()"
							@blur="$v.user.password.$touch()"
						/>

						<v-row justify="end" dense>
							<v-col cols="auto">
								<v-btn color="primary" type="submit">
									Sign in
								</v-btn>
							</v-col>
						</v-row>
					</v-form>
				</div>

				<v-divider />

				<div class="p-a-3 p-t-3 p-b-1">
					<h2>
						Create an account
					</h2>
					<p class="body-2">
						Add assessments, get peer reviews, share and find out what your
						organisations needs now and in the future.
					</p>

					<v-row justify="end" dense>
						<v-col cols="auto">
							<v-btn :to="{ name: 'register' }">
								Create account
							</v-btn>
						</v-col>
					</v-row>
				</div>
			</v-card>
		</v-col>
	</v-row>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import { required, email } from '@/utils/validators';
import HandleValidationErrors from '@/utils/HandleValidationErrors';
import { STATUS } from '@/utils/Constants';

export default {
	data() {
		return {
			valid: true,
			user: {
				email: 'test@test.test',
				password: 'test',
			},
			serverValidationErrors: {},
			error: false,
		};
	},
	computed: {
		...mapState('auth', ['status']),
		responseError() {
			if (this.error?.status === 400) {
				return 'Your email and/or password do not match.';
			}
			if (this.error?.data && this.error?.data['non_field_errors']) {
				return this.error.data.non_field_errors[0];
			}
			return this.error;
		},
		emailErrors() {
			return HandleValidationErrors(this.$v.user.email);
		},
		passwordErrors() {
			return HandleValidationErrors(this.$v.user.password);
		},
	},
	methods: {
		...mapActions('auth', {
			obtainToken: 'obtainToken',
		}),
		login() {
			this.error = false;
			const nextUrl = this.$route.params.nextUrl || { name: 'home' };
			if (this.$v.$invalid || this.status === STATUS.IN_PROGRESS) return;

			this.obtainToken(this.user)
				.then(() => {
					this.$router.push(nextUrl);
				})
				.catch((error) => {
					this.error = error?.response;
				});
		},
	},
	validations: {
		user: {
			email: { required, email },
			password: { required },
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
