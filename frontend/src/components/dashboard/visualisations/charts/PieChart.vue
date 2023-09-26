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
            const mapping = chartData?.mapping
            if (!mapping) return { title: titleOptions }
            const categoryKey = mapping?.['Category Field']?.key
            const valueKey = mapping?.['Value Field']?.key
            if (!categoryKey || !valueKey) return { title: titleOptions }
            const data = chartData.data
            const unsortedData = data?.map(row => { return { value: row[valueKey], name: row[categoryKey] } })
            const allData = unsortedData.sort(function (a, b) { if (a.value > b.value) { return -1 } else if (a.value < b.value) { return 1 } else if (a.name > b.name) { return -1 } else if (a.name < b.name) { return 1 } else { return 0 } })

            const chartOptions = chartData.options
            const categoryLimit = chartOptions?.categoryLimit ?? 0
            const slicedData = categoryLimit > 0 ? allData.slice(0, categoryLimit) : allData

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
                        data: slicedData,
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
