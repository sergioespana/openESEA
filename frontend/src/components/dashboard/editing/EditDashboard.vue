<template>
    <div class="flex flex-column">

        <!-- Edit area title -->
        <div class="edit-area-title">Dashboard</div>

        <!-- Dashboard name -->
        <div class="edit-area-field">Name:</div>
        <InputText class="near-width"
            v-model="dashboardName">
        </InputText>

        <!-- Overview selection -->
        <div class="edit-area-field">Overviews:</div>
        <OverviewSelection class="near-width">
        </OverviewSelection>
    </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'

import OverviewSelection from '../OverviewSelection.vue'
import InputText from 'primevue/inputtext'

export default {
    components: {
        OverviewSelection,
        InputText
    },
    computed: {
        dashboardName: {
            get () { return this.getDashboardName()() },
            async set (value) { this.setDashboardName({ value: value }) }
        }
    },
    methods: {
        ...mapGetters('dashboardModel', ['getDashboardName']),
        ...mapMutations('dashboardModel', ['setDashboardName'])
    }
}
</script>
