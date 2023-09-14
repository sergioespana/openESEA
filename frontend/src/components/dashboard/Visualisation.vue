<template>
    <div class="visualisation" v-on:click="isClicked" :style="styleObject">
        <!-- Display visualisation of type `visualisationComponent` and giving the `dataSet` object when this is loaded -->
        <component v-if="dataSet" :is="visualisationComponent"
            :chartData="dataSet">
        </component>
        <!-- While waiting, display progress spinner -->
        <div v-else class="loading-container">
            <ProgressSpinner class="progress-spinner">
            </ProgressSpinner>
        </div>
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

import EmptyVisualisation from './visualisations/charts/EmptyVisualisation.vue'
import SingleValueDisplay from './visualisations/charts/SingleValueDisplay.vue'
import FractionalValueDisplay from './visualisations/charts/FractionalValueDisplay.vue'
import ProgressBar from './visualisations/charts/ProgressBar.vue'
import RadialProgressBar from './visualisations/charts/RadialProgressBar.vue'
import PieChart from './visualisations/charts/PieChart.vue'
import BarChart from './visualisations/charts/BarChart.vue'
import GroupedBarChart from './visualisations/charts/GroupedBarChart.vue'
import StackedBarChart from './visualisations/charts/StackedBarChart.vue'
import LineChart from './visualisations/charts/LineChart.vue'
import Table from './visualisations/tables/Table.vue'

import ProgressSpinner from 'primevue/progressspinner'

export default {
    components: {
        EmptyVisualisation,
        SingleValueDisplay,
        FractionalValueDisplay,
        ProgressBar,
        RadialProgressBar,
        PieChart,
        BarChart,
        GroupedBarChart,
        StackedBarChart,
        LineChart,
        Table,

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
                    case 'Radial Progress Bar':
                        return 'RadialProgressBar'
                    case 'Pie Chart':
                        return 'PieChart'
                    case 'Bar Chart':
                        return 'BarChart'
                    case 'Grouped Bar Chart':
                        return 'GroupedBarChart'
                    case 'Stacked Bar Chart':
                        return 'StackedBarChart'
                    case 'Line Chart':
                        return 'LineChart'
                    case 'Table':
                        return 'Table'
                    default:
                        return 'EmptyVisualisation'
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
        ...mapGetters('dashboardModel', ['getOverviewFilters', 'getVisualisation', 'getDataDisplay', 'getDataConfiguration', 'getVisualisationFilters', 'getValueField', 'getFractionalValueField', 'getTotalValueField', 'getCurrentValueField', 'getTargetValueField', 'getCategoryField', 'getGroupingField', 'getStackingField', 'getCategoryLimit', 'getSideways', 'getVisualisationType', 'getVisualisationPosition', 'getVisualisationTitle']),
        ...mapActions('dashboardModel', ['updateSelectionConfig']),
        async isClicked (event) {
            event.stopPropagation()
            console.log('Click!')
            console.log(this.config)
            await this.updateSelectionConfig(this.config)
        },
        isEmpty (string) { return string === null || string === undefined || string === '' },
        // Create dataset, add title and save the dataset
        async createVisualisationDataSet () {
            // Create data set
            this.dataSet = await this.createDataSet() // { mapping: ..., data: ... }
            // Add title to data set
            this.dataSet.title = this.visualisationTitle
            // Add category limit to dataset
            this.dataSet.categoryLimit = await this.getCategoryLimit()(this.config)
            // Add sideways indicator to dataset
            this.dataSet.sideways = await this.getSideways()(this.config)
            // Save dataset for sending to rl model
            await this.saveVisualisationDataset({ config: this.config, dataset: this.dataSet.data })
        },
        // For each visualisation type create the corresponding dataset
        async createDataSet () {
            // Create dataset based for this visualisation type
            switch (this.visualisationType) {
                case 'Single Value Display':
                    return await this.createSingleValueDisplayDataSet()
                case 'Fractional Value Display':
                    return await this.createFractionalValueDisplayDataSet()
                case 'Progress Bar':
                case 'Radial Progress Bar':
                    return await this.createProgressBarDataSet()
                case 'Pie Chart':
                case 'Bar Chart':
                case 'Line Chart':
                case 'Table':
                    return await this.createCategoryValueDataSet()
                case 'Grouped Bar Chart':
                case 'Stacked Bar Chart':
                    return await this.createGroupedCategoryValueDataSet()
                default:
                    return {}
            }
        },
        // Get data/info for the indicator fields/values/named field
        async getFieldInfo (fieldName, type) {
            const field = await this.getField(fieldName)
            if (field?.Indicator) {
                return await this.getIndicatorInfo(field)
            }
            if (field?.Indicators) {
                return await this.getIndicatorsInfo(field)
            }
            if (field?.Values) {
                return await this.getValuesInfo(field)
            }
            if (field?.['Named Field']) { // && type !== 'Indicator' && type !== 'Indicators') {
                return await this.getNamedFieldInfo(field)
            }
            return null
        },
        async getField (fieldName) {
            switch (fieldName) {
                case 'Value Field':
                    return await this.getValueField()(this.config)
                case 'Fractional Value Field':
                    return await this.getFractionalValueField()(this.config)
                case 'Total Value Field':
                    return await this.getTotalValueField()(this.config)
                case 'Current Value Field':
                    return await this.getCurrentValueField()(this.config)
                case 'Target Value Field':
                    return await this.getTargetValueField()(this.config)
                case 'Category Field':
                    return await this.getCategoryField()(this.config)
                case 'Grouping Field':
                    return await this.getGroupingField()(this.config)
                case 'Stacking Field':
                    return await this.getStackingField()(this.config)
                case null:
                case '':
                default:
                    return null
            }
        },
        async getIndicatorInfo (field) {
            const fieldIndicator = field.Indicator
            const fieldName = field.Name

            // Get dataset for the current value field indicator
            const indicatorDataSet = await this.getIndicatorDataSet()(fieldIndicator)
            const indicatorName = indicatorDataSet.name
            const indicatorData = await this.applyVisualisationFilters(indicatorDataSet.data)

            // Devise mapping for field
            const fieldKey = indicatorName
            const info = { key: fieldKey, name: fieldName, data: indicatorData, type: 'Indicator' }
            return info
        },
        async getIndicatorsInfo (field) {
            const fieldIndicators = field.Indicators
            const fieldName = field.Name
            const fieldKey = this.isEmpty(fieldName) ? 'Value Field' : fieldName

            var dataset = []
            for (const fieldIndicator of fieldIndicators) {
                // Get dataset for the current value field indicator
                const indicatorDataSet = await this.getIndicatorDataSet()(fieldIndicator)
                const indicatorName = indicatorDataSet.name
                const indicatorData = await this.applyVisualisationFilters(indicatorDataSet.data)

                // Collect data together with indicator name
                const indicatorFieldKey = indicatorName
                for (const row of indicatorData) {
                    var rowInfo = {}
                    rowInfo['Indicator Key'] = fieldIndicator
                    rowInfo[fieldKey] = row[indicatorFieldKey]
                    rowInfo.Year = row.Year
                    dataset.push(rowInfo)
                }
            }

            // Devise mapping for field
            const info = { key: fieldKey, name: fieldName, data: dataset, type: 'Indicators', indicators: fieldIndicators }
            return info
        },
        async getValuesInfo (field) {
            const fieldValues = field.Values
            const fieldName = field.Name
            const fieldKey = this.isEmpty(fieldName) ? 'Category Field' : fieldName

            var dataset = []
            for (const fieldValue of fieldValues) {
                var rowInfo = {}
                rowInfo[fieldKey] = fieldValue
                dataset.push(rowInfo)
            }

            // Devise mapping for field
            const info = { key: fieldKey, name: fieldName, data: dataset, type: 'Values', values: fieldValues }
            return info
        },
        async getNamedFieldInfo (field) {
            const fieldKey = field['Named Field']
            const fieldName = field.Name

            var dataset = []

            // Devise mapping for field
            const info = { key: fieldKey, name: fieldName, data: dataset, type: 'Named Field' }
            return info
        },
        // Apply filters to a dataset
        async applyVisualisationFilters (dataSet) {
            const filters = await this.collectVisualisationFilters()
            if (filters && dataSet?.[0]) {
                for (const filter of filters) {
                    const filterField = filter.Field
                    if (!Object.keys(dataSet[0]).includes(filterField)) continue
                    const filterValues = filter.Values
                    dataSet = dataSet.filter(row => filterValues.includes(row[filterField]))
                }
            }
            return dataSet
        },
        // Collect filters
        async collectVisualisationFilters () {
            // Get filters
            const overviewFilters = await this.getOverviewFilters()(this.config) ?? []
            const visualisationFilters = await this.getVisualisationFilters()(this.config) ?? []
            // Combine filters
            const combinedFilters = overviewFilters.concat(visualisationFilters)
            return combinedFilters
        },
        async createSingleValueDisplayDataSet () {
            // Record for single value
            var dataset = []
            // Values per field
            var valueFields = []
            // Mapping for fields
            var mapping = {}

            // Get value field info
            const valueFieldInfo = await this.getFieldInfo('Value Field') //, 'Indicator')
            if (valueFieldInfo !== null) {
                // Devise mapping for value field
                mapping['Value Field'] = { key: valueFieldInfo.key, name: valueFieldInfo.name }
                // Add data to list
                valueFields.push({ key: valueFieldInfo.key, data: valueFieldInfo.data })
            }

            // Create dataset
            var valuesRecord = {}
            for (const valueField of valueFields) {
                const key = valueField.key
                const data = valueField.data
                var value = 0
                for (const row of data) {
                    value += Number(row[key])
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

            // Get fractional value field
            const fractionalValueFieldInfo = await this.getFieldInfo('Fractional Value Field') // , 'Indicator')
            if (fractionalValueFieldInfo !== null) {
                // Devise mapping for value field
                mapping['Fractional Value Field'] = { key: fractionalValueFieldInfo.key, name: fractionalValueFieldInfo.name }
                // Add data to list
                valueFields.push({ key: fractionalValueFieldInfo.key, data: fractionalValueFieldInfo.data })
            }

            // Get total value field
            const totalValueFieldInfo = await this.getFieldInfo('Total Value Field') // , 'Indicator')
            if (totalValueFieldInfo !== null) {
                // Devise mapping for value field
                mapping['Total Value Field'] = { key: totalValueFieldInfo.key, name: totalValueFieldInfo.name }
                // Add data to list
                valueFields.push({ key: totalValueFieldInfo.key, data: totalValueFieldInfo.data })
            }

            // Create dataset
            var valuesRecord = {}
            for (const valueField of valueFields) {
                const key = valueField.key
                const data = valueField.data
                var value = 0
                for (const row of data) {
                    value += Number(row[key])
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

            // Get fractional value field
            const currentValueFieldInfo = await this.getFieldInfo('Current Value Field') // , 'Indicator')
            if (currentValueFieldInfo !== null) {
                // Devise mapping for value field
                mapping['Current Value Field'] = { key: currentValueFieldInfo.key, name: currentValueFieldInfo.name }
                // Add data to list
                valueFields.push({ key: currentValueFieldInfo.key, data: currentValueFieldInfo.data })
            }

            // Get target value field
            const targetValueFieldInfo = await this.getFieldInfo('Target Value Field') // , 'Indicator')
            if (targetValueFieldInfo !== null) {
                // Devise mapping for value field
                mapping['Target Value Field'] = { key: targetValueFieldInfo.key, name: targetValueFieldInfo.name }
                // Add data to list
                valueFields.push({ key: targetValueFieldInfo.key, data: targetValueFieldInfo.data })
            }

            // Create dataset
            var valuesRecord = {}
            for (const valueField of valueFields) {
                const key = valueField.key
                const data = valueField.data
                var value = 0
                for (const row of data) {
                    value += Number(row[key])
                }
                valuesRecord[key] = value
            }
            dataset.push(valuesRecord)

            // Return data info
            const dataSet = { data: dataset, mapping: mapping }
            return dataSet
        },
        async createPieChartDataSet () {
            return await this.createCategoryValueDataSet()
        },
        async createBarChartDataSet () {
            return await this.createCategoryValueDataSet()
        },
        async createLineChartDataSet () {
            return await this.createCategoryValueDataSet()
        },
        async createCategoryValueDataSet () {
            // Record for single value
            var dataset = []
            // Values per field
            var valueFields = []
            // Groupings per field
            var groupingFields = []
            // Mapping for fields
            var mapping = {}

            // Get value field
            const valueFieldInfo = await this.getFieldInfo('Value Field')
            if (valueFieldInfo !== null) {
                // Devise mapping for value field
                mapping['Value Field'] = { key: valueFieldInfo.key, name: valueFieldInfo.name }
                // Add data to list
                valueFields.push({ key: valueFieldInfo.key, data: valueFieldInfo.data })
            }

            // Get category field
            const categoryFieldInfo = await this.getFieldInfo('Category Field')
            if (categoryFieldInfo !== null) {
                // Devise mapping for category field
                mapping['Category Field'] = { key: categoryFieldInfo.key, name: categoryFieldInfo.name }
                // Add data to list
                groupingFields.push({ key: categoryFieldInfo.key, data: valueFieldInfo.data })
            }

            // Map list of category values to list of indicators
            if (categoryFieldInfo?.values && valueFieldInfo?.indicators) {
                const valueFieldIndicators = valueFieldInfo.indicators
                const categoryValues = categoryFieldInfo.values
                // Check if both are present
                if (valueFieldIndicators && categoryValues) {
                    // Mapping to category value for each indicator key
                    var categoryMapping = {}
                    for (let i = 0; i < valueFieldIndicators.length; i++) {
                        const valueFieldIndicator = valueFieldIndicators[i]
                        const categoryValue = categoryValues[i]
                        categoryMapping[valueFieldIndicator] = categoryValue
                    }
                    // Add category field with value for each indicator
                    const valueData = valueFieldInfo.data
                    for (var valueDataRow of valueData) {
                        const valueFieldIndicator = valueDataRow['Indicator Key']
                        const categoryValue = categoryMapping[valueFieldIndicator]
                        valueDataRow[categoryFieldInfo.key] = categoryValue
                        delete valueDataRow['Indicator Key']
                    }
                }
            }

            // Create dataset
            var accumulatedRows = []
            for (const valueField of valueFields) {
                const valueKey = valueField.key
                const valueData = valueField.data
                for (const row of valueData) {
                    var groupingAlreadyPresent = false
                    for (const accumulatedRow of accumulatedRows) {
                        var sameGrouping = true
                        for (const groupingField of groupingFields) {
                            if (accumulatedRow[groupingField.key] !== row[groupingField.key]) {
                                sameGrouping = false
                                break
                            }
                        }
                        if (sameGrouping) {
                            accumulatedRow[valueKey] += Number(row[valueKey])
                            groupingAlreadyPresent = true
                            break
                        }
                    }
                    if (!groupingAlreadyPresent) {
                        var newGroupingRow = {}
                        newGroupingRow[valueKey] = Number(row[valueKey])
                        for (const groupingField of groupingFields) {
                            newGroupingRow[groupingField.key] = row[groupingField.key]
                        }
                        accumulatedRows.push(newGroupingRow)
                    }
                }
            }
            // Optional sorting by Year
            for (const groupingField of groupingFields) {
                if (groupingField.key === 'Year') accumulatedRows = accumulatedRows.sort((a, b) => a.Year - b.Year)
            }
            dataset = accumulatedRows

            // Return data info
            const dataSet = { data: dataset, mapping: mapping }
            console.log(dataSet)
            return dataSet
        },
        async createGroupedCategoryValueDataSet () {
            // Record for single value
            var dataset = []
            // Values per field
            var valueFields = []
            // Groupings per field
            var groupingFields = []
            // Mapping for fields
            var mapping = {}

            // Get value field
            const valueFieldInfo = await this.getFieldInfo('Value Field')
            if (valueFieldInfo !== null) {
                // Devise mapping for value field
                mapping['Value Field'] = { key: valueFieldInfo.key, name: valueFieldInfo.name }
                // Add data to list
                valueFields.push({ key: valueFieldInfo.key, data: valueFieldInfo.data })
            }

            // Get category field
            const categoryFieldInfo = await this.getFieldInfo('Category Field')
            if (categoryFieldInfo !== null) {
                // Devise mapping for category field
                mapping['Category Field'] = { key: categoryFieldInfo.key, name: categoryFieldInfo.name }
                // Add data to list
                groupingFields.push({ key: categoryFieldInfo.key, data: categoryFieldInfo.data })
            }

            // Get grouping field
            const groupingFieldInfo = await this.getFieldInfo('Grouping Field')
            if (groupingFieldInfo !== null) {
                // Devise mapping for category field
                mapping['Grouping Field'] = { key: groupingFieldInfo.key, name: groupingFieldInfo.name }
                // Add data to list
                groupingFields.push({ key: groupingFieldInfo.key, data: groupingFieldInfo.data })
            }
            // Or get stacking field
            const stackingFieldInfo = await this.getFieldInfo('Stacking Field')
            if (stackingFieldInfo !== null) {
                // Devise mapping for category field
                mapping['Stacking Field'] = { key: stackingFieldInfo.key, name: stackingFieldInfo.name }
                // Add data to list
                groupingFields.push({ key: stackingFieldInfo.key, data: stackingFieldInfo.data })
            }

            // Map list of category values to list of indicators
            if (categoryFieldInfo?.values && valueFieldInfo?.indicators) {
                const valueFieldIndicators = valueFieldInfo.indicators
                const categoryValues = categoryFieldInfo.values
                // Check if both are present
                if (valueFieldIndicators && categoryValues) {
                    // Mapping to category value for each indicator key
                    var categoryMapping = {}
                    for (let i = 0; i < valueFieldIndicators.length; i++) {
                        const valueFieldIndicator = valueFieldIndicators[i]
                        const categoryValue = categoryValues[i]
                        categoryMapping[valueFieldIndicator] = categoryValue
                    }
                    // Add category field with value for each indicator
                    const valueData = valueFieldInfo.data
                    for (var valueDataRow of valueData) {
                        const valueFieldIndicator = valueDataRow['Indicator Key']
                        const categoryValue = categoryMapping[valueFieldIndicator]
                        valueDataRow[categoryFieldInfo.key] = categoryValue
                        delete valueDataRow['Indicator Key']
                    }
                }
            }

            // Create dataset
            var accumulatedRows = []
            for (const valueField of valueFields) {
                const valueKey = valueField.key
                const valueData = valueField.data
                for (const row of valueData) {
                    var groupingAlreadyPresent = false
                    for (const accumulatedRow of accumulatedRows) {
                        var sameGrouping = true
                        for (const groupingField of groupingFields) {
                            if (accumulatedRow[groupingField.key] !== row[groupingField.key]) {
                                sameGrouping = false
                                break
                            }
                        }
                        if (sameGrouping) {
                            accumulatedRow[valueKey] += Number(row[valueKey])
                            groupingAlreadyPresent = true
                            break
                        }
                    }
                    if (!groupingAlreadyPresent) {
                        var newGroupingRow = {}
                        newGroupingRow[valueKey] = Number(row[valueKey])
                        for (const groupingField of groupingFields) {
                            newGroupingRow[groupingField.key] = row[groupingField.key]
                        }
                        accumulatedRows.push(newGroupingRow)
                    }
                }
            }
            // Optional sorting by Year
            for (const groupingField of groupingFields) {
                if (groupingField.key === 'Year') accumulatedRows = accumulatedRows.sort((a, b) => a.Year - b.Year)
            }
            dataset = accumulatedRows

            // Return data info
            const dataSet = { data: dataset, mapping: mapping }
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
  width: 100%;
  height: 100%;
}
.progress-spinner {
    max-height: 100%;
    max-width: 100%;
}
</style>
