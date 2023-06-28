<template>
    <div :id="'overview_' + this.overviewId + '_headsection'" class="head-section">
        <OverviewSelection
            :overviewId="this.overviewId">
        </OverviewSelection>
        <h1 :id="'overview_' + this.overviewId + '_headsection_title'"
            :hidden="headsectionTitle === null">
            {{ headsectionTitle }}
        </h1>
        <p :id="'overview_' + this.overviewId + '_headsection_text'"
            :hidden="headsectionText === null">
            {{ headsectionText }}
        </p>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

import OverviewSelection from './OverviewSelection.vue'

export default {
    name: 'HeadSection',
    components: {
        OverviewSelection
    },
    props: {
        overviewId: { type: Number, required: true }
    },
    computed: {
        headsectionTitle () {
            return this.getHeadSectionTitle()(this.overviewId)
        },
        headsectionText () {
            return this.getHeadSectionText()(this.overviewId)
        }
    },
    methods: {
        ...mapGetters('dashboard', { getHeadSectionTitle: 'getHeadSectionTitle', getHeadSectionText: 'getHeadSectionText' })
    }
}
</script>

<style>
.head-section {
    position: absolute;
    height: 25%;
    width: 100%;
}
</style>
