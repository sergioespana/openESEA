<template>
    <div class="flex flex-column">

        <!-- Edit area title -->
        <div class="edit-area-title">Visualisation</div>

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
            <Dropdown class="near-width"
                :options="indicators">
            </Dropdown>
        </div>
    </div>
</template>

<script>
import { mapState, mapGetters, mapMutations } from 'vuex'

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
        indicators: {
            get () { return this.getIndicators()() }
        }
    },
    methods: {
        ...mapGetters('dashboardData', ['getIndicators']),

        ...mapGetters('dashboardModel', ['getVisualisationTitle', 'getVisualisationType', 'getVisualisationXStart', 'getVisualisationXEnd', 'getVisualisationYStart', 'getVisualisationYEnd']),
        ...mapMutations('dashboardModel', ['setVisualisationTitle', 'setVisualisationType', 'setVisualisationXStart', 'setVisualisationXEnd', 'setVisualisationYStart', 'setVisualisationYEnd'])
    }
}
</script>
