<template>
    <div
        :id="'overview_' + this.overviewId + '_container_' + this.containerId + '_visualisation_' + this.visualisationId"
        class="visualisation"
        :style="styleObject"
    >
        <p :hidden="visualisationTitle === null">{{ visualisationTitle }}</p>
        <div :style="{ position: 'relative', 'max-height': '100%' }">
            <BarChart
                v-if="visualisationType === 'Bar Chart'"
                :data="visualisationData"
                :style="{ width: '100%', height: '100%' }"
            >
            </BarChart>
            <LineChart
                v-else-if="visualisationType === 'Line Chart'"
                :data="visualisationData"
            >

            </LineChart>
            <p
                v-else
            >
                {{ visualisationData }}
            </p>
        </div>
    </div>
</template>

<script>

import BarChart from '../../components/visualisations/charts/BarChart.vue'
import LineChart from '../../components/visualisations/charts/LineChart.vue'
// import Table from '../../components/visualisations/tables/Table.vue'

import { mapGetters, mapMutations } from 'vuex'

export default {
    name: 'Visualisation',
    components: {
        BarChart,
        LineChart
    },
    props: {
        overviewId: { type: Number, required: true },
        containerId: { type: Number, required: true },
        visualisationId: { type: Number, required: true }
    },
    computed: {
        visualisationData () {
            return this.createDataSet()
        },
        visualisationType () {
            return this.getVisualisationType()(this.overviewId, this.containerId, this.visualisationId)
        },
        styleObject () {
            var styleObject = {}
            if (this.position) {
                styleObject.position = 'absolute'
                styleObject.left = this.position[0] + '%'
                styleObject.right = (100 - this.position[1]) + '%'
                styleObject.top = this.position[2] + '%'
                styleObject.bottom = (100 - this.position[3]) + '%'
            }
            return styleObject
        },
        position () {
            const rawPosition = this.getVisualisationPosition()(this.overviewId, this.containerId, this.visualisationId)
            if (!rawPosition) return null
            return rawPosition.split(' ')
        },
        visualisationTitle () {
            return this.getVisualisationTitle()(this.overviewId, this.containerId, this.visualisationId)
        }
    },
    methods: {
        ...mapGetters('dashboard', { getVisualisationField: 'getVisualisationField', getVisualisationData: 'getVisualisationData', getVisualisationDataValues: 'getVisualisationDataValues', getVisualisationDataLabels: 'getVisualisationDataLabels', getVisualisationType: 'getVisualisationType', getVisualisationPosition: 'getVisualisationPosition', getVisualisationTitle: 'getVisualisationTitle' }),
        ...mapMutations('dashboard', ['setDashboard', 'setCurrentOverview']),
        createDataSet () {
            const visType = this.getVisualisationType()(this.overviewId, this.containerId, this.visualisationId)
            const values = this.getVisualisationDataValues()(this.overviewId, this.containerId, this.visualisationId)
            const labels = this.getVisualisationDataLabels()(this.overviewId, this.containerId, this.visualisationId)
            if (visType === 'Line Chart' || visType === 'Bar Chart') {
                var dataset = {
                    labels: labels,
                    datasets: [{
                        data: values,
                        backgroundColor: '#f87979',
                        label: 'Dataset Label'
                    }]
                }
                return dataset
            }
            return 0
        }
    }
}
</script>

<style>

</style>
