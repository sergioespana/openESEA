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
                return this.getSelectedOverviewIndex()()
            },
            overviewNames () {
                return this.getOverviewNames()(this.overviewId)
            }
        },
        methods: {
            ...mapGetters('dashboard', { getSelectedOverviewIndex: 'getSelectedOverviewIndex', getOverviewNames: 'getOverviewNames' }),
            ...mapMutations('dashboard', { setCurrentOverview: 'setCurrentOverview' }),
            onChange (event) {
                const optionIndex = event.target.options.selectedIndex
                this.saveOverviewIndex(optionIndex)
            },
            async saveOverviewIndex (index) {
                await this.setCurrentOverview(index)
            }
        }
    }
</script>

<style>
.overview-selection {
    right: 50px;
    position: absolute;
}
</style>
