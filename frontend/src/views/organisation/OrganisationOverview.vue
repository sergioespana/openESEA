<template>
    <div class="p-grid nested-grid" style="min-height: 60vh;">
        <div class="p-col-12 p-m-0 p-p-0">
            <div class="p-p-3 p-shadow-2" style="border: 1px solid lightgray; background-color: white;">
                <div class="p-text-justify"><p class="p-text-bold">Organisation Manager</p>
                    <router-link :to="{name: 'userdetails', params: { id: organisation.owner_id } }" style="text-decoration: none; color: blue;">{{organisation.owner}}</router-link>
                </div>
                <div class="p-text-justify"><p class="p-text-bold">Description</p>
                        {{organisation.description}}
                </div>
            </div>
            <Divider />
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
                </div>
            </div>
        </div>
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
