<template>
      <Toolbar>
        <template #left>
            <ToggleButton v-model="surveyWithResponse" onLabel="Filled in Surveys" offLabel="Available Surveys" onIcon="pi pi-check" offIcon="pi pi-pencil" class="p-mr-2" @change="changeSurveyType" />
        </template>

        <template #right>
            <span class="p-input-icon-left">
                <i class="pi pi-search" />
                <InputText v-model="filters['global']" placeholder="Search..." />
            </span>
        </template>
    </Toolbar>
    <div v-if="surveys.length && !loading">
        <DataTable ref="dt" autoLayout="false" :value="surveys" v-model:selection="selectedRows" :selectionMode="selectionToggle? 'multiple' : 'single'" :dataKey="id" :loading="loading" @row-select="goToSurvey"
        :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

            <template #loading>
                Loading records, please wait...
            </template>
            <!-- <template # empty>
                empty
            </template> -->
            <Column
                v-for="column in columns"
                :key="column"
                :field="column.field"
                :header="column.header"
                ><template v-if="column.header === 'action'" #body="slotProps">
                    <Button v-if="surveyWithResponse" type="button" label="Results" class="p-button-raised p-button secondary" @click="goToSurveyResult(slotProps.data)" />
                    <Button v-else label="Participate"  @click="goToSurveyResult(slotProps.data)" />
                </template>
            </Column>

            <!-- <Column field="name" header="Name"></Column>
            <Column v-if="false" field="description" header="Description"></Column>
            <Column field="questions.length" header="Questions"></Column>
            <Column field="method.name" header="Method"></Column>
            <Column field="stakeholders" header="Stakeholder group"></Column>
            <Column header="Action" headerStyle="width: 15%">
                <template #body="slotProps">
                    <Button v-if="surveyWithResponse" type="button" label="Results" class="p-button-raised p-button secondary" @click="goToSurveyResult(slotProps.data)" />
                    <Button v-else label="Participate"  @click="goToSurveyResult(slotProps.data)" />
                </template>
            </Column> -->
        </DataTable>
    </div>
    <div v-else class="p-p-5 p-text-italic">
        Your organisation has no surveys to display. This can have the following reasons: <br> 1). you have done all surveys, <br> 2). related networks have not deployed a survey <br> 3). this organisation isn't member of a network.
    </div>
    {{surveyWithResponse}}
</template>

<script>
import { mapState, mapActions } from 'vuex'
import DataTable from 'primevue/datatable'
export default {
    components: {
        DataTable
    },
    data () {
        return {
            filters: {},
            loading: false,
            surveyWithResponse: false,
            columns: [
                { field: 'name', header: 'Name' },
                { field: 'description', header: 'Description' },
                { field: 'questions.length', header: 'Questions' },
                { field: 'method.name', header: 'Method' },
                { field: 'stakeholders', header: 'Stakeholder group' }
            ]
        }
    },
    computed: {
        ...mapState('survey', ['surveys']),
        ...mapState('method', ['methods'])
    },
    created () {
        this.initialize()
    },
    methods: {
        ...mapActions('survey', ['fetchSurveys', 'setSurvey']),
        ...mapActions('method', ['fetchMethods']),
        ...mapActions('surveyResponse', ['fetchSurveyResponses']),
        async initialize () {
            this.loading = true
            await this.fetchSurveys({ mId: 0, query: `?organisation=${this.$route.params.OrganisationId}` })
            this.loading = false
        },
        async changeSurveyType () {
            // this.$forceUpdate()
            if (this.surveyWithResponse) {
                this.loading = true
                if (this.columns.length === 5) {
                this.columns.push({ header: 'action' })
                }
                await this.fetchSurveys({ mId: 0, query: `?completedbyorganisation=${this.$route.params.OrganisationId}` })
                this.loading = false
            } else {
                this.columns.splice(5, 1)
                this.initialize()
            }
        },
        async goToSurvey (survey) {
            await this.setSurvey(survey.data)
            this.$router.push({ name: 'survey-fill', params: { id: 27, surveyId: survey.data.id } })
        },
        async goToSurveyResult (row) {
            await this.fetchSurveyResponses({ mId: 27, sId: row.id, OrganisationId: this.$route.params.OrganisationId })
            this.$router.push({ name: 'method-survey-result', params: { OrganisationId: this.$route.params.OrganisationId, methodId: 27, surveyId: row.id, id: 0 } })
        }
    }
}
        // await this.fetchMethods({})
        // for (const method of this.methods) {
        // setTimeout(() => { this.loading = false }, 1000)
</script>
