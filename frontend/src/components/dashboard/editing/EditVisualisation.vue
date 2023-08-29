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
        <div v-if="visualisationId === null">
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
                    :options="[{ key: null, name: 'No Indicator' }, ...indicators]"
                    :optionLabel="'name'"
                    :optionValue="'key'"
                    placeholder="Choose an indicator field">
                </Dropdown>
            </div>
            <div v-else-if="visualisationType === 'Fractional Value Display'">
                <div class="edit-area-field">Fractional Value Field:</div>
                <Dropdown class="near-width"
                    v-model="fractionalValueField"
                    :options="[{ key: null, name: 'No Indicator' }, ...indicators]"
                    :optionLabel="'name'"
                    :optionValue="'key'"
                    placeholder="Choose an indicator field">
                </Dropdown>
                <div class="edit-area-field">Total Value Field:</div>
                <Dropdown class="near-width"
                    v-model="totalValueField"
                    :options="[{ key: null, name: 'No Indicator' }, ...indicators]"
                    :optionLabel="'name'"
                    :optionValue="'key'"
                    placeholder="Choose an indicator field">
                </Dropdown>
            </div>
            <div v-else-if="visualisationType === 'Progress Bar'">
                <div class="edit-area-field">Current Value Field:</div>
                <Dropdown class="near-width"
                    v-model="currentValueField"
                    :options="[{ key: null, name: 'No Indicator' }, ...indicators]"
                    :optionLabel="'name'"
                    :optionValue="'key'"
                    placeholder="Choose an indicator field">
                </Dropdown>
                <div class="edit-area-field">Target Value Field:</div>
                <Dropdown class="near-width"
                    v-model="targetValueField"
                    :options="[{ key: null, name: 'No Indicator' }, ...indicators]"
                    :optionLabel="'name'"
                    :optionValue="'key'"
                    placeholder="Choose an indicator field">
                </Dropdown>
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

import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Dropdown from 'primevue/dropdown'

export default {
    components: {
        InputText,
        InputNumber,
        Dropdown
    },
    data () {
        return {
            showPosition: false,
            visualisationTypes: [
                'Single Value Display',
                'Fractional Value Display',
                'Progress Bar',
                'Pie Chart',
                'Bar Chart',
                'Line Chart'
            ]
        }
    },
    computed: {
        ...mapState('dashboardModel', ['selectionConfig']),
        visualisationId: {
            get () { return this.selectionConfig?.visualisationId ?? null }
        },
        visualisationTitle: {
            get () { return this.getVisualisationTitle()() },
            set (value) { this.setVisualisationTitle({ value: value }) }
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
        visualisationType: {
            get () { return this.getVisualisationType()() },
            set (value) { this.setVisualisationType({ value: value }) }
        },
        valueField: {
            get () { return this.getValueField()()?.Indicator },
            set (value) { this.updateValueField({ value: { Indicator: value } }) }
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
        indicators: {
            get () { return this.getIndicators()() }
        }
    },
    methods: {
        ...mapGetters('dashboardData', ['getIndicators']),

        ...mapGetters('dashboardModel', ['getVisualisationTitle', 'getVisualisationType', 'getVisualisationXStart', 'getVisualisationXEnd', 'getVisualisationYStart', 'getVisualisationYEnd', 'getValueField', 'getFractionalValueField', 'getTotalValueField', 'getCurrentValueField', 'getTargetValueField']),
        ...mapMutations('dashboardModel', ['setVisualisationTitle', 'setVisualisationType', 'setVisualisationXStart', 'setVisualisationXEnd', 'setVisualisationYStart', 'setVisualisationYEnd']),
        ...mapActions('dashboardModel', ['addVisualisation', 'deleteVisualisation', 'updateValueField', 'updateFractionalValueField', 'updateTotalValueField', 'updateCurrentValueField', 'updateTargetValueField'])
    }
}
</script>
