// used by NetworkCampaigns.vue

<template>
    <form id="campaignform" @submit.prevent="createNewCampaign" class="p-input-filled p-fluid p-text-left">
        <div class="p-field ">
            <label for="name">Name<span style="color:red">*</span></label>
            <InputText id="name" v-model.trim="campaignForm.name" :class="{'p-invalid': v$.campaignForm.name.$error}" />
            <div class="p-error p-text-italic" v-for="error in nameErrors" :key="error">{{error}}</div>
        </div>

        <div class="p-grid">
            <div class="p-field p-col-6">
                <label for="method">Method<span style="color:red">*</span></label>
                <Dropdown id="method" v-model="campaignForm.method" :options="methods"  optionLabel="name" optionValue="id" placeholder="Select a Method" :class="{'p-invalid': v$.campaignForm.method.$error}" />
                <div class="p-error p-text-italic" v-for="error in methodErrors" :key="error">{{error}}</div>
            </div>

            <div class="p-field p-col-6">
                <label for="organisations">Organisations</label>
                <MultiSelect id="organisations" v-model="selectedOrganisations" :options="organisations" optionLabel="name" placeholder="Select Organisations" :filter="true" class="multiselect-custom" :class="{'p-invalid': v$.campaignForm.organisations.$error}">
                    <template #value="slotProps">
                        <div v-for="option of slotProps.value" :key="option.code">
                            <div>{{option.name}}</div>
                        </div>
                        <template v-if="!slotProps.value || slotProps.value.length === 0">
                            Select Organisations
                        </template>
                    </template>
                    <template #option="slotProps">
                        <div class="country-item">
                            <div>{{slotProps.option.name}}</div>
                        </div>
                    </template>
                </MultiSelect>
            </div>
        </div>

        <div class="p-grid">
            <div class="p-field p-col-6 p-m-0">
                <label for="opendate">Opening Date</label>
                <Calendar id="opendate" v-model="campaignForm.open_survey_date" placeholder="Calendar" appendTo="body" :showTime="true" :showIcon="true" />
                <div class="p-error p-text-italic" v-for="error in openingDateErrors" :key="error"><small>{{error}}</small></div>
            </div>
            <div class="p-field p-col-6">
                <label for="enddate">Closing Date</label>
                <Calendar id="enddate" v-model="campaignForm.close_survey_date" placeholder="Calendar" appendTo="body" showTime="true" :showIcon="true" />
                <div class="p-error p-text-italic" v-for="error in closingDateErrors" :key="error"><small>{{error}}</small></div>
            </div>
        </div>
        <div class="p-field">
            <label for="description">Description</label>
            <Textarea id="description" v-model="something" :autoResize="true" rows="3" />
        </div>
        <div class="p-field">
            <label for="message">Message to Organisations</label>
            <Textarea id="message" v-model="something" :autoResize="true" rows="3" />
        </div>

        <div class="p-d-flex p-jc-between">
            <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="closeDialog" style="width: 100px" />
            <Button type="submit" form="campaignform" label="Save" icon="pi pi-check" class="p-button-text" :disabled="v$.campaignForm.$error" style="width: 100px" />
        </div>
    </form>
</template>

<script>
    import { mapActions, mapState } from 'vuex'
    import useVuelidate from '@vuelidate/core'
    import { required, minLength, maxLength } from 'vuelidate/lib/validators'
    import HandleValidationErrors from '../../utils/HandleValidationErrors'
    import Calendar from 'primevue/calendar'
    import Dropdown from 'primevue/dropdown'
    import MultiSelect from 'primevue/multiselect'

    export default {
        components: {
            Calendar,
            Dropdown,
            MultiSelect
        },
        data () {
            return {
                selectedOrganisations: [],
                campaignForm: {
                    name: null,
                    network: this.$route.params.NetworkId,
                    method: null,
                    organisations: [],
                    open_survey_date: new Date(),
                    close_survey_date: new Date()
                }
            }
        },
        // Validation of the Campaign Form
        setup: () => ({ v$: useVuelidate() }),
        validations: {
            campaignForm: {
                name: { required, minLength: minLength(4), maxLength: maxLength(255) },
                network: { required },
                method: { required },
                organisations: {},
                open_survey_date: {},
                close_survey_date: {}
            }
        },
        computed: {
            ...mapState('campaign', ['campaign', 'error']),
            ...mapState('network', ['network']),
            ...mapState('method', ['methods']),
            ...mapState('organisation', ['organisations']),
            nameErrors () {
                return HandleValidationErrors(this.v$.campaignForm.name, this.error.name)
            },
            methodErrors () {
                return HandleValidationErrors(this.v$.campaignForm.method, this.error.method)
            },
            openingDateErrors () {
                return HandleValidationErrors(this.v$.campaignForm.open_survey_date, this.error.open_survey_date)
            },
            closingDateErrors () {
                return HandleValidationErrors(this.v$.campaignForm.close_survey_date, this.error.close_survey_date)
            }
        },
        created () {
            this.fetchMethods({ query: `?network=${this.network?.id || 0}` })
            this.initialize()
        },
        methods: {
            ...mapActions('organisation', ['fetchOrganisations']),
            ...mapActions('campaign', ['createCampaign', 'setCampaign']),
            ...mapActions('method', ['fetchMethods']),
            async initialize () {
                // Sets the campaign's surveys closing date to 30 days from now as default
                this.campaignForm.close_survey_date = new Date(this.campaignForm.close_survey_date.setDate(this.campaignForm.open_survey_date.getDate() + 30))
                await this.setCampaign({})
                await this.fetchOrganisations({ query: `?network=${this.$route.params.NetworkId}` })
            },
            async createNewCampaign () {
                this.v$.campaignForm.$touch()
                if (this.v$.$invalid) { return }
                if (this.selectedOrganisations.length) {
                    for (var organisation of this.selectedOrganisations) {
                        this.campaignForm.organisations.push(organisation.name)
                    }
                }
                await this.createCampaign({ nId: this.$route.params.NetworkId, data: this.campaignForm })
                this.closeDialog()
                if (this.campaign.id) {
                    this.$router.push({ name: 'networkcampaign', params: { NetworkId: this.$route.params.NetworkId, CampaignId: this.campaign.id } })
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
