<template>
    <network-list :permission="permission" v-model:refresh="refresh" :organisationnetworks="true" :joinableNetworks="joinableNetworksBool" @leave-network="leaveNetwork" @join-network="joinNetwork">
        <Button v-if="permission" :label="(joinableNetworksBool) ? 'Show own Network':'Join Network'" :class="(joinableNetworksBool) ? 'p-button-warning':'p-button-success'" @click="joinableNetworksBool= !joinableNetworksBool" />
    </network-list>

    <invitation-window v-if="permission" parenttype="organisation" @refresh="refreshData()" />

    <Dialog v-model:visible="removeDialog" style="width: 500px" header="Confirm Deletion" :modal="true"  :dismissableMask="true">
            Are you sure you want to <b>delete</b> the following network?
            <div class="p-shadow-1 p-p-3 p-m-5">{{selectedNetwork.name}}</div>
        <template #footer>
        <Button label="No" icon="pi pi-times" class="p-button-text" @click="removeDialog=false" />
        <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="removeNetwork()" />
      </template>
    </Dialog>

    <Dialog v-model:visible="requestParticipationDialog" class="p-fluid" style="width: 500px" :header="`Network: ${selectedNetwork?.name}`" :modal="true" :dismissableMask="true">
        <div class="p-field">
        <label for="message">Message</label>
        <Textarea id="message" v-model="something" rows="5" :autoResize="true" placeholder="Write a message to the network you want to participate in." />
        </div>
        <template #footer>
            <Button label="Cancel" icon="pi pi-times" @click="requestParticipationDialog=false" class="p-button-text"/>
            <Button label="Request Participation" icon="pi pi-check" @click="requestNetworkParticipation" />
        </template>
    </Dialog>
</template>

<script>
    import { mapState, mapActions } from 'vuex'
    import NetworkList from '../../components/lists/NetworkList'
    import InvitationWindow from '../../components/InvitationWindow'

    export default {
        components: {
            NetworkList,
            InvitationWindow
        },
        data () {
            return {
                joinableNetworksBool: false,
                refresh: false,
                removeDialog: false,
                requestParticipationDialog: false,
                loading: true,
                selectedNetwork: null,
                columns: [
                        { field: 'network_name', header: 'Name' },
                        { field: 'network_description', header: 'Description' }
                    ]
            }
        },
        computed: {
            ...mapState('network', ['networks']),
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
        },
        watch: {
            joinableNetworksBool (val) {
                this.refresh = !this.refresh
            }
        },
        async created () {
        this.refreshData()
        },
        methods: {
            ...mapActions('organisation', ['patchOrganisation']),
            ...mapActions('membership', ['fetchMemberships', 'createMembership', 'updateMembership']),
            async refreshData () {
                this.refresh = !this.refresh
                this.loading = true
                await this.fetchMemberships({ query: `?organisation=${this.$route.params.OrganisationId}` })
                this.loading = false
            },
            joinNetwork (network) {
                this.selectedNetwork = network
                this.requestParticipationDialog = true
                console.log('-->', network)
            },
            async requestNetworkParticipation () {
                this.joinableNetworksBool = false
                await this.createMembership({ data: { network: this.selectedNetwork.id, organisation: this.$route.params.OrganisationId, requester: 'organisation' } })
                this.requestParticipationDialog = false
                this.refreshData()
            },
            leaveNetwork (network) {
                this.selectedNetwork = network
                this.removeDialog = true
                console.log(network)
            },
            async removeNetwork () {
                console.log(this.organisation.networks, this.selectedNetwork)
                this.removeDialog = false
                if (this.selectedNetwork) {
                    var newListOfNetworks = this.organisation.networks.filter(item => item !== this.selectedNetwork.id)
                    console.log('>>>', newListOfNetworks, 'iii', this.selectedNetwork)
                    await this.patchOrganisation({ networks: newListOfNetworks })
                }
                this.refreshData()
            }
        }
    }
</script>
