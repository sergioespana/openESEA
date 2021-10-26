<template>
<div class="p-grid nested-grid" style="min-height: 60vh;">
    <div class="p-col-12 p-m-0 p-p-0">
        <div class="p-p-3 p-shadow-2" style="border: 1px solid lightgray; background-color: white;">
            <div class="p-text-justify"><p class="p-text-bold">Organisation Manager</p>
                <router-link :to="{name: 'userdetails', params: { id: organisation.owner_id } }" style="text-decoration: none; color: blue;">{{organisation.owner}}</router-link>
            </div>
            <div class="p-text-justify"><p class="p-text-bold">Description</p>
                    {{organisation.description}}
                    <!-- Lorem ipsum dolor sit amet, consectetur adipiscing elit. In convallis mi sit amet faucibus malesuada. Vestibulum fringilla sed dui bibendum laoreet. Donec suscipit sit amet leo et mattis. Aenean mattis tempus turpis a vulputate. Nunc bibendum pulvinar neque, nec mattis nisl tincidunt ut. Nam a quam id justo dictum pulvinar. Sed luctus dictum ligula, id sagittis tellus aliquam id. Vestibulum auctor vestibulum turpis. -->
            </div>
        </div>
        <Divider />
        <!-- <div class="p-grid">
            <div class="p-col-12 p-d-flex p-jc-end">
                <Button label="Edit Organisation" icon="pi pi-user-plus" class="p-button-secondary p-mr-2" @click="editOrganisationDialog = true"/>
                <Button label="Delete Organisation" icon="pi pi-trash" class="p-button-danger" @click="confirmDeletion" />
            </div>
        </div> -->
        <!-- <div class="p-col-12 p-text-justify"><h4 class="p-text-bold">Description</h4>
         <div class="p-text-justify"><p class="p-text-bold">Organisation Manager</p>
            <router-link :to="{name: 'userdetails', params: { id: organisation.created_by_id } }" style="text-decoration: none; color: blue;">{{organisation.created_by}}</router-link>
        </div>
                <span v-if="organisation.description.length">{{organisation.description}}</span><span v-else>This organisation has no description</span>
        </div> -->
         <div v-if="(organisation.accesLevel === 'esea accountant' || organisation.accesLevel === 'admin')" class="p-col-12 p-p-5 p-text-left" style="border: 1px solid lightgray">
            <div v-if="!eseaAccounts.length">
                <h4>All Done!</h4>
                <p class="p-text-italic">
                    {{organisation.name}} and all related networks do not require your attention right now.
                </p>
            </div>
            <div v-else class="p-col-12">
                <h4 class="p-mb-0">The following tasks require your attention.</h4>
                <div class="p-shadow-5 p-p-3 p-m-3">
                    <h4>Deployment Tasks</h4>
                    <div v-for="eseaAccount in eseaAccounts" :key="eseaAccount.id" class="p-m-3 p-shadow-1">
                        <div v-for="survey in eseaAccount.survey_response_by_survey" :key="survey.id">
                            <div v-if="survey.type === 'multi' && !survey.respondees.length">
                                <Button :label="`Deploy survey: '${survey.name}' belonging to '${eseaAccount.campaign_name}' by '${eseaAccount.network_name}'.`" class="p-button-text p-col-12 p-shadow-1 p-p-4" @click="goToEseaAccount(eseaAccount)"/>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="p-shadow-5 p-p-3 p-m-3">
                    <h4>Responding Tasks</h4>
                    <div v-for="eseaAccount in eseaAccounts" :key="eseaAccount.id" class="p-m-3 p-shadow-1">
                        <div v-for="survey in eseaAccount.survey_response_by_survey" :key="survey.id">
                            <div v-if="survey.type === 'single' && survey.sufficient_responses === false">
                                <Button :label="`Fill in Survey '${survey.name}' belonging to '${eseaAccount.campaign_name}' by '${eseaAccount.network_name}'.`" class="p-button-text p-col-12 p-shadow-1 p-p-4" @click="goToEseaAccount(eseaAccount)"/>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- <div v-for="survey, index in surveys" :key="survey.id" class="p-p-5"> Should be a v-for="task in tasks"
                    <Button :label="`Survey ${index+1}: As ${survey.stakeholdergroup} of ${organisation.name} you are asked to fill in the following survey deployed by network 1: '${survey.name}'.`" class="p-button-text p-shadow-3 p-p-4" @click="goToSurvey(survey.method.id, survey.id)"/>
                    <br><br>
                    <Button label="Task 2: As manager of organisation 2 you are asked to fill in the survey of network 1." class="p-button-text p-shadow-1" />
                </div> -->
            </div>
        </div>
    </div>
    <!-- <div class="p-col-1">
        <Divider layout="vertical"></Divider>
    </div>
    <div class="p-col-2">
        <div class="p-grid">
             <div class="p-col-12">
                <h3 class="p-mb-2 p-text-left">Available Surveys</h3>
                <Divider class="p-m-0" />
                <div class="p-m-3">
                    <div v-if="surveys.length">
                        <div v-for="survey, num in surveys" :key="survey.name">
                            {{num+1}}. <router-link :to="{name: 'survey-fill', params: { id: survey.method.id, surveyId: survey.id }}" style="text-decoration: none; color: blue;">survey {{num+1}}</router-link>
                            <Divider class="p-m-1" />
                        </div>
                    </div>
                    <div v-else>
                        <div class="p-py-5 p-text-italic">No surveys</div>
                    </div>
                </div>
                <router-link :to="{name: 'organisationsurveys', params: { OrganisationId: this.$route.params.OrganisationId }}" style="text-decoration: none; color: blue;">Show all Organisation Surveys</router-link>
            </div>
            <div class="p-col-12">
                <h3 class="p-mb-2 p-text-left">Reports</h3>
                <Divider class="p-m-0" />
                <div class="p-m-3">
                    <div v-if="organisations">
                        <div v-for="organisation, num in organisations" :key="organisation.name">
                            {{num+1}}. <router-link :to="{name: 'organisationreports', params: { OrganisationId: this.$route.params.OrganisationId }}" style="text-decoration: none; color: blue;">report {{num+1}}</router-link>
                            <Divider class="p-m-1" />
                        </div>
                    </div>
                    <div v-else>
                        <div class="p-py-5 p-text-italic">No reports yet</div>
                    </div>
                </div>
                <router-link :to="{name: 'organisationreports', params: { OrganisationId: this.$route.params.OrganisationId } }" style="text-decoration: none; color: blue;">Show all Organisation Reports</router-link>
            </div>
        </div>
    </div> -->
</div>
</template>
<script>
import { mapActions, mapState } from 'vuex'
export default {
    computed: {
        ...mapState('organisation', ['organisation']),
        ...mapState('eseaAccount', ['eseaAccounts', 'eseaAccount']),
        ...mapState('method', ['methods']),
        ...mapState('survey', ['surveys'])
    },
    created () {
        this.initialize()
    },
    methods: {
        ...mapActions('eseaAccount', ['fetchEseaAccounts', 'setEseaAccount']),
        ...mapActions('method', ['fetchMethods']),
        ...mapActions('survey', ['fetchSurveys']),
        async initialize () {
            await this.fetchEseaAccounts({ oId: this.$route.params.OrganisationId })
            await this.fetchMethods({})
            for (const method of this.methods) {
                await this.fetchSurveys({ mId: method.id, query: `?organisation=${this.$route.params.OrganisationId}` })
            }
        },
        goToSurvey (methodid, surveyid) {
            console.log(methodid)
            this.$router.push({ name: 'survey-fill', params: { OrganisationId: this.$route.params.OrganisationId, id: methodid, surveyId: surveyid } })
        },
        async goToEseaAccount (eseaaccount) {
            await this.setEseaAccount(eseaaccount)
            if (this.eseaAccount.id) {
                this.$router.push({ name: 'organisationeseaaccount', params: { OrganisationId: this.$route.params.OrganisationId, EseaAccountId: this.eseaAccount.id } })
            }
        }
    }
}
</script>
