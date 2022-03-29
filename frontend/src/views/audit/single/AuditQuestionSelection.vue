<template>
    <div class="p-grid p-m-5">
        <div class="p-col-12 p-d-flex p-ai-center p-jc-between">
            <h2 class="p-text-left">Audit Selection</h2>
            <!-- {{selectedQuestions}} -->
            <!-- {{chosenDirectIndicators}} -->
            <Button @click="(helpDialog = !helpDialog)" label="Help" class="p-button-sm p-button-warning" icon="pi pi-external-link" />
        </div>
        <DataTable class="p-col-12" :value="indicators" rowGroupMode="rowspan" groupRowsBy="section.name" sortMode="single" sortField="section.name" :sortOrder="1" responsiveLayout="scroll"
        v-model:expandedRowGroups="expandedRowGroups" @rowgroupExpand="onRowGroupExpand" @rowgroupCollapse="onRowGroupCollapse" v-model:selection="selectedQuestions" dataKey="name">
            <Column selectionMode="multiple" headerStyle="width: 3em"></Column>
            <Column field="topic" header="Topic" sortable></Column>
            <Column field="name" header="Name" sortable></Column>
            <Column field="value" header="Value"></Column>
            <Column field="critical_impact" header="Critical Impact" sortable>
                <template #body="data"> <!-- (row.data.critical_impact & row.data.outliers) -->
                    <Button v-if="data.data.critical_impact" label="Critical" class="p-button-sm p-button-rounded p-py-1 p-button-danger" @click="openCriticalDialog(data.data)" />
                </template>
            </Column>
            <Column header="Anomaly" sortable>
                <template #body="row"> <!-- (row.data.critical_impact & row.data.outliers) -->
                    <Button v-if="row.data.outliers" label="Anomaly" class="p-button-sm p-button-rounded p-py-1 p-button-danger" />
                </template>
            </Column>
            <Column headerStyle="width: 4rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                <template #body="data">
                    <Button @click="ShowOutlierDetectionMethods(data)" icon="pi pi-chart-bar" class="p-buttom-sm" style="width: 30px; height: 30px;"></Button>
                </template>
            </Column>
        </DataTable>
        <div class="p-text-right p-col-12 p-as-end">
            <Button class="p-my-5" label="Start audit for selected questions" @click="startAudit(selectedQuestions)" :disabled="!selectedQuestions.length" icon="pi pi-check" />
        </div>
        <Dialog v-model:visible="helpDialog" style="width: 500px;" header="Help" :modal="true" dismissableMask="true">
            <p>Please select the questions that you want to audit.</p>

            <p>In the next step, you will be able to request documentation for your selected questions.</p>
            <template #footer>
                <Button label="Ok" icon="pi pi-check" @click="(helpDialog = !helpDialog)" />
            </template>
        </Dialog>

        <Dialog v-model:visible="criticalDialog" style="width: 500px;" :header="`Critical Impact: ${indicator_name}`" :modal="true" dismissableMask="true">
        <p class="p-text-justify">This Indicator was flagged as critical due to it's indirect indicator parent: <b>'{{ criticalDialogIndicator.critical_impact_by.indicator }}'</b> which has an <b>impact of '{{ criticalDialogIndicator.critical_impact_by.impact }}'</b>
        which would lower the <b>total score of '{{ criticalDialogIndicator.critical_impact_by.total_score }}'</b> to <b>'{{ (criticalDialogIndicator.critical_impact_by.total_score - criticalDialogIndicator.critical_impact_by.impact).toFixed(2) }}'</b>, which is below the <b>threshold of '{{method.certification_theshold}}'</b>.
        </p>
        </Dialog>

    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
    data () {
        return {
            helpDialog: false,
            criticalDialog: false,
            expandedRowGroups: null,
            selectedQuestions: [],
            criticalDialogIndicator: {},
            chosenDirectIndicators: []
            // questions: [
            //     {
            //         name: 'What is the total number of men staff?',
            //         response: 5,
            //         recommendations: '',
            //         section: { name: 'Gender' }
            //     },
            //     {
            //         name: 'What is the total number of women staff?',
            //         response: 7,
            //         recommendations: '',
            //         section: { name: 'Gender' }

            //     },
            //     {
            //         name: 'What is the average monthly salary per employee?',
            //         response: '$4000',
            //         recommendations: '',
            //         section: { name: 'Salary' }
            //     }
            // ]
        }
    },
    computed: {
        ...mapState('auditIndicators', ['indicators', 'selectedIndicators']),
        ...mapState('method', ['method']),
        ...mapState('surveyResponse', ['surveyResponse']),
        ...mapState('surveyAudit', ['surveyAudit']),
        ...mapState('eseaAccount', ['eseaAccount']),
        indicator_name () {
            if ('name' in this.criticalDialogIndicator) {
                return this.criticalDialogIndicator.name
            } else {
                return 'indicator'
            }
        }
        // directIndicators () {
        //     return this.selectedQuestions.map((question) => {
        //         if (question.absolute_weights.length) { return item }
        //         return Object.assign(item, data)
        // }
    },
    mounted () {
        this.selectedQuestions = this.selectedIndicators
    },
    methods: {
        ...mapActions('auditIndicators', ['selectIndicators']),
        ...mapActions('surveyResponse', ['fetchSurveyResponse']),
        ...mapActions('questionResponse', ['updateQuestionResponse']),
        async startAudit (selectedQuestions) {
            // Gets Direct Indicators belonging to an indirect indicator
            await this.fetchSurveyResponse({ oId: this.eseaAccount?.organisation, eaId: this.eseaAccount?.id, id: `survey=${this.surveyAudit.survey}` })
            var self = this
            var chosenDirectIndicators = []
            selectedQuestions.forEach(function (question) {
                if (question?.formula) {
                chosenDirectIndicators.push(self.getAllChildren(question.absolute_weights))
                } else {
                    chosenDirectIndicators.push(question.key)
                }
            })
            this.chosenDirectIndicators = [...new Set(chosenDirectIndicators.flat())]

            var selectedIndicators = []
            for (const directIndicator of this.chosenDirectIndicators) {
                // console.log(directIndicator)
                console.log(directIndicator)
                const indicator = this.indicators.find(indicator => indicator.key === directIndicator)
                if (indicator) {
                    // change surveyResponse.question_responses to questionResponses to be able to see the updated database on updated question response changes!
                    indicator.question_response = this.surveyResponse.question_responses.find(questionResponse => questionResponse.direct_indicator_key === indicator.key)
                    selectedIndicators.push(indicator)
                }
                // should use these direct indicator id's to update the question responses
                // await this.updateQuestionResponse({})
            }
            console.log(selectedIndicators)
            await this.selectIndicators({ indicators: selectedIndicators })
            // ToDo: Change audit status of question responses (also in backend)!
            for (var indicator of selectedIndicators) {
                if (indicator.question_response.auditstatus === 'Not Under Audit') {
                    indicator.question_response.auditstatus = 'Open'
                }
                this.updateQuestionResponse({ oId: 0, eaId: 0, id: indicator.question_response.id, data: indicator.question_response })
            }
            this.$router.push({ name: 'documentationrequest', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } })
        },
        openCriticalDialog (indicator) {
            this.criticalDialogIndicator = indicator
            this.criticalDialog = true
        },
        ShowOutlierDetectionMethods () {
            // Show outlier detection methods dialog
            // console.log('...')
        },
        onRowGroupExpand () {
        },
        onRowGroupCollapse () {
        },
        getAllChildren (group, children) {
            children = children || []
            // console.log(typeof group, group, children)
            if (group) {
                for (const value of Object.values(group)) {
                    if (Object.prototype.toString.call(value) === '[object Object]') {
                        this.getAllChildren(value, children)
                    } else {
                        children.push(value)
                    }
                }
                return children
            }
        }
    }
}
</script>
