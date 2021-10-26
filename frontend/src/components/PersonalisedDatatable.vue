<template>
        <DataTable ref="dt" :value="customData" v-model:selection="selectedRows" :selectionMode="selectionToggle? 'multiple' : 'single'" dataKey="id" :metaKeySelection="false" @row-select="onRowSelect"
        :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

            <!-- <h1>{{tableName}}</h1> -->
            <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field">
            <template v-if="col.field === 'ispublic'" #body="slotProps">
                <i class="pi" :class="{'true-icon pi-check-circle': slotProps.data.ispublic, 'false-icon pi-times-circle': !slotProps.data.ispublic}"></i>
            </template>
            </Column>
        </DataTable>
</template>

<script>
export default {
    props: {
        tableName: {
            type: String
        },
        customData: {
            type: Object
        },
        columns: {
            type: Array
        },
        selectionToggle: {
            type: Boolean
        },
        filters: {
            type: Object
        }
    },
    data () {
        return {
            selectedRows: null
            // enableButton: { name: 'Off', value: false },
            // options: [{ name: 'Off', value: false }, { name: 'On', value: true }]
        }
    },
    watch: {
        selectedRows: function (val) {
            if (val) {
            console.log(this.selectedRows)
            }
        }
    },
    methods: {
        onRowSelect (event) {
            this.$emit('item-redirect', this.selectedRows)
        }
    }
}
</script>
