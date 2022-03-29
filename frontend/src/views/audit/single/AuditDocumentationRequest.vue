<template>
    <div class="p-grid p-m-5">
        <div class="p-col-12 p-d-flex p-ai-center p-jc-between">
            <h2 class="p-text-left">Documentation Request</h2>
            <Button @click="(helpDialog = !helpDialog)" label="Help" class="p-button-sm p-button-warning" icon="pi pi-external-link" />
        </div>
        {{selectedIndicators}}
        <DataTable class="p-col-12" :value="selectedIndicators" rowGroupMode="rowspan" groupRowsBy="name" sortMode="single" sortField="name" :sortOrder="1" responsiveLayout="scroll"
            v-model:expandedRowGroups="expandedRowGroups" @rowgroupExpand="onRowGroupExpand" @rowgroupCollapse="onRowGroupCollapse" v-model:selection="selectedQuestions" dataKey="name">
            <Column selectionMode="multiple" headerStyle="width: 3em"></Column>
            <Column field="topic" header="Topic" sortable></Column>
            <Column field="name" header="Name" sortable></Column>
            <Column field="value" header="Value"></Column>
            <Column field="critical_impact" header="Critical Impact" sortable>
                <template #body="data"> <!-- (row.data.critical_impact & row.data.outliers) -->
                    <Button v-if="data.data.critical_impact" label="Critical" class="p-button-sm p-button-rounded p-py-1 p-button-danger" @click="openCriticalDialog(data.data)" />
                    <!--<Button v-if="row.data.outliers || row.data.critical_impact" label="Recommended" class="p-button-sm p-button-rounded p-py-1" :class="(((row.data.critical_impact & row.data.outliers) == true) ? 'p-button-danger' : 'p-button-warning')" @click="openRecommended()" />
                    -->
                </template>
            </Column>
            <Column header="Anomaly" sortable>
                <template #body="row"> <!-- (row.data.critical_impact & row.data.outliers) -->
                    <Button v-if="row.data.outliers" label="Anomaly" class="p-button-sm p-button-rounded p-py-1 p-button-danger" />
                    <!--<Button v-if="row.data.outliers || row.data.critical_impact" label="Recommended" class="p-button-sm p-button-rounded p-py-1" :class="(((row.data.critical_impact & row.data.outliers) == true) ? 'p-button-danger' : 'p-button-warning')" @click="openRecommended()" />
                    -->
                </template>
            </Column>
            <Column headerStyle="width: 10rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                <template #body="row">
                    <Button v-if="this.selectedQuestions.find(object => object.name === row.data.name)" label="Message" icon="pi pi-plus" class="p-button-sm p-button-success" @click="openMessage(row.data)" />
                </template>
            </Column>
        </DataTable>
        <div class="p-text-right p-col-12 p-as-end">
            <Button class="p-my-5" label="Request documentation" @click="requestDocumentation()" icon="pi pi-check" />
            <!-- <Button class="p-my-5 p-ml-2" label="Audit" @click="requestDocumentation()" /> -->
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

    <Dialog v-model:visible="criticalDialog" style="width: 500px;" :header="`Critical Impact: ${indicator_name}`" :modal="true" dismissableMask="true">
        <p class="p-text-justify">This Indicator was flagged as critical due to it's indirect indicator parent: <b>'{{ criticalDialogIndicator.critical_impact_by.indicator }}'</b> which has an <b>impact of '{{ criticalDialogIndicator.critical_impact_by.impact }}'</b>
        which would lower the <b>total score of '{{ criticalDialogIndicator.critical_impact_by.total_score }}'</b> to <b>'{{ (criticalDialogIndicator.critical_impact_by.total_score - criticalDialogIndicator.critical_impact_by.impact).toFixed(2) }}'</b>, which is below the <b>threshold of '{{method.certification_theshold}}'</b>.
        </p>
    </Dialog>
</template>

<script>
    import { mapState, mapActions } from 'vuex'
    // import Tag from 'primevue/tag'

export default {
    components: {
        // Tag
    },
    data () {
        return {
            helpDialog: false,
            criticalDialog: false,
            criticalDialogIndicator: {},
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
        ...mapState('auditIndicators', ['indicators', 'selectedIndicators']),
        ...mapState('method', ['method']),
        ...mapState('eseaAccount', ['eseaAccount']),
        indicator_name () {
            if ('name' in this.criticalDialogIndicator) {
                return this.criticalDialogIndicator.name
            } else {
                return 'indicator'
            }
        }
    },
    methods: {
        ...mapActions('questionResponse', ['updateQuestionResponse']),
        requestDocumentation () {
            // Attach message to indicator
            // this.selectedQuestions
            this.$router.push({ name: 'singleauditaudit', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } })
        },
        openMessage (indicator) {
            this.MessagedIndicator = indicator
            this.messageToOrganisationDialog = true
        },
        async saveMessage () {
            this.MessagedIndicator.question_response.doc_request_note = this.message
            this.selectedIndicators = this.selectedIndicators.map((item) => {
                if (item.id !== this.MessagedIndicator.id) { return item }
                return Object.assign(item, this.MessagedIndicator)
            })
            this.messageToOrganisationDialog = false

            // Save Question Response to Database

            await this.updateQuestionResponse({ oId: 0, eaId: 0, id: this.MessagedIndicator.question_response.id, data: this.MessagedIndicator.question_response })
            // await this.UpdateQuestionResponse({ data: this.MessagedIndicator.question_response })
        },
        openCriticalDialog (indicator) {
            this.criticalDialogIndicator = indicator
            this.criticalDialog = true
        },
        openRecommended () {
            print()
        }
    }
}
</script>

 await this.updateSurveyResponse({
                    oId: this.eseaAccount?.organisation,
                    eaId: this.eseaAccount?.id,
                    token: this.surveyResponse.id, // this.$route.params.uniquetoken,
                    surveyResponse: {
                        ...this.surveyResponse
                    }
                })
