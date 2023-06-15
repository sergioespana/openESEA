<template>
    <div :id="topLevelId()" class="dashboard"> </div>
</template>

<script>
    import createDivWrapper from '../../utils/createDivWrapper.js'
    import Overview from './Overview.vue'

    export default {
        name: 'Dashboard',
        props: {
            yamlData: {
                type: Object,
                required: true
            }
        },
        data () {
            return {
                name: null,
                overviews: null
            }
        },
        mounted () {
            this.updateElements()
        },
        methods: {
            topLevelId () {
                return 'wrapper-overviews'
            },
            updateElements () {
                this.name = this.yamlData.Name
                this.overviews = this.yamlData.Overviews

                const overviews = this.overviews

                this.$nextTick(() => {
                    var parent = document.getElementById(this.topLevelId())
                    for (let index = 0; index < overviews.length; index++) {
                        const overview = overviews[index]

                        if (overview) createDivWrapper(parent, Overview, { yamlData: overview, currentOverviewId: 0, overviewId: index }, { id: 'overview_wrapper_' + index })
                    }
                })
            },
            getSideBarWidth () {
                const sidebarwidth = document.getElementById('sidebar').offsetWidth
                console.log(sidebarwidth)
            }
        }
    }
</script>

<style>
.dashboard {
    width: calc(100vw - var(--sidebar-width));
    height: calc(100vh - var(--menubar-height));
}
</style>
