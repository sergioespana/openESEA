<template>
    <div class="head-section">
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
        }
    },
    methods: {
        ...mapGetters('dashboardModel', ['getHeadSectionTitle', 'getHeadSectionText'])
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
