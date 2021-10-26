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
            refresh: false,
            styleObject: { backgroundColor: '#EFEEEE' },
            createCampaignDialog: false
        }
    },
    computed: {
        ...mapState('network', ['network']),
        ...mapState('campaign', ['campaigns', 'campaign']),
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
// <div style="min-width: 1000px;">
//     <div class="p-d-flex p-m-5 p-jc-between">
//         <div>
//         <Button label="Change Display" class="p-button-sm p-mr-2" @click="tableDisplay = !tableDisplay" />
//         </div>
//         <span class="p-input-icon-left">
//             <i class="pi pi-search" /><InputText v-model="search" placeholder="Search Campaigns..." />
//         </span>
//     </div>
//     <Divider />
// </div>
</script>
