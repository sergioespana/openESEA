// http://localhost:8080/network/1/organisations/

<template>
    <organisation-list :permission="permission" v-model:refresh="refresh" :networkorganisations="true" :invitableorganisations="invitableOrganisations" @invite-organisation="openOrganisationInvitationDialog" @remove-organisation="openOrganisationRemovalDialog">
        <Button v-if="permission" :label="(invitableOrganisations) ? 'Show own Organisations':'Invite Organisations'" :class="(invitableOrganisations) ? 'p-button-warning':'p-button-success'" @click="invitableOrganisations= !invitableOrganisations" />
    </organisation-list>

    <invitation-window v-if="permission" parenttype="network" @refresh="refreshData()"/>

    <Dialog v-model:visible="removeDialog" style="width: 500px" header="Confirm Deletion" :modal="true"  :dismissableMask="true">
            Are you sure you want to <b>delete</b> the following organisation(s)?
            <div class="p-shadow-1 p-p-3 p-m-5">{{selectedOrganisation.name}}</div>
        <template #footer>
            <Button label="No" icon="pi pi-times" class="p-button-text" @click="removeDialog=false" />
            <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="removeOrganisation" />
      </template>
    </Dialog>

    <Dialog v-model:visible="inviteDialog" class="p-fluid" style="width: 500px" :header="`Organisation: ${selectedOrganisation?.name}`" :modal="true" :dismissableMask="true">
        <div class="p-field">
        <label for="message">Message</label>
        <Textarea id="message" v-model="something" rows="5" :autoResize="true" placeholder="Write a message to the organisation you want to invite." />
        </div>
        <template #footer>
            <Button label="Cancel" icon="pi pi-times" @click="inviteDialog=false" class="p-button-text"/>
            <Button label="Invite Organisation" icon="pi pi-check" @click="inviteOrganisation" />
        </template>
    </Dialog>
</template>

<script>
    import { mapActions, mapState, mapGetters } from 'vuex'
    import OrganisationList from '../../components/lists/OrganisationList'
    import InvitationWindow from '../../components/InvitationWindow'

    export default {
        components: {
            OrganisationList,
            InvitationWindow
        },
        data () {
            return {
                refresh: false,
                invitableOrganisations: false,
                loading: true,
                selectedOrganisation: null,
                inviteDialog: false,
                removeDialog: false,
                columns: [
                        { field: 'organisation_name', header: 'Name' },
                        { field: 'organisation_description', header: 'Description' }
                    ]
            }
        },
        computed: {
            ...mapState('network', ['network']),
            // membership stands for 'membership requests'
            ...mapState('membership', ['memberships']),
            // Whether Network or Organisation has requested the membership
            ...mapGetters('membership', ['requestsByNetwork', 'requestsByOrganisation']),
            permission () {
                if (this.network.accesLevel) {
                    const accesLevel = this.network.accesLevel
                    if (accesLevel === 'admin' || accesLevel === 'network admin') {
                        return true
                    }
                }
                return false
            }
        },
        async created () {
            this.refreshData()
        },
        methods: {
            ...mapActions('network', ['patchNetwork']),
            ...mapActions('membership', ['fetchMemberships', 'createMembership']),
            async refreshData () {
                this.refresh = !this.refresh
                this.loading = true
                await this.fetchMemberships({ query: `?network=${this.$route.params.NetworkId}` })
                this.loading = false
            },
            openOrganisationRemovalDialog (organisation) {
                this.selectedOrganisation = organisation
                this.removeDialog = true
            },
            async removeOrganisation () {
                if (this.selectedOrganisation.id) {
                    var newListOfOrganisations = this.network?.organisations?.filter(item => item !== this.selectedOrganisation.id)
                    await this.patchNetwork({ organisations: newListOfOrganisations })
                    this.removeDialog = false
                    this.refreshData()
                }
            },
            openOrganisationInvitationDialog (organisation) {
                this.selectedOrganisation = organisation
                this.inviteDialog = true
            },
            async inviteOrganisation () {
                if (this.selectedOrganisation.id) {
                    await this.createMembership({ data: { network: this.$route.params.NetworkId, organisation: this.selectedOrganisation.id, requester: 'network' } })
                    this.inviteDialog = false
                    this.refreshData()
                }
            }
        }
    }
</script>
