<template>
    <div :id="'overview_' + this.overviewId + '_bodysection'" class="body-section">
        <Container
            v-for="(item, index) in containers"
            :key="index"
            :overviewId="this.overviewId"
            :containerId="index">
        </Container>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

import Container from './Container.vue'

export default {
    name: 'BodySection',
    components: {
        Container
    },
    props: {
        overviewId: { type: Number, required: true }
    },
    computed: {
        containers () {
            return this.getContainers()(this.overviewId) ?? []
        }
    },
    methods: {
        ...mapGetters('dashboard', { getContainers: 'getContainers' })
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
