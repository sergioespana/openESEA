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
            const categoryKey = chartData.mapping['Category Field']?.key
            const valueKey = chartData.mapping['Value Field']?.key
            if (!categoryKey || !valueKey) return { title: titleOptions }
            const categories = chartData.data.map(el => el[categoryKey])
            const values = chartData.data.map(el => el[valueKey])

            const options = {
                title: titleOptions,
                xAxis: {
                    type: 'category',
                    data: categories,
                    axisLabel: {
                        interval: 0,
                        rotate: 37.5
                    }
                },
                yAxis: {
                    type: 'value'
                },
                grid: {
                    top: '15%',
                    bottom: '5%',
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
