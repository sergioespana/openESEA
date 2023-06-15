<template>
    <div :id="topLevelId()">
    </div>
</template>

<script>
    import createElement from '../../utils/createElement.js'
    import createDivWrapper from '../../utils/createDivWrapper.js'
    import Visualisation from './Visualisation.vue'

    export default {
        name: 'Container',
        props: {
            yamlData: {
                type: Object,
                required: true
            },
            overviewId: {
                type: Number,
                required: true
            },
            containerId: {
                type: Number,
                required: true
            }
        },
        mounted () {
            this.updateElements()
        },
        methods: {
            topLevelId () {
                return 'overview_' + this.overviewId + '_container_' + this.containerId
            },
            updateElements () {
                const title = this.yamlData.Title
                const position = this.yamlData.Position || null
                const visualisations = this.yamlData.Visualisations || []
                const overviewId = this.overviewId
                const containerId = this.containerId
                this.$nextTick(() => {
                    var overviewElement = document.getElementById(this.topLevelId())
                    if (title) createElement(overviewElement, 'p', { textContent: title })
                    overviewElement.style.cssText = 'position:absolute;'
                    overviewElement.style.cssText += `left:${position['X Pos']}%`
                    overviewElement.style.cssText += `bottom:${position['Y Pos']}%`
                    overviewElement.style.cssText += `width:${position.Width}%`
                    overviewElement.style.cssText += `height:${position.Height}%`
                    if (this.yamlData.Style['Background Color']) overviewElement.style.backgroundColor = this.yamlData.Style['Background Color']

                    const length = visualisations.length
                    for (var index = 0; index < length; index++) {
                        var visualisationId = index
                        var visualisation = visualisations[visualisationId]
                        console.log(visualisation)
                        createDivWrapper(overviewElement, Visualisation, { yamlData: visualisation, overviewId: overviewId, containerId: containerId, visualisationId: visualisationId }, { id: 'wrapper_overview_' + overviewId + '_container_' + containerId + '_visualisation_' + visualisationId })
                    }
                })
            }
        }
    }
</script>

<style>
</style>
