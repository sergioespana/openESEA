<template>
    <div :id="topLevelId()" :hidden="this.overviewId != this.currentOverviewId">
        <!-- <h1 :id="topLevelId() + '_name'"></h1>
        Temporary for showing name -->
    </div>
</template>

<script>
    import createDivWrapper from '../../utils/createDivWrapper.js'
    import HeadSection from './HeadSection.vue'
    import BodySection from './BodySection.vue'
    import SidePanel from './SidePanel.vue'

    export default {
        name: 'Overview',
        props: {
            yamlData: {
                type: Object,
                required: true
            },
            overviewId: {
                type: Number,
                required: true
            },
            currentOverviewId: {
                type: Number,
                required: true
            }
        },
        data () {
            return {
                // name: null,
                // headsection: null,
                // bodysection: null,
                // sidepanel: null
            }
        },
        mounted () {
            this.updateElements()
        },
        methods: {
            topLevelId () { return 'overview_' + this.overviewId },
            updateElements () {
                // const name = this.yamlData.Name || null
                const headsection = this.yamlData.HeadSection || null
                const bodysection = this.yamlData.BodySection || null
                const sidepanel = this.yamlData.SidePanel || null
                const overviewId = this.overviewId
                this.$nextTick(() => {
                    // var nameElement = document.getElementById(this.topLevelId() + '_name')
                    // nameElement.innerHTML = name

                    var parent = document.getElementById(this.topLevelId())
                    if (headsection) createDivWrapper(parent, HeadSection, { yamlData: headsection, overviewId: overviewId }, { id: 'headsection_' + overviewId })
                    if (headsection) createDivWrapper(parent, BodySection, { yamlData: bodysection, overviewId: overviewId }, { id: 'bodysection_' + overviewId })
                    if (sidepanel) createDivWrapper(parent, SidePanel, { yamlData: sidepanel }, { id: 'sidepanel' })
                })
            }
        }
    }
</script>
