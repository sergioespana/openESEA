<template>
    <div class="edit-element">
        <div class="edit-panel" v-on:click="onClick">
        </div>
        <div v-if="this.editing" class="edit-area">
            <select class="value-selection" @change="onValueChange($event)">
                <option :value="null"></option>
                <option
                    v-for="(item, index) in dataColumns"
                    :key="index"
                    :value="item.field"
                    :selected="item.field === selectedValueField">
                    {{item.field}}
                </option>
            </select>
            <select class="category-selection" @change="onCategoryChange($event)">
                <option :value="null"></option>
                <option
                    v-for="(item, index) in dataColumns"
                    :key="index"
                    :value="item.field"
                    :selected="item.field === selectedCategoryField">
                    {{item.field}}
                </option>
            </select>
        </div>
    </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'

export default {
    name: 'EditDashboardElement',
    data () {
        return {
            editing: false
        }
    },
    computed: {
        dataColumns () {
            const indicatorFields = this.getIndicatorFields()()
            return indicatorFields.map(el => ({ fieldType: 'Indicator', field: el }))
        },
        visualisationConfig () {
            console.log('config')
            return this.getSelectedVisualisation()()
        },
        selectedValueField () {
            console.log('value')
            const config = this.visualisationConfig
            console.log(this.visualisationConfig)
            const field = this.getVisualisationIndicators()(config)
            console.log('FIELD', field)
            return field
        },
        selectedCategoryField () {
            console.log('category')
            return this.getVisualisationCategories()(this.getSelectedVisualisation()())
        }
    },
    methods: {
        ...mapGetters('dashboardModel', { getVisualisationIndicators: 'getVisualisationIndicators', getVisualisationCategories: 'getVisualisationCategories' }),
        ...mapGetters('dashboardData', { getIndicatorFields: 'getIndicatorFields' }),
        ...mapGetters('dashboardEditing', { getSelectedVisualisation: 'getSelectedVisualisation' }),
        ...mapMutations('dashboardModel', { setVisualisationValueField: 'setVisualisationValueField', setVisualisationCategoryField: 'setVisualisationCategoryField' }),
        onClick () {
            this.editing = !this.editing
            var pixels = 10
            pixels += this.editing * 200

            const element = document.querySelector('.dashboards')
            element.style.setProperty('--edit-element-width', pixels + 'px')
        },
        async onValueChange (event) {
            const selectedValue = event.target.value
            console.log('Selected', selectedValue)
            const config = this.visualisationConfig
            config.field = selectedValue
            const indicatorFields = this.getIndicatorFields()()
            if (indicatorFields.includes(selectedValue)) {
                config.fieldType = 'Indicator'
            } else {
                config.fieldType = 'Column'
            }
            await this.setVisualisationValueField(config)
            console.log('CONFIG', config)
        },
        async onCategoryChange (event) {
            const selectedValue = event.target.value
            const config = this.visualisationConfig
            config.field = selectedValue
            const indicatorFields = this.getIndicatorFields()()
            if (indicatorFields.includes(selectedValue)) {
                config.fieldType = 'Indicator'
            } else {
                config.fieldType = 'Column'
            }
            await this.setVisualisationCategoryField(config)
            console.log(selectedValue)
        }
    }
}
</script>

<style>
.edit-panel {
    width: 10px;
    height: 100%;
    right: 0;
    position: absolute;
    border-color: lightgray;
    border-style: solid;
    background-color: #e8e8e8;
    cursor: pointer;
    z-index: 10;
}
.edit-area {
    right: 10px;
    width: 200px;
    height: 100%;
    position: absolute;
    border-color: lightgray;
    border-style: solid;
    z-index: 10;
}
</style>
