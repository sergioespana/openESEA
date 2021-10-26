<template>
    <div class="p-m-1" style="min-width: 1000px;">
        <h1>Networks Overview</h1>
        <Button v-if="admin" label="Create Network" icon="pi pi-plus" class="p-button-success p-button-sm p-d-flex p-m-5" @click="createNetworkDialog=true" />
        <network-list :search="search" />
    </div>
    <Dialog v-model:visible="createNetworkDialog" style="width: 500px" header="Network Details" :modal="true" :dismissableMask="true">
        <network-form @closedialog="createNetworkDialog=false" />
    </Dialog>
</template>

<script>
import { mapState } from 'vuex'
import NetworkList from '../../components/lists/NetworkList'
import NetworkForm from '../../components/forms/NetworkForm'

export default {
    components: {
        NetworkList,
        NetworkForm
    },
    data () {
        return {
            search: '',
            createNetworkDialog: false,
            admin: false
        }
    },
    computed: {
        ...mapState('network', ['networks', 'network']),
        ...mapState('authentication', ['currentuser', 'authenticatedUser'])
    },
    mounted () {
        if (this.authenticatedUser.is_superuser) {
            this.admin = true
        }
    }
}
 </script>

// NetworkColumns: [
//     { field: 'ispublic', header: 'Public' },
//     { field: 'name', header: 'Name' },
//     { field: 'description', header: 'Description' },
//     { field: 'organisations.length', header: 'Organisations' },
//     { field: 'created_by', header: 'Created by' }
// ],
        <!-- <div class="p-d-flex p-jc-between p-ai-center p-m-5">
            <div class="p-d-flex p-ai-center">
                <Button :label="(allNetworks ? 'All Networks' : 'My Networks')" class="p-button-sm p-mr-2" @click="allNetworks = !allNetworks"/>
                <div class="p-ml-2">
                <Checkbox id="includeItems" v-model="allNetworks" :binary="true" class="p-mr-2" />
                 <label for="includeItems">Include Public Networks</label>
                 </div>
            </div>
            <div class="p-d-flex p-ai-center">
                                <div class="p-d-flex p-ai-center">
                <i class="pi pi-list" :style="(tableDisplay ? 'color: lightgrey;': '')" style="font-size: 30px;" @click="tableDisplay = !tableDisplay" />
                <i class="pi pi-microsoft p-mx-3" :style="(tableDisplay ? '' : 'color: lightgrey;')" style="font-size: 23px;" @click="tableDisplay = !tableDisplay" />
                </div>
                <span class="p-input-icon-left">
                    <i class="pi pi-search" /><InputText v-model="search" placeholder="Search Networks..." />
                </span>
            </div>
        </div> -->
