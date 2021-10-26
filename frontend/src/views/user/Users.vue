<template>
    <div class="p-m-1" style="min-width: 1000px;">
        <h1>Manage Users</h1>
        <div class="p-d-flex p-jc-between p-m-5">
    </div>
    <user-list :users="users" :table="tableDisplay" :search="search" :loading="loading" @clicked-user="goToUser">
        <Button label="Send Message" icon="pi pi-plus" class="p-button-success p-button-sm p-mr-2" @click="messageDialog = true" />
    </user-list>
<!-- <my-users /> -->
    <!-- <div class="users">
        <Toast position="top-right"/>
        <div class="card p-m-5 p-shadow-2">
              <Toolbar>
                <template #left>
                    <ToggleButton v-model="selectionToggle" onLabel="Selecting: Enabled" offLabel="Selecting: Disabled" onIcon="pi pi-check" offIcon="pi pi-times" class="p-mr-2" />
                </template>

                <template #right>
                    <span class="p-input-icon-left">
                        <i class="pi pi-search" />
                        <InputText v-model="filters['global']" placeholder="Search..." />
                    </span>
                </template>
            </Toolbar>
          <personalised-datatable table-name="users" selectionToggle :columns="ParticipantsColumns" :filters="filters" :custom-data="users" @item-redirect="goToUser"/>

        </div>
    </div> -->
    </div>
    <Dialog v-model:visible="messageDialog" style="width: 500px" header="Send Message" :modal="true" :dismissableMask="true" class="p-fluid">
        <div>
         <MultiSelect id="users" v-model="usersToMessage" :options="users" optionLabel="username" placeholder="Select Users" :filter="true" class="multiselect-custom">
                <template #value="slotProps">
                    <div v-for="option of slotProps.value" :key="option.id">
                        <div>{{option.username}}</div>
                    </div>
                    <template v-if="!slotProps.value || slotProps.value.length === 0">
                        Select Users
                    </template>
                </template>
                <template #option="slotProps">
                    <div>{{slotProps.option.username}}</div>
                </template>
            </MultiSelect>
</div>
<div class="p-field p-grid">
            <label for="message" class="p-col-12">Message to selected User(s)</label>
            <Textarea id="message" v-model="something" :autoResize="true" rows="3" />
</div>
        <template #footer>
                <Button label="Send Message" icon="pi pi-plus" @click="SendMessage()"/>
                <Button label="Cancel" icon="pi pi-check" class="p-button-text" @click="messageDialog = false" />
        </template>
    </Dialog>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import UserList from '../../components/lists/UserList'
import MultiSelect from 'primevue/multiselect'

export default {
    name: 'Users',
    components: {
        UserList,
        MultiSelect

    },
    data () {
        return {
            tableDisplay: false,
            search: '',
            loading: true,
            messageDialog: false,
            usersToMessage: []
        //     ParticipantsColumns: [
        //          { field: 'username', header: 'Username' },
        //          { field: 'email', header: 'E-mail' },
        //          { field: 'first_name', header: 'First Name' },
        //          { field: 'last_name_prefix', header: 'Prefix' },
        //          { field: 'last_name', header: 'Last Name' }
        //          ],
        //     selectionToggle: false,
        //   filters: {},
        //   selectedUsers: []
        }
    },
    computed: {
        ...mapState('user', ['users', 'user'])
      },
    async created () {
      await this.fetchUsers({})
      this.loading = false
    },
    methods: {
      ...mapActions('user', ['fetchUsers', 'setUser']),
    //   async initialize () {
    //     await this.fetchUsers({})
    //   },
      goToUser (user) {
          console.log(user)
          if (user.id) {
            this.$toast.add({ severity: 'info', summary: 'User Selected', detail: `${user.username}`, life: 3000 })
            this.setUser(user)
            this.$router.push({ name: 'userdetails', params: { id: user.id } })
        }
      }
    }
}
        // AxiosInstance.get('/users/', { headers: { Authorization: `Bearer ${this.$store.state.accessToken}` } })
        // .then(response => {
        //     this.$store.state.users = response.data
        // })
        // .catch(err => {
        //     console.log(err)
        // })
</script>
