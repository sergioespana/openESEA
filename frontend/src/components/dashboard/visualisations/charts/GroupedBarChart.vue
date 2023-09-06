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
            const data = chartData?.data
            const categoryKey = mapping?.['Category Field']?.key
            const groupingKey = mapping?.['Grouping Field']?.key
            const valueKey = mapping?.['Value Field']?.key
            if (!categoryKey || !groupingKey || !valueKey) return { title: titleOptions }
            const categoryList = data.map(row => row[categoryKey])
            const groupList = data.map(row => row[groupingKey])

            // Get distinct categories and groups to make lists of values
            const categories = [...new Set(categoryList)]
            const groups = [...new Set(groupList)]
            const dataLists = groups.map(
                group => {
                    return {
                        group: group,
                        values: categories.map(
                            category => {
                                return data.find(row => row[groupingKey] === group && row[categoryKey] === category)?.[valueKey]
                            }
                        )
                    }
                }
            )

            // Encapsulate in series object
            const series = dataLists.map(data => { return { type: 'bar', group: 'Group', data: data.values, name: data.group } })

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
                    trigger: 'axis'
                },
                legend: {
                    orient: 'horizontal',
                    bottom: 'left'
                },
                series: series
            }
            return options
        }
    }
}
</script>
