// used by NetworkOrganisations.vue, OrganisationNetworks.vue

<template>
    <TabView class="p-m-5 p-shadow-2">
        <TabPanel :header="incomingInvitations.length ? 'Received Invites ' + `(${incomingInvitations.length})`: 'Received Invites'">
            <div v-if="incomingInvitations.length">
                <div class="p-d-flex p-jc-end p-pb-2">
                    <Button icon="pi pi-check" label="Accept all" class="p-button-success p-button-sm p-mr-2" @click="reactOnAllRequests('accepted')" />
                    <Button icon="pi pi-check" label="Decline all" class="p-button-danger p-button-sm" @click="reactOnAllRequests('denied')" />
                </div>
                <DataTable :value="incomingInvitations" datakey="id" selectionMode="single" @row-select="goToOrganisation" showGridlines autoLayout
                :paginator="true" :rows="5" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

                    <Column v-for="col of incomingInvitationsColumns" :field="col.field" :header="col.header" :key="col.field" bodyStyle="" /> <!-- text-align: center; overflow: visible  contentStyle="width: 500px;" -->
                    <Column headerStyle="width: 5rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                        <template #body="{data}">
                            <div class="p-d-flex">
                                <Button icon="pi pi-check" class="p-button-success p-button-sm p-mr-2" @click="reactOnRequest(data, 'accepted')" style="width: 50px" />
                                <Button icon="pi pi-times" class="p-button-danger p-button-sm" @click="reactOnRequest(data, 'denied')" style="width: 50px" />
                            </div>
                        </template>
                    </Column>
                </Datatable>
            </div>
            <div v-else>
                <p class="p-m-5 p-text-left">No received invitations</p>
            </div>
        </TabPanel>
        <TabPanel :header="outgoingInvitations.length ? 'Sent Requests ' + `(${outgoingInvitations.length})`: 'Sent Requests'">
             <div v-if="outgoingInvitations.length"> <!-- style="background-color: rgba(0, 105, 92, 0.4); border-radius: 5px;" -->
                <DataTable :value="outgoingInvitations" datakey="id" selectionMode="single" @row-select="goToOrganisation" showGridlines autoLayout
                :paginator="true" :rows="5" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

                    <Column v-for="col of outgoingInvitationsColumns" :field="col.field" :header="col.header" :key="col.field" bodyStyle="" /> <!-- text-align: center; overflow: visible  contentStyle="width: 500px;" -->
                    <Column headerStyle="width: 5rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                        <template #body="{data}">
                            <div class="p-d-flex">
                                <Button label="Cancel" class="p-button-danger p-button-sm" @click="cancelRequest(data)" />
                            </div>
                        </template>
                    </Column>
                </Datatable>
            </div>
            <div v-else>
                <p class="p-m-5 p-text-left">No current invites</p>
            </div>
        </TabPanel>
    </TabView>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
    props: {
        parenttype: {
            type: String,
            required: true
        }
    },
    data () {
        return {
        }
    },
    computed: {
        ...mapState('membership', ['memberships']),
        // Did the organisation or the network create the membership request?
        incomingInvitations () {
            let temp = []
            temp = this.memberships.filter(m => m.requester !== this.parenttype)
            return temp
        },
        outgoingInvitations () {
            let temp = []
            temp = this.memberships.filter(m => m.requester === this.parenttype)
            return temp
        },
        incomingInvitationsColumns () {
            if (this.parenttype === 'network') {
                return [
                    { field: 'organisation_name', header: 'Name' },
                    { field: 'organisation_description', header: 'Description' },
                    { field: 'status', header: 'Status' }
                ]
            }
            if (this.parenttype === 'organisation') {
                return [
                    { field: 'network_name', header: 'Name' },
                    { field: 'network_description', header: 'Description' },
                    { field: 'status', header: 'Status' }
                ]
            }
            return [{ field: 'id', header: 'id' }]
        },
        // Sets the right columns dependent whether an organisation or network send out the invite
        outgoingInvitationsColumns () {
            if (this.parenttype === 'network') {
                return [
                    { field: 'organisation_name', header: 'Name' },
                    { field: 'organisation_description', header: 'Description' },
                    { field: 'status', header: 'Status' }
                ]
            }
            if (this.parenttype === 'organisation') {
                return [
                    { field: 'network_name', header: 'Name' },
                    { field: 'network_description', header: 'Description' },
                    { field: 'status', header: 'Status' }
                ]
            }
            return [{ field: 'id', header: 'Id' }]
        }
    },
    methods: {
        ...mapActions('membership', ['fetchMemberships', 'deleteMembership', 'updateMembership']),
        async getMembershipRequests () {
            this.$emit('refresh', true)
        },
        async reactOnAllRequests (choice) {
            for (const request of this.memberships) {
                if (choice === 'accepted') {
                    await this.updateMembership({ id: request.id, data: { network: request.network, organisation: request.organisation, requester: request.requester, status: choice } })
                } else if (choice === 'denied') {
                    await this.deleteMembership({ id: request.id })
                }
            }
            this.getMembershipRequests()
        },
        async reactOnRequest (request, choice) {
             if (choice === 'accepted') {
                await this.updateMembership({ id: request.id, data: { network: request.network, organisation: request.organisation, requester: request.requester, status: choice } })
            } else if (choice === 'denied') {
                await this.deleteMembership({ id: request.id })
            }
            this.getMembershipRequests()
        },
        async cancelRequest (request) {
            await this.deleteMembership({ id: request.id })
            this.getMembershipRequests()
        }
    }
}
</script>
