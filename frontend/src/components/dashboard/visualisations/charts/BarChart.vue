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
            const categoryKey = chartData.mapping['Category Field']?.key
            const valueKey = chartData.mapping['Value Field']?.key
            if (!categoryKey || !valueKey) return { title: titleOptions }
            const categories = [...new Set(chartData.data.map(el => el[categoryKey]))]
            var values = []
            for (const category of categories) {
                const filteredData = chartData.data.filter(el => el[categoryKey] === category)
                const value = filteredData.map(el => parseInt(el[valueKey])).reduce((partialSum, a) => partialSum + a, 0)
                values.push(value)
            }

            const options = {
                title: titleOptions,
                xAxis: {
                    type: 'category',
                    data: categories,
                    axisLabel: {
                        interval: 0
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
