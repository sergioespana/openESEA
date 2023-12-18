<template>
    <my-users :query="`?organisation=${this.$route.params.OrganisationId}`" selection-enabled></my-users>
</template>

<script>
import MyUsers from '../../components/MyUsers'

export default {
    components: {
        MyUsers
    }
}
</script>
