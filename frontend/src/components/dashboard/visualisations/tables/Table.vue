<template>
    <div class="table">
        <!-- showGridlines autoLayout -->
        <DataTable :value="data"
        :paginator="true" :rows="10"
        :rowsPerPageOptions="[5,10]">
            <Column v-for="(col, key) of Object.entries(data)" :header="key" :key="key"/>
            <!-- :field="key"  :key="key"  -->
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
            data: {
                type: Object,
                required: true
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
