<template>
    <div class="table">
        <DataTable showGridlines
            :value="data"
            :paginator="true" :rows="10"
            :rowsPerPageOptions="[lowerRowLimit, higherRowLimit]">
            <template #header v-if="title">
                <div class="flex flex-wrap align-items-center justify-content-between gap-2">
                    <span class="text-xl text-900 font-bold">{{ title }}</span>
                </div>
            </template>
            <Column v-for="field of fields" :key="field.key" :field="field.key" :header="field.name">
            </Column>
        </DataTable>
    </div>
</template>

<script>
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

export default {
    name: 'Table',
    components: {
        DataTable,
        Column
    },
    props: {
        chartData: {
            type: Object,
            required: true
        }
    },
    computed: {
        lowerRowLimit: {
            get () { return (this.chartData.options?.categoryLimit === null || this.chartData.options?.categoryLimit === undefined) ? 5 : this.chartData.options?.categoryLimit }
        },
        higherRowLimit: {
            get () { return (this.chartData.options?.categoryLimit === null || this.chartData.options?.categoryLimit === undefined) ? 10 : (this.chartData.options?.categoryLimit * 2) }
        },
        data: {
            get () { return this.getData(this.chartData) }
        },
        fields: {
            get () { return this.listFields(this.chartData) }
        },
        title: {
            get () { return this.getTitle(this.chartData) }
        }
    },
    methods: {
        getData (chartData) {
            return chartData.data
        },
        listFields (chartData) {
            const mapping = chartData.mapping
            if (!mapping) return []
            var fields = []
            const categoryFieldData = mapping?.['Category Field']
            if (categoryFieldData) fields.push(this.getFieldInfo(categoryFieldData))
            const valueFieldData = mapping?.['Value Field']
            if (valueFieldData) fields.push(this.getFieldInfo(valueFieldData))
            return fields
        },
        getFieldInfo (fieldData) {
            const fieldKey = fieldData.key
            const fieldName = fieldData?.name ?? fieldData.key
            const info = { key: fieldKey, name: fieldName }
            return info
        },
        getTitle (chartData) {
            return chartData.title
        }
    }
}
</script>

<style>
.table {
    width: 100%;
    height: 100%;
}
</style>
