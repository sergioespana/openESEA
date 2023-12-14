<template>
    <div class="flex flex-column">

        <!-- Edit area title -->
        <div class="edit-area-title">Visualisation</div>

        <!-- Add Visualisation -->
        <div :style="{ height: '5px' }"></div>

        <div class="full-width" :style="{ position: 'relative', width: '100%' }">
            <Button label="Add Visualisation" icon="pi pi-plus" class="p-button-success p-button-sm"
                @click="addVisualisation">
            </Button>
        </div>

        <div :style="{ height: '5px' }"></div>

        <!-- If no visualisation selected, display this message -->
        <div v-if="visualisationId === null || visualisationId === undefined">
            <div class="edit-area-field">Select a Visualisation to display its information!</div>
        </div>
        <!-- Otherwise display visualisation information -->
        <div v-else>

            <!-- Title input -->
            <div class="edit-area-field">Title:</div>
            <InputText class="near-width"
                v-model="visualisationTitle">
            </InputText>
            <!-- Position -->
            <div class="edit-area-field">
                Position:
                <i v-on:click="showPosition = !showPosition">
                    <i v-if="showPosition" class="pi pi-angle-up"></i>
                    <i v-else class="pi pi-angle-down"></i>
                </i>
            </div>
            <div v-if="showPosition">
                <InputNumber class="near-width"
                    v-model="visualisationXStart">
                </InputNumber>
                <InputNumber class="near-width"
                    v-model="visualisationXEnd">
                </InputNumber>
                <InputNumber class="near-width"
                    v-model="visualisationYStart">
                </InputNumber>
                <InputNumber class="near-width"
                    v-model="visualisationYEnd">
                </InputNumber>
            </div>
            <!-- Visualisation type input -->
            <div class="edit-area-field">Visualisation Type:</div>
            <Dropdown class="near-width"
                v-model="visualisationType"
                :options="visualisationTypes">
            </Dropdown>
            <!-- Indicators -->
            <div v-if="visualisationType === 'Single Value Display'">
                <div class="edit-area-field">Value Field:</div>
                <Dropdown class="near-width"
                    v-model="valueField"
                    :options="[noIndicatorOption, ...indicators]"
                    :optionLabel="'name'"
                    :optionValue="'key'"
                    placeholder="Choose an indicator field">
                </Dropdown>
                <div class="edit-area-field">Name:</div>
                <InputText class="near-width"
                    v-model="valueFieldName">
                </InputText>
            </div>
            <div v-else-if="visualisationType === 'Fractional Value Display'">
                <div class="edit-area-field">Fractional Value Field:</div>
                <Dropdown class="near-width"
                    v-model="fractionalValueField"
                    :options="[noIndicatorOption, ...indicators]"
                    :optionLabel="'name'"
                    :optionValue="'key'"
                    placeholder="Choose an indicator field">
                </Dropdown>
                <div class="edit-area-field">Name:</div>
                <InputText class="near-width"
                    v-model="fractionalValueFieldName">
                </InputText>
                <div class="edit-area-field">Total Value Field:</div>
                <Dropdown class="near-width"
                    v-model="totalValueField"
                    :options="[noIndicatorOption, ...indicators]"
                    :optionLabel="'name'"
                    :optionValue="'key'"
                    placeholder="Choose an indicator field">
                </Dropdown>
                <div class="edit-area-field">Name:</div>
                <InputText class="near-width"
                    v-model="totalValueFieldName">
                </InputText>
            </div>
            <div v-else-if="progressBarVisualisations.includes(visualisationType)">
                <div class="edit-area-field">Current Value Field:</div>
                <Dropdown class="near-width"
                    v-model="currentValueField"
                    :options="[noIndicatorOption, ...indicators]"
                    :optionLabel="'name'"
                    :optionValue="'key'"
                    placeholder="Choose an indicator field">
                </Dropdown>
                <div class="edit-area-field">Name:</div>
                <InputText class="near-width"
                    v-model="currentValueFieldName">
                </InputText>
                <div class="edit-area-field">Target Value Field:</div>
                <Dropdown class="near-width"
                    v-model="targetValueField"
                    :options="[noIndicatorOption, ...indicators]"
                    :optionLabel="'name'"
                    :optionValue="'key'"
                    placeholder="Choose an indicator field">
                </Dropdown>
                <div class="edit-area-field">Name:</div>
                <InputText class="near-width"
                    v-model="targetValueFieldName">
                </InputText>
            </div>
            <div v-else-if="categoricalVisualisations.includes(visualisationType)">
                <!-- Simple field or composed field -->
                <div class="edit-area-field">
                    Composed field:
                    <InputSwitch
                        :modelValue="composedField"
                        @update:modelValue="(isComposedField) => { if (isComposedField) { valueFieldIndicators = []; categoryFieldValues = [] } else { valueFieldIndicators = null; categoryFieldValues = null } }">
                    </InputSwitch>
                </div>
                <div v-if="composedField">
                    <!-- Value field composed of multiple indicators -->
                    <div class="edit-area-field">Value Indicators:</div>
                    <!-- Alter/Remove indicators -->
                    <div v-for="(item, index) in (valueFieldIndicators ?? [])" :key="index">
                        <Dropdown class="near-width"
                            :modelValue="valueFieldIndicators[index]"
                            @update:modelValue="(newValue) => { if (newValue !== null) { valueFieldIndicators[index] = newValue } else { valueFieldIndicators.splice(index, 1); categoryFieldValues.splice(index, 1) } }"
                            :options="[noIndicatorOption, ...indicators]"
                            :optionLabel="'name'"
                            :optionValue="'key'"
                            placeholder="Choose an indicator field">
                        </Dropdown>
                    </div>
                    <!-- Add additional indicators -->
                    <Dropdown class="near-width"
                        :modelValue="null"
                        @update:modelValue="(newValue) => { if (false) { console.log(valueFieldIndicators, newValue, (valueFieldIndicators ?? []).push(newValue)) } else if (newValue !== null) { if (!valueFieldIndicators) { valueFieldIndicators = []; categoryFieldValues = [] }; valueFieldIndicators.push(newValue); categoryFieldValues.push('') } }"
                        :options="[noIndicatorOption, ...indicators]"
                        :optionLabel="'name'"
                        :optionValue="'key'"
                        placeholder="Choose an indicator field">
                    </Dropdown>
                </div>
                <div v-else>
                    <!-- Simple value field -->
                    <div class="edit-area-field">Value Field:</div>
                    <Dropdown class="near-width"
                        v-model="valueField"
                        :options="[noIndicatorOption, ...indicators]"
                        :optionLabel="'name'"
                        :optionValue="'key'"
                        placeholder="Choose an indicator field">
                    </Dropdown>
                </div>
                <!-- Value field name -->
                <div class="edit-area-field">Name:</div>
                <InputText class="near-width"
                    v-model="valueFieldName">
                </InputText>
                <!-- Simple category field or values -->
                <div v-if="composedField">
                    <!-- Value field composed of multiple indicators -->
                    <div class="edit-area-field">Category Values:</div>
                    <!-- Alter values -->
                    <div v-for="(item, index) in (valueFieldIndicators ?? [])" :key="index">
                        <InputText class="near-width"
                            :modelValue="categoryFieldValues[index]"
                            @update:modelValue="(newValue) => { categoryFieldValues[index] = newValue }"
                            placeholder="Choose a category value">
                        </InputText>
                    </div>
                </div>
                <div v-else>
                    <!-- Simple category field -->
                    <div class="edit-area-field">Category Field:</div>
                    <Dropdown class="near-width"
                        v-model="categoryField"
                        :options="[noIndicatorOption, yearField]"
                        :optionLabel="'name'"
                        :optionValue="'key'"
                        placeholder="Choose an indicator field">
                    </Dropdown>
                </div>
                <!-- Category field name -->
                <div class="edit-area-field">Name:</div>
                <InputText class="near-width"
                    v-model="categoryFieldName">
                </InputText>
            </div>
            <div v-if="visualisationType === 'Grouped Bar Chart'">
                <!-- Simple grouping field -->
                <div class="edit-area-field">Grouping Field:</div>
                <Dropdown class="near-width"
                    v-model="groupingField"
                    :options="[noIndicatorOption, yearField]"
                    :optionLabel="'name'"
                    :optionValue="'key'"
                    placeholder="Choose an indicator field">
                </Dropdown>
                <!-- Grouping field name -->
                <div class="edit-area-field">Grouping Field Name:</div>
                <InputText class="near-width"
                    v-model="groupingFieldName">
                </InputText>
            </div>
            <div v-if="visualisationType === 'Stacked Bar Chart'">
                <!-- Simple stacking field -->
                <div class="edit-area-field">Stacking Field:</div>
                <Dropdown class="near-width"
                    v-model="stackingField"
                    :options="[noIndicatorOption, yearField]"
                    :optionLabel="'name'"
                    :optionValue="'key'"
                    placeholder="Choose an indicator field">
                </Dropdown>
                <!-- Stacking field name -->
                <div class="edit-area-field">Stacking Field Name:</div>
                <InputText class="near-width"
                    v-model="stackingFieldName">
                </InputText>
            </div>
            <div v-if="visualisationType === 'Multi-Series Line Chart'">
                <div v-for="(_, valueFieldIndex) in valueFields" :key="valueFieldIndex">
                    <div v-if="composedFields">
                        <!-- Value field composed of multiple indicators -->
                        <div class="edit-area-field">Value Indicators:</div>
                        <!-- Alter/Remove indicators -->
                        <div v-for="(indicator, indicatorIndex) in (valueFields[valueFieldIndex]?.Indicators ?? [])" :key="indicatorIndex">
                            <Dropdown class="near-width"
                                :modelValue="valueFields[valueFieldIndex].Indicators[indicatorIndex]"
                                @update:modelValue="(newValue) => { if (newValue !== null) { valueFields[valueFieldIndex].Indicators[indicatorIndex] = newValue } else { valueFields = valueFields.foreach(field => field.Indicators.splice(indicatorIndex, 1)) } }"
                                :options="[noIndicatorOption, ...indicators]"
                                :optionLabel="'name'"
                                :optionValue="'key'"
                                placeholder="Choose an indicator field">
                            </Dropdown>
                        </div>
                        <!-- Add additional indicators -->
                        <Dropdown class="near-width"
                            :modelValue="null"
                            @update:modelValue="(newValue) => { console.log(newValue, valueFields); if (newValue !== null) { valueFields = valueFields.map(field => { if (field?.Indicators === null || field?.Indicators === undefined) { field.Indicators = [null]; return field } else { field?.Indicators.push(null); return field } }); valueFields[valueFieldIndex].Indicators[valueFields[valueFieldIndex].Indicators.length - 1] = newValue } }"
                            :options="[noIndicatorOption, ...indicators]"
                            :optionLabel="'name'"
                            :optionValue="'key'"
                            placeholder="Choose an indicator field">
                        </Dropdown>
                    </div>
                    <div v-else>
                        <!-- Simple value field -->
                        <div class="edit-area-field">Value Field:</div>
                        <Dropdown class="near-width"
                            :modelValue="valueFields[valueFieldIndex]?.Indicator"
                            @update:modelValue="(newValue) => valueFields[valueFieldIndex].Indicator = newValue"
                            :options="[noIndicatorOption, ...indicators]"
                            :optionLabel="'name'"
                            :optionValue="'key'"
                            placeholder="Choose an indicator field">
                        </Dropdown>
                    </div>
                    <!-- Value field name -->
                    <div class="edit-area-field">Name:</div>
                    <InputText class="near-width"
                        :modelValue="valueFields[valueFieldIndex]?.Name"
                        @update:modelValue="(newValue) => valueFields[valueFieldIndex].Name = newValue">
                    </InputText>
                </div>
                <!-- Simple fields or composed fields -->
                <div class="edit-area-field">
                    Composed fields:
                    <InputSwitch
                        :modelValue="composedFields"
                        @update:modelValue="(isComposedField) => { if (isComposedField) { categoryFieldValues = [] } else { categoryFieldValues = null }; valueFields = valueFields.map(field => { if (isComposedField) { var newField = field; newField.Indicators = []; return newField } else { var newField = field; newField.Indicators = null; return newField } }) }">
                    </InputSwitch>
                </div>
                <!-- Simple category field or values -->
                <div v-if="composedFields">
                    <!-- Value field composed of multiple indicators -->
                    <div class="edit-area-field">Category Values:</div>
                    <!-- Alter values -->
                    <div v-for="(item, index) in (valueFields?.[0]?.Indicators ?? [])" :key="index">
                        <InputText class="near-width"
                            :modelValue="categoryFieldValues?.[index]"
                            @update:modelValue="(newValue) => { categoryFieldValues[index] = newValue }"
                            placeholder="Choose a category value">
                        </InputText>
                    </div>
                </div>
                <div v-else>
                    <!-- Simple category field -->
                    <div class="edit-area-field">Category Field:</div>
                    <Dropdown class="near-width"
                        v-model="categoryField"
                        :options="[noIndicatorOption, yearField]"
                        :optionLabel="'name'"
                        :optionValue="'key'"
                        placeholder="Choose an indicator field">
                    </Dropdown>
                </div>
                <!-- Category field name -->
                <div class="edit-area-field">Name:</div>
                <InputText class="near-width"
                    v-model="categoryFieldName">
                </InputText>
                <!-- Add additional value fields -->
                <Button label="Add Value Field" icon="pi pi-plus" class="p-button-success p-button-sm"
                    @click="{ console.log(valueFields, composedFields); if (valueFields === null || valueFields === undefined) { if (!composedFields) { valueFields = [{ Indicator: null }]} else { valueFields = [{ Indicators: null }] } } else { if (!composedFields) { valueFields = valueFields.concat([{ Indicator: null }]) } else { var nullIndicators = []; for (const _ of valueFields?.[0]?.Indicators) { nullIndicators.push(null) }; valueFields = valueFields.concat([{ Indicators: nullIndicators }]) } } }">
                </Button>
            </div>

            <div v-if="categoricalVisualisations.includes(visualisationType)">
                <!-- Item Limit -->
                <div class="edit-area-field">Category Limit:</div>
                <InputNumber
                    v-model="categoryLimit">
                </InputNumber>
            </div>
            <div v-if="barChartVisualisations.includes(visualisationType)">
                <!-- Sideways Bars -->
                <div class="edit-area-field">Sideways:</div>
                <InputSwitch
                    v-model="sideways">
                </InputSwitch>
            </div>

            <!-- Delete Visualisation -->
            <div :style="{ height: '5px' }"></div>

            <div class="full-width" :style="{ position: 'relative', width: '100%' }">
                <Button label="Delete Visualisation" icon="pi pi-trash" class="p-button-danger p-button-sm" @click="deleteVisualisation">
                </Button>
            </div>

            <div :style="{ height: '5px' }"></div>
        </div>
    </div>
</template>

<script>
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'

import Dropdown from 'primevue/dropdown'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import InputSwitch from 'primevue/inputswitch'

export default {
    components: {
        Dropdown,
        InputText,
        InputNumber,
        InputSwitch
    },
    data () {
        return {
            showPosition: false,
            noIndicatorOption: { key: null, name: 'No Indicator' },
            yearField: { key: 'Year', name: 'Year' },
            visualisationTypes: [
                'Single Value Display',
                'Fractional Value Display',
                'Progress Bar',
                'Radial Progress Bar',
                'Pie Chart',
                'Bar Chart',
                'Grouped Bar Chart',
                'Stacked Bar Chart',
                'Line Chart',
                'Multi-Series Line Chart',
                'Table'
            ],
            progressBarVisualisations: [
                'Progress Bar',
                'Radial Progress Bar'
            ],
            barChartVisualisations: [
                'Bar Chart',
                'Grouped Bar Chart',
                'Stacked Bar Chart'
            ],
            categoricalVisualisations: [
                'Pie Chart',
                'Bar Chart',
                'Grouped Bar Chart',
                'Stacked Bar Chart',
                'Line Chart',
                'Table'
            ],
            multiSeriesVisualisations: [
                'Multi-Series Line Chart'
            ]
        }
    },
    computed: {
        ...mapState('dashboardModel', ['selectionConfig']),
        visualisationId: {
            get () { return this.selectionConfig?.visualisationId }
        },
        visualisationTitle: {
            get () { return this.getVisualisationTitle()() },
            set (value) { this.setVisualisationTitle({ value: value }) }
        },
        visualisationType: {
            get () { return this.getVisualisationType()() },
            set (value) { this.changeVisualisationType({ value: value }) }
        },

        visualisationXStart: {
            get () { return this.getVisualisationXStart()() },
            set (value) { this.setVisualisationXStart({ value: value }) }
        },
        visualisationXEnd: {
            get () { return this.getVisualisationXEnd()() },
            set (value) { this.setVisualisationXEnd({ value: value }) }
        },
        visualisationYStart: {
            get () { return this.getVisualisationYStart()() },
            set (value) { this.setVisualisationYStart({ value: value }) }
        },
        visualisationYEnd: {
            get () { return this.getVisualisationYEnd()() },
            set (value) { this.setVisualisationYEnd({ value: value }) }
        },
        valueFields: {
            get () { return this.getValueFields()() ?? [] },
            set (value) { this.updateValueFields({ value: value }) }
        },
        valueField: {
            get () { return this.getValueField()()?.Indicator },
            set (value) { this.updateValueField({ value: { Indicator: value } }) }
        },
        valueFieldIndicators: {
            get () { return this.getValueField()()?.Indicators },
            set (value) { this.updateValueField({ value: { Indicators: value } }) }
        },
        fractionalValueField: {
            get () { return this.getFractionalValueField()()?.Indicator },
            set (value) { this.updateFractionalValueField({ value: { Indicator: value } }) }
        },
        totalValueField: {
            get () { return this.getTotalValueField()()?.Indicator },
            set (value) { this.updateTotalValueField({ value: { Indicator: value } }) }
        },
        currentValueField: {
            get () { return this.getCurrentValueField()()?.Indicator },
            set (value) { this.updateCurrentValueField({ value: { Indicator: value } }) }
        },
        targetValueField: {
            get () { return this.getTargetValueField()()?.Indicator },
            set (value) { this.updateTargetValueField({ value: { Indicator: value } }) }
        },
        categoryField: {
            get () { return this.getCategoryField()()?.['Named Field'] },
            set (value) { this.updateCategoryField({ value: { 'Named Field': value } }) }
        },
        categoryFieldValues: {
            get () { return this.getCategoryField()()?.Values },
            set (value) { this.updateCategoryField({ value: { Values: value } }) }
        },
        groupingField: {
            get () { return this.getGroupingField()()?.['Named Field'] },
            set (value) { this.updateGroupingField({ value: { 'Named Field': value } }) }
        },
        groupingFieldValues: {
            get () { return this.getGroupingField()()?.Values },
            set (value) { this.updateGroupingField({ value: { Values: value } }) }
        },
        stackingField: {
            get () { return this.getStackingField()()?.['Named Field'] },
            set (value) { this.updateStackingField({ value: { 'Named Field': value } }) }
        },
        stackingFieldValues: {
            get () { return this.getStackingField()()?.Values },
            set (value) { this.updateStackingField({ value: { Values: value } }) }
        },

        valueFieldName: {
            get () { return this.getValueFieldName()() },
            set (value) { this.setValueFieldName({ value: value }) }
        },
        fractionalValueFieldName: {
            get () { return this.getFractionalValueFieldName()() },
            set (value) { this.setFractionalValueFieldName({ value: value }) }
        },
        totalValueFieldName: {
            get () { return this.getTotalValueFieldName()() },
            set (value) { this.setTotalValueFieldName({ value: value }) }
        },
        currentValueFieldName: {
            get () { return this.getCurrentValueFieldName()() },
            set (value) { this.setCurrentValueFieldName({ value: value }) }
        },
        targetValueFieldName: {
            get () { return this.getTargetValueFieldName()() },
            set (value) { this.setTargetValueFieldName({ value: value }) }
        },
        categoryFieldName: {
            get () { return this.getCategoryFieldName()() },
            set (value) { this.setCategoryFieldName({ value: value }) }
        },
        groupingFieldName: {
            get () { return this.getGroupingFieldName()() },
            set (value) { this.updateGroupingFieldName({ value: value }) }
        },
        stackingFieldName: {
            get () { return this.getStackingFieldName()() },
            set (value) { this.updateStackingFieldName({ value: value }) }
        },
        indicators: {
            get () {
                const indicators = this.getIndicators()()
                const sortedIndicators = indicators.sort(function (a, b) { if (a.name > b.name) return 1; if (a.name < b.name) return -1; return 0 })
                return sortedIndicators
            }
        },
        composedField: {
            get () { return this.valueFieldIndicators !== null && this.valueFieldIndicators !== undefined }
        },
        composedFields: {
            get () { for (var field of this.valueFields) { if (field?.Indicators !== null && field?.Indicators !== undefined) { return true } } return false }
        },
        categoryLimit: {
            get () { return this.getCategoryLimit()() },
            set (value) { this.updateCategoryLimit({ value: value }) }
        },
        sideways: {
            get () { return this.getSideways()() },
            set (value) { this.updateSideways({ value: value }) }
        }
    },
    methods: {
        ...mapGetters('dashboardData', ['getIndicators']),

        ...mapGetters('dashboardModel', ['getVisualisationTitle', 'getVisualisationType', // Title & Type
            'getVisualisationXStart', 'getVisualisationXEnd', 'getVisualisationYStart', 'getVisualisationYEnd', // Position
            'getValueField', 'getValueFields', 'getFractionalValueField', 'getTotalValueField', 'getCurrentValueField', 'getTargetValueField', 'getCategoryField', 'getGroupingField', 'getStackingField', // Fields
            'getValueFieldName', 'getFractionalValueFieldName', 'getTotalValueFieldName', 'getCurrentValueFieldName', 'getTargetValueFieldName', 'getCategoryFieldName', 'getGroupingFieldName', 'getStackingFieldName', // Field Names
            'getCategoryLimit', // Category Limit
            'getSideways' // Bar chart sideways
        ]),
        ...mapMutations('dashboardModel', ['setVisualisationTitle', // Title
            'setVisualisationXStart', 'setVisualisationXEnd', 'setVisualisationYStart', 'setVisualisationYEnd', // Position
            'setValueFieldName', 'setFractionalValueFieldName', 'setTotalValueFieldName', 'setCurrentValueFieldName', 'setTargetValueFieldName', 'setCategoryFieldName', 'setGroupingFieldName', 'setStackingFieldName' // Field Names
        ]),
        ...mapActions('dashboardModel', ['addVisualisation', 'deleteVisualisation', // Add / Delete
            'changeVisualisationType', // Change type
            'updateValueField', 'updateValueFields', 'updateFractionalValueField', 'updateTotalValueField', 'updateCurrentValueField', 'updateTargetValueField', 'updateCategoryField', 'updateGroupingField', 'updateStackingField', // Fields
            'updateCategoryLimit', // Category Limit
            'updateSideways' // Bar chart sideways
        ])
    }
}
</script>
