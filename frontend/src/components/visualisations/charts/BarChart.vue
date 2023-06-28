<template>
    <Bar :chartData="data" :options="options"/>
</template>

<script>
    import { Bar } from 'vue-chartjs'
    import { Chart, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

    Chart.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

    export default {
        name: 'BarChart',
        components: { Bar },
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
