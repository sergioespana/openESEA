<template>
    <div :id="'overview_' + this.overviewId" class="overview">
        <HeadSection
            v-if="headsection"
            :overviewId="this.overviewId">
        </HeadSection>
        <BodySection
            v-if="bodysection"
            :overviewId="this.overviewId">
        </BodySection>
        <SidePanel
            v-if="sidepanel"
            :overviewId="this.overviewId">
        </SidePanel>
    </div>
</template>

<script>
    import { mapGetters } from 'vuex'

    import HeadSection from './HeadSection.vue'
    import BodySection from './BodySection.vue'
    import SidePanel from './SidePanel.vue'

    export default {
        name: 'Overview',
        components: {
            HeadSection,
            BodySection,
            SidePanel
        },
        props: {
            overviewId: { type: Number, required: true }
        },
        computed: {
            headsection () {
                const headsection = this.getHeadSection()(this.overviewId)
                return headsection !== null
            },
            bodysection () {
                const bodysection = this.getBodySection()(this.overviewId)
                return bodysection !== null
            },
            sidepanel () {
                const sidepanel = this.getSidePanel()(this.overviewId)
                return sidepanel !== null
            }
        },
        methods: {
            ...mapGetters('dashboard', { getHeadSection: 'getHeadSection', getBodySection: 'getBodySection', getSidePanel: 'getSidePanel' })
        }
    }
</script>

<style>
.overview {
    width: 100%;
    height: 100%;
    /* min-height: 1000px; */
}
</style>
