<template>
    <vue-echarts :option="createOptions(chartData)" autoresize>
    </vue-echarts>
</template>

<script>
import 'echarts'
import ECharts from 'vue-echarts'
import { use } from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'

use([LineChart, CanvasRenderer])

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
                    fontSize: 12,
                    overflow: 'break'
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

            const categoryLimit = chartData?.categoryLimit ?? 0

            var sliderObject = null
            if (categoryLimit > 0) {
                sliderObject = {
                    type: 'slider', // Create a slider
                    show: true, // Show It
                    xAxisIndex: [0], // Show on correct axis
                    startValue: 0, // Show `categoryLimit` values, first starting at index 0
                    endValue: categoryLimit - 1, // Show `categoryLimit` values
                    handleSize: 0, // Disable handles at the edge of the slider
                    zoomLock: true, // Prevent adjusting the slider size
                    showDataShadow: false, // Hide the miniature chart
                    brushSelect: false // Prevent arbitrary brush selection
                }
            }

            const options = {
                title: titleOptions,
                xAxis: {
                    type: 'category',
                    name: categoryName,
                    nameLocation: 'center',
                    nameTextStyle: {
                        align: 'left'
                    },
                    data: categories,
                    axisLabel: {
                        interval: 0,
                        rotate: 37.5
                    }
                },
                yAxis: {
                    type: 'value',
                    name: valueName
                },
                dataZoom: [sliderObject],
                grid: {
                    top: '15%',
                    bottom: sliderObject ? '5%' : '20%',
                    left: '5%',
                    right: '5%',
                    containLabel: true
                },
                tooltip: {
                    show: 'item'
                },
                series: [
                    {
                        type: 'line',
                        data: values
                    }
                ]
            }
            return options
        }
    }
}
</script>
