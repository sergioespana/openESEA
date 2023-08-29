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
        ...mapGetters('dashboardData', ['getIndicatorData', 'getIndicatorDataSet', 'getVisualisationDatasets']),
        ...mapActions('dashboardData', ['saveVisualisationDataset']),
        ...mapGetters('dashboardModel', ['getVisualisation', 'getDataDisplay', 'getDataConfiguration', 'getValueField', 'getFractionalValueField', 'getTotalValueField', 'getCurrentValueField', 'getTargetValueField', 'getCategoryField', 'getGroupingField', 'getStackingField', 'getVisualisationType', 'getVisualisationPosition', 'getVisualisationTitle']),
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

            // Save dataset
            await this.saveVisualisationDataset({ config: this.config, dataset: this.dataSet.data })
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
        async applyFilters (dataSet, filters) {
            if (filters && dataSet && dataSet[0]) {
                for (const filter of filters) {
                    const filterField = filter.Field
                    if (!Object.keys(dataSet[0]).includes(filterField)) continue
                    const filterValues = filter.Values
                    dataSet = dataSet.filter(row => filterValues.includes(row[filterField]))
                }
            }
            return dataSet
        },
        async getFieldInfo (field) {
            if (!field) return null
            if (field.Indicator) {
                return await this.getIndicatorInfo(field)
            }
            if (field.Indicators) {
                return await this.getIndicatorsInfo(field)
            }
            if (field.Values) {
                return await this.getValuesInfo(field)
            }
            // When no values -> name
            if (field.Name) {
                return await this.getNamedFieldInfo(field)
            }
            return null
        },
        async getIndicatorInfo (field) {
            const fieldIndicator = field.Indicator
            const fieldName = field.Name

            // Get dataset for the current value field indicator
            const indicatorDataSet = await this.getIndicatorDataSet()(fieldIndicator)
            const indicatorName = indicatorDataSet.name
            const indicatorData = indicatorDataSet.data

            // Devise mapping for field
            const fieldKey = indicatorName
            const info = { key: fieldKey, name: fieldName, data: indicatorData, type: 'Indicator' }
            return info
        },
        async getIndicatorsInfo (field) {
            const fieldIndicators = field.Indicators
            const fieldName = field.Name
            const fieldKey = fieldName ?? 'Value Field'

            var dataset = []
            for (const fieldIndicator of fieldIndicators) {
                // Get dataset for the current value field indicator
                const indicatorDataSet = await this.getIndicatorDataSet()(fieldIndicator)
                const indicatorName = indicatorDataSet.name
                const indicatorData = indicatorDataSet.data

                // Collect data together with indicator name
                const indicatorFieldKey = indicatorName
                for (const row of indicatorData) {
                    var rowInfo = {}
                    rowInfo.Year = row.Year
                    rowInfo['Indicator Key'] = fieldIndicator
                    // rowInfo['Indicator Name'] = indicatorFieldKey
                    rowInfo[fieldKey] = row[indicatorFieldKey]
                    dataset.push(rowInfo)
                }
            }
            // Devise mapping for field
            const info = { key: fieldKey, name: fieldName, data: dataset, type: 'Indicators' }
            return info
        },
        async getValuesInfo (field) {
            const fieldValues = field.Values
            const fieldName = field.Name
            const fieldKey = fieldName ?? 'Category Field'

            var dataset = []
            for (const fieldValue of fieldValues) {
                var rowInfo = {}
                rowInfo[fieldKey] = fieldValue
                dataset.push(rowInfo)
            }
            // Devise mapping for field
            const info = { key: fieldKey, name: fieldName, data: dataset, type: 'Values' }
            return info
        },
        async getNamedFieldInfo (field) {
            const fieldName = field.Name
            const fieldKey = fieldName ?? 'Named Field'

            var dataset = []

            // Devise mapping for field
            const info = { key: fieldKey, name: fieldName, data: dataset, type: 'Named Field' }
            return info
        },
        async createSingleValueDisplayDataSet () {
            // Record for single value
            var dataset = []
            // Values per field
            var valueFields = []
            // Mapping for fields
            var mapping = {}
            // Get filters
            const dataConfiguration = await this.getDataConfiguration()(this.config)
            const visualisationFilters = dataConfiguration.Filters

            // Get value field info
            const valueField = await this.getValueField()(this.config)
            const valueFieldInfo = await this.getFieldInfo(valueField)
            if (valueFieldInfo !== null) {
                // Devise mapping for value field
                mapping['Value Field'] = { key: valueFieldInfo.key, name: valueFieldInfo.name }

                // Filter data and add data to list
                const filteredValueIndicatorData = await this.applyFilters(valueFieldInfo.data, visualisationFilters)
                valueFields.push({ key: valueFieldInfo.key, data: filteredValueIndicatorData })
            }

            // Create dataset
            var valuesRecord = {}
            for (const valueField of valueFields) {
                const key = valueField.key
                const data = valueField.data
                var value = 0
                for (const row of data) {
                    value += parseInt(row[key])
                }
                valuesRecord[key] = value
            }
            dataset.push(valuesRecord)

            // Return data info
            const dataSet = { data: dataset, mapping: mapping }
            return dataSet
        },
        async createFractionalValueDisplayDataSet () {
            // Record for single value
            var dataset = []
            // Values per field
            var valueFields = []
            // Mapping for fields
            var mapping = {}
            // Get filters
            const dataConfiguration = await this.getDataConfiguration()(this.config)
            const visualisationFilters = dataConfiguration.Filters

            // Get fractional value field
            const fractionalValueField = await this.getFractionalValueField()(this.config)
            const fractionalValueFieldInfo = await this.getFieldInfo(fractionalValueField)
            if (fractionalValueFieldInfo !== null) {
                // Devise mapping for value field
                mapping['Fractional Value Field'] = { key: fractionalValueFieldInfo.key, name: fractionalValueFieldInfo.name }

                // Filter data and add data to list
                const filteredFractionalValueIndicatorData = await this.applyFilters(fractionalValueFieldInfo.data, visualisationFilters)
                valueFields.push({ key: fractionalValueFieldInfo.key, data: filteredFractionalValueIndicatorData })
            }

            // Get total value field
            const totalValueField = await this.getTotalValueField()(this.config)
            const totalValueFieldInfo = await this.getFieldInfo(totalValueField)
            if (totalValueFieldInfo !== null) {
                // Devise mapping for value field
                mapping['Total Value Field'] = { key: totalValueFieldInfo.key, name: totalValueFieldInfo.name }

                // Filter data and add data to list
                const filteredTotalValueIndicatorData = await this.applyFilters(totalValueFieldInfo.data, visualisationFilters)
                valueFields.push({ key: totalValueFieldInfo.key, data: filteredTotalValueIndicatorData })
            }

            // Create dataset
            var valuesRecord = {}
            for (const valueField of valueFields) {
                const key = valueField.key
                const data = valueField.data
                var value = 0
                for (const row of data) {
                    value += parseInt(row[key])
                }
                valuesRecord[key] = value
            }
            dataset.push(valuesRecord)

            // Return data info
            const dataSet = { data: dataset, mapping: mapping }
            return dataSet
        },
        async createProgressBarDataSet () {
            // Record for single value
            var dataset = []
            // Values per field
            var valueFields = []
            // Mapping for fields
            var mapping = {}
            // Get filters
            const dataConfiguration = await this.getDataConfiguration()(this.config)
            const visualisationFilters = dataConfiguration.Filters

            // Get fractional value field
            const currentValueField = await this.getCurrentValueField()(this.config)
            const currentValueFieldInfo = await this.getFieldInfo(currentValueField)
            if (currentValueFieldInfo !== null) {
                // Devise mapping for value field
                mapping['Current Value Field'] = { key: currentValueFieldInfo.key, name: currentValueFieldInfo.name }

                // Filter data and add data to list
                const filteredCurrentValueIndicatorData = await this.applyFilters(currentValueFieldInfo.data, visualisationFilters)
                valueFields.push({ key: currentValueFieldInfo.key, data: filteredCurrentValueIndicatorData })
            }

            // Get target value field
            const targetValueField = await this.getTargetValueField()(this.config)
            const targetValueFieldInfo = await this.getFieldInfo(targetValueField)
            if (targetValueFieldInfo !== null) {
                // Devise mapping for value field
                mapping['Target Value Field'] = { key: targetValueFieldInfo.key, name: targetValueFieldInfo.name }

                // Filter data and add data to list
                const filteredTargetValueIndicatorData = await this.applyFilters(targetValueFieldInfo.data, visualisationFilters)
                valueFields.push({ key: targetValueFieldInfo.key, data: filteredTargetValueIndicatorData })
            }

            // Create dataset
            var valuesRecord = {}
            for (const valueField of valueFields) {
                const key = valueField.key
                const data = valueField.data
                var value = 0
                for (const row of data) {
                    value += parseInt(row[key])
                }
                valuesRecord[key] = value
            }
            dataset.push(valuesRecord)

            // Return data info
            const dataSet = { data: dataset, mapping: mapping }
            return dataSet
        },
        async createPieChartDataSet () {
            // Record for single value
            var dataset = []
            // Values per field
            var valueFields = []
            // Groupings per field
            var groupingFields = []
            // Mapping for fields
            var mapping = {}
            // Get filters
            const dataConfiguration = await this.getDataConfiguration()(this.config)
            const visualisationFilters = dataConfiguration.Filters

            // Get value field
            const valueField = await this.getValueField()(this.config)
            const valueFieldInfo = await this.getFieldInfo(valueField)
            console.log(valueFieldInfo)
            if (valueFieldInfo !== null) {
                // Devise mapping for value field
                mapping['Value Field'] = { key: valueFieldInfo.key, name: valueFieldInfo.name }

                // Filter data and add data to list
                const filteredValueIndicatorData = await this.applyFilters(valueFieldInfo.data, visualisationFilters)
                valueFields.push({ key: valueFieldInfo.key, data: filteredValueIndicatorData })
            }

            // Get category field
            const categoryField = await this.getCategoryField()(this.config)
            const categoryFieldInfo = await this.getFieldInfo(categoryField)
            console.log(categoryFieldInfo)
            if (categoryFieldInfo !== null) {
                // Devise mapping for category field
                mapping['Category Field'] = { key: categoryFieldInfo.key, name: categoryFieldInfo.name }

                // Filter data and add data to list
                const filteredCategoryData = await this.applyFilters(valueFieldInfo.data, visualisationFilters)
                groupingFields.push({ key: categoryFieldInfo.key, data: filteredCategoryData })
            }

            // Map list of category values to list of indicators
            if (categoryFieldInfo.type === 'Values' && valueFieldInfo.type === 'Indicators') {
                const valueFieldIndicators = valueField.Indicators
                const categoryValues = categoryField.Values
                var categoryMapping = {}
                for (let i = 0; i < valueFieldIndicators.length; i++) {
                    const valueFieldIndicator = valueFieldIndicators[i]
                    const categoryValue = categoryValues[i]
                    categoryMapping[valueFieldIndicator] = categoryValue
                }
                const valueData = valueFieldInfo.data
                for (var valueDataRow of valueData) {
                    const valueFieldIndicator = valueDataRow['Indicator Key']
                    const categoryValue = categoryMapping[valueFieldIndicator]
                    valueDataRow[categoryFieldInfo.key] = categoryValue
                    delete valueDataRow['Indicator Key']
                }
            }
            console.log(valueFieldInfo.data)

            // Create dataset
            var accumulatedRows = []
            for (const valueField of valueFields) {
                const valueKey = valueField.key
                const valueData = valueField.data
                for (const row of valueData) {
                    for (const accumulatedRow of accumulatedRows) {
                        var sameGrouping = true
                        for (const groupingField of groupingFields) {
                            if (accumulatedRow[groupingField.key] !== row[groupingField.key]) {
                                sameGrouping = false
                                break
                            }
                        }
                        if (sameGrouping) {
                            accumulatedRow[valueKey] = row[valueKey]
                            break
                        }
                    }
                    var newGroupingRow = {}
                    newGroupingRow[valueKey] = row[valueKey]
                    for (const groupingField of groupingFields) {
                        newGroupingRow[groupingField.key] = row[groupingField.key]
                    }
                    accumulatedRows.push(newGroupingRow)
                }
            }
            dataset = accumulatedRows
            console.log(accumulatedRows)

            // Return data info
            const dataSet = { data: dataset, mapping: mapping }
            return dataSet
        },
        async createPieChartDataSet2 () {
            // Get data for all indicators
            const methodIndicatorsData = await this.getIndicatorData()()

            // Get data/fields configuration for this visualisation
            const dataDisplay = await this.getDataDisplay()(this.config)
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
            indicatorsData = await this.applyFilters(indicatorsData, dataConfiguration.Filters)

            // Return data info
            const dataSet = { data: indicatorsData, mapping: mapping }
            return dataSet
        },
        async createBarChartDataSet () {
            // Get data for all indicators
            const methodIndicatorsData = await this.getIndicatorData()()

            // Get data/fields configuration for this visualisation
            const dataDisplay = await this.getDataDisplay()(this.config)
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
            indicatorsData = await this.applyFilters(indicatorsData, dataConfiguration.Filters)

            // Return data info
            const dataSet = { data: indicatorsData, mapping: mapping }
            return dataSet
        },
        async createLineChartDataSet () {
            // Get data for all indicators
            const methodIndicatorsData = await this.getIndicatorData()()

            // Get data/fields configuration for this visualisation
            const dataDisplay = await this.getDataDisplay()(this.config)
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
            indicatorsData = await this.applyFilters(indicatorsData, dataConfiguration.Filters)

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
