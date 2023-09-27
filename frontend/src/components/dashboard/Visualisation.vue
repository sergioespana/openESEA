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
import MultiSeriesLineChart from './visualisations/charts/MultiSeriesLineChart.vue'
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
        MultiSeriesLineChart,
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
                    case 'Multi-Series Line Chart':
                        return 'MultiSeriesLineChart'
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
            handler: 'createAndSaveDataset',
            deep: true
        }
    },
    async created () {
        await this.createAndSaveDataset()
    },
    methods: {
        ...mapGetters('dashboardData', ['getIndicatorData', 'getIndicatorDataSet', 'getVisualisationDatasets']),
        ...mapActions('dashboardData', ['saveVisualisationDataset']),
        ...mapGetters('dashboardModel', ['getOverviewFilters', 'getVisualisation', 'getDataDisplay', 'getDataConfiguration', 'getVisualisationFilters', 'getValueField', 'getValueFields', 'getFractionalValueField', 'getTotalValueField', 'getCurrentValueField', 'getTargetValueField', 'getCategoryField', 'getGroupingField', 'getStackingField', 'getCategoryLimit', 'getSideways', 'getVisualisationType', 'getVisualisationPosition', 'getVisualisationTitle']),
        ...mapActions('dashboardModel', ['updateSelectionConfig']),
        async isClicked (event) {
            event.stopPropagation()
            await this.updateSelectionConfig(this.config)
        },
        isEmpty (string) { return string === null || string === undefined || string === '' },
        // Create dataset and save the dataset
        async createAndSaveDataset () {
            // Create data set
            const dataset = await this.createDataset()
            // Update visualisation dataset
            this.dataSet = dataset
            // Save dataset for sending to rl model
            await this.saveVisualisationDataset({ config: this.config, dataset: dataset })
        },
        // Create dataset consisting of data, mapping, visualisation options and a title
        async createDataset () {
            // Collect data
            var dataset = await this.collectData() // { mapping: ..., data: ... }
            // console.log(dataset)
            // Add options to dataset
            dataset.options = await this.collectVisualisationOptions()
            // Add title to data set
            dataset.title = this.visualisationTitle

            // Return dataset information
            return dataset
        },
        async collectVisualisationOptions () {
            var options = {}
            // Add category limit
            const categoryLimit = await this.getCategoryLimit()(this.config)
            if (categoryLimit !== null && categoryLimit !== undefined) { options.categoryLimit = categoryLimit }
            // Add sideways indicator
            const sideways = await this.getSideways()(this.config)
            if (sideways !== null && sideways !== undefined) { options.sideways = sideways }
            // Add showValue indicator
            const showValue = null
            if (showValue !== null && showValue !== undefined) { options.showValue = showValue }
            // Add showArea indicator
            const showArea = null
            if (showArea !== null && showArea !== undefined) { options.showArea = showArea }
            // Add showBoundaryGap indicator
            const showBoundaryGap = null
            if (showBoundaryGap !== null && showBoundaryGap !== undefined) { options.showBoundaryGap = showBoundaryGap }

            return options
        },
        // For each visualisation type create the corresponding dataset
        async collectData () {
            // Create dataset based for this visualisation type
            switch (this.visualisationType) {
                case 'Single Value Display':
                    return await this.createDatasetForFields(['Value Field'])
                case 'Fractional Value Display':
                    return await this.createDatasetForFields(['Fractional Value Field', 'Total Value Field'])
                case 'Progress Bar':
                case 'Radial Progress Bar':
                    return await this.createDatasetForFields(['Current Value Field', 'Target Value Field'])
                case 'Pie Chart':
                case 'Bar Chart':
                case 'Line Chart':
                case 'Table':
                    return await this.createDatasetForFields(['Value Field'], ['Category Field'])
                case 'Multi-Series Line Chart':
                    return await this.createDatasetForFields(['Value Fields'], ['Category Field'])
                case 'Grouped Bar Chart':
                case 'Stacked Bar Chart':
                    return await this.createDatasetForFields(['Value Field'], ['Category Field', 'Stacking Field', 'Grouping Field'])
                default:
                    return {}
            }
        },
        async retrieveInfoForField (field) {
            if (field?.Indicators) {
                return await this.retrieveIndicatorsInfo(field)
            }
            if (field?.Indicator) {
                return await this.retrieveIndicatorInfo(field)
            }
            if (field?.['Named Field']) {
                return await this.retrieveNamedFieldInfo(field)
            }
            if (field?.Values) {
                return await this.retrieveFieldValuesInfo(field)
            }
            return null
        },
        async getField (fieldName) {
            switch (fieldName) {
                case 'Value Field':
                    return await this.getValueField()(this.config)
                case 'Value Fields':
                    return await this.getValueFields()(this.config)
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
        async retrieveIndicatorInfo (field) {
            const fieldIndicator = field.Indicator
            const fieldName = field.Name

            // Get dataset for the current value field indicator
            const indicatorDataSet = await this.getIndicatorDataSet()(fieldIndicator)
            const indicatorName = indicatorDataSet.name
            const indicatorData = await this.applyVisualisationFilters(indicatorDataSet.data)

            // Devise mapping for field
            const fieldKey = indicatorName
            const info = { key: fieldKey, name: fieldName, data: indicatorData, indicator: fieldIndicator }
            return info
        },
        async retrieveIndicatorsInfo (field) {
            const fieldIndicators = field.Indicators
            const fieldName = field.Name
            const fieldKey = this.isEmpty(fieldName) ? 'Value Field' : fieldName

            var dataset = []
            for (let indicatorNumber = 0; indicatorNumber < fieldIndicators.length; indicatorNumber++) {
                const fieldIndicator = fieldIndicators[indicatorNumber]
                if (!fieldIndicator) { continue }

                // Get dataset for the current value field indicator
                const indicatorDataSet = await this.getIndicatorDataSet()(fieldIndicator)
                const indicatorName = indicatorDataSet.name
                const indicatorData = await this.applyVisualisationFilters(indicatorDataSet.data)

                // Collect data together with indicator name
                const indicatorFieldKey = indicatorName
                for (var row of indicatorData) {
                    var rowData = {}
                    rowData['Indicator Order'] = indicatorNumber
                    rowData[fieldKey] = row[indicatorFieldKey]
                    rowData.Year = row.Year
                    dataset.push(rowData)
                }
            }

            // Devise mapping for field
            const info = { key: fieldKey, name: fieldName, data: dataset, indicators: fieldIndicators }
            return info
        },
        async retrieveFieldValuesInfo (field) {
            const fieldValues = field.Values
            const fieldName = field.Name
            const fieldKey = this.isEmpty(fieldName) ? 'Category Field' : fieldName

            var dataset = []
            for (const fieldValue of fieldValues) {
                var rowData = {}
                rowData[fieldKey] = fieldValue
                dataset.push(rowData)
            }

            // Devise mapping for field
            const info = { key: fieldKey, name: fieldName, data: dataset, values: fieldValues }
            return info
        },
        async retrieveNamedFieldInfo (field) {
            const fieldKey = field['Named Field']
            const fieldName = field.Name

            // Devise mapping for field
            const info = { key: fieldKey, name: fieldName, namedField: fieldName }
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
            // Combine and return filters
            const combinedFilters = overviewFilters.concat(visualisationFilters)
            return combinedFilters
        },
        // Summarize data by summing value fields for each grouping in the grouping fields
        summarizeData (valueFields, groupingFields) {
            // List for storing summarized rows accumulated so far
            var accumulatedRows = []
            // Summarize values for all value fields
            for (const valueField of valueFields) {
                const valueKey = valueField.key
                const valueData = valueField.data
                // For each row in data, add value to existing row or add new row with value
                for (const row of valueData) {
                    var groupingAlreadyPresent = false
                    // Check if same grouping already exists in accumulated rows
                    for (var accumulatedRow of accumulatedRows) {
                        var sameGrouping = true
                        for (const groupingField of groupingFields) {
                            const groupingKey = (groupingField?.values !== undefined && groupingField?.values !== null) ? 'Indicator Order' : groupingField.key
                            if (accumulatedRow[groupingKey] !== row[groupingKey]) {
                                sameGrouping = false
                                break
                            }
                        }
                        // If so add value to current value
                        if (sameGrouping) {
                            const newValue = (accumulatedRow[valueKey] ?? 0) + (isNaN(row[valueKey]) ? 0 : Number(row[valueKey]))
                            accumulatedRow[valueKey] = newValue
                            groupingAlreadyPresent = true
                            break
                        }
                    }
                    // Otherwise if grouping is not present, add a new row for this grouping together with the value
                    if (!groupingAlreadyPresent) {
                        var newGroupingRow = {}
                        const newValue = isNaN(row[valueKey]) ? 0 : Number(row[valueKey])
                        newGroupingRow[valueKey] = newValue
                        for (const groupingField of groupingFields) {
                            newGroupingRow[groupingField.key] = row[groupingField.key]
                            // Keep track of indicator order in case of duplicate category values
                            if (groupingField?.values !== undefined && groupingField?.values !== null) {
                                newGroupingRow['Indicator Order'] = row['Indicator Order']
                            }
                        }
                        accumulatedRows.push(newGroupingRow)
                    }
                }
            }
            return accumulatedRows
        },
        async collectFields (fieldNames) {
            var fieldsInfo = []
            for (const fieldName of fieldNames) {
                const field = await this.getField(fieldName)
                if (!Array.isArray(field)) {
                    var fieldInfo = await this.retrieveInfoForField(field)
                    if (fieldInfo === null) continue
                    fieldInfo.fieldName = fieldName
                    fieldsInfo.push(fieldInfo)
                } else {
                    for (let i = 0; i < field.length; i++) {
                        var subFieldInfo = await this.retrieveInfoForField(field[i])
                        if (subFieldInfo === null) continue
                        subFieldInfo.fieldName = fieldName + ' ' + i.toString()
                        subFieldInfo.fieldNumber = i
                        fieldsInfo.push(subFieldInfo)
                    }
                }
            }
            return fieldsInfo
        },
        async createDatasetForFields (valueFieldNames, groupingFieldNames = []) {
            // Collect value fields
            const valueFields = await this.collectFields(valueFieldNames)
            // Collect grouping fields
            const groupingFields = await this.collectFields(groupingFieldNames)

            // Map category values to indicators
            this.mapCategoryValues(valueFields, groupingFields)

            // Create dataset by summarizing data
            var dataset = this.summarizeData(valueFields, groupingFields)
            console.log(dataset)

            // Sort dataset by year if this column is in dataset
            const groupingKeys = groupingFields.map(field => field.key)
            if (groupingKeys.includes('Year')) dataset = dataset.sort((a, b) => a.Year - b.Year)

            // Create mapping from fields
            const allFields = valueFields.concat(groupingFields)
            const mapping = this.createMapping(allFields)

            // Return data info
            const dataSet = { data: dataset, mapping: mapping }
            console.log(dataSet)
            return dataSet
        },
        createMapping (fields) {
            var mapping = {}
            for (const field of fields) {
                mapping[field.fieldName] = { key: field.key, name: field.name }
            }
            return mapping
        },
        mapCategoryValues (valueFields, groupingFields) {
            // Map list of category values to list of indicators
            console.log(valueFields, groupingFields)
            for (const groupingField of groupingFields) {
                const categoryValues = groupingField.values
                if (categoryValues) {
                    const categoryKey = groupingField.key
                    for (const valueField of valueFields) {
                        const valueIndicators = valueField.indicators
                        if (valueIndicators) {
                            const valueData = valueField.data
                            for (var valueDataRow of valueData) {
                                const valueFieldIndicatorOrder = valueDataRow['Indicator Order']
                                valueDataRow[categoryKey] = categoryValues[valueFieldIndicatorOrder]
                            }
                        }
                    }
                }
            }
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
