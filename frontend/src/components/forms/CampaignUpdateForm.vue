<template>
    <form @submit.prevent="editCampaign" class="p-input-filled p-fluid p-text-left p-p-5">
        <div class="p-field p-grid">
            <label for="name" class="p-col-fixed" style="width:200px">Name</label>
            <InputText id="name" v-model.trim="campaign.name" class="p-col" :class="{'p-invalid': v$.campaign.name.$invalid }" />
            <small class="p-col-12 p-error p-text-italic" v-for="error in nameErrors" :key="error" style="padding-left: 200px;">{{error}}</small>
        </div>

        <div class="p-field p-grid">
            <label for="method" class="p-col-fixed" style="width: 200px">Method</label>
            <Dropdown id="method" v-model="campaign.method" :options="methods" optionLabel="name" optionValue="id" placeholder="Select a Method" class="p-col" :class="{'p-invalid': v$.campaign.method.$error}" />
            <small class="p-error p-text-italic" v-for="error in methodErrors" :key="error" style="padding-left: 200px;">{{error}}</small>
        </div>

        <div class="p-field p-grid">
            <label for="opendate" class="p-col-fixed" style="width: 200px">Opening Date</label>
            <Calendar id="opendate" v-model="campaign.open_survey_date" placeholder="Calendar" appendTo="body" :showTime="true" :showIcon="true" class="p-col p-p-0" :class="{'p-invalid': v$.campaign.open_survey_date.$error}" />
            <small class="p-error p-text-italic" v-for="error in openingDateErrors" :key="error" style="padding-left: 200px;">{{error}}</small>
        </div>
        <div class="p-field p-grid">
            <label for="enddate" class="p-col-fixed" style="width: 200px">Closing Date</label>
            <Calendar id="enddate" v-model="campaign.close_survey_date" placeholder="Calendar" appendTo="body" showTime="true" :showIcon="true" class="p-col p-p-0" :class="{'p-invalid': v$.campaign.close_survey_date.$error}" />
            <small class="p-error p-text-italic" v-for="error in closingDateErrors" :key="error" style="padding-left: 200px;">{{error}}</small>
        </div>

        <div class="p-field p-grid">
            <label for="description" class="p-col-fixed" style="width: 200px">Description</label>
            <Textarea id="description" v-model="empty" rows="3" cols="20" class="p-col" />
            <small class="p-error p-text-italic" v-for="error in descriptionErrors" :key="error" style="padding-left: 200px;">{{error}}</small>
        </div>

        <div class="p-field p-grid">
            <label for="reminder" class="p-col-fixed" style="width: 200px">Respondent reminder before deadline (in days)</label>
            <InputNumber id="inputnumber" v-model="empty" :min=1 class="p-col p-p-0"/>
            <small class="p-error p-text-italic" v-for="error in reminderErrors" :key="error" style="padding-left: 200px;">{{error}}</small>
        </div>
        <div class="p-d-flex p-jc-between p-p-0 p-m-0">
            <Button type="submit" :label="loading? 'Saving...': 'Save Details'" :loading="loading" class="p-button-primary p-button-sm p-mr-5" />
            <Button label="Delete Campaign" class="p-button-danger p-button-sm p-ml-5" @click="deleteCampaignDialog = true" />
        </div>
    </form>

     <Dialog v-model:visible="deleteCampaignDialog" style="width: '450px" header="Confirm" :modal="true" dismissableMask="true">
        <div class="confirmation-content">
            <i class="pi pi-exclamation-triangle p-mr-3" style="font-size:1.5rem" />
            <span>Are you sure you want to delete <b>{{campaign.name || 'this campaign'}}</b>?</span>
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" class="p-button-text" @click="deleteCampaignDialog = false" />
            <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="destroyCampaign" />
        </template>
    </Dialog>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import useVuelidate from '@vuelidate/core'
import { required } from 'vuelidate/lib/validators'
import HandleValidationErrors from '../../utils/HandleValidationErrors'
import Calendar from 'primevue/calendar'
import Dropdown from 'primevue/dropdown'

export default {
    components: {
        Calendar,
        Dropdown
    },
    data () {
        return {
            deleteCampaignDialog: false,
            loading: false
        }
    },
    setup: () => ({ v$: useVuelidate() }),
    validations: {
        campaign: {
            name: { required },
            method: {},
            open_survey_date: {},
            close_survey_date: {}
        }
    },
    computed: {
        ...mapState('campaign', ['campaign', 'error']),
        ...mapState('method', ['methods']),
        nameErrors () {
            return HandleValidationErrors(this.v$.campaign.name, this.error.name)
        },
        methodErrors () {
            return HandleValidationErrors(this.v$.campaign.method, this.error.method)
        },
        openingDateErrors () {
            return HandleValidationErrors(this.v$.campaign.open_survey_date, this.error.open_survey_date)
        },
        closingDateErrors () {
            return HandleValidationErrors(this.v$.campaign.close_survey_date, this.error.close_survey_date)
        }
    },
    async created () {
        await this.fetchMethods({ query: `?network=${this.$route.params.NetworkId}` })
    },
    methods: {
        ...mapActions('campaign', ['updateCampaign', 'deleteCampaign']),
        ...mapActions('method', ['fetchMethods']),
        async editCampaign () {
            this.v$.campaign.$touch()
            if (this.v$.campaign.$invalid) { return }
            this.loading = true
            var newcampaign = this.campaign
            delete newcampaign.image
            await this.updateCampaign({ nId: this.$route.params.NetworkId, data: newcampaign })
            setTimeout(() => { this.loading = false }, 500)
        },
        async destroyCampaign () {
            this.deleteCampaignDialog = false
            await this.deleteCampaign({ nId: this.$route.params.NetworkId, id: this.$route.params.CampaignId })
            this.$router.push({ name: 'networkcampaigns' })
        }
    }
}
</script>
