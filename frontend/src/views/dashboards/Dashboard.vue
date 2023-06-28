<template>
    <div id="dashboard" class="dashboard">
        <Overview
            v-for="(_, index) in overviewRange"
            :key="index"
            :hidden="index !== selectedIndex"
            :overviewId="index">
        </Overview>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

import Overview from './Overview.vue'

import range from '../../utils/range.js'

export default {
    name: 'Dashboard',
    components: {
        Overview
    },
    computed: {
        selectedIndex () {
            return this.getSelectedOverviewIndex()()
        },
        overviewRange () {
            return range(this.getOverviewsAmount()())
        }
    },
    methods: {
        ...mapGetters('dashboard', { getSelectedOverviewIndex: 'getSelectedOverviewIndex', getOverviewsAmount: 'getOverviewsAmount' })
    }
}
</script>

<style>
.dashboard {
    /* min-width: 1000px; */
    /* min-height: 1000px; */
    position: absolute;
    height: calc(100% - 70px);
    width: calc(100% - 55px);
    left: 55px;
}
</style>
