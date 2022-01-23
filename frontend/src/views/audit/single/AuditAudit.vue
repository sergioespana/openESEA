<template>
    <div class="p-grid p-mx-5">
        <div class="p-col-12 p-as-start">
            <div class="p-col-12 p-d-flex p-ai-center p-jc-between">
                <h2 class="p-text-left">Audit</h2>
                <Button @click="(helpDialog = !helpDialog)" label="Help" class="p-button-sm p-button-warning" icon="pi pi-external-link" />
            </div>
            <div class="card">
                 <DataTable :value="selectedIndicators" rowGroupMode="rowspan" groupRowsBy="section.name" selectionMode="single" @row-select="goToQuestion" sortMode="single" sortField="section.name" :sortOrder="1" responsiveLayout="scroll"
                v-model:expandedRowGroups="expandedRowGroups" @rowgroupExpand="onRowGroupExpand" @rowgroupCollapse="onRowGroupCollapse" dataKey="name">
                    <Column field="topic" header="Topic"></Column>
                    <Column field="name" header="Name" sortable></Column>
                    <Column field="value" header="Value" sortable></Column>
                    <Column header="Status" headerStyle="width: 10rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
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
    import { mapState, mapActions } from 'vuex'

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
        computed: {
            ...mapState('auditIndicators', ['selectedIndicators', 'indicator'])
        },
        methods: {
            ...mapActions('auditIndicators', ['setSelectedIndicator']),
            finishAudit () {
                console.log('finishing audit')
            },
            async goToQuestion (question) {
                await this.setSelectedIndicator({ id: question.data.id })
                if (this.indicator.id) {
                    // await this.setQuestion(question)
                    this.$router.push({ name: 'singleauditquestion', params: { QuestionId: this.indicator.id } })
                }
            }
        }
    }
</script>
