<template>
     <div class="p-grid nested-grid" style="height: 90vh;">
    <organisation-sidebar class=""></organisation-sidebar>
    <div class="p-col p-grid nested-grid p-mx-5 p-px-5">
        <div class="p-col-9 p-py-5">
            <div class="p-grid">
                <div class="p-col-2 p-d-flex p-jc-start">
                    <div class="p-grid">
                        <p class="p-col-12 p-text-left p-text-italic p-m-0" >{{ organisation.name }}</p>
                        <h3 class="p-col-12 p-text-left p-m-0">Overview</h3>
                    </div>
            </div>
            <div class="p-col-10 p-d-flex p-ai-center p-jc-end">
                <Button label="Edit Organisation" icon="pi pi-user-plus" class="p-button-secondary p-mr-2" @click="editOrganisationDialog = true"/>
                <Button label="Delete Organisation" icon="pi pi-trash" class="p-button-danger" @click="confirmDeletion" />
            </div>
            <Divider />
            <div class="p-col-12 p-text-justify"><h4 class="p-text-bold">Description</h4>
                {{ organisation.description }} - Lorem ipsum dolor sit amet, consectetur adipiscing elit. In convallis mi sit amet faucibus malesuada. Vestibulum fringilla sed dui bibendum laoreet. Donec suscipit sit amet leo et mattis. Aenean mattis tempus turpis a vulputate. Nunc bibendum pulvinar neque, nec mattis nisl tincidunt ut. Nam a quam id justo dictum pulvinar. Sed luctus dictum ligula, id sagittis tellus aliquam id. Vestibulum auctor vestibulum turpis.
                </div>
        </div>
        <div class="p-col-12 p-shadow-5">
            <div v-if="tasks">
                <h4>All Done!</h4>
                <p class="p-text-italic">
                    {{organisation.name}} and all related networks does not require your attention right now.
                </p>
            </div>
            <div v-else>
                <h4>The following tasks require your attention.</h4>
                <Button label="Task 1: As employee of organisation 2 you are asked to fill in the survey of network 1." class="p-button-success p-shadow-10"/>
                <br><br>
                <Button label="Task 2: As manager of organisation 2 you are asked to fill in the survey of network 1." class="p-button-primary p-shadow-10" />

                <!-- <div class="p-shadow-2 p-m-3 p-p-3 p-text-left"><span class="p-text-bold">Task 1:</span> As employee of {{organisation.name}} you are asked to fill in the survey of network 1.</div>
                <div class="p-shadow-2 p-m-3 p-p-3 p-text-left"><span class="p-text-bold">Task 2:</span> As manager of {{organisation.name}} you are asked to fill in the survey of network 1.</div> -->
            </div>
        </div>
    </div>
    <div class="p-col-1"><Divider layout="vertical" /></div>
    <div class="p-col-2">
        <div class="p-grid">
            <div class="p-col-12">
                <h3 class="p-mb-2 p-text-left">Network Membership</h3>
                <Divider class="p-m-0" />
                <div class="p-m-3">
                    <div v-if="networks.length">
                        <div v-for="network, num in networks" :key="network.name">
                            {{num+1}}. <router-link :to="{name: 'networkdetails', params: { id: network.id } }" style="text-decoration: none; color: blue;">{{network.name}}</router-link>
                            <Divider class="p-m-1" />
                        </div>
                    </div>
                    <div v-else>
                        <div class="p-py-5 p-text-italic">No networks to display</div>
                    </div>
                </div>
                <router-link :to="{name: 'organisationnetworks', params: { id: this.organisation?.id}}" style="text-decoration: none; color: blue;">Show all Related Networks</router-link>
            </div>
            <div class="p-col-12">
                <h3 class="p-mb-2 p-text-left">Related Surveys</h3>
                <Divider class="p-m-0" />
                <div class="p-m-3">
                    <div v-if="!organisations.length">
                        <div v-for="organisation, num in organisations" :key="organisation.name">
                            {{num+1}}. <router-link :to="{name: 'organisationsurveys', params: { id: organisation.id }}" style="text-decoration: none; color: blue;">survey {{num+1}}</router-link>
                            <Divider class="p-m-1" />
                        </div>
                    </div>
                    <div v-else>
                        <div class="p-py-5 p-text-italic">No available surveys</div>
                    </div>
                </div>
                <router-link :to="{name: 'organisationsurveys', params: { id: organisation.id }}" style="text-decoration: none; color: blue;">Show all Organisation Surveys</router-link>
            </div>
              <div class="p-col-12">
                <h3 class="p-mb-2 p-text-left">Reports</h3>
                <Divider class="p-m-0" />
                <div class="p-m-3">
                    <div v-if="!organisations.length">
                        <div v-for="organisation, num in organisations" :key="organisation.name">
                            {{num+1}}. <router-link :to="{name: 'organisationreports', params: { id: organisation.id }}" style="text-decoration: none; color: blue;">report {{num+1}}</router-link>
                            <Divider class="p-m-1" />
                        </div>
                    </div>
                    <div v-else>
                        <div class="p-py-5 p-text-italic">No reports yet</div>
                    </div>
                </div>
                <router-link :to="{name: 'organisationreports', params: { id: organisation.id } }" style="text-decoration: none; color: blue;">Show all Organisation Reports</router-link>
            </div>
        </div>
    </div>
</div>
     </div>

    <Dialog v-model:visible="editOrganisationDialog" :style="{width: '450px'}" header="Network Details" :modal="true" class="p-fluid">
        <div class="p-field">
            <label for="name">Name</label>
            <InputText id="name" v-model.trim="organisation.name" required="true" autofocus :class="{'p-invalid': submitted && !organisation.name}" />
            <small class="p-error" v-if="submitted && !organisation.name">Name is required.</small>
        </div>
        <div class="p-field">
            <label for="description">Description</label>
            <Textarea id="description" v-model="organisation.description" required="true" rows="3" cols="20" />
        </div>
        <div class="p-field">
            <label for="ispublic">Should this organisation be public? </label>
            <SelectButton id="ispublic" v-model="organisation.ispublic" :options="ispublicbool" />
        </div>
        <template #footer>
            <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="hideDialogs"/>
            <Button label="Save" icon="pi pi-check" class="p-button-text" @click="editOrganisation" :disabled="!organisation.name" />
        </template>
    </Dialog>

    <Dialog v-model:visible="deleteOrganisationDialog" :style="{width: '450px'}" header="Confirm" :modal="true">
        <div class="confirmation-content">
            <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 2rem" />
            <span v-if="organisation">Are you sure you want to delete <b>{{organisation.name}}</b>?</span>
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" class="p-button-text" @click="deleteOrganisationDialog = false"/>
            <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="removeOrganisation()" />
        </template>
    </Dialog>
</template>

<script>
import { mapState, mapActions } from 'vuex'
// import PersonalisedDatatable from '../components/PersonalisedDatatable'
import OrganisationSidebar from '../components/OrganisationSidebar'
// import { AxiosInstance } from '../plugins/axios'
// import { required, minLength } from 'vuelidate/lib/validators'

export default {
    components: {
        // PersonalisedDatatable,
        OrganisationSidebar
    },
    data () {
        return {
            ParticipantsColumns: [
                { field: 'username', header: 'Username' },
                { field: 'first_name', header: 'First Name' },
                { field: 'last_name_prefix', header: 'Prefix' },
                { field: 'last_name', header: 'Last Name' }
            ],
            // organisationPart: [{
            //     username: 'Henk',
            //     first_name: 'Harry'
            // }],
            editOrganisationDialog: false,
            ispublicbool: ['true', 'false'],
            deleteOrganisationDialog: false,
            inviteUsersWindow: false,
            filters: {},
            selectedUsers: null,
            selectionToggle: false,
            submitted: false
        }
    },
    computed: {
        ...mapState('organisation', ['organisations', 'organisation', 'organisationParticipants']), // organisationparticipants
        ...mapState('network', ['networks']),
        ...mapState('user', ['users', 'user'])
    },
    created () {
        this.initialize()
    //     AxiosInstance.get(`/organisations/${this.$route.params.id}/`, { headers: { Authorization: `Bearer ${this.$store.state.accessToken}` } })
    //       .then(response => { this.$store.state.organisation = response.data })
    //       .catch(err => { console.log(err) })
    //     AxiosInstance.get(`/organisationparticipants/${this.$route.params.id}/`, { headers: { Authorization: `Bearer ${this.$store.state.accessToken}` } })
    //     .then(response => { this.$store.state.organisationparticipants = response.data })
    //     .catch(err => { console.log(err) })
    },
    methods: {
        ...mapActions('organisation', ['fetchOrganisation', 'updateOrganisation', 'deleteOrganisation', 'deleteOrganisationUsers']),
        ...mapActions('user', ['fetchUsers', 'setUser']),
        async initialize () {
            await this.fetchOrganisation({ id: this.$route.params.id || this.organisation?.id || 0 })
            await this.fetchUsers({ query: `organisation=${this.organisation?.id || 0}` })
            // await this.fetchOrganisationParticipants(this.organisation?.id || 0)
        },
        async editOrganisation () {
            this.editOrganisationDialog = false
            await this.updateOrganisation({})
            this.$toast.add({ severity: 'success', summary: 'Successful', detail: 'Organisation Updated', life: 3000 })
        },
        confirmDeletion () {
            this.deleteOrganisationDialog = true
        },
        async removeOrganisation () {
            this.deleteOrganisationDialog = false
            await this.deleteOrganisation({ id: this.organisation?.id || 0 })
            this.$toast.add({ severity: 'success', summary: 'Succesful', detail: 'Organisation Deleted', life: 3000 })
            this.$router.push({ name: 'organisations' })
        },
        async openInviteUsersWindow () {
            await this.fetchUsers({ query: `excludeorganisation=${this.organisation?.id || 0}` })
            this.inviteUsersWindow = true
        },
        async sendInvitationToUsers () {
            await this.deleteOrganisationUsers({ data: this.selectedUsers })
            this.initialize()
        },
        hideDialogs () {
            this.editOrganisation = false
            this.deleteOrganisation = false
        },
        goToSelectedUsers (selectedRows) {
            if (!this.selectionToggle) {
                this.setUser({ ...selectedRows[0] }) // SelectedRows instead of selectedRows[0], might be because there is only one item in the datatable
                this.$router.push({ name: 'userdetails', params: { id: this.user.id } })
            } else {
                this.selectedUsers = selectedRows
            }
       }
    }
}
</script>
