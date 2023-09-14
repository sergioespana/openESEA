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
            const mapping = chartData?.mapping
            const currentValueField = mapping?.['Current Value Field']?.key
            const targetValueField = mapping?.['Target Value Field']?.key
            if (!currentValueField) return { title: titleOptions }
            const currentValueName = mapping?.['Current Value Field']?.name
            const targetValueName = mapping?.['Target Value Field']?.name
            const isPercentage = targetValueField === null || targetValueField === undefined || chartData.options?.isPercentage === true

            const currentValue = chartData.data[0][currentValueField]
            const targetValue = isPercentage ? 100 : chartData.data[0][targetValueField]

            const currentValueNameRevised = !currentValueName ? [isPercentage ? 'Progress' : 'Current'] : currentValueName
            const targetValueNameRevised = !targetValueName ? [isPercentage ? '' : 'Target'] : targetValueName
            var formattedText = '<b>' + currentValueNameRevised + '</b> ' + currentValue + (isPercentage ? '%' : '')
            if (!isPercentage) {
                formattedText += '<br />' +
                    '<b>' + targetValueNameRevised + '</b> ' + targetValue
            }

            const options = {
                title: titleOptions,
                tooltip: {
                    trigger: 'item',
                    axisPointer: {
                        type: 'shadow'
                    },
                    formatter: formattedText
                },
                series: [
                    {
                        type: 'pie',
                        radius: ['40%', '60%'],
                        center: ['50%', '60%'],
                        startAngle: 90,
                        data: [
                            {
                                value: currentValue,
                                label: {
                                    show: false
                                },
                                labelLine: {
                                    show: false
                                }
                            },
                            {
                                value: currentValue > targetValue ? 0 : targetValue - currentValue,
                                itemStyle: {
                                    color: 'rgba(180, 180, 180, 0.2)'
                                },
                                label: {
                                    show: false
                                },
                                labelLine: {
                                    show: false
                                },
                                cursor: 'unset',
                                emphasis: {
                                    disabled: true
                                }
                            }
                        ],
                        emphasis: {
                            label: {
                                show: false
                            }
                        }
                    }
                ],
                legend: {
                    show: false
                }
            }
            return options
        }
    }
}
</script>
