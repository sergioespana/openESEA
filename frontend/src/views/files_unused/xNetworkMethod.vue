<template>
    <div>
        <TabView v-model:activeIndex="active">
            <TabPanel header="Surveys">
                <DataTable :value="surveys" :filters="filters2" class="p-datatable-striped">
                    <template #header>
                        <div class="p-d-flex p-jc-between p-ai-center">
                            <h3 class="p-m-0">Surveys</h3>
                            <Button :label="`Deploy method '${this.method.name}' to organisations`" class="p-button-primary" @click="deployMethodDialog = true" />
                            <span class="p-input-icon-left"> <i class="pi pi-search" />
                                <InputText v-model="filters2['global']" placeholder="Keyword Search" />
                            </span>
                        </div>
                    </template>
                    <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field" />
                </DataTable>
            </TabPanel>
            <TabPanel header="Responses">
                <DataTable :value="organisations" :filters="filters3" v-model:expandedRows="expandedRows" dataKey="id" responsiveLayout="scroll">
                    <template #header>
                        <div class="p-d-flex p-jc-between p-ai-center">
                        <h3 class="p-m-0">Survey Responses</h3>
                        <ToggleButton v-model="amountToggle" onLabel="Summarized Responses" offLabel="Individual Responses" onIcon="pi pi-users" offIcon="pi pi-user" />
                        <span class="p-input-icon-left"> <i class="pi pi-search" />
                            <InputText v-model="filters3['global']" placeholder="Keyword Search" />
                        </span>
                        </div>
                    </template>

                    <Column :expander="true" headerStyle="width: 3rem" />
                    <Column field="name" header="Name" sortable></Column>
                    <Column field="members.length" header="Members" sortable></Column>
                    <Column field="organisation_members.length" header="Respondents" sortable></Column>

                    <template #expansion="slotProps">
                        <div class="p-mx-5 p-px-5">
                            <DataTable v-if="!amountToggle" :value="slotProps.data.organisation_members">
                                    <Column field="user" header="Participant"></Column>
                                    <Column field="" header="Survey"></Column>
                                    <Column field="stakeholdergroups" header="Stakeholder Group"></Column>
                                    <Column header="Finished?">
                                        <template #body="slotProps">
                                            <i class="pi" :class="{'true-icon pi-check-circle': slotProps.data.survey_responses[0].finished, 'false-icon pi-times-circle': !slotProps.data.survey_responses[0].finished}"></i>
                                        </template>
                                    </Column>
                                    <Column>
                                    <template #body="slotProps">
                                        <Button type="button" label="Results" class="p-button-raised p-button secondary p-button-sm" @click="goToSurveyResponse(slotProps.data)" />
                                    </template>
                                    </Column>
                            </DataTable>
                            <DataTable v-else :value="surveys" :filters="filters2">
                                <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field" />
                                <Column>
                                    <template #body="slotProps">
                                    <Button type="button" label="Results" class="p-button-raised p-button secondary p-button-sm" @click="goToSurveyResponse(slotProps.data)" />
                                </template>
                                </Column>
                            </DataTable>
                        </div>
                    </template>
                </DataTable>
            </TabPanel>
            <TabPanel header="Reports">
                No Available Reports
            </TabPanel>
        </TabView>
        <Button @click="active = 0" class="p-button-text" label="Activate 1st" />
        <Button @click="active = 1" class="p-button-text" label="Activate 2nd" />
        <Button @click="active = 2" class="p-button-text" label="Activate 3rd" />
    </div>

    <Dialog v-model:visible="deployMethodDialog" contentStyle="width: 450px; height: 300px" header="Deploy Method" :modal="true">
        <div v-if="!organisations.length">
            All network organisations have access to this method and its surveys.
        </div>
        <div v-else class="p-text-left">
            Select the organisations that you want to deploy the surveys of the current method to.
            <div class="p-p-5">
                <MultiSelect v-model="selectedOrganisations" :options="organisations" :filters="true" optionLabel="name" placeholder="Select Organisations" style="width: 300px" />
            </div>
        </div>
        <template #footer>
            <Button label="cancel" icon="pi pi-times" class="p-button-text" @click="(deployMethodDialog = false) && (selectedRows = [])"/>
            <Button label="Deploy" icon="pi pi-check" class="p-button-text" @click="deployMethod()" :disabled="!selectedOrganisations.length"/>
        </template>
    </Dialog>

</template>

<script>
    import { mapState, mapActions } from 'vuex'
    import MultiSelect from 'primevue/multiselect'

    export default {
        components: {
            MultiSelect
        },
        data () {
            return {
                filters: {},
                filters2: {},
                filters3: {},
                columns: [
                    { field: 'name', header: 'Name' },
                    { field: 'questions.length', header: 'Questions' },
                    { field: 'stakeholders', header: 'Stakeholder Group' },
                    { field: '', header: 'Responserate' }
                ],
                responsecolumns: [
                    { field: 'survey', header: 'Survey' },
                    { field: 'user_organisation.user', header: 'Participant' },
                    { field: 'user_organisation.organisation', header: 'Organisation' },
                    { field: 'user_organisation.stakeholdergroups', header: 'Stakeholder Groups' }
                ],
                selectedOrganisations: [],
                deployMethodDialog: false,
                expandedRows: [],
                amountToggle: false,
                active: 0
            }
        },
        computed: {
            ...mapState('method', ['method']),
            ...mapState('organisation', ['organisations']),
            ...mapState('survey', ['surveys'])
        },
        created () {
            this.initialize()
        },
        methods: {
            ...mapActions('method', ['fetchMethod", "patchMethod']),
            ...mapActions('organisation', ['fetchOrganisations']),
            ...mapActions('survey', ['fetchSurveys']),
            async initialize () {
                this.fetchOrganisations({ query: `?network=${this.$route.params.NetworkId}&method=${this.$route.params.MethodId || 0}` })
                this.fetchSurveys({ mId: this.$route.params.MethodId || 0 })
            },
            async deployMethod () {
                await this.patchMethod({ data: this.selectedOrganisations })
                this.deployMethodDialog = false
                this.initialize()
            },
            async goToSurveyResponse (row) {
                if (!this.amountToggle) {
                    this.$router.push({ name: 'method-survey-result', params: { OrganisationId: row.organisation, methodId: this.method.id, surveyId: row.id, id: row.survey_responses[0].id } })
                } else {
                    this.$router.push({ name: 'method-survey-results', params: { OrganisationId: row.organisation, methodId: this.$route.params.MethodId, surveyId: row.id } })
                }
            }
        }
    }
</script>
