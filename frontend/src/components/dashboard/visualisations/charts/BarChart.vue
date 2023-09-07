<template>
    <vue-echarts :option="createOptions(chartData)" autoresize>
    </vue-echarts>
</template>

<script>
import 'echarts'
import ECharts from 'vue-echarts'
import { use } from 'echarts/core'
import { BarChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'

use([BarChart, CanvasRenderer])

export default {
    components: {
        'vue-echarts': ECharts
    },
    props: {
        chartData: {
            type: Object,
            required: true
        }
    },
    methods: {
        createOptions (chartData) {
            const title = chartData.title
            const titleOptions = {
                text: title,
                left: 'center',
                textStyle: {
                    overflow: 'break',
                    fontSize: 12,
                    width: this.$parent.$el.clientWidth
                }
            }
            const mapping = chartData?.mapping
            if (!mapping) return { title: titleOptions }
            const categoryKey = mapping?.['Category Field']?.key
            const valueKey = mapping?.['Value Field']?.key
            if (!categoryKey || !valueKey) return { title: titleOptions }
            const categoryName = mapping?.['Category Field']?.name
            const valueName = mapping?.['Value Field']?.name
            const categories = chartData.data.map(el => el[categoryKey])
            const values = chartData.data.map(el => el[valueKey])

            const itemLimit = 0
            const sideways = false

            var sliderObject = null
            if (itemLimit > 0) {
                sliderObject = {
                    type: 'slider', // Create a slider
                    show: true, // Show It
                    xAxisIndex: sideways ? [] : [0], // Show on correct axis
                    yAxisIndex: sideways ? [0] : [], // Show on correct axis
                    startValue: 0, // Show `itemLimit` values, first starting at index 0
                    endValue: itemLimit - 1, // Show `itemLimit` values
                    handleSize: 0, // Disable handles at the edge of the slider
                    zoomLock: true, // Prevent adjusting the slider size
                    showDataShadow: false, // Hide the miniature chart
                    brushSelect: false // Prevent arbitrary brush selection
                }
            }

            const categoryAxis = {
                type: 'category',
                data: categories,
                name: categoryName,
                axisLabel: {
                    interval: 0
                }
            }
            const valueAxis = {
                type: 'value',
                name: valueName
            }
            const xAxis = sideways ? valueAxis : categoryAxis
            const yAxis = sideways ? categoryAxis : valueAxis

            const options = {
                title: titleOptions,
                xAxis: xAxis,
                yAxis: yAxis,
                dataZoom: [sliderObject],
                grid: {
                    top: '15%',
                    bottom: sliderObject && !sideways ? '20%' : '5%',
                    left: '5%',
                    right: sliderObject && sideways ? '20%' : '5%',
                    containLabel: true
                },
                tooltip: {
                    trigger: 'item'
                },
                series: [
                    {
                        type: 'bar',
                        data: values
                    }
                ]
            }
            return options
        }
    }
}
</script>
