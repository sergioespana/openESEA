<template>
    <list-bar v-model:tabledisplay="tableDisplay" v-model:allitems="allCampaigns" :includecheckbox="false" v-model:search="customSearch" name="Campaigns">
        <slot></slot>
    </list-bar>
    <ProgressSpinner v-if="loading && !failedLoad" />
    <div v-else-if="loading && failedLoad" class="p-text-italic">Esea Accounts could not be retrieved!</div>
    <div v-else-if="eseaAccounts.length">
        <div v-if="tableDisplay" class="p-grid p-m-5">
            <div v-for="eseaAccount in filteredEseaAccounts" :key="eseaAccount.id" class="p-col-12 p-md-6 p-lg-4" style="width: 300px; height: auto;">
                <div class="p-p-3" :class="eseaAccount.hover ? 'p-shadow-2 p-m-1' : 'p-shadow-1 p-m-2'" :style="(eseaAccount.hover ? styleObject: '')" @mouseover="eseaAccount.hover = true" @mouseleave="eseaAccount.hover = false" @click="goToEseaAccount(eseaAccount)">
                    <p class="p-text-bold">{{eseaAccount.method_name}}</p>
                    <p class="p-text-italic">{{eseaAccount.year}}</p>
                </div>
            </div>
        </div>
        <DataTable v-else :value="filteredEseaAccounts" datakey="id" selectionMode="single" @row-select="goToEseaAccount" showGridlines autoLayout
            :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
            :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

            <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field" bodyStyle="" />
            <Column field="sufficient_responses" header="Sufficient Responses" headerStyle="width: 15rem">
                <template #body="slotProps">
                    <i class="p-text-center p-text-bold" style="width:100%; font-size: 20px;" :class="{'true-icon pi pi-check': slotProps.data.sufficient_responses, 'false-icon pi pi-times': !slotProps.data.sufficient_responses}" :style="(slotProps.data.sufficient_responses ? 'color: green;':'color: red;')"></i>
                </template>
            </Column>
        </Datatable>
    </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import ProgressSpinner from 'primevue/progressspinner'
import ListBar from '@/components/lists/ListBar/'

export default {
    components: {
        ProgressSpinner,
        ListBar
    },
    data () {
        return {
            tableDisplay: false,
            loading: true,
            failedLoad: false,
            customSearch: '',
            styleObject: { backgroundColor: '#EFEEEE', cursor: 'pointer' },
            columns: [
                { field: 'method_name', header: 'Method' },
                { field: 'year', header: 'Year' },
                { field: 'campaign_name', header: 'Campaign' },
                { field: 'network_name', header: 'Network' }
            ]
        }
    },
    computed: {
        ...mapState('eseaAccount', ['eseaAccounts', 'eseaAccount']),
        filteredEseaAccounts () {
            return this.eseaAccounts.filter((eseaAccount) => {
                return (
                    eseaAccount.method_name.toLowerCase().includes(this.customSearch.toLowerCase()) ||
                    eseaAccount.year.toString().includes(this.customSearch.toLowerCase()) ||
                    eseaAccount.campaign?.toLowerCase().includes(this.customSearch.toLowerCase()) ||
                    eseaAccount.network?.toLowerCase().includes(this.customSearch.toLowerCase())
                    )
                })
        }
    },
    created () {
        this.getEseaAccounts()
        setTimeout(() => { this.failedLoad = true }, 10000)
    },
    methods: {
        ...mapActions('eseaAccount', ['fetchEseaAccounts', 'setEseaAccount']),
        async getEseaAccounts () {
            await this.fetchEseaAccounts({ oId: this.$route.params.OrganisationId })
            this.loading = false
        },
        async goToEseaAccount (eseaAccount) {
            if (eseaAccount?.data) {
                eseaAccount = eseaAccount.data
            }
            await this.setEseaAccount(eseaAccount)
            if (this.eseaAccount.id) {
                this.$router.push({ name: 'organisationeseaaccount', params: { EseaAccountId: eseaAccount.id } })
            }
        }
    }
}
</script>
