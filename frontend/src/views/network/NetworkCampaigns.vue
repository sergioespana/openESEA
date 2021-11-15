// http://localhost:8080/network/1/campaigns/

<template>
    <campaign-list>
        <Button v-if="permission" label="New Campaign" icon="pi pi-plus" class="p-button-success p-button-sm" @click="createCampaignDialog=true" />
    </campaign-list>

    <Dialog v-model:visible="createCampaignDialog" style="width: 700px" header="Campaign Details" :modal="true" :dismissableMask="true">
        <campaign-form @closedialog="createCampaignDialog=false" />
    </Dialog>
</template>

<script>
    import { mapState } from 'vuex'
    import CampaignList from '../../components/lists/CampaignList'
    import CampaignForm from '../../components/forms/CampaignForm'

    export default {
        components: {
            CampaignList,
            CampaignForm
        },
        data () {
            return {
                createCampaignDialog: false
            }
        },
        computed: {
            ...mapState('network', ['network']),
            permission () {
                if (this.network.accesLevel) {
                    const accesLevel = this.network.accesLevel
                    if (accesLevel === 'admin' || accesLevel === 'network admin') {
                        return true
                    }
                }
                return false
            }
        }
    }
</script>
