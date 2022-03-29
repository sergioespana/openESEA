<template>
    <div class="p-grid p-mx-5">
        <div class="p-col-12 p-as-start">
            <!--<div class="p-col-12 p-d-flex p-ai-center p-jc-between">-->
            <h2 class="p-text-left">Audit Results</h2>
            <Card v-if="surveyAudit.status === 'verified'" class="p-text-left p-m-2">
            <template #title>
            Audit Result
            </template>
            <template #content class="p-col-12">
            <div class="p-mr-5">
                <div class="p-grid">
                    <div class="p-col-2 p-text-center"><i class="pi pi-check" style="font-size: 3rem; background-color: #689F38; color: white; border-radius: 50%; padding: 30px;"></i></div>
                    <div class="p-col-10">
                        <h3 class="p-mt-0 p-pt-0">Single Stakeholder Survey</h3>
                        The auditor has verified this survey.
                    </div>
                </div>
            </div>
            </template>
        </Card>

        <Card v-if="surveyAudit.status === 'rejected'" class="p-text-left p-m-2">
            <template #title>
            Audit Result
            </template>
            <template #content class="p-col-12">
            <div class="p-mr-5">
                <div class="p-grid">
                    <div class="p-col-2 p-text-center"><i class="pi pi-times" style="font-size: 3rem; background-color: red; color: white; border-radius: 50%; padding: 30px;"></i></div>
                    <div class="p-col-10">
                        <h3 class="p-mt-0 p-pt-0">Single Stakeholder Survey</h3>
                        Unfortunately, the auditor has rejected this survey.
                    </div>
                </div>
            </div>
            </template>
        </Card>
            <div class="card">
                 <DataTable :value="selectedIndicators" rowGroupMode="rowspan" groupRowsBy="section.name" selectionMode="single" @row-select="goToQuestion" sortMode="single" sortField="section.name" :sortOrder="1" responsiveLayout="scroll"
                v-model:expandedRowGroups="expandedRowGroups" @rowgroupExpand="onRowGroupExpand" @rowgroupCollapse="onRowGroupCollapse" dataKey="name">
                    <Column field="topic" header="Section"></Column>
                    <Column field="name" header="name" sortable></Column>
                    <Column field="value" header="Responses" sortable></Column>
                    <Column header="Status" headerStyle="width: 15rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                        <template #body="data">
                            <div class="p-d-flex p-ai-center p-jc-between">
                                {{data.data.question_response.auditstatus}}
                                <Button v-if="data.data.question_response.auditstatus === 'Verified'" icon="pi pi-check"  style="border-radius: 50%; background-color: green; border: none;" />
                        <Button v-else-if="data.data.question_response.auditstatus === 'Rejected'" icon="pi pi-times" style="border-radius: 50%; background-color: red; border: none;" />
                        <Button v-else-if="data.data.question_response.auditstatus === 'Awaiting Correction'" style="border-radius: 50%; p-col-12; background-color: #FBC02D; border: none;" />
                        <Button v-else style="border-radius: 50%; background-color: #2196F3; border: none;" />
                            </div>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        data () {
            return {
                questions: [
                    {
                        name: 'What is the total number of men staff?',
                        response: 5,
                        status: 'verified',
                        section: { name: 'Gender' }
                    },
                    {
                        name: 'What is the total number of women staff?',
                        response: 7,
                        status: 'open',
                        section: { name: 'Gender' }

                    },
                    {
                        name: 'What is the average monthly salary per employee?',
                        response: '$4000',
                        status: 'rejected',
                        section: { name: 'Salary' }
                    }
                ]
            }
        },
        computed: {
            ...mapState('surveyAudit', ['surveyAudit']),
            ...mapState('auditIndicators', ['selectedIndicators'])
        },
        methods: {
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
