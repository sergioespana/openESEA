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
            const data = chartData?.data
            const categoryKey = mapping?.['Category Field']?.key
            const stackingKey = mapping?.['Stacking Field']?.key
            const valueKey = mapping?.['Value Field']?.key
            if (!categoryKey || !stackingKey || !valueKey) return { title: titleOptions }
            const categoryName = mapping?.['Category Field']?.name
            const stackingName = mapping?.['Stacking Field']?.name
            const valueName = mapping?.['Value Field']?.name

            const categoryList = data.map(row => row[categoryKey])
            const stackList = data.map(row => row[stackingKey])

            // Get distinct categories and stacks to make lists of values
            const categories = [...new Set(categoryList)]
            const stacks = [...new Set(stackList)]
            const dataLists = stacks.map(
                stack => {
                    return {
                        stack: stack,
                        values: categories.map(
                            category => {
                                return data.find(row => row[stackingKey] === stack && row[categoryKey] === category)?.[valueKey]
                            }
                        )
                    }
                }
            )

            // Encapsulate in series object
            const series = dataLists.map(data => { return { type: 'bar', stack: 'Stack', data: data.values, name: data.stack, encode: { tooltip: [0, 2] } } })

            const categoryLimit = chartData?.categoryLimit ?? 0
            const sideways = chartData?.sideways

            var sliderObject = null
            if (categoryLimit > 0) {
                sliderObject = {
                    type: 'slider', // Create a slider
                    show: true, // Show It
                    xAxisIndex: sideways ? [] : [0], // Show on correct axis
                    yAxisIndex: sideways ? [0] : [], // Show on correct axis
                    startValue: 0, // Show `categoryLimit` values, first starting at index 0
                    endValue: categoryLimit - 1, // Show `categoryLimit` values
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
                    formatter: function (params) {
                        return params.name + '<br/>' + params.marker + params.seriesName + '&nbsp;&nbsp;&nbsp;&nbsp;' + '<b>' + params.value + '</b>'
                    },
                    trigger: 'item'
                },
                legend: {
                    orient: 'horizontal',
                    bottom: sliderObject && !sideways ? '10%' : '0%',
                    name: stackingName
                },
                series: series
            }
            return options
        }
    }
}
</script>
