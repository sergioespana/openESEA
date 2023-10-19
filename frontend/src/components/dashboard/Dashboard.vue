<template>
    <div class="dashboard">
        <div v-for="(item, index) in overviews" :key="index">
            <Overview v-if="selectionConfig.overviewId === index"
                :config="{ overviewId: index }">
            </Overview>
        </div>
    </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

import Overview from './Overview.vue'

export default {
    components: {
        Overview
    },
    computed: {
        ...mapState('dashboardModel', ['selectionConfig']),
        overviews: {
            get () { return this.getOverviews()() }
        },
        backgroundColor: {
            get () { return this.getDashboardBackgroundColor()(this.config) }
        },
        styleObject: {
            get () {
                var styleObject = {}
                if (this.backgroundColor) {
                    styleObject['background-color'] = this.backgroundColor
                }
                return styleObject
            }
        }
    },
    methods: {
        ...mapGetters('dashboardModel', ['getOverviews', 'getDashboardBackgroundColor'])
    }
}
</script>

<style>
.dashboard {
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: calc(100% - (var(--edit-area-current-width) + var(--edit-sidebar-width)));
}
</style>
