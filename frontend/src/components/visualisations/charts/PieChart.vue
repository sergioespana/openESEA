<template>
    <vue-echarts :option="this.options" autoresize>
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
            default: () => null
        }
    },
    watch: {
        chartData: {
            immediate: true,
            handler (value) {
                this.options = this.createOptions(value)
            }
        }
    },
    data () {
        return {
            options: {}
        }
    },
    methods: {
        createOptions (chartData) {
            if (!chartData) return {}
            const categoryKey = chartData.mapping['Category Field']?.key
            const valueKey = chartData.mapping['Value Field']?.key
            const title = chartData.title
            var data = []
            if (chartData.data) {
                for (var row of chartData.data) {
                    data.push({ value: row[valueKey], name: row[categoryKey] })
                }
            }
            return {
                title: {
                    text: title,
                    left: 'center',
                    textStyle: {
                        overflow: 'break',
                        fontSize: 12
                    }
                },
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
                        radius: '30%',
                        label: {
                            show: true,
                            overflow: 'none',
                            distance: 5
                        }
                    }
                ]
            }
        }
    }
}
</script>
