<template>
    <div class="p-m-1">
        <list-bar v-model:tabledisplay="tableDisplay" v-model:allitems="allMethods" :includecheckbox="false" v-model:search="customSearch" name="Methods">
            <Button label="Create Survey" @click="createNewSurvey" />
        </list-bar>
        <ProgressSpinner v-if="loading && !failedLoad" />
        <div v-else-if="loading && failedLoad" class="p-text-italic">Surveys could not be retrieved</div>
        <div v-else-if="surveys.length">
            <div v-if="tableDisplay" class="p-grid p-m-5" style="height: 500px;">
                <div v-for="survey in filteredSurveys" :key="survey.id" class="p-col-12 p-md-6 p-lg-4" style="width: 300px; height: 200px; ">
                    <div class="p-d-flex p-p-3" :class="method.hover ? 'p-shadow-2 p-m-1' : 'p-shadow-1 p-m-2'" style="height: 100%;" :style="(survey.hover ? styleObject : '')" @mouseover="survey.hover=true" @mouseleave="survey.hover=false" @click.left="goToSurvey(survey)">
                        <!-- <img :src="method.image" alt="method Image" style="max-width: 150px; max-height: 150px; border-radius: 50%;" format="PNG" /> -->
                        <p class="p-as-center p-text-bold p-text-italic" style="width: 100%">{{survey.name}}</p>
                    </div>
                </div>
            </div>
            <DataTable v-else :value="filteredSurveys"  dataKey="id" :loading="loading" selectionMode="single" @row-select="goToSurvey" showGridlines autoLayout
            :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
            :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped"> <!-- p-datatable-sm -->

                <!-- <Column field="ispublic" header="Public" headerStyle="width: 5rem">
                    <template #body="slotProps">
                        <i class="pi p-text-center p-text-bold" style="width:100%; font-size: 20px;" :class="{'true-icon pi-check': slotProps.data.ispublic, 'false-icon pi-times': !slotProps.data.ispublic}" :style="(slotProps.data.ispublic ? 'color: green;':'color: red;')"></i>
                    </template>
                </Column> -->
                <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field" bodyStyle="" /> <!-- text-align: center; overflow: visible  contentStyle="width: 500px;" -->
                <Column headerStyle="width: 5rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                <template #body="{data}">
                    <Button v-if="data.created_by === this.currentuser" icon="pi pi-trash" class="p-button-danger p-button-sm" @click="openDeleteSurveyDialog(data)" style="width: 50px" />
                </template>
                </Column>
                <!-- <Button v-if="(data.created_by === this.currentuser)" label="Update" class="p-button-sm" @click="updateSurvey(data)"  style="width: 100px" /> -->
             <!-- <div v-if="(networkmethods && permission)">
                           <Button v-if="importablemethods" label="Import Method" class="p-button-success p-button-sm" @click="importMethod(data)" />
                            <Button v-if="!importablemethods" label="Drop Method" class="p-button-danger p-button-sm" @click="dropMethod(data)" />
                         </div> -->

                <!-- <Column field="created_by" header="Creator">
                    <template #body="slotProps">
                        <div v-if="slotProps.data.created_by !== currentuser">{{slotProps.data.created_by}}</div> <div v-else class="p-text-bold">You</div>
                    </template>
                </Column> -->

                <!-- <div v-if="networkmethods && permission"> -->
                <!-- </div>
                <div v-else style="width: 0px;"><Column bodyStyle="width: 0rem;" /></div> -->
            </Datatable>
        </div>
        <div v-else class="p-text-italic">No Surveys to display!</div>
    </div>
    <Dialog v-model:visible="deleteSurveyDialog" style="width: 450px;" header="Confirm" :modal="true" :dismissableMask="true">
        <div class="confirmation-content">
            <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 1.5rem" />
            <span>Are you sure you want to delete survey '<b>{{selected.name}}</b>'?</span>
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" class="p-button-text" @click="deleteSurveyDialog = false" />
            <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="removeSurvey()" />
        </template>
    </Dialog>
</template>

<script>
    import { mapState, mapActions } from 'vuex'
    import ProgressSpinner from 'primevue/progressspinner'
    import ListBar from '@/components/lists/ListBar'

    export default {
        components: {
            ProgressSpinner,
            ListBar
        },
        props: {
            refresh: {}
        },
        data () {
            return {
                customSearch: '',
                loading: true,
                failedLoad: false,
                tableDisplay: false,
                styleObject: { backgroundColor: '#EFEEEE', cursor: 'pointer' },
                columns: [
                    { field: 'name', header: 'Name' },
                    { field: 'description', header: 'Description' },
                    { field: 'response_type', header: 'Response Type' },
                    { field: 'min_threshold', header: 'Minimal Threshold' }
                ],
                selected: null,
                deleteSurveyDialog: false
            }
        },
        computed: {
            ...mapState('survey', ['surveys', 'survey']),
            ...mapState('method', ['method']),
            filteredSurveys () {
                return this.surveys.filter(survey => {
                return (
                    survey.name.toLowerCase().includes(this.customSearch.toLowerCase()) ||
                    survey.description.toLowerCase().includes(this.customSearch.toLowerCase())
                )
                })
            }
        },
        created () {
            this.getSurveys()
        },
        methods: {
            ...mapActions('survey', ['fetchSurveys', 'addNewSurvey', 'setSurvey', 'deleteSurvey']),
            async getSurveys () {
                this.loading = true
                setTimeout(() => { this.failedLoad = true }, 10000)
                await this.fetchSurveys({ mId: this.method.id })
                this.loading = false
            },
            async goToSurvey (survey) {
                if (survey?.data) {
                    survey = survey.data
                }
                if (survey.id) {
                    await this.setSurvey(survey)
                    this.$router.push({ name: 'method-wizard-survey-settings', params: { SurveyId: this.survey.id } })
                }
            },
            async createNewSurvey () {
                await this.addNewSurvey({ method: this.method.id })
                console.log('yeha')
                if (this.survey?.id) {
                this.$router.push({ name: 'method-wizard-survey-settings', params: { SurveyId: this.survey.id } })
                }
            },
            openDeleteSurveyDialog (survey) {
                this.selected = survey
                this.deleteSurveyDialog = true
            },
            async removeSurvey () {
                await this.deleteSurvey({ mId: this.$route.params.id, id: this.selected.id })
                this.deleteSurveyDialog = false
            }
        }
}
// <Column headerStyle="width: 15rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
//                     <template #body="{data}">
//                         <Button v-if="(data.created_by === this.currentuser)" label="Update" class="p-button-sm" @click="updateSurvey(data)"  style="width: 100px" />
//                         <!-- <div v-if="(networkmethods && permission)">
//                             <Button v-if="importablemethods" label="Import Method" class="p-button-success p-button-sm" @click="importMethod(data)" />
//                             <Button v-if="!importablemethods" label="Drop Method" class="p-button-danger p-button-sm" @click="dropMethod(data)" />
//                         </div> -->
//                         <!-- <Button v-if="data.created_by === this.currentuser" icon="pi pi-trash" class="p-button-danger p-button-sm" @click="(selectedMethod = data) && (destroyMethodDialog = true)" style="width: 50px" /> -->
//                     </template>
//                 </Column>
</script>
