<template>
    <organisation-list :permission="permission" v-model:refresh="refresh" :networkorganisations="true" :invitableorganisations="invitableOrganisations" @invite-organisation="inviteChosenOrganisation" @remove-organisation="removeChosenOrganisation">
        <Button v-if="permission" :label="(invitableOrganisations) ? 'Show own Organisations':'Invite Organisations'" :class="(invitableOrganisations) ? 'p-button-warning':'p-button-success'" @click="invitableOrganisations= !invitableOrganisations" />
    </organisation-list>

    <invitation-window v-if="permission" parenttype="network" @refresh="refreshData()"/>

    <Dialog v-model:visible="removeDialog" style="width: 500px" header="Confirm Deletion" :modal="true"  :dismissableMask="true">
            Are you sure you want to <b>delete</b> the following organisation(s)?
            <div class="p-shadow-1 p-p-3 p-m-5">{{selectedOrganisation.name}}</div>
        <template #footer>
        <Button label="No" icon="pi pi-times" class="p-button-text" @click="removeDialog=false" />
        <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="removeOrg" />
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
        // ...mapState('organisation', ['organisations', 'organisation']),
        ...mapState('network', ['network']),
        ...mapState('membership', ['memberships']),
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
        async removeChosenOrganisation (organisation) {
            this.selectedOrganisation = organisation
            this.removeDialog = true
        },
        async removeOrg () {
            if (this.selectedOrganisation.id) {
                var newListOfOrganisations = this.network?.organisations?.filter(item => item !== this.selectedOrganisation.id)
                console.log(newListOfOrganisations)
                await this.patchNetwork({ organisations: newListOfOrganisations })
                this.removeDialog = false
                this.refreshData()
            }
        },
        inviteChosenOrganisation (organisation) {
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
// <!-- <div class="p-d-flex p-m-5" :class="permission ? 'p-jc-between' : 'p-jc-end' " style="min-width: 600px;">
//     <div v-if="permission">
//         <Button :label="'Invite Organisation'" icon="pi pi-plus" class="p-button-success p-button-sm p-mr-2" @click="addableOrganisations()" />
//         <Button :label="removeMode ? 'Select the organisation to remove': 'Enable Remove Mode'" icon="pi pi-trash" class="p-button-sm" :class="removeMode ? 'p-button-danger' : 'p-button-warning'" :disabled="!organisations.length" @click="removeMode = !removeMode" />
//     </div>
//     <span class="p-input-icon-left">
//         <i class="pi pi-search" /><InputText v-model="search" placeholder="Search Organisations..." />
//     </span>
// </div>
// <Divider /> -->
// const result = this.organisationsToInvite.map(a => a.id)
// var newListOfOrganisations = this.network.organisations.concat(result)
// await this.patchNetwork({ organisations: newListOfOrganisations })
// console.log(this.selectedOrganisations)
// this.removeDialog = false
// if (this.selectedOrganisations.length) {
//     const result = this.selectedOrganisations.map(a => a.id)
//     var newListOfOrganisations = this.network.organisations.filter((item) => !result.includes(item))
//     console.log('>>>', newListOfOrganisations)
//     await this.patchNetwork({ organisations: newListOfOrganisations })
// }
// this.refreshData()
// async reactOnAllRequests (action) {
//     for (const request of this.memberships) {
//         await this.updateMembership({ id: request.id, data: { network: this.$route.params.NetworkId, organisation: request.organisation, requester: 'organisation', status: action } })
//     }
//     this.initialize()
// },
// async reactOnRequest (request, action) {
//     console.log(action, request)
//     await this.updateMembership({ id: request.id, data: { network: this.$route.params.NetworkId, organisation: request.organisation, requester: 'organisation', status: action } })
//     this.initialize()
// },
// async goToOrganisation (organisation) {
//     // if (this.removeMode) {
//     //     this.selectedOrganisations = []
//     //     this.selectedOrganisations.push(organisation)
//     //     this.removeDialog = true
//     // } else {
//     if (organisation.id) {
//     await this.setOrganisation({ ...organisation })
//     this.$router.push({ name: 'organisationoverview', params: { OrganisationId: organisation.id } })
//     }
//     <!-- <h3 class="p-text-left p-ml-2">Invites</h3>
//     <TabView>
//         <TabPanel header="Received">
//             {{ requestsByNetwork }}
//             {{ requestsByOrganisation }}
//         </TabPanel>
//         <TabPanel header="Sent">
//         </TabPanel>
//     </TabView>

//     <div v-if="memberships.length" class="p-p-3 p-shadow-3" style="background-color: rgba(0, 105, 92, 0.4); margin: 100px; border-radius: 5px;">
//         <div class="p-d-flex p-jc-between p-ai-center">
//              <h3 class="p-text-left p-text-bold">Participation Requests</h3>
//              <div>
//             <Button icon="pi pi-check" label="Accept all" class="p-button-success p-button-sm p-mr-2" @click="reactOnAllRequests('accepted')" />
//             <Button icon="pi pi-check" label="Decline all" class="p-button-danger p-button-sm" @click="reactOnAllRequests('denied')" />
//             </div>
//         </div>
//         <DataTable :value="memberships" datakey="id" selectionMode="single" @row-select="goToOrganisation" showGridlines autoLayout
//         :paginator="true" :rows="5" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
//         :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

//            <Column field="ispublic" header="Public" headerStyle="width: 5rem">
//                 <template #body="slotProps">
//                     <i class="pi p-text-center p-text-bold" style="width:100%; font-size: 20px;" :class="{'true-icon pi-check': slotProps.data.ispublic, 'false-icon pi-times': !slotProps.data.ispublic}" :style="(slotProps.data.ispublic ? 'color: green;':'color: red;')"></i>
//                 </template>
//             </Column>
//             <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field" bodyStyle="" /> text-align: center; overflow: visible  contentStyle="width: 500px;"
//             <Column field="created_by" header="Creator">
//                 <template #body="slotProps">
//                     <div v-if="slotProps.data.created_by !== currentuser">{{slotProps.data.created_by}}</div> <div v-else class="p-text-bold">You</div>
//                 </template>
//             </Column>
//             <Column headerStyle="width: 5rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
//                 <template #body="{data}">
//                     <div class="p-d-flex">
//                         <Button icon="pi pi-check" class="p-button-success p-button-sm p-mr-2" @click="reactOnRequest(data, 'accepted')" style="width: 50px" />
//                         <Button icon="pi pi-times" class="p-button-danger p-button-sm" @click="reactOnRequest(data, 'denied')" style="width: 50px" />
//                     </div>
//                 </template>
//             </Column>
//         </Datatable>
//     </div>
//     <div v-else>
//         <h3 class="p-m-5 p-text-left p-text-bold">No current requests</h3>
//     </div>
// {{organisationsToInvite}} -->
//  <!-- <Dialog v-model:visible="inviteDialog" style="width: 500px" modal="true" dismissableMask="true" class="p-fluid">
//      <div class="p-field">
//         <MultiSelect id="organisations" v-model="organisationsToInvite" :options="organisations" optionLabel="name" placeholder="Select Organisations" :filter="true" class="multiselect-custom">
//             <template #value="slotProps">
//                 <div v-for="option of slotProps.value" :key="option.id">
//                     <div>{{option}}</div>
//                 </div>
//                 <template v-if="!slotProps.value || slotProps.value.length === 0">
//                     Select Organisations
//                 </template>
//             </template>
//             <template #option="slotProps">
//                 <div>{{slotProps.option.name}}</div>
//             </template>
//         </MultiSelect>
//      </div>
//         <div class="p-field">
//         <label for="message">Message to Organisations</label>
//         <Textarea id="message" v-model="something" required="true" :autoResize="true" rows="3" />
//         </div>
//     <template #footer>
//             <Button label="Invite Organisations" icon="pi pi-plus" @click="addOrganisations"/>
//             <Button label="Cancel" icon="pi pi-check" class="p-button-text" @click="inviteDialog=false" />
//     </template>
// </Dialog> -->
        // async addableOrganisations () {
    //     await this.fetchOrganisations({ query: `?excludenetwork=${this.$route.params.NetworkId}` })
    //     this.organisationsToInvite = []
    //     this.inviteDialog = true
    // },
    // async addOrganisations () {
    //     this.inviteDialog = false
    //     if (this.organisationsToInvite.length) {
    //         for (const organisation of this.organisationsToInvite) {
    //             console.log('>>', organisation)
    //             await this.createMembership({ network: this.$route.params.NetworkId, organisation: organisation.id, requester: 'network' })
    //         }
    //         console.log(this.organisationsToInvite)
    //     }
    //     this.refreshData()
    // },
</script>
