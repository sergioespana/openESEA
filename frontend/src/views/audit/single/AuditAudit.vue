<template>
    <div class="p-grid p-mx-5">
        <div class="p-col-12 p-as-start">
            <div class="p-col-12 p-d-flex p-ai-center p-jc-between">
                <h2 class="p-text-left">Audit</h2>
                <Button @click="(helpDialog = !helpDialog)" label="Help" class="p-button-sm p-button-warning" icon="pi pi-external-link" />
            </div>
            <div class="card">
                 <DataTable :value="questions" rowGroupMode="rowspan" groupRowsBy="section.name" selectionMode="single" @row-select="goToQuestion" sortMode="single" sortField="section.name" :sortOrder="1" responsiveLayout="scroll"
                v-model:expandedRowGroups="expandedRowGroups" @rowgroupExpand="onRowGroupExpand" @rowgroupCollapse="onRowGroupCollapse" dataKey="name">
                    <Column field="section.name" header="Section"></Column>
                    <Column field="name" header="name" sortable></Column>
                    <Column field="response" header="Responses" sortable></Column>
                    <Column field="status" header="Status">
                    </Column>
                    <Column headerStyle="width: 10rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                        <template #body="">
                            Open
                            <Button icon="pi pi-check" disabled="true" class="p-button-sm" />
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
        <div class="p-text-right p-col-12">
            <Button class="p-my-5" label="Finish" icon="pi pi-check" @click="finishAudit()" />
        </div>
    </div>
</template>

<script>
export default {
    data () {
        return {
            helpDialog: false,
            questions: [
                {
                    name: 'What is the total number of men staff?',
                    response: 5,
                    status: 'Awaiting documentation',
                    section: { name: 'Gender' }
                },
                {
                    name: 'What is the total number of women staff?',
                    response: 7,
                    status: 'Open',
                    section: { name: 'Gender' }

                },
                {
                    name: 'What is the average monthly salary per employee?',
                    response: '$4000',
                    status: 'Verified',
                    section: { name: 'Salary' }
                }
            ]
        }
    },
    methods: {
        finishAudit () {
            console.log('finishing audit')
        },
        goToQuestion (question) {
            console.log('go to Question')
            question = { id: 5 }
            if (question.id) {
                // await this.setQuestion(question)
                this.$router.push({ name: 'singleauditquestion', params: { QuestionId: question.id } })
            }
        }
    }
}
</script>
