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
            const field = mapping?.['Value Field']?.key
            if (!field) return { graphic: [titleOptions] }
            const name = mapping?.['Value Field']?.name

            const data = chartData.data
            const value = data[0][field] // Single value

            const options = {
                graphic: [
                    titleOptions,
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
