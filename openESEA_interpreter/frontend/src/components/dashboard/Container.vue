<template>
    <div class="container" v-on:click="isClicked" :style="styleObject">
        <span :hidden="!containerTitle">
            <b>{{ containerTitle }}</b>
        </span>
        <Visualisation
            v-for="(item, index) in visualisations"
            :key="index"
            :config="{ ...config, visualisationId: index }">
        </Visualisation>
        <TextParagraph
            v-for="(item, index) in textParagraphs"
            :key="index"
            :config="{ ...config, textParagraphId: index }">
        </TextParagraph>
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

import Visualisation from './Visualisation.vue'
import TextParagraph from './TextParagraph.vue'

export default {
    components: {
        Visualisation,
        TextParagraph
    },
    props: {
        config: { type: Object, required: true }
    },
    computed: {
        containerTitle: {
            get () { return this.getContainerTitle()(this.config) }
        },
        backgroundColor: {
            get () { return this.getContainerBackgroundColor()(this.config) }
        },
        visualisations: {
            get () { return this.getVisualisations()(this.config) }
        },
        textParagraphs: {
            get () { return this.getTextParagraphs()(this.config) }
        },
        position: {
            get () { return this.getContainerPosition()(this.config) }
        },
        styleObject: {
            get () {
                var styleObject = {}
                if (this.backgroundColor) {
                    styleObject['background-color'] = this.backgroundColor
                }
                const position = this.position
                if (position) {
                    styleObject.position = 'absolute'
                    styleObject.left = position['X Start'] + '%'
                    styleObject.right = (100 - position['X End']) + '%'
                    styleObject.bottom = position['Y Start'] + '%'
                    styleObject.top = (100 - position['Y End']) + '%'
                }
                return styleObject
            }
        }
    },
    methods: {
        ...mapGetters('dashboardModel', ['getDashboardModel', 'getContainerTitle', 'getContainerPosition', 'getContainerBackgroundColor', 'getVisualisations', 'getTextParagraphs']),
        ...mapActions('dashboardModel', ['updateSelectionConfig']),
        async isClicked (event) {
            event.stopPropagation()
            await this.updateSelectionConfig(this.config)
        }
    }
}
</script>
