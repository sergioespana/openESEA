<template>
    <div :id="topLevelId()" class="visualisation">
    </div>
</template>

<script>
// import createElement from '../../utils/createElement.js'
import BarChart from '../../components/charts/BarChart.vue'
import createDivWrapper from '../../utils/createDivWrapper'

    export default {
        name: 'Visualisation',
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
            },
            visualisationId: {
                type: Number,
                required: true
            }
        },
        mounted () {
            this.updateElements()
        },
        methods: {
            topLevelId () {
                return 'overview_' + this.overviewId + '_container_' + this.containerId + '_visualisation_' + this.visualisationId
            },
            updateElements () {
                // const overviewId = this.overviewId
                // const containerId = this.containerId
                const position = this.yamlData.Position
                // const title = this.yamlData.Title
                const type = this.yamlData.DataDisplay.Type
                const rawData = this.yamlData.DataDisplay.Data
                this.$nextTick(() => {
                    var thisElement = document.getElementById(this.topLevelId())
                    console.log('This', thisElement)
                    var componentType = null
                    switch (type) {
                        case 'Pie Chart':
                            componentType = BarChart
                            break
                        case 'Bar Chart':
                            componentType = BarChart
                            break
                    }
                    console.log(componentType)
                    // if (title) createElement(element, '', { textContent: title })
                    var element = createDivWrapper(thisElement, componentType, {
                        chartData: {
                            labels: rawData.Labels,
                            datasets: [{
                                data: rawData.Data,
                                backgroundColor: '#f87979',
                                label: 'Label'
                            }]
                        }
                    })
                    console.log(position)
                    element.style.cssText = `position:absolute;left:${position['X Pos']}%;bottom:${position['Y Pos']}%;right:${100 - position.Width - position['X Pos']}%;top:${100 - position.Height - position['Y Pos']}%;max-width:100%;max-height:100%;`
                })
            }
        }
    }
</script>

<style>
.visualisation {
    position: absolute;
    left: 5%;
    right: 5%;
    top: 5%;
    bottom: 5%;
}

</style>
