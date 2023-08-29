<template>
    <vue-echarts :option="createOptions(chartData)" autoresize>
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
    methods: {
        createOptions (chartData) {
            const title = chartData?.title
            const titleOptions = {
                text: title,
                left: 'center',
                textStyle: {
                    overflow: 'break',
                    fontSize: 12,
                    width: this.$parent.$el.clientWidth
                }
            }
            const currentValueField = chartData.mapping?.['Current Value Field']?.key
            const currentValueName = chartData.mapping?.['Current Value Field']?.name
            const targetValueField = chartData.mapping?.['Target Value Field']?.key
            const targetValueName = chartData.mapping?.['Target Value Field']?.name
            if (!currentValueField) return { title: titleOptions }
            const isPercentage = !targetValueField ?? chartData.options?.isPercentage === true

            const currentValue = chartData.data[0][currentValueField]
            const targetValue = isPercentage ? 100 : chartData.data[0][targetValueField]

            const currentValueNameRevised = currentValueName ?? [isPercentage ? 'Progress' : 'Current']

            const options = {
                title: titleOptions,
                xAxis: {
                    type: 'value',
                    min: 0,
                    max: targetValue,
                    show: false
                },
                yAxis: {
                    type: 'category',
                    data: currentValueNameRevised,
                    show: false
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    },
                    formatter: '<b>' + currentValueNameRevised + '</b> ' + currentValue + (isPercentage ? '%' : '<br /><b>' + (targetValueName ?? 'Target') + '</b> ' + targetValue)
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
                    height: this.$parent.$el.clientHeight / 10
                }
            }
            return options
        }
    }
}
</script>
