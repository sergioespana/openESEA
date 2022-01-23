<template>
    <div class="p-grid p-mx-5">
        <div class="p-col-12 p-as-start">
        <div class="p-col-12 p-d-flex p-ai-center p-jc-between">
            <h2 class="p-text-left">Documentation Request</h2>
            <Button @click="(helpDialog = !helpDialog)" label="Help" class="p-button-sm p-button-warning" icon="pi pi-external-link" />
        </div>
        <div class="card">
            <DataTable :value="selectedIndicators" rowGroupMode="rowspan" groupRowsBy="section.name" sortMode="single" sortField="section.name" :sortOrder="1" responsiveLayout="scroll"
            v-model:expandedRowGroups="expandedRowGroups" @rowgroupExpand="onRowGroupExpand" @rowgroupCollapse="onRowGroupCollapse" v-model:selection="selectedQuestions" dataKey="name">
                <Column selectionMode="multiple" headerStyle="width: 3em"></Column>
                <Column field="topic" header="Topic" sortable></Column>
                <Column field="name" header="Name" sortable></Column>
                <Column field="value" header="Value"></Column>
                <Column field="indicator_impact" header="Impact" sortable></Column>
                <Column header="Outliers" sortable>
                    <template #body="">
                        Y
                    </template>
                </Column>
                <Column sortable>
                    <template #body="">
                        <Button label="Recommended" class="p-button-sm p-button-danger p-button-rounded p-py-1" @click="openRecommended()" />
                    </template>
                </Column>
                <Column headerStyle="width: 10rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                    <template #body="row">
                        <Button v-if="this.selectedQuestions.find(object => object.id === row.data.id)" label="Message" icon="pi pi-plus" class="p-button-sm p-button-success" @click="openMessage(row.data)" />
                    </template>
                </Column>
            </DataTable>
        </div>
        </div>
        <div class="p-text-right p-col-12 p-as-end">
            <Button class="p-my-5" label="Request documentation" @click="requestDocumentation()" icon="pi pi-check" />
            <Button class="p-my-5 p-ml-2" label="Audit" @click="requestDocumentation()" />
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
        <p>About: '{{MessagedIndicator.name}}'</p>
        <Textarea class="p-col-12" id="description" v-model="message" :autoResize="true" rows="3" />
        <template #footer>
            <Button label="Cancel" class="p-button-sm" icon="pi pi-times" @click="(messageToOrganisationDialog = false)" />
            <Button label="Save" class="p-button-sm p-button-success" icon="pi pi-check" @click="saveMessage()" />
        </template>
    </Dialog>
</template>

<script>
    import { mapState } from 'vuex'
    // import Tag from 'primevue/tag'

export default {
    components: {
        // Tag
    },
    data () {
        return {
            helpDialog: false,
            messageToOrganisationDialog: false,
            message: '',
            MessagedIndicator: null,
            expandedRowGroups: null,
            selectedQuestions: [],
            questions: [
                {
                    name: 'What is the total number of men staff?',
                    response: 5,
                    recommendations: '',
                    section: { name: 'Gender' }
                },
                {
                    name: 'What is the total number of women staff?',
                    response: 7,
                    recommendations: '',
                    section: { name: 'Gender' }

                },
                {
                    name: 'What is the average monthly salary per employee?',
                    response: '$4000',
                    recommendations: '',
                    section: { name: 'Salary' }
                }
            ]
        }
    },
    computed: {
        ...mapState('auditIndicators', ['indicators', 'selectedIndicators'])
    },
    methods: {
        requestDocumentation () {
            // Attach message to indicator
            // this.selectedQuestions
            this.$router.push({ name: 'singleauditaudit', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } })
        },
        openMessage (indicator) {
            this.MessagedIndicator = indicator
            this.messageToOrganisationDialog = true
        },
        saveMessage () {
            this.MessagedIndicator.message = this.message
            this.selectedIndicators = this.selectedIndicators.map((item) => {
                if (item.id !== this.MessagedIndicator.id) { return item }
                return Object.assign(item, this.MessagedIndicator)
            })
            this.messageToOrganisationDialog = false
        },
        openRecommended () {
            print()
        }
    }
}
</script>
