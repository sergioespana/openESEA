<template>
    <select class="overview-selection" @change="onChange($event)">
        <option
            v-for="(item, index) in overviewNames"
            :key="index"
            :selected="index === selectedIndex">
            {{item}}
        </option>
    </select>
</template>

<script>

import { mapGetters, mapMutations } from 'vuex'

    export default {
        name: 'OverviewSelection',
        props: {
            overviewId: { type: Number, required: true }
        },
        computed: {
            selectedIndex () {
                return this.getSelectedOverviewId()()
            },
            overviewNames () {
                return this.getOverviewNames()()
            }
        },
        methods: {
            ...mapGetters('dashboardModel', { getSelectedOverviewId: 'getSelectedOverviewId', getOverviewNames: 'getOverviewNames' }),
            ...mapMutations('dashboardModel', { setCurrentOverview: 'setCurrentOverview' }),
            onChange (event) {
                const optionIndex = event.target.options.selectedIndex
                this.setCurrentOverview(optionIndex)
            }
        }
    }
</script>

<style>
.overview-selection {
    right: 0%;
    position: absolute;
}
</style>
