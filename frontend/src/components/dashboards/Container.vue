<template>
    <div :id="'overview_' + this.overviewId + '_container_' + this.containerId" class="container"
        :style="styleObject">
        <b><EditableText
            :hidden="containerTitle === null"
            :initialValue="containerTitle"
            @enteredValue="(value) => updateTitle(value)">
        </EditableText></b>
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
import { mapGetters, mapMutations } from 'vuex'

import Visualisation from './Visualisation.vue'
import EditableText from './EditableText.vue'

export default {
    name: 'Container',
    components: {
        Visualisation,
        EditableText
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
                styleObject.bottom = this.position[2] + '%'
                styleObject.top = (100 - this.position[3]) + '%'
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
        ...mapGetters('dashboardModel', { getDashboard: 'getDashboard', getVisualisations: 'getVisualisations', getContainerTitle: 'getContainerTitle', getContainerPosition: 'getContainerPosition', getContainerBackgroundColor: 'getContainerBackgroundColor' }),
        ...mapMutations('dashboardModel', { setContainerTitle: 'setContainerTitle' }),
        updateTitle (title) {
            const payload = { overviewId: this.overviewId, containerId: this.containerId, visualisationId: this.visualisationId, title: title }
            this.setContainerTitle(payload)
        }
    }
}
</script>

<style>
</style>
