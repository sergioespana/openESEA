<template>
    <list-bar v-model:tabledisplay="tableDisplay" v-model:allitems="allCampaigns" :includecheckbox="false" v-model:search="customSearch" name="Campaigns">
        <slot></slot>
    </list-bar>
    <ProgressSpinner v-if="loading && !failedLoad" />
    <div v-else-if="loading && failedLoad" class="p-text-italic">Campaigns could not be retrieved!</div>
    <div v-else-if="campaigns.length">
        <div v-if="tableDisplay" class="p-grid p-m-5">
            <div v-for="campaign in filteredCampaigns" :key="campaign.name" class="p-col-12 p-md-6 p-lg-4" style="width: 400px">
                <div class="p-p-3" :class="campaign.hover ? 'p-shadow-1 p-m-1' : 'p-shadow-1 p-m-0'" style="border-radius: 3px" :style="(campaign.hover ? styleObject : '')"  @mouseover="campaign.hover=true" @mouseleave="campaign.hover = false" @click="goToCampaign(campaign)">
                        <p class="p-text-light">{{ dateFixer(campaign.open_survey_date, 'MMMM Do YYYY') }} - {{ dateFixer(campaign.close_survey_date, 'MMMM Do YYYY') }}</p> <!-- MM/Do/YYYY' -->
                    <img :src="campaign.image" alt="Campaign Image" style="max-width: 150px; max-height: 150px; border-radius: 50%;" format="PNG">
                    <p class="p-text-italic">{{campaign.name}}</p>
                    <Divider />
                    <div class="p-text-left p-ml-3">
                        <p>Method: <span class="p-text-bold">{{campaign.method_name}}</span></p> <!-- Should be method name instead of pk! -->
                        <p>Participating Organisations: <span class="p-text-bold">{{campaign.organisation_accounts.length}}</span></p>
                    </div>
                </div>
            </div>
        </div>
        <DataTable v-else :value="filteredCampaigns" datakey="id" selectionMode="single" @row-select="goToCampaign" showGridlines autoLayout
        :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

            <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field" bodyStyle="" />
        </Datatable>
    </div>
    <div v-else class="p-text-italic">No Campaigns to display!</div>
</template>

<script>
    import { mapState, mapActions } from 'vuex'
    import ListBar from '@/components/lists/ListBar/'
    import ProgressSpinner from 'primevue/progressspinner'
    import dateFixer from '../../utils/datefixer'

    export default {
        components: {
            ListBar,
            ProgressSpinner
        },
        data () {
            return {
                tableDisplay: false,
                loading: true,
                failedLoad: false,
                customSearch: '',
                allCampaigns: false,
                styleObject: { backgroundColor: '#EFEEEE', cursor: 'pointer' },
                columns: [
                    { field: 'name', header: 'Name' },
                    { field: 'method_name', header: 'Method' },
                    { field: 'organisation_accounts.length', header: 'Organisations' }
                ]
            }
        },
        computed: {
            ...mapState('network', ['network']),
            ...mapState('campaign', ['campaigns']),
            filteredCampaigns () {
                return this.campaigns.filter(campaign => {
                    return (
                        campaign.name.toLowerCase().includes(this.customSearch.toLowerCase()) ||
                        campaign.method_name.toLowerCase().includes(this.customSearch.toLowerCase())
                    )
                })
            }
        },
        created () {
            this.getCampaigns()
            setTimeout(() => { this.failedLoad = true }, 10000)
        },
        methods: {
            ...mapActions('campaign', ['fetchCampaigns', 'setCampaign']),
            dateFixer,
            async getCampaigns () {
                await this.fetchCampaigns({ nId: this.$route.params.NetworkId })
                this.loading = false
            },
            async goToCampaign (campaign) {
                if (campaign?.data) {
                    campaign = campaign.data
                }
                if (campaign?.id) {
                    await this.setCampaign(campaign)
                    this.$router.push({ name: 'networkcampaign', params: { CampaignId: campaign.id } })
                }
            }
        }
    }
</script>
