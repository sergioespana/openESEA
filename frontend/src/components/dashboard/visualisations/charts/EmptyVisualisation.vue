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
            return { graphic: [titleOptions] }
        }
    }
}
</script>
