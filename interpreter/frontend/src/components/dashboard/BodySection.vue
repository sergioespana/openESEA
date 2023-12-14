<template>
    <div class="body-section" :style="styleObject">
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
        },
        headSectionPosition: {
            get () { return this.getHeadSectionPosition()(this.config) }
        },
        position: {
            get () { return this.getBodySectionPosition()(this.config) }
        },
        styleObject: {
            get () {
                var styleObject = {}
                const position = this.position
                if (position) {
                    styleObject.position = 'absolute'
                    styleObject.left = position['X Start'] + '%'
                    styleObject.right = (100 - position['X End']) + '%'
                    styleObject.bottom = position['Y Start'] + '%'
                    styleObject.top = (100 - position['Y End']) + '%'
                } else if (this.headSectionPosition) {
                    const middleXHeadSection = (this.headSectionPosition['X End'] - this.headSectionPosition['X Start']) / 2
                    const middleYHeadSection = (this.headSectionPosition['Y End'] - this.headSectionPosition['Y Start']) / 2
                    styleObject.position = 'absolute'
                    if (middleXHeadSection < middleYHeadSection) {
                        // place to the right
                        styleObject.left = this.headSectionPosition['X End'] + '%'
                        styleObject.right = '0%'
                        styleObject.bottom = '0%'
                        styleObject.top = '0%'
                    } else {
                        // place below
                        styleObject.left = '0%'
                        styleObject.right = '0%'
                        styleObject.bottom = '0%'
                        styleObject.top = (100 - this.headSectionPosition['Y End']) + '%'
                    }
                } else {
                    styleObject.position = 'absolute'
                    styleObject.left = '0%'
                    styleObject.right = '0%'
                    styleObject.bottom = '0%'
                    styleObject.top = '25%'
                }
                return styleObject
            }
        }
    },
    methods: {
        ...mapGetters('dashboardModel', ['getContainers', 'getBodySectionPosition', 'getHeadSectionPosition'])
    }
}
</script>
