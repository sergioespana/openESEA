<template>
    <div class="body-section">
        <Container v-for="(item, index) in containers"
            :key="index"
            :config="{ ...config, containerId: index }">
        </Container>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

import Container from './Container.vue'

export default {
    components: {
        Container
    },
    props: {
        config: { type: Object, required: true }
    },
    computed: {
        containers: {
            get () { return this.getContainers()(this.config) }
        }
    },
    methods: {
        ...mapGetters('dashboardModel', ['getContainers'])
    }
}
</script>

<style>
.body-section {
    position: absolute;
    width: 100%;
    height: 75%;
    top: 25%;
}
</style>
