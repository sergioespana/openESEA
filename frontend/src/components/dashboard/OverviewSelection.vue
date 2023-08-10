<template>
    <Dropdown class="full-width"
        :options="overviewInfo"
        :optionLabel="'description'"
        :optionValue="'index'"
        :placeholder="overviewInfo[configData?.overviewId]?.description"
        @change="goToOverview">
    </Dropdown>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'

import Dropdown from 'primevue/dropdown'

export default {
    components: {
        Dropdown
    },
    props: {
        config: { type: Object, default: () => { return null } }
    },
    computed: {
        ...mapState('dashboardModel', ['selectionConfig']),
        configData: {
            get () { return this.config ?? this.selectionConfig }
        },
        overviewInfo: {
            get () {
                const overviews = this.getOverviews()()
                const overviewNames = overviews.map(overview => overview?.Name)
                return overviewNames.map((value, index) => ({ description: value, index: index }))
            }
        }
    },
    methods: {
        ...mapGetters('dashboardModel', ['getOverviews']),
        ...mapActions('dashboardModel', ['updateSelectionConfig']),
        goToOverview (event) {
            const selectedOverviewId = event.value
            this.updateSelectionConfig({ overviewId: selectedOverviewId })
        }
    }
}
</script>
