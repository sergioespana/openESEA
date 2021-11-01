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
</script>
