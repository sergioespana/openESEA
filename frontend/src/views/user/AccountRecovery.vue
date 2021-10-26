<template>
    <unauthenticated-base>
        <form v-on:submit.prevent="recoverAccount" class="p-grid p-fluid p-shadow-10 p-px-5 p-pb-5" style="background-color: white; border-radius: 3px;">
            <h1 class="p-col-12" style="border-bottom: 1px solid #00695C;">Recover Account</h1>
            <small v-if="emailSend" class="p-col-12 p-p-4 p-mb-5 p-text-left" style="border: 1px solid #00695C;">We've sent you an e-mail with a password reset link.</small>
            <div class="p-col-12 p-field">
                    <span class="p-float-label">
                        <InputText type="email" id="email" v-model="email" :class="{borderless: v$.email.$error}" @change="v$.email.$touch()" />
                        <label for="email">Email</label>
                    </span>
                    <div v-if="v$.email.$error" class="p-error p-text-left">The email is invalid.</div>
                    <div class="p-error p-text-italic" v-for="error in password2Errors" :key="error"><small>{{error}}</small></div>
            </div>
            <div class="button" :class="(v$.email.$invalid ? 'unclickable' : 'clickable')" @click="sendRecoveryMail">
                Send Recovery Link
            </div>
        </form>
        <div class="p-grid p-m-5" style="color: white;">
            <router-link to="/login" class="link p-col-12">Return to login</router-link>
        </div>
    </unauthenticated-base>
</template>

<script>
import useVuelidate from '@vuelidate/core'
import { required, email } from 'vuelidate/lib/validators'
import UnauthenticatedBase from '@/components/UnauthenticatedBase'

export default {
    components: {
        UnauthenticatedBase
    },
    data () {
        return {
            email: null,
            emailSend: false
        }
    },
    setup: () => ({ v$: useVuelidate() }),
    validations: {
        email: { required, email }
    },
    methods: {
        sendRecoveryMail () {
            this.emailSend = false
            console.log('sending recovery mail...')
            this.emailSend = true
        }
    }
}
</script>
<style lang="scss" scoped>
    .borderless {
        border-bottom: 1px solid red;
    }
    .button {
        width: 100%;
        padding: 10px;
        text-align: center;
    }
    .unclickable {
        background-color: rgba(0, 105, 92, 0.2);
        cursor: not-allowed;
    }
    .clickable {
        background-color: #00695C;
        cursor: pointer;
        color: white;
    }
    .clickable:hover {
        background-color: rgba(0, 105, 92, 0.8);
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
