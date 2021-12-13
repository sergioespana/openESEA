<template>
    <div class="p-grid vertical-container">
        <div class="p-col-12 p-as-start">
        <div class="p-d-flex p-ai-center p-jc-between">
            <h2 class="p-text-left">Audit Selection</h2>
            <Button @click="(helpDialog = !helpDialog)" label="Help" class="p-button-sm p-button-warning" icon="pi pi-external-link" />
        </div>
        <div class="card">
            <DataTable :value="questions" rowGroupMode="rowspan" groupRowsBy="section.name" sortMode="single" sortField="section.name" :sortOrder="1" responsiveLayout="scroll"
            v-model:expandedRowGroups="expandedRowGroups" @rowgroupExpand="onRowGroupExpand" @rowgroupCollapse="onRowGroupCollapse" v-model:selection="selectedQuestions" dataKey="name">
                <Column selectionMode="multiple" headerStyle="width: 3em"></Column>
                <Column field="section.name" header="Section"></Column>
                <Column field="name" header="name" sortable></Column>
                <Column field="responses" header="Responses" sortable></Column>
                <Column field="recommendations" header="Recommendations">
                    <template #body="">
                        status
                    </template>
                </Column>
                <!-- <Column header="Status" headerStyle="width: 15rem; text-align: center" bodyStyle="text-align: center; overflow: visible" :style="permission ? '': 'display:none;'">
                    <template #body="{data}">
                        <div v-if="permission">
                            <div v-if="data.auditobject">{{data.auditobject}}</div>
                            <Button v-else label="Start Audit" type="button" class="p-button-sm" @click="startAudit(data)"  style="width: 200px" />
                        </div>
                        <div v-else></div>
                    </template>
rowGroupMode="subheader" groupRowsBy="section"
                sortMode="single" sortField="section" :sortOrder="1" responsiveLayout="scroll"
                :expandableRowGroups="true" v-model:expandedRowGroups="expandedRowGroups"
                @rowgroupExpand="onRowGroupExpand" @rowgroupCollapse="onRowGroupCollapse"

                </Column> -->
            </DataTable>
        </div>
        </div>
        <div class="p-text-right p-col-12 p-as-end">
            <Button class="p-m-5" label="Start audit for selected questions" icon="pi pi-check" />
        </div>
        <Dialog v-model:visible="helpDialog" style="width: 500px;" header="Help" :modal="true" dismissableMask="true">
            <p>Please select the questions that you want to audit.</p>

            <p>In the next step, you will be able to request documentation for your selected questions.</p>
            <template #footer>
                <Button label="Ok" icon="pi pi-check" @click="(helpDialog = !helpDialog)" />
            </template>
        </Dialog>

    </div>
</template>

<script>
export default {
    data () {
        return {
            helpDialog: false,
            expandedRowGroups: null,
            selectedQuestions: [],
            questions: [
                {
                    name: 'What is the total number of men staff?',
                    responses: 5,
                    recommendations: '',
                    section: { name: 'Gender' }
                },
                {
                    name: 'What is the total number of women staff?',
                    responses: 5,
                    recommendations: '',
                    section: { name: 'Gender' }

                },
                {
                    name: 'What is the average monthly salary per employee?',
                    responses: 5,
                    recommendations: '',
                    section: { name: 'Salary' }
                }
            ]
        }
    },
    methods: {
        onRowGroupExpand () {
        },
        onRowGroupCollapse () {
        }
    }
}
</script>
