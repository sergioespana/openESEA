// http://localhost:8080/userprofile/
// Redirects to the personal page of a person by setting up the User and going to userdetails.

<template>
    <div></div>
</template>

<script>
    import { mapActions, mapState } from 'vuex'

    export default {
        async created () {
            await this.setUser({ ...this.authenticatedUser })
            this.$router.push({ name: 'userdetails', params: { id: this.user.id } })
        },
        computed: {
            ...mapState('authentication', ['authenticatedUser']),
            ...mapState('user', ['user'])
        },
        methods: {
            ...mapActions('user', ['setUser'])
        }
    }
</script>
