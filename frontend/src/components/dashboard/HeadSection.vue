<template>
    <div class="head-section" :style="styleObject">
        <div class="head-section-overview-selection">
            <OverviewSelection
                :config="config">
            </OverviewSelection>
        </div>
        <h1 class="head-section-title"
            :hidden="headsectionTitle === null">
            {{ headsectionTitle }}
        </h1>
        <span class="head-section-text"
            :hidden="headsectionText === null">
            {{ headsectionText }}
        </span>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

import OverviewSelection from './OverviewSelection.vue'

export default {
    components: {
        OverviewSelection
    },
    props: {
        config: { type: Object, required: true }
    },
    computed: {
        headsectionTitle: {
            get () { return this.getHeadSectionTitle()(this.config) }
        },
        headsectionText: {
            get () { return this.getHeadSectionText()(this.config) }
        },
        position: {
            get () { return this.getHeadSectionPosition()(this.config) }
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
                }
                return styleObject
            }
        }
    },
    methods: {
        ...mapGetters('dashboardModel', ['getHeadSectionTitle', 'getHeadSectionText', 'getHeadSectionPosition'])
    }
}
</script>

<style>
.head-section {
    position: absolute;
    height: 25%;
    width: 100%;
}
.head-section-title {
    height: 50%;
    width: 100%;
}
.head-section-text {
    top: 50%;
    height: 50%;
    width: 100%;
}
.head-section-overview-selection {
    position: absolute;
    width: 20%;
    right: 0;
}
</style>
