<template>
    <div
        class="visualisation"
        v-on:click="onClick"
        :style="styleObject">
        <!-- <EditableText
            ref="title"
            :hidden="visualisationTitle === null"
            :initialValue="visualisationTitle"
            @enteredValue="(value) => updateTitle(value)">
        </EditableText> -->
        <component
            :is="visualisationComponent"
            :chartData="this.dataSet">
        </component>
    </div>
</template>

<script>

import { mapGetters, mapMutations } from 'vuex'

import EditableText from './EditableText.vue'
import SingleValueDisplay from '../../components/visualisations/charts/SingleValueDisplay.vue'
import FractionalValueDisplay from '../../components/visualisations/charts/FractionalValueDisplay.vue'
import ProgressBar from '../../components/visualisations/charts/ProgressBar.vue'
import PieChart from '../../components/visualisations/charts/PieChart.vue'
import BarChart from '../../components/visualisations/charts/BarChart.vue'
import LineChart from '../../components/visualisations/charts/LineChart.vue'

export default {
    name: 'Visualisation',
    components: {
        EditableText,
        SingleValueDisplay,
        FractionalValueDisplay,
        ProgressBar,
        PieChart,
        BarChart,
        LineChart
    },
    props: {
        overviewId: { type: Number, required: true },
        containerId: { type: Number, required: true },
        visualisationId: { type: Number, required: true }
    },
    data () {
        return {
            dataSet: null,
            visualisationType: null
        }
    },
    computed: {
        visualisationComponent () {
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
        },
        styleObject () {
            var styleObject = {}
            if (this.position) {
                styleObject.position = 'absolute'
                styleObject.left = this.position[0] + '%'
                styleObject.right = (100 - this.position[1]) + '%'
                styleObject.bottom = this.position[2] + '%'
                styleObject.top = (100 - this.position[3]) + '%'
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
    async mounted () {
        // Get visualisation type
        this.visualisationType = await this.getVisualisationType()(this.overviewId, this.containerId, this.visualisationId)

        // Create data set
        const dataSet = await this.createDataSet()

        // Add title to data set
        const visualisationTitle = await this.getVisualisationTitle()(this.overviewId, this.containerId, this.visualisationId)
        dataSet.title = visualisationTitle

        // Save and log dataset
        this.dataSet = dataSet
        console.log('Dataset:', dataSet)
    },
    methods: {
        ...mapGetters('dashboardEditing', { getSelectedVisualisation: 'getSelectedVisualisation' }),
        ...mapGetters('dashboardData', { getIndicatorData: 'getIndicatorData' }), // getSupplementaryData: 'getSupplementaryData' }),
        ...mapGetters('dashboardModel', { getVisualisationDataDisplay: 'getVisualisationDataDisplay', getVisualisationGroupingField: 'getVisualisationGroupingField', getVisualisationStackingField: 'getVisualisationStackingField', getVisualisationIndicators: 'getVisualisationIndicators', getVisualisationCategories: 'getVisualisationCategories', getVisualisationType: 'getVisualisationType', getVisualisationPosition: 'getVisualisationPosition', getVisualisationTitle: 'getVisualisationTitle' }),
        ...mapMutations('dashboardEditing', { setSelectedVisualisation: 'setSelectedVisualisation' }),
        ...mapMutations('dashboardModel', { setDashboard: 'setDashboard', setCurrentOverview: 'setCurrentOverview', setVisualisationTitle: 'setVisualisationTitle' }),
        async createSingleValueDisplayDataSet () {
            console.log('Creating Dataset\n\n\n')
            // Get data for all indicators
            const methodIndicatorsData = await this.getIndicatorData()()

            // Get indicator field for this visualisation
            const dataDisplay = await this.getVisualisationDataDisplay()(this.overviewId, this.containerId, this.visualisationId)
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
            const dataDisplay = await this.getVisualisationDataDisplay()(this.overviewId, this.containerId, this.visualisationId)
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
            const dataDisplay = await this.getVisualisationDataDisplay()(this.overviewId, this.containerId, this.visualisationId)
            const dataConfiguration = dataDisplay?.DataConfiguration
            const currentValueField = dataConfiguration['Current Value Field']?.Indicator
            const currentValueName = dataConfiguration['Current Value Field']?.Name
            const targetValueField = dataConfiguration['Target Value Field']?.Indicator
            const targetValueName = dataConfiguration['Target Value Field']?.Name
            const isPercentage = dataConfiguration.isPercentage || false
            const indicatorFields = [currentValueField].concat(targetValueField ? [targetValueField] : [])

            console.log(indicatorFields)

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
            const dataDisplay = await this.getVisualisationDataDisplay()(this.overviewId, this.containerId, this.visualisationId)
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
            const dataDisplay = await this.getVisualisationDataDisplay()(this.overviewId, this.containerId, this.visualisationId)
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
            const dataDisplay = await this.getVisualisationDataDisplay()(this.overviewId, this.containerId, this.visualisationId)
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
                    console.log('Filtering start', indicatorsData)
                    indicatorsData = indicatorsData.filter(el => filterValues.includes(el[filterField]))
                    console.log('Filtering end', indicatorsData)
                }
            }

            // Return data info
            const dataSet = { data: indicatorsData, mapping: mapping }
            return dataSet
        },
        async createDataSet () {
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
            /*
            if (this.visualisationType === 'Progress Bar') return await this.createDataSetProgressBar()
            const allIndicatorData = await this.getIndicatorData()()

            // Get indicators of current visualisation
            const indicators = await this.getVisualisationIndicators()(this.overviewId, this.containerId, this.visualisationId)
            console.log('Indicators:', indicators)
            // Retrieve indicator values from indicator data
            var values = []
            if (indicators) {
                for (var indicator of indicators) {
                    var indicatorData_ = allIndicatorData?.filter(el => el['Indicator Key'] === indicator)
                    const maxYear = max(indicatorData_.map(el => el.Year))
                    const GETLASTYEAR = true
                    if (GETLASTYEAR) {
                        indicatorData_ = indicatorData_?.filter(el => el.Year === maxYear)
                    }
                    const indicatorValues = indicatorData_.map(el => el.Value)
                    const value = indicatorValues[0]
                    values.push(value)
                }
            }

            // Get labels of current visualisation
            const categories = await this.getVisualisationCategories()(this.overviewId, this.containerId, this.visualisationId)

            var data = { values: values }
            if (categories) data.categories = categories
            if (this.visualisationType === 'Pie Chart') console.log('Pie data:', data)
            return data
            */
        },
        async updateTitle (title) {
            const payload = { overviewId: this.overviewId, containerId: this.containerId, visualisationId: this.visualisationId, title: title }
            await this.setVisualisationTitle(payload)
        },
        async onClick () {
            const payload = { overviewId: this.overviewId, containerId: this.containerId, visualisationId: this.visualisationId }
            await this.setSelectedVisualisation(payload)
            console.log(await this.getSelectedVisualisation()())
        }
    }
}
</script>
