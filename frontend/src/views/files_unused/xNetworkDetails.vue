<template>
               <!-- <div class="p-grid p-m-3">
                    <div class="p-col-3" v-for="organisation in networkorganisations" :key="organisation.id">
                        <div class="p-shadow-1 p-p-4" @click="testclick(organisation)">
                            <h3>{{ organisation.name }}</h3>
                            <h6>Founded by {{ organisation.creator.username }}</h6>
                            <p>{{ organisation.description }}</p>
                            <Button icon="pi pi-times" label="Remove" class="p-button-warning" />
                        </div>
                    </div>
                </div> -->
    <div class="card p-mx-5">
        <h1>{{ network.name }} - created by {{ network.created_by }}</h1>
        <div class="p-grid">
            <div class="p-col-5 p-d-flex p-ai-center p-jc-center">
                <div class="p-fluid">
                   <p class="p-text-justify">{{ network.description }} <br> Below you can find a tab with the organisations, methods, surveys, users and reports that are linked to this specific network. </p>
                </div>
            </div>
            <div class="p-col-2">
                <Divider layout="vertical" />
            </div>
            <div class="p-col-5 p-d-flex p-ai-center p-jc-center">
                 <p>{{ network.created_by }}</p>
                <Button label="Edit Network" icon="pi pi-user-plus" class="p-button-success p-m-2" @click="editNetworkDialog = true" />
                <Button label="Delete Network" icon="pi pi-trash" class="p-button-danger" @click="deleteNetworkDialog = true" />
            </div>
            <div class="p-col-12">
                <Button label="Request Network Participation" icon="pi pi-plus" class="p-button-success p-m-2" @click="requestParticipation" />
                </div>
        </div>
    </div>
    <TabView>
        <TabPanel header="Organisations">
            <my-organisations network-organisations selection-enabled></my-organisations>
        </TabPanel>
        <TabPanel header="Methods">
            <my-methods network-methods selection-enabled></my-methods>
        </TabPanel>
        <TabPanel header="Surveys">
            By Method or By Organisation
        </TabPanel>
        <TabPanel header="Users">
            <personalised-datatable table-name="Members" selection-toggle :columns="ParticipantsColumns" :custom-data="users" @item-redirect="goToSelectedUsers"/>
        </TabPanel>
    </TabView>

    <Dialog v-model:visible="editNetworkDialog" :style="{width: '450px'}" header="Network Details" :modal="true" class="p-fluid">
        <div class="p-field">
            <label for="name">Name</label>
            <InputText id="name" v-model.trim="network.name" required="true" autofocus :class="{'p-invalid': submitted && !network.name}" />
            <small class="p-error" v-if="submitted && !network.name">Name is required.</small>
        </div>
        <div class="p-field">
            <label for="description">Description</label>
            <Textarea id="description" v-model="network.description" required="true" rows="3" cols="20" />
        </div>
        <div class="p-field">
            <label for="ispublic">Should this network be public? </label>
            <SelectButton id="ispublic" v-model="network.ispublic" :options="ispublicbool" />
        </div>
        <template #footer>
            <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="editNetworkDialog = false"/>
            <Button label="Save" icon="pi pi-check" class="p-button-text" @click="editNetwork" :disabled="!network.name" />
        </template>
    </Dialog>

    <Dialog v-model:visible="deleteNetworkDialog" :style="{width: '450px'}" header="Confirm" :modal="true">
      <div class="confirmation-content">
          <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 2rem" />
            <span v-if="network">Are you sure you want to delete <b>{{network.name}}</b>?</span>
      </div>
      <template #footer>
        <Button label="No" icon="pi pi-times" class="p-button-text" @click="deleteNetworkDialog = false"/>
        <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="removeNetwork()" />
      </template>
    </Dialog>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import PersonalisedDatatable from '../components/PersonalisedDatatable'
import MyOrganisations from '../components/MyOrganisations'
import MyMethods from '../components/MyMethods'

export default {
    components: {
        PersonalisedDatatable,
        MyOrganisations,
        MyMethods
    },
    data () {
        return {
            ParticipantsColumns: [
                 { field: 'username', header: 'Username' },
                 { field: 'email', header: 'E-mail' },
                 { field: 'first_name', header: 'First Name' },
                 { field: 'last_name_prefix', header: 'Prefix' },
                 { field: 'last_name', header: 'Last Name' }
                 ],
            editNetworkDialog: false,
            deleteNetworkDialog: false,
            ispublicbool: ['true', 'false'],
            boolChoice: null,
            submitted: false
        }
    },
    computed: {
        ...mapState('network', ['network', 'networkorganisations']),
        ...mapState('organisation', ['organisations', 'organisation']),
        ...mapState('method', ['methods', 'method']),
        ...mapState('user', ['users', 'user'])
    },
    created () {
        this.initialize()
    },
    methods: {
        ...mapActions('network', ['fetchNetwork', 'updateNetwork', 'deleteNetwork', 'deleteNetworkOrganisations']),
        ...mapActions('organisation', ['fetchOrganisations', 'setOrganisation']),
        ...mapActions('method', ['fetchMethods', 'setMethod']),
        ...mapActions('user', ['fetchUsers', 'setUser']),
        async initialize () {
            await this.fetchNetwork({ id: this.network?.id || 0 })
            await this.fetchUsers({ query: `?network=${this.network?.id || 0}` })
        },
        async editNetwork () {
            this.editNetworkDialog = false
            await this.updateNetwork({})
            this.$toast.add({ severity: 'success', summary: 'Successful', detail: 'Network Updated', life: 3000 })
        },
        async removeNetwork () {
            this.deleteNetworkDialog = false
            await this.deleteNetwork({ id: this.network?.id || 0 })
            this.$toast.add({ severity: 'success', summary: 'Succesful', detail: 'Network Deleted', life: 3000 })
            this.$router.push({ name: 'networks' })
        },
       goToSelectedUsers (selectedRows) {
        this.setUser({ ...selectedRows[0] })
        this.$router.push({ name: 'userdetails', params: { id: this.user.id } })
       }
    }
}
</script>
