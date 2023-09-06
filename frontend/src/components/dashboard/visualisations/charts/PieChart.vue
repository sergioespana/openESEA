<template>
    <vue-echarts :option="createOptions(chartData)" autoresize>
    </vue-echarts>
</template>

<script>
import 'echarts'
import ECharts from 'vue-echarts'
import { use } from 'echarts/core'
import { PieChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'

use([PieChart, CanvasRenderer])

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
                    fontSize: 12
                }
            }
            const categoryKey = chartData.mapping['Category Field']?.key
            const valueKey = chartData.mapping['Value Field']?.key
            if (!categoryKey || !valueKey) return { title: titleOptions }
            const data = chartData.data.map(row => { return { value: row[valueKey], name: row[categoryKey] } })

            const showLabels = false

            const options = {
                title: titleOptions,
                tooltip: {
                    trigger: 'item'
                },
                legend: {
                    orient: 'horizontal',
                    bottom: 'left'
                },
                series: [
                    {
                        type: 'pie',
                        data: data,
                        radius: '60%',
                        label: {
                            show: showLabels,
                            overflow: 'none',
                            distance: 5
                        },
                        labelLine: {
                            show: showLabels
                        }
                    }
                ]
            }
            return options
        }
    }
}
</script>
