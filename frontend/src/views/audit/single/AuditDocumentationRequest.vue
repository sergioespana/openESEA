<template>
    <div class="p-grid vertical-container p-m-5">
        <div class="p-col-12 p-d-flex p-ai-center p-jc-between">
            <h2 class="p-text-left">Documentation Request</h2>
            <Button @click="(helpDialog = !helpDialog)" label="Help" class="p-button-sm p-button-warning" icon="pi pi-external-link" />
        </div>
        <div class="p-col-12 card">
            <DataTable :value="questions" rowGroupMode="rowspan" groupRowsBy="section.name" sortMode="single" sortField="section.name" :sortOrder="1" responsiveLayout="scroll"
            v-model:expandedRowGroups="expandedRowGroups" @rowgroupExpand="onRowGroupExpand" @rowgroupCollapse="onRowGroupCollapse" v-model:selection="selectedQuestions" dataKey="name">
                <Column selectionMode="multiple" headerStyle="width: 3em"></Column>
                <Column field="section.name" header="Section"></Column>
                <Column field="name" header="name" sortable></Column>
                <Column field="responses" header="Responses" sortable></Column>
                <Column field="recommendations" headerStyle="width: 5rem;">
                    <template #body="">
                        <Tag v-if="true" severity="danger" value="Recommendation"></Tag>
                    </template>
                </Column>
                <Column headerStyle="width: 10rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                    <template #body="">
                        <Button label="Message" icon="pi pi-plus" class="p-button-sm p-button-success" @click="messageToOrganisationDialog = true" />
                    </template>
                </Column>
            </DataTable>
        </div>
    </div>

    <Dialog v-model:visible="helpDialog" style="width: 500px;" header="Help" :modal="true" dismissableMask="true">
        <p>Select the questions for which you want to request documentation. Attach a message to request specific documentation or add other remarks.</p>

        <p>During the audit, you will be able to upload your own documentation.</p>
        <template #footer>
            <Button label="Ok" icon="pi pi-check" @click="(helpDialog = !helpDialog)" />
        </template>
    </Dialog>

        <Dialog v-model:visible="messageToOrganisationDialog" style="width: 500px;" header="Message to Organisation" :modal="true" dismissableMask="true">
            <h5>Receiver: Sjaak Chocolonely</h5>
            <Textarea class="p-col-12" id="description" v-model="message" :autoResize="true" rows="3" />
        <template #footer>
            <Button label="Cancel" class="p-button-sm" icon="pi pi-times" @click="(messageToOrganisationDialog = false)" />
            <Button label="Save" class="p-button-sm p-button-success" icon="pi pi-check" @click="saveMessage()" />
        </template>
    </Dialog>
</template>

<script>
    import Tag from 'primevue/tag'

export default {
    components: {
        Tag
    },
    data () {
        return {
            helpDialog: false,
            messageToOrganisationDialog: false,
            message: '',
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
        saveMessage () {
            console.log('e')
        }
    }
}
</script>
