<template>
<div></div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
    created () {
        this.initialize()
    },
    computed: {
        ...mapState('authentication', ['authenticatedUser']),
        ...mapState('user', ['user'])
    },
    methods: {
        ...mapActions('user', ['setUser']),
        async initialize () {
            console.log(this.authenticatedUser)
            await this.setUser({ ...this.authenticatedUser })
            console.log(this.user)
            this.$router.push({ name: 'userdetails', params: { id: this.user.id } })
        }
    }
}
</script>
