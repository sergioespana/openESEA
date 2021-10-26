<template>
    <div style="min-width: 1000px;">
    <esea-account-list :esea-accounts="eseaAccounts" :table="tableDisplay" :search="search" :loading="loading" @clicked-esea-account="goToEseaAccount">
    <Button v-if="permission" label="Create ESEA Account" icon="pi pi-plus" class="p-button-success p-button-sm" @click="createEseaAccountDialog = true" />
    </esea-account-list>
    </div>

    <Dialog v-model:visible="createEseaAccountDialog" style="width: 700px" header="Esea Account Details" :modal="true" :dismissableMask="true">
        <esea-account-form :eseaAccounts="eseaAccounts" @closedialog="createEseaAccountDialog=false" />
    </Dialog>
</template>
<script>
import { mapState } from 'vuex'
import EseaAccountList from '../../components/lists/EseaAccountList'
import EseaAccountForm from '../../components/forms/EseaAccountForm.vue'
export default {
    components: {
        EseaAccountList,
        EseaAccountForm
    },
    data () {
        return {
            loading: true,
            createEseaAccountDialog: false,
            hover: false,
            styleObject: { backgroundColor: '#EFEEEE' }
        }
    },
    computed: {
        ...mapState('eseaAccount', ['eseaAccounts']),
        ...mapState('organisation', ['organisation']),
        permission () {
            if (this.organisation.accesLevel) {
                const accesLevel = this.organisation.accesLevel
                if (accesLevel === 'admin' || accesLevel === 'organisation admin') {
                    return true
                }
            }
            return false
        }
    }
}
    // <!-- <div class="p-grid p-m-5">
    //     <div v-for="eseaAccount in eseaAccounts" :key="eseaAccount.id" class="p-col-12 p-md-6 p-lg-4" style="width: 450px">
    //         <div class="p-p-3" :class="eseaAccount.hover ? 'p-shadow-10 p-m-1' : 'p-shadow-5 p-m-2'" style="border-radius: 3px" :style="(eseaAccount.hover ? styleObject : '')"
    //         @mouseover="eseaAccount.hover=true" @mouseleave="eseaAccount.hover = false" @click="goToEseaAccount(eseaAccount)">
    //             <h3>Method: {{ eseaAccount.method }}</h3>
    //             <Divider />
    //             <div class="p-text-left p-ml-5">
    //                 <div class="p-grid">
    //                     <p class="p-col-12">Deployed by <span v-if="eseaAccount.network" class="p-text-bold">Network: {{eseaAccount.network}}</span><span v-else class="p-text-bold">Organisation: {{eseaAccount.organisation}}</span></p>
    //                     <p v-if="eseaAccount.campaign" class="p-col-6">campaign: {{ eseaAccount.campaign }}</p>
    //                     <p v-else class="p-col-6">No Campaign</p>
    //                     <p class="p-col-6">Report: <span class="p-text-bold">{{eseaAccount.report || 'No'}}</span></p>
    //                     <p class="p-col-6">Respondents: <span class="p-text-bold">{{eseaAccount.all_respondents}}</span></p>
    //                     <p class="p-col-6">Responses: <span class="p-text-bold">{{eseaAccount.all_responses.length}}</span></p>
    //                     <p class="p-col-6">Year: {{ eseaAccount.year }}</p>
    //                 </div>
    //             </div>
    //         </div>
    //     </div>
    // </div> -->
</script>
