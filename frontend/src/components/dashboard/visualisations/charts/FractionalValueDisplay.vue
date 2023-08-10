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
            chartData: {
                type: Object,
                required: true
            }
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
            const fractionalValueField = chartData.mapping?.['Fractional Value Field']?.key
            const totalValueField = chartData.mapping?.['Total Value Field']?.key
            const name = chartData.mapping?.['Fractional Value Field']?.name
            const title = chartData.title
            var fractionalValue = 0
            var totalValue = 0
            for (var row of chartData.data) {
                if (row['Indicator Key'] === fractionalValueField) {
                    fractionalValue += parseInt(row.Value)
                }
                if (row['Indicator Key'] === totalValueField) {
                    totalValue += parseInt(row.Value)
                }
            }

            const options = {
                graphic: [
                    {
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
                    },
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
