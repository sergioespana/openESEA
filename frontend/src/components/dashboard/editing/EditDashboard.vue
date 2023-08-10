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

        <div :style="{ height: '5px' }"></div>

        <div class="full-width" :style="{ position: 'relative', width: '100%' }">
            <Button label="Add overview" icon="pi pi-plus" class="p-button-success p-button-sm"
                @click="addOverview">
            </Button>
        </div>

        <div :style="{ height: '5px' }"></div>
    </div>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from 'vuex'

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
            set (value) { this.setDashboardName({ value: value }) }
        }
    },
    methods: {
        ...mapGetters('dashboardModel', ['getDashboardName']),
        ...mapMutations('dashboardModel', ['setDashboardName']),
        ...mapActions('dashboardModel', ['addOverview'])
    }
}
</script>
