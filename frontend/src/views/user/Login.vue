<template>
    <unauthenticated-base>
        {{accessToken}}
        <form v-on:submit.prevent="login" class="p-grid p-fluid p-shadow-10 p-px-5 p-pb-5" style="background-color: white; border-radius: 3px;">
            <h1 class="p-col-12" style="border-bottom: 1px solid #00695C;">Login</h1>
            <Message v-if="incorrectAuth" severity="error" class="p-col-12">Invalid credentials. Please try again!</Message>
            <div class="p-col-12 p-field">
                <span class="p-float-label">
                    <InputText type="text" id="username" v-model="username" :class="{'borderless': v$.username.$invalid && submitted}"/>
                    <label for="username">Username</label>
                </span>
                <div v-if="v$.username.required.$invalid && submitted" class="p-error p-text-italic">Username is required</div>
            </div>
            <div class="p-col-12 p-field">
                <span class="p-float-label">
                    <Password id="password" v-model="password" :feedback="false" :class="{'borderless': v$.password.$invalid && submitted}" />
                    <label for="password">Password</label>
                </span>
                <div v-if="v$.password.required.$invalid && submitted" class="p-error p-text-italic">Password is required</div>
            </div>
            <Button type="submit" value="submit" class="p-jc-center p-button-success" style="background-color: #00695C; border: 0px solid #00695C">Login</Button>
        </form>
        <div class="p-grid p-mt-5" style="color: white;">
            <router-link to="/account-recovery" class="link p-col-12">Can't Login?</router-link>
            <router-link to="/register" class="link p-col-12">Sign up for an Account</router-link>
            <!-- <Divider />
            <div class="p-text-left" style="color: lightgrey;">
                <small>Add assessments, get peer reviews, share and find out what your organisations
                    needs now and in the future!</small>
            </div> -->
        </div>
    </unauthenticated-base>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { required } from 'vuelidate/lib/validators'
import useVuelidate from '@vuelidate/core'
import HandleValidationErrors from '../../utils/HandleValidationErrors'
import Message from 'primevue/message'
import UnauthenticatedBase from '@/components/UnauthenticatedBase'

export default {
    name: 'login',
    components: {
        UnauthenticatedBase,
        Message
    },
    data () {
        return {
            username: 'admin', // Filled in for easy login, should be removed before deployment!
            password: 'admin',
            submitted: false,
            incorrectAuth: false
        }
    },
    computed: {
        ...mapState('authentication', ['accessToken', 'currentuser']),
        nameErrors () {
            return HandleValidationErrors(this.v$.username)
        },
        passwordErrors () {
            return HandleValidationErrors(this.v$.password)
        }
    },
    setup: () => ({ v$: useVuelidate() }),
    validations: {
        username: { required },
        password: { required }
    },
    created () {
    },
    methods: {
        ...mapActions('authentication', ['userLogin']),
        async login () {
            this.submitted = true
            if (this.v$.$invalid) { return }

            await this.userLogin({
                username: this.username,
                password: this.password
            })
            .then(() => {
                this.$router.push({ name: 'home' })
            })
            .catch(() => {
                this.incorrectAuth = true
            })
        }
    }
}
</script>

<style lang="scss" scoped>
    .borderless {
        border-bottom: 1px solid red;
    }
    .link {
        text-decoration: None;
        color: white;
        font-size: 14px;
    }
    .link:hover {
        text-decoration: underline;
    }
</style>
