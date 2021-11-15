// http://localhost:8080/register/

<template>
    <unauthenticated-base>
        <form @submit.prevent="register" class="p-grid p-fluid p-shadow-10 p-px-5 p-pb-5" style="background-color: white; border-radius: 3px;">
            <h1 class="p-col-12" style="border-bottom: 1px solid #00695C;">Create Account</h1>
            <div class="p-col-12 p-field">
                <span class="p-float-label">
                        <InputText type="text" id="username" v-model="customuser.username" :class="{'borderless': usernameErrors.length}" @change="v$.customuser.username.$touch()" />
                        <label for="username">Username</label>
                    </span>
                    <div class="p-error p-text-italic p-text-left" v-for="error in usernameErrors" :key="error"><small v-if="error === 'This field must be unique.'">Username is already taken.</small><small v-else>{{ error }}</small></div>
            </div>
            <div class="p-col-12 p-field">
                <span class="p-float-label">
                        <InputText type="text" id="email" v-model="customuser.email" :class="{'borderless': emailErrors.length}" @change="v$.customuser.email.$touch()" />
                        <label for="email">Email</label>
                    </span>
                    <div class="p-error p-text-italic p-text-left" v-for="error in emailErrors" :key="error"><small>{{error}}</small></div>
            </div>
            <div class="p-col-12 p-field">
                <span class="p-float-label">
                        <InputText type="password" id="password" v-model="customuser.password" :class="{'borderless': passwordErrors.length}" @change="v$.customuser.password.$touch()" />
                        <label for="password">Password</label>
                    </span>
                    <div class="p-error p-text-italic p-text-left" v-for="error in passwordErrors" :key="error"><small>{{error}}</small></div>
            </div>
            <div class="p-col-12 p-field">
                <span class="p-float-label">
                        <InputText type="password" id="password2" v-model="customuser.password2" :class="{'borderless': password2Errors.length}" @change="v$.customuser.password2.$touch()"/>
                        <label for="password2">Confirm Password</label>
                    </span>
                    <div class="p-error p-text-italic p-text-left" v-for="error in password2Errors" :key="error"><small>{{error}}</small></div>
            </div>
            <div class="p-text-left p-p-3" style="color: grey;">
                <small>By signing up, you agree to the <span style="text-decoration: underline;">Terms of Use</span> and <span style="text-decoration: underline;">Privacy Policy</span></small>
            </div>
            <Button type="submit" value="submit" class="p-jc-center p-button-success" style="background-color: #00695C;" :disabled="v$.customuser.$invalid">Register Account</Button>
        </form>
        <div class="p-m-5">
            <router-link to="/login" class="link">Already have an Account? Log in.</router-link>
        </div>
    </unauthenticated-base>
</template>

<script>
    import useVuelidate from '@vuelidate/core'
    import { required, minLength, maxLength, email, sameAs } from 'vuelidate/lib/validators'
    import HandleValidationErrors from '../../utils/HandleValidationErrors'
    import { mapActions, mapState } from 'vuex'
    import UnauthenticatedBase from '@/components/UnauthenticatedBase'

    export default {
        components: {
            UnauthenticatedBase
        },
        data () {
            return {
                customuser: {
                    username: '',
                    password: '',
                    password2: '',
                    email: '',
                    first_name: '',
                    last_name_prefix: '',
                    last_name: ''
                },
                submitted: false
            }
        },
        computed: {
            ...mapState('authentication', ['errors']),
            usernameErrors () {
                return HandleValidationErrors(this.v$.customuser.username, this.errors.username)
            },
            emailErrors () {
                return HandleValidationErrors(this.v$.customuser.email, this.errors.email)
            },
            passwordErrors () {
                return HandleValidationErrors(this.v$.customuser.password, this.errors.password)
            },
            password2Errors () {
                return HandleValidationErrors(this.v$.customuser.password2)
            },
            firstnameErrors () {
                return HandleValidationErrors(this.v$.customuser.first_name)
            },
            lastnameprefixErrors () {
                return HandleValidationErrors(this.v$.customuser.last_name_prefix)
            },
            lastnameErrors () {
                return HandleValidationErrors(this.v$.customuser.last_name)
            }
        },
        watch: {
            customuser: {
                handler (val) {
                    this.initialize()
                },
                deep: true
            }
        },
        setup: () => ({ v$: useVuelidate() }),
        validations: {
            customuser: {
                username: { required, minLength: minLength(4), maxLength: maxLength(100) },
                password: { required, minLength: minLength(8) },
                password2: { required, sameAsPassword: sameAs(function () { return this.customuser.password }) },
                email: { required, email }
                // Left out on registration, to make registration easier for the user
                /*
                first_name: { required, maxLength: maxLength(50) },
                last_name_prefix: { maxLength: maxLength(50) },
                last_name: { required, maxLength: maxLength(50) }
                */
            }
        },
        created () {
            this.initialize()
        },
        methods: {
            ...mapActions('authentication', ['userRegister']),
            initialize () {
                this.$store.commit('authentication/clearErrors')
            },
            register (e) {
                this.submitted = true
                this.v$.customuser.$touch()
                if (this.v$.$invalid) { return }
                console.log('succes!')
                this.userRegister(this.customuser)
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

    <!-- <h4 class="p-col-12 p-text-center" style="border-bottom: 1px solid #00695C">Optional fields <small>(to be pushed to account settings page)</small></h4>
    <div class="p-col-12 p-field">
        <span class="p-float-label">
                <InputText type="text" id="firstname" v-model="customuser.first_name" :class="{'borderless': firstnameErrors.length && submitted}" />
                <label for="firstname">First Name</label>
            </span>
            <div class="p-error p-text-italic" v-for="error in firstnameErrors" :key="error"><small>{{error}}</small></div>
    </div>
    <div class="p-col-12 p-field">
        <span class="p-float-label">
                <InputText type="text" id="lastnameprefix" v-model="customuser.last_name_prefix" :class="{'borderless': lastnameprefixErrors.length && submitted}" />
                <label for="lastnameprefix">Last Name Prefix</label>
            </span>
            <div class="p-error p-text-italic" v-for="error in lastnameprefixErrors" :key="error"><small>{{error}}</small></div>
    </div>
    <div class="p-col-12 p-field">
        <span class="p-float-label">
                <InputText type="text" id="lastname" v-model="customuser.last_name" :class="{'borderless': lastnameErrors.length && submitted}" />
                <label for="lastname">Last Name</label>
            </span>
            <div class="p-error p-text-italic" v-for="error in lastnameErrors" :key="error"><small>{{error}}</small></div>
    </div> -->
