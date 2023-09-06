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
            console.log(this.dataSet)
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
                case 'Radial Progress Bar':
                    return await this.createProgressBarDataSet()
                // case 'Pie Chart':
                //     return await this.createPieChartDataSet()
                // case 'Bar Chart':
                //     return await this.createBarChartDataSet()
                // case 'Line Chart':
                //     return await this.createLineChartDataSet()
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
        async applyVisualisationFilters (dataSet) {
            const filters = await this.getVisualisationFilters()
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
        async getVisualisationFilters () {
            // Get filters
            const dataConfiguration = await this.getDataConfiguration()(this.config)
            const visualisationFilters = dataConfiguration?.Filters
            return visualisationFilters
        },
        // Get data/info for the indicator fields/values/named field
        async getFieldInfo (field, type) {
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
            if (field.Name && type !== 'Indicator' && type !== 'Indicators') {
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
            const fieldKey = fieldName !== null && fieldName !== '' ? fieldName : 'Value Field'

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
                    rowInfo['Indicator Key'] = fieldIndicator
                    rowInfo[fieldKey] = row[indicatorFieldKey]
                    rowInfo.Year = row.Year
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
            const fieldKey = fieldName !== null && fieldName !== '' ? fieldName : 'Category Field'

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
            const fieldKey = fieldName !== null && fieldName !== '' ? fieldName : 'Named Field'

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

            // Get value field info
            const valueField = await this.getValueField()(this.config)
            const valueFieldInfo = await this.getFieldInfo(valueField, 'Indicator')
            if (valueFieldInfo !== null) {
                // Devise mapping for value field
                mapping['Value Field'] = { key: valueFieldInfo.key, name: valueFieldInfo.name }

                // Filter data and add data to list
                const filteredValueIndicatorData = await this.applyVisualisationFilters(valueFieldInfo.data)
                valueFields.push({ key: valueFieldInfo.key, data: filteredValueIndicatorData })
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
            const fractionalValueField = await this.getFractionalValueField()(this.config)
            const fractionalValueFieldInfo = await this.getFieldInfo(fractionalValueField, 'Indicator')
            if (fractionalValueFieldInfo !== null) {
                // Devise mapping for value field
                mapping['Fractional Value Field'] = { key: fractionalValueFieldInfo.key, name: fractionalValueFieldInfo.name }

                // Filter data and add data to list
                const filteredFractionalValueIndicatorData = await this.applyVisualisationFilters(fractionalValueFieldInfo.data)
                valueFields.push({ key: fractionalValueFieldInfo.key, data: filteredFractionalValueIndicatorData })
            }

            // Get total value field
            const totalValueField = await this.getTotalValueField()(this.config)
            const totalValueFieldInfo = await this.getFieldInfo(totalValueField, 'Indicator')
            if (totalValueFieldInfo !== null) {
                // Devise mapping for value field
                mapping['Total Value Field'] = { key: totalValueFieldInfo.key, name: totalValueFieldInfo.name }

                // Filter data and add data to list
                const filteredTotalValueIndicatorData = await this.applyVisualisationFilters(totalValueFieldInfo.data)
                valueFields.push({ key: totalValueFieldInfo.key, data: filteredTotalValueIndicatorData })
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
            const currentValueField = await this.getCurrentValueField()(this.config)
            const currentValueFieldInfo = await this.getFieldInfo(currentValueField, 'Indicator')
            if (currentValueFieldInfo !== null) {
                // Devise mapping for value field
                mapping['Current Value Field'] = { key: currentValueFieldInfo.key, name: currentValueFieldInfo.name }

                // Filter data and add data to list
                const filteredCurrentValueIndicatorData = await this.applyVisualisationFilters(currentValueFieldInfo.data)
                valueFields.push({ key: currentValueFieldInfo.key, data: filteredCurrentValueIndicatorData })
            }

            // Get target value field
            const targetValueField = await this.getTargetValueField()(this.config)
            const targetValueFieldInfo = await this.getFieldInfo(targetValueField, 'Indicator')
            if (targetValueFieldInfo !== null) {
                // Devise mapping for value field
                mapping['Target Value Field'] = { key: targetValueFieldInfo.key, name: targetValueFieldInfo.name }

                // Filter data and add data to list
                const filteredTargetValueIndicatorData = await this.applyVisualisationFilters(targetValueFieldInfo.data)
                valueFields.push({ key: targetValueFieldInfo.key, data: filteredTargetValueIndicatorData })
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
            const valueField = await this.getValueField()(this.config)
            const valueFieldInfo = await this.getFieldInfo(valueField)
            if (valueFieldInfo !== null) {
                // Devise mapping for value field
                mapping['Value Field'] = { key: valueFieldInfo.key, name: valueFieldInfo.name }

                // Filter data and add data to list
                const filteredValueIndicatorData = await this.applyVisualisationFilters(valueFieldInfo.data)
                valueFields.push({ key: valueFieldInfo.key, data: filteredValueIndicatorData })
            }

            // Get category field
            const categoryField = await this.getCategoryField()(this.config)
            const categoryFieldInfo = await this.getFieldInfo(categoryField)
            if (categoryFieldInfo !== null) {
                // Devise mapping for category field
                mapping['Category Field'] = { key: categoryFieldInfo.key, name: categoryFieldInfo.name }

                // Filter data and add data to list
                const filteredCategoryData = await this.applyVisualisationFilters(valueFieldInfo.data)
                groupingFields.push({ key: categoryFieldInfo.key, data: filteredCategoryData })
            }

            // Map list of category values to list of indicators
            if (categoryFieldInfo?.type === 'Values' && valueFieldInfo?.type === 'Indicators') {
                const valueFieldIndicators = valueField.Indicators
                const categoryValues = categoryField.Values
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
            const valueField = await this.getValueField()(this.config)
            const valueFieldInfo = await this.getFieldInfo(valueField)
            if (valueFieldInfo !== null) {
                // Devise mapping for value field
                mapping['Value Field'] = { key: valueFieldInfo.key, name: valueFieldInfo.name }

                // Filter data and add data to list
                const filteredValueIndicatorData = await this.applyVisualisationFilters(valueFieldInfo.data)
                valueFields.push({ key: valueFieldInfo.key, data: filteredValueIndicatorData })
            }

            // Get category field
            const categoryField = await this.getCategoryField()(this.config)
            const categoryFieldInfo = await this.getFieldInfo(categoryField)
            if (categoryFieldInfo !== null) {
                // Devise mapping for category field
                mapping['Category Field'] = { key: categoryFieldInfo.key, name: categoryFieldInfo.name }

                // Filter data and add data to list
                const filteredCategoryData = await this.applyVisualisationFilters(categoryFieldInfo.data)
                groupingFields.push({ key: categoryFieldInfo.key, data: filteredCategoryData })
            }

            // Get grouping field
            const groupingField = await this.getGroupingField()(this.config)
            const groupingFieldInfo = await this.getFieldInfo(groupingField)
            if (groupingFieldInfo !== null) {
                // Devise mapping for category field
                mapping['Grouping Field'] = { key: groupingFieldInfo.key, name: groupingFieldInfo.name }

                // Filter data and add data to list
                const filteredGroupingData = await this.applyVisualisationFilters(groupingFieldInfo.data)
                groupingFields.push({ key: groupingFieldInfo.key, data: filteredGroupingData })
            }
            // Or get stacking field
            const stackingField = await this.getStackingField()(this.config)
            const stackingFieldInfo = await this.getFieldInfo(stackingField)
            if (stackingFieldInfo !== null) {
                // Devise mapping for category field
                mapping['Stacking Field'] = { key: stackingFieldInfo.key, name: stackingFieldInfo.name }

                // Filter data and add data to list
                const filteredStackingData = await this.applyVisualisationFilters(stackingFieldInfo.data)
                groupingFields.push({ key: stackingFieldInfo.key, data: filteredStackingData })
            }
            console.log(categoryFieldInfo)
            console.log(groupingFieldInfo)
            console.log(stackingFieldInfo)

            // Map list of category values to list of indicators
            if (categoryFieldInfo?.type === 'Values' && valueFieldInfo?.type === 'Indicators') {
                const valueFieldIndicators = valueField.Indicators
                const categoryValues = categoryField.Values
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
