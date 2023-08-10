<template>
    <div class="visualisation" v-on:click="isClicked" :style="styleObject">
        <component v-if="dataSet" :is="visualisationComponent"
            :chartData="dataSet">
        </component>
        <div v-else class="loading-container">
            <ProgressSpinner class="progress-spinner">
            </ProgressSpinner>
        </div>
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

import SingleValueDisplay from './visualisations/charts/SingleValueDisplay.vue'
import FractionalValueDisplay from './visualisations/charts/FractionalValueDisplay.vue'
import ProgressBar from './visualisations/charts/ProgressBar.vue'
import PieChart from './visualisations/charts/PieChart.vue'
import BarChart from './visualisations/charts/BarChart.vue'
import LineChart from './visualisations/charts/LineChart.vue'

import ProgressSpinner from 'primevue/progressspinner'

export default {
    components: {
        SingleValueDisplay,
        FractionalValueDisplay,
        ProgressBar,
        PieChart,
        BarChart,
        LineChart,

        ProgressSpinner
    },
    props: {
        config: { type: Object, required: true }
    },
    data () {
        return {
            dataSet: null
        }
    },
    computed: {
        visualisation: {
            get () { return this.getVisualisation()(this.config) }
        },
        visualisationTitle: {
            get () { return this.getVisualisationTitle()(this.config) }
        },
        visualisationType: {
            get () { return this.getVisualisationType()(this.config) }
        },
        visualisationComponent: {
            get () {
                switch (this.visualisationType) {
                    case 'Single Value Display':
                        return 'SingleValueDisplay'
                    case 'Fractional Value Display':
                        return 'FractionalValueDisplay'
                    case 'Progress Bar':
                        return 'ProgressBar'
                    case 'Pie Chart':
                        return 'PieChart'
                    case 'Bar Chart':
                        return 'BarChart'
                    case 'Line Chart':
                        return 'LineChart'
                    default:
                        return 'p'
                }
            }
        },
        position: {
            get () { return this.getVisualisationPosition()(this.config) }
        },
        styleObject () {
            var styleObject = {}
            const position = this.position
            if (position) {
                styleObject.position = 'absolute'
                styleObject.left = position['X Start'].toString() + '%'
                styleObject.right = (100 - position['X End'].toString()) + '%'
                styleObject.bottom = position['Y Start'].toString() + '%'
                styleObject.top = (100 - position['Y End'].toString()) + '%'
            }
            return styleObject
        }
    },
    watch: {
        visualisation: {
            handler: 'createVisualisationDataSet',
            deep: true
        }
    },
    async created () {
        await this.createVisualisationDataSet()
    },
    methods: {
        ...mapGetters('dashboardData', ['getIndicatorData']),
        ...mapGetters('dashboardModel', ['getVisualisation', 'getVisualisationDataDisplay', 'getVisualisationGroupingField', 'getVisualisationStackingField', 'getVisualisationIndicators', 'getVisualisationCategories', 'getVisualisationType', 'getVisualisationPosition', 'getVisualisationTitle']),
        ...mapActions('dashboardModel', ['updateSelectionConfig']),
        async isClicked (event) {
            event.stopPropagation()
            await this.updateSelectionConfig(this.config)
        },
        async createVisualisationDataSet () {
            // Create data set
            this.dataSet = await this.createDataSet()
            // Add title to data set
            this.dataSet.title = this.visualisationTitle
        },
        async createDataSet () {
            // Create dataset based for this visualisation type
            switch (this.visualisationType) {
                case 'Single Value Display':
                    return await this.createSingleValueDisplayDataSet()
                case 'Fractional Value Display':
                    return await this.createFractionalValueDisplayDataSet()
                case 'Progress Bar':
                    return await this.createProgressBarDataSet()
                case 'Pie Chart':
                    return await this.createPieChartDataSet()
                case 'Bar Chart':
                    return await this.createBarChartDataSet()
                case 'Line Chart':
                    return await this.createLineChartDataSet()
                default:
                    return {}
            }
        },
        async createSingleValueDisplayDataSet () {
            // Get data for all indicators
            const methodIndicatorsData = await this.getIndicatorData()()

            // Get indicator field for this visualisation
            const dataDisplay = await this.getVisualisationDataDisplay()(this.config)
            const dataConfiguration = dataDisplay?.DataConfiguration
            const indicatorField = dataConfiguration['Value Field']?.Indicator
            const indicatorName = dataConfiguration['Value Field']?.Name
            const indicatorFields = [indicatorField]

            // Get data for this visualisation
            var indicatorsData = methodIndicatorsData?.filter(el => indicatorFields.includes(el['Indicator Key']))

            // Devise mapping for fields
            const mapping = {
                'Value Field': { key: indicatorField, name: indicatorName }
            }

            // Filter data
            const filters = dataConfiguration.Filters
            if (filters) {
                for (const filter of filters) {
                    const filterField = filter.Field
                    const filterValues = filter.Values
                    indicatorsData = indicatorsData.filter(el => filterValues.includes(el[filterField]))
                }
            }

            // Return data info
            const dataSet = { data: indicatorsData, mapping: mapping }
            return dataSet
        },
        async createFractionalValueDisplayDataSet () {
            // Get data for all indicators
            const methodIndicatorsData = await this.getIndicatorData()()

            // Get indicator field for this visualisation
            const dataDisplay = await this.getVisualisationDataDisplay()(this.config)
            const dataConfiguration = dataDisplay?.DataConfiguration
            const fractionalValueField = dataConfiguration['Fractional Value Field']?.Indicator
            const fractionalValueName = dataConfiguration['Fractional Value Field']?.Name
            const totalValueField = dataConfiguration['Total Value Field']?.Indicator
            const totalValueName = dataConfiguration['Total Value Field']?.Name
            const indicatorFields = [fractionalValueField, totalValueField]

            // Get data for this visualisation
            var indicatorsData = methodIndicatorsData?.filter(el => indicatorFields.includes(el['Indicator Key']))

            // Devise mapping for fields
            const mapping = {
                'Fractional Value Field': { key: fractionalValueField, name: fractionalValueName },
                'Total Value Field': { key: totalValueField, name: totalValueName }
            }

            // Filter data
            const filters = dataConfiguration.Filters
            if (filters) {
                for (const filter of filters) {
                    const filterField = filter.Field
                    const filterValues = filter.Values
                    indicatorsData = indicatorsData.filter(el => filterValues.includes(el[filterField]))
                }
            }

            // Return data info
            const dataSet = { data: indicatorsData, mapping: mapping }
            return dataSet
        },
        async createProgressBarDataSet () {
            // Get data for all indicators
            const methodIndicatorsData = await this.getIndicatorData()()

            // Get indicator field for this visualisation
            const dataDisplay = await this.getVisualisationDataDisplay()(this.config)
            const dataConfiguration = dataDisplay?.DataConfiguration
            const currentValueField = dataConfiguration['Current Value Field']?.Indicator
            const currentValueName = dataConfiguration['Current Value Field']?.Name
            const targetValueField = dataConfiguration['Target Value Field']?.Indicator
            const targetValueName = dataConfiguration['Target Value Field']?.Name
            const isPercentage = dataConfiguration.isPercentage || false
            const indicatorFields = [currentValueField].concat(targetValueField ? [targetValueField] : [])

            // Get data for this visualisation
            var indicatorsData = methodIndicatorsData?.filter(el => indicatorFields.includes(el['Indicator Key']))

            // Devise mapping for fields
            const mapping = {
                'Current Value Field': { key: currentValueField, name: currentValueName },
                'Target Value Field': { key: targetValueField, name: targetValueName }
            }

            // Filter data
            const filters = dataConfiguration.Filters
            if (filters) {
                for (const filter of filters) {
                    const filterField = filter.Field
                    const filterValues = filter.Values
                    indicatorsData = indicatorsData.filter(el => filterValues.includes(el[filterField]))
                }
            }

            // Return data info
            const dataSet = { data: indicatorsData, mapping: mapping, options: { isPercentage: isPercentage } }
            return dataSet
        },
        async createPieChartDataSet () {
            // Get data for all indicators
            const methodIndicatorsData = await this.getIndicatorData()()

            // Get data/fields configuration for this visualisation
            const dataDisplay = await this.getVisualisationDataDisplay()(this.config)
            const dataConfiguration = dataDisplay?.DataConfiguration
            const valueFieldIndicators = dataConfiguration['Value Field']?.Indicators
            const valueFieldName = dataConfiguration['Value Field']?.Name
            const valueFieldKey = valueFieldName ?? 'ValueField'
            const categoryFieldValues = dataConfiguration['Category Field']?.Values ?? valueFieldIndicators
            const categoryFieldName = dataConfiguration['Category Field']?.Name
            const categoryFieldKey = categoryFieldName ?? 'CategoryField'
            const indicatorFields = valueFieldIndicators

            // Get data for this visualisation
            var indicatorsData = methodIndicatorsData?.filter(el => indicatorFields.includes(el['Indicator Key']))

            // Sort data by given list of indicators
            const compareFunction = (a, b) => {
                const indexA = valueFieldIndicators.indexOf(a['Indicator Key'])
                const indexB = valueFieldIndicators.indexOf(b['Indicator Key'])
                return indexA - indexB
            }
            indicatorsData.sort(compareFunction)

            // Map category values to the indicator keys
            if (categoryFieldValues) {
                for (var indicatorData of indicatorsData) {
                    const value = indicatorData.Value
                    indicatorData[valueFieldKey] = value
                    const categoryIndex = indicatorFields.indexOf(indicatorData['Indicator Key'])
                    if (categoryIndex >= 0) {
                        const category = categoryFieldValues[categoryIndex]
                        indicatorData[categoryFieldKey] = category
                    }
                }
            }

            // Devise mapping for fields
            const mapping = {
                'Value Field': { key: valueFieldKey, name: valueFieldName },
                'Category Field': { key: categoryFieldKey, name: categoryFieldName }
            }

            // Filter data
            const filters = dataConfiguration.Filters
            if (filters) {
                for (const filter of filters) {
                    const filterField = filter.Field
                    const filterValues = filter.Values
                    indicatorsData = indicatorsData.filter(el => filterValues.includes(el[filterField]))
                }
            }

            // Return data info
            const dataSet = { data: indicatorsData, mapping: mapping }
            return dataSet
        },
        async createBarChartDataSet () {
            // Get data for all indicators
            const methodIndicatorsData = await this.getIndicatorData()()

            // Get data/fields configuration for this visualisation
            const dataDisplay = await this.getVisualisationDataDisplay()(this.config)
            const dataConfiguration = dataDisplay?.DataConfiguration
            const valueFieldIndicators = dataConfiguration['Value Field']?.Indicators
            const valueFieldName = dataConfiguration['Value Field']?.Name
            const valueFieldKey = valueFieldName ?? 'ValueField'
            const categoryFieldValues = dataConfiguration['Category Field']?.Values
            const categoryFieldName = dataConfiguration['Category Field']?.Name
            const categoryFieldKey = categoryFieldName ?? 'CategoryField'
            const indicatorFields = valueFieldIndicators

            // Get data for this visualisation
            var indicatorsData = methodIndicatorsData?.filter(el => indicatorFields.includes(el['Indicator Key']))

            // Map values to value field
            for (const indicatorData of indicatorsData) {
                const value = indicatorData.Value
                indicatorData[valueFieldKey] = value
                // delete indicatorData.Value
            }

            // Map category values to the indicator keys and sort by category
            if (categoryFieldValues) {
                for (const indicatorData of indicatorsData) {
                    const categoryIndex = indicatorFields.indexOf(indicatorData['Indicator Key'])
                    if (categoryIndex >= 0) {
                        const category = categoryFieldValues[categoryIndex]
                        indicatorData[categoryFieldKey] = category
                    }
                }

                // Sort data by given list of indicators
                const compareFunction = (a, b) => {
                    const indexA = categoryFieldValues.indexOf(a[categoryFieldKey])
                    const indexB = categoryFieldValues.indexOf(b[categoryFieldKey])
                    return indexA - indexB
                }
                indicatorsData.sort(compareFunction)
            }

            // Devise mapping for fields
            const mapping = {
                'Value Field': { key: valueFieldKey, name: valueFieldName },
                'Category Field': { key: categoryFieldKey, name: categoryFieldName }
            }

            // Filter data
            const filters = dataConfiguration.Filters
            if (filters) {
                for (const filter of filters) {
                    const filterField = filter.Field
                    const filterValues = filter.Values
                    indicatorsData = indicatorsData.filter(el => filterValues.includes(el[filterField]))
                }
            }

            // Return data info
            const dataSet = { data: indicatorsData, mapping: mapping }
            return dataSet
        },
        async createLineChartDataSet () {
            // Get data for all indicators
            const methodIndicatorsData = await this.getIndicatorData()()

            // Get data/fields configuration for this visualisation
            const dataDisplay = await this.getVisualisationDataDisplay()(this.config)
            const dataConfiguration = dataDisplay?.DataConfiguration
            const valueFieldIndicators = dataConfiguration['Value Field']?.Indicators
            const valueFieldName = dataConfiguration['Value Field']?.Name
            const valueFieldKey = valueFieldName ?? 'ValueField'
            const categoryFieldValues = dataConfiguration['Category Field']?.Values
            const categoryFieldName = dataConfiguration['Category Field']?.Name
            const categoryFieldKey = categoryFieldName ?? 'CategoryField'
            const indicatorFields = valueFieldIndicators

            // Get data for this visualisation
            var indicatorsData = methodIndicatorsData?.filter(el => indicatorFields.includes(el['Indicator Key']))

            // Map values to value field
            for (const indicatorData of indicatorsData) {
                const value = indicatorData.Value
                indicatorData[valueFieldKey] = value
                // delete indicatorData.Value // Somehow does not work?
            }

            // Map category values to the indicator keys and sort by category
            if (categoryFieldValues) {
                for (var indicatorData_ of indicatorsData) {
                    const categoryIndex = indicatorFields.indexOf(indicatorData_['Indicator Key'])
                    if (categoryIndex >= 0) {
                        const category = categoryFieldValues[categoryIndex]
                        indicatorData_[categoryFieldKey] = category
                    }
                }

                // Sort data by given list of indicators
                const compareFunction = (a, b) => {
                    const indexA = categoryFieldValues.indexOf(a[categoryFieldKey])
                    const indexB = categoryFieldValues.indexOf(b[categoryFieldKey])
                    return indexA - indexB
                }
                indicatorsData.sort(compareFunction)
            } else {
                indicatorsData.sort((a, b) => a[categoryFieldKey] - b[categoryFieldKey])
            }

            // Devise mapping for fields
            const mapping = {
                'Value Field': { key: valueFieldKey, name: valueFieldName },
                'Category Field': { key: categoryFieldKey, name: categoryFieldName }
            }

            // Filter data
            const filters = dataConfiguration.Filters
            if (filters) {
                for (const filter of filters) {
                    const filterField = filter.Field
                    const filterValues = filter.Values
                    // console.log('Filtering start', indicatorsData)
                    indicatorsData = indicatorsData.filter(el => filterValues.includes(el[filterField]))
                    // console.log('Filtering end', indicatorsData)
                }
            }

            // Return data info
            const dataSet = { data: indicatorsData, mapping: mapping }
            return dataSet
        }
    }
}
</script>

<style>
.loading-container {
  display: flex;
  align-items: center;
  justify-content: center;
  /* Set the desired dimensions for the container */
  width: 100%;
  height: 100%;
}
.progress-spinner {
    max-height: 100%;
    max-width: 100%;
}
</style>
