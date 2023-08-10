<template>
    <div class="overview" v-on:click="isClicked">
        <HeadSection v-if="headsection !== null"
            :config="config">
        </HeadSection>
        <BodySection v-if="bodysection !== null"
            :config="config">
        </BodySection>
        <SidePanel v-if="sidepanel !== null"
            :config="config">
        </SidePanel>
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

import HeadSection from './HeadSection.vue'
import BodySection from './BodySection.vue'
import SidePanel from './SidePanel.vue'

export default {
    components: {
        HeadSection,
        BodySection,
        SidePanel
    },
    props: {
        config: { type: Object, required: true }
    },
    computed: {
        headsection: {
            get () { return this.getHeadSection()(this.config) }
        },
        bodysection: {
            get () { return this.getBodySection()(this.config) }
        },
        sidepanel: {
            get () { return this.getSidePanel()(this.config) }
        }
    },
    methods: {
        ...mapGetters('dashboardModel', ['getHeadSection', 'getBodySection', 'getSidePanel']),
        ...mapActions('dashboardModel', ['updateSelectionConfig']),
        async isClicked (event) {
            event.stopPropagation()
            await this.updateSelectionConfig(this.config)
        }
    }
}
</script>
