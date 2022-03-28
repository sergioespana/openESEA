// used by NetworkCampaigns.vue

<template>
    <form id="auditform" @submit.prevent="createNewAudit" class="p-input-filled p-text-left">
        <div class="p-field p-col-12 p-mx-0 p-px-0">
            <span class="p-float-label p-mt-3">
                <InputText type="text" class="p-col-12 p-mx-0" id="name" v-model.trim="name" />
                <label for="name">Name</label>
            </span>
        </div>

        <div class="p-field-checkbox">
            <Checkbox id="binary" v-model="checked" :binary="true" />
            <label for="binary">Deadline</label>
        </div>

        <div v-if="checked" class="p-field">
                <Calendar id="opendate" v-model="auditdate" placeholder="Calendar" appendTo="body" :showIcon="true" :inline="true" />
                <!-- <div class="p-error p-text-italic" v-for="error in openingDateErrors" :key="error"><small>{{error}}</small></div> -->
            </div>

        <div class="p-d-flex p-jc-between">
            <Button label="Cancel" icon="pi pi-times" class="" @click="closeDialog" style="width: 100px" />
            <Button type="submit" form="auditform" label="Save" icon="pi pi-check" style="width: 100px" />
        </div>
    </form>
</template>

<script>
    // :disabled="v$.campaignForm.$error"
    import { mapActions, mapState } from 'vuex'
    // import useVuelidate from '@vuelidate/core'
    // import { required, minLength, maxLength } from 'vuelidate/lib/validators'
    // import HandleValidationErrors from '../../utils/HandleValidationErrors'
    import Calendar from 'primevue/calendar'

    export default {
        components: {
            Calendar
        },
        props: {
            // survey: {
            //     type: Number
            // }
            type: {
                type: String
            }
        },
        data () {
            return {
                name: '',
                checked: false,
                auditdate: null // new Date()
            }
        },
        computed: {
            ...mapState('survey', ['surveys', 'survey']),
            ...mapState('eseaAccount', ['eseaAccount']),
            ...mapState('campaign', ['campaign'])
        },
        methods: {
            ...mapActions('auditIndicators', ['fetchIndicators']),
            ...mapActions('surveyAudit', ['createSurveyAudit']),
            ...mapActions('campaign', ['updateCampaign']),
            async createNewAudit () {
                console.log(this.survey)
                if (this.type === 'batch') {
                    this.campaign.auditstatus = 'Organisation Selection'
                    if (this.auditdate != null) {
                        this.campaign.deadline = this.auditdate
                    }
                    delete this.campaign.image
                    await this.updateCampaign({ nId: this.$route.params.NetworkId, data: this.campaign })
                    this.$router.push({ name: 'batchauditselection', NetworkId: this.$route.params.NetworkId, CampaignId: this.$route.params.CampaignId })
                } else {
                    print()
                    await this.createSurveyAudit({ oId: this.$route.params.OrganisationId, eaId: this.$route.params.EseaAccountId, data: { account_audit: this.eseaAccount.account_audit.id, survey: this.survey.id, deadline: this.auditdate } })
                    if (this.survey.response_type === 'single') {
                        await this.fetchIndicators({ id: this.$route.params.EseaAccountId }) //  oId: this.$route.params.OrganisationId, eaId: this.$route.params.EseaAccountId
                        this.$router.push({ name: 'questionselection', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.survey.id } })
                    } else if (this.survey.response_type === 'multiple') {
                        console.log('he')
                        this.$router.push({ name: 'multipleauditsampling', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.survey.id } })
                    }
                }
            },
            closeDialog () {
                this.$emit('closedialog')
            }
        }
    }
</script>

<style lang="scss" scoped>
    .borderless {
        border-bottom: 1px solid red;

    }
</style>
