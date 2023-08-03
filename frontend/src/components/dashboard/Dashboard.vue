<template>
    <div class="dashboard" id="dashboard_id">
        <Overview
            v-for="(_, index) in overviewRange"
            :key="index"
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
        overviewRange () {
            return range(this.getOverviews()().length)
        }
    },
    methods: {
        ...mapGetters('dashboardModel', { getOverviews: 'getOverviews' })
    }
}
</script>

<style>
.dashboard {
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: calc(100% - (var(--edit-area-current-width) + var(--edit-panel-width)));
}
</style>
