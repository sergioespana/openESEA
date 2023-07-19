<template>
    <vue-echarts :option="this.options" autoresize>
    </vue-echarts>
</template>

<script>
import 'echarts'
import ECharts from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'

use([CanvasRenderer])

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
            console.log('Chart Data!!', chartData)
            if (!chartData) return {}
            const currentValueField = chartData.mapping?.['Current Value Field']?.key
            const currentValueName = chartData.mapping?.['Current Value Field']?.name
            const targetValueField = chartData.mapping?.['Target Value Field']?.key
            const targetValueName = chartData.mapping?.['Target Value Field']?.name
            const isPercentage = chartData.options?.isPercentage
            var currentValue = null
            var targetValue = null
            if (chartData.data) {
                for (var row of chartData.data) {
                    if (row['Indicator Key'] === currentValueField) {
                        currentValue += parseInt(row.Value)
                    }
                    if (row['Indicator Key'] === targetValueField) {
                        targetValue += parseInt(row.Value)
                    }
                }
            }
            if (isPercentage && !targetValue) targetValue = 100
            return {
                title: {
                    text: chartData?.title,
                    left: 'center',
                    textStyle: {
                        overflow: 'break',
                        fontSize: 12,
                        width: this.$parent.$el.clientWidth
                    }
                },
                xAxis: {
                    type: 'value',
                    min: 0,
                    max: targetValue,
                    show: false
                },
                yAxis: {
                    type: 'category',
                    data: currentValueName ?? [isPercentage ? 'Progress' : 'Current'],
                    show: false
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    },
                    formatter: '<b>{b}</b> {c}' + (isPercentage ? '%' : '<br /><b>' + (targetValueName ?? 'Target') + '</b> ' + targetValue)
                },
                series: [
                    {
                        data: [currentValue],
                        type: 'bar',
                        showBackground: true,
                        backgroundStyle: {
                            color: 'rgba(180, 180, 180, 0.2)'
                        },
                        barWidth: '100%'
                    }
                ],
                grid: {
                    height: this.$parent.$el.clientWidth / 20
                }
            }
        }
    }
}
</script>
