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
