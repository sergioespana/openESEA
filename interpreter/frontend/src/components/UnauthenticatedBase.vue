// used in <router-view name="loginview" />
// used by AccountRecovery.vue, Login.vue, Register.vue

<template>
    <div style="position: absolute; height: 100%; width: 100%;background-color: #00695C;">
        <div class="centered">
            <h3 style="color: white; font-size: 60px;">Open ESEA</h3>
            <slot></slot>
        </div>
        <div class="p-d-flex p-text-center" style="position: absolute; bottom: 0px; left: 0; right: 0; margin-left: auto; margin-right: auto; width: 580px; color: lightgrey;">
            <div>
                <router-link to="/login" class="link">Terms of Service</router-link>
                <span> | </span>
                <router-link to="/login" class="link">Privacy Policy</router-link>
                <span> | </span>
                <span style="color: lightgrey; font-size: 14px;">Copyright 2021 ESEA Team. All rights reserved.</span>
            </div>
        </div>
    </div>
</template>
