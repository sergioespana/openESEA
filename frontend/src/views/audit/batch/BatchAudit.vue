<template>
    <div style="background-color: white; height: 100%;">
        <div class="p-d-flex p-ai-center" style="background-color: #f7f7f7;" @click="goT()">
            <i class="pi pi-angle-left p-mx-3" style="fontSize: 2rem"></i>
            <h4>ESEA account</h4>
        </div>
        <h1>Workforce Survey audit</h1>
        <div class="p-grid p-mt-5">
            <div class="p-col-6">Organisation:</div>
            <div class="p-col-6">Auditor:</div>
            <div class="p-col-6">Type:</div>
            <div class="p-col-6">Deadline:</div>
        </div>
        <Steps :model="batch_audit_steps" :readonly="false" @click="test">
            <template #item="{item}">
                {{item.label}} {{item.label}}
                <!-- <a :href="item.to">{{item.label}}--1</a> -->
            </template>
            <!--<router-link :to="item.to" custom v-slot="{href, navigate, activeIndex}"> :style="[activeIndex ? 'background-color: red;':'background-color: blue;']"
                <a :href="href" @click="navigate" style="background-color: blue;">{{activeIndex}}--{{item.label}}</a>
                {{activeIndex}}
            </router-link>-->
        </Steps>
        <Divider class="p-my-5" />
        <router-view class="p-m-5" />
    </div>
</template>

<script>
    import Steps from 'primevue/steps'
    import { mapState } from 'vuex'

    export default {
        components: {
            Steps
        },
        data () {
            return {
                batch_audit_steps: [
                    {
                        label: 'Organisation Selection',
                        to: { name: 'batchauditselection', params: { NetworkId: this.$route.params.NetworkId, CampaignId: this.$route.params.CampaignId } },
                        active: true
                    },
                    {
                        label: 'Audits in Progress',
                        to: { name: 'batchauditoverview', params: { NetworkId: this.$route.params.NetworkId, CampaignId: this.$route.params.CampaignId } },
                        active: false
                    },
                    {
                        label: 'All Audits Finished',
                        to: { name: 'batchauditresults', params: { NetworkId: this.$route.params.NetworkId, CampaignId: this.$route.params.CampaignId } },
                        active: false
                    }
                ]
            }
        },
        computed: {
            ...mapState('campaign', ['campaign'])
        },
        methods: {
        //     goToPage () {
        //         this.$router.push({ name: 'questionselection', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } })
        //     },
            goToCampaign () {
                this.$router.push({ name: 'networkcampaign', params: { CampaignId: this.campaign.id } })
            }
        }
    }
</script>
