<template>
    <div :id="'overview_' + this.overviewId + '_container_' + this.containerId" class="container"
        :style="styleObject">
        <p :hidden="containerTitle === null">{{ containerTitle }}</p>
        <Visualisation
            v-for="(item, index) in visualisations"
            :key="index"
            :overviewId="this.overviewId"
            :containerId="this.containerId"
            :visualisationId="index">
        </Visualisation>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

import Visualisation from './Visualisation.vue'

export default {
    name: 'Container',
    components: {
        Visualisation
    },
    props: {
        overviewId: { type: Number, required: true },
        containerId: { type: Number, required: true }
    },
    computed: {
        styleObject () {
            var styleObject = {}
            if (this.backgroundColor) styleObject['background-color'] = this.backgroundColor
            if (this.position) {
                styleObject.position = 'absolute'
                styleObject.left = this.position[0] + '%'
                styleObject.right = (100 - this.position[1]) + '%'
                styleObject.top = this.position[2] + '%'
                styleObject.bottom = (100 - this.position[3]) + '%'
            }
            return styleObject
        },
        backgroundColor () {
            return this.getContainerBackgroundColor()(this.overviewId, this.containerId)
        },
        position () {
            const rawPosition = this.getContainerPosition()(this.overviewId, this.containerId)
            if (!rawPosition) return null
            return rawPosition.split(' ')
        },
        containerTitle () {
            return this.getContainerTitle()(this.overviewId, this.containerId)
        },
        visualisations () {
            const getVisualisationsFunction = this.getVisualisations()
            return getVisualisationsFunction(this.overviewId, this.containerId) ?? []
        }
    },
    methods: {
        ...mapGetters('dashboard', { getDashboard: 'getDashboard', getVisualisations: 'getVisualisations', getContainerTitle: 'getContainerTitle', getContainerPosition: 'getContainerPosition', getContainerBackgroundColor: 'getContainerBackgroundColor' })
    }
}
</script>

<style>
</style>
