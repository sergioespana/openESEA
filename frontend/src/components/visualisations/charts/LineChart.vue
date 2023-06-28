<template>
    <Line :chartData="data" :options="options"/>
</template>

<script>
    import { Line } from 'vue-chartjs'
    import { Chart, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js'

    Chart.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

    export default {
        name: 'LineChart',
        components: { Line },
        props: {
            data: {
                type: Object,
                required: true
            },
            options: {
                type: Object,
                default: () => { return { responsive: true, maintainAspectRatio: true, plugins: { legend: { display: false, labels: { display: false } } } } }
            }
        }
    }
</script>
