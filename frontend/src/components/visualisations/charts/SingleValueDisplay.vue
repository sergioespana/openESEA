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
    name: 'SingleValueDisplay',
    components: {
        'vue-echarts': ECharts
    },
    props: {
        chartData: {
            chartData: {
                type: Object,
                default: () => null
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
            if (!chartData) return {}

            const field = chartData.mapping?.['Value Field']?.key
            const title = chartData.title
            const name = chartData.mapping?.['Value Field']?.name

            var value = 0
            for (var row of chartData.data) {
                if (row['Indicator Key'] === field) {
                    value += parseInt(row.Value)
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
                            text: (name ? name + ': ' : '') + value,
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

<style>

.p {
    display: block;
}
</style>
