http://localhost:8080/logout/

<template>
  <div class="log" style="height: 100vh; width: 100vh; background-color: black;">
    Log out
  </div>
</template>

<script>
  import { mapActions } from 'vuex'
    export default {
      mounted () {
          this.userLogout()
          this.$router.push({ name: 'login' })
      },
      methods: {
        ...mapActions('authentication', ['userLogout'])
      }
    }
</script>
