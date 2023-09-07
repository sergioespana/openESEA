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
            chartData: {
                type: Object,
                required: true
            }
        }
    },
    methods: {
        createOptions (chartData) {
            const title = chartData.title
            const titleOptions = {
                type: 'text',
                left: 'center',
                top: '0%',
                    silent: true,
                style: {
                    text: title,
                    fontSize: 12,
                    fontWeight: 'bold',
                    fill: '#000'
                }
            }
            const mapping = chartData?.mapping
            if (!mapping) return { graphic: [titleOptions] }
            const fractionalValueField = mapping?.['Fractional Value Field']?.key
            const totalValueField = mapping?.['Total Value Field']?.key
            if (!totalValueField || !fractionalValueField) return { graphic: [titleOptions] }
            const fractionalValueFieldName = mapping?.['Fractional Value Field']?.name
            const totalValueFieldName = mapping?.['Total Value Field']?.name
            const name = (fractionalValueFieldName && totalValueFieldName) ? fractionalValueFieldName + ' / ' + totalValueFieldName : ''

            const fractionalValue = chartData.data[0][fractionalValueField]
            const totalValue = chartData.data[0][totalValueField]

            const options = {
                graphic: [
                    titleOptions,
                    {
                        type: 'text',
                        left: 'center',
                        top: '40%',
                        style: {
                            text: (name ? name + ': ' : '') + fractionalValue + ' / ' + totalValue,
                            fontSize: 20,
                            fontWeight: 'normal',
                            fill: '#888'
                        }
                    }
                ]
            }
            return options
        }
    }
}
</script>
