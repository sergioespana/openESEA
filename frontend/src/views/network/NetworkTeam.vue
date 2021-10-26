<template>
     <div class="p-d-flex p-mb-5 p-mx-5" :class="(permission) ? 'p-jc-between' : 'p-jc-end' " style="min-width: 600px;">
        <Button v-if="permission" label="Invite User" icon="pi pi-plus" class="p-button-success p-button-sm p-mr-2" @click="openInviteDialog" />
        <span class="p-input-icon-left">
            <i class="pi pi-search" /><InputText v-model="search" placeholder="Search Team members..." />
        </span>
    </div>
    <Divider />
    <DataTable :value="filteredMembers"  dataKey="id" :loading="loading" selectionMode="single" @row-select="goToUser" showGridlines autoLayout
    :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
    :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

        <template #loading>
            Loading records, please wait...
        </template>
        <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field" />
        <Column header="Actions" headerStyle="width: 10rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
            <template #body="{data}">
                <div v-if="(network?.accesLevel === 'network admin' || network?.accesLevel ==='admin')" class="p-d-flex">
                    <Button label="change" class="p-button-info p-button-sm p-mr-2" @click="changeRole(data)" />
                    <Button label="delete" icon="pi pi-trash" class="p-button-danger p-button-sm" @click="deleteRole(data)" />
                </div>
            </template>
        </Column>
    </Datatable>
    <Button v-if="currentuser" label="leave this network" class="p-button-danger p-button-sm p-mt-5" @click="Nowhere" disabled="true" />

    <Dialog v-model:visible="changeDialog" style="width: 500px" :header="`Change ${member?.user_name}'s role`" :modal="true"  :dismissableMask="true">
        <div class="p-d-flex p-jc-between">
            <Dropdown v-model="member.role" :options="roles" optionLabel="role_name" optionValue="role" placeholder="Select a Role" style="width: 100%;" />
        </div>
        <template #footer>
            <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="changeDialog=false" />
             <Button label="Save Member" icon="pi pi-check" class="p-button-text" @click="updateRole()" />
        </template>
    </Dialog>

    <Dialog v-model:visible="inviteDialog" style="width: 1000px" header="Invite Users" :modal="true" :dismissableMask="true">
        <invite-users :users="users" @inviteduser="inviteUser" />
        <template #footer>
            <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="inviteDialog=false" />
        </template>
    </Dialog>

    <Dialog  v-model:visible="messageDialog" style="width: 500px" :modal="true"  :dismissableMask="true">
        Can't perform this action because this network requires atleast one network admin. Promote someone else before you continue with this action.
    </Dialog>

    <Dialog v-model:visible="deleteDialog" style="width: 500px" header="Confirm Action" :modal="true"  :dismissableMask="true">
            Are you sure you want to remove the following network member?
            <div class="p-shadow-1 p-p-3 p-m-5">{{this.member.user_name}}</div>
        <template #footer>
        <Button label="No" icon="pi pi-times" class="p-button-text" @click="deleteDialog=false" />
        <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="deleteUser()" />
      </template>
    </Dialog>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import InviteUsers from '@/components/dialogs/InviteUsers'
import Dropdown from 'primevue/dropdown'

export default {
    components: {
        InviteUsers,
        Dropdown
    },
    data () {
        return {
            inviteDialog: false,
            changeDialog: false,
            messageDialog: false,
            deleteDialog: false,
            member: null,
            search: '',
            columns: [
                { field: 'user_name', header: 'User' },
                { field: 'role_name', header: 'Role' }
                // { field: 'invitation', header: 'Invitation' }
            ],
            roles: [
                { role_name: 'network admin', role: 2 },
                { role_name: 'guest', role: 1 }
            ]
        }
    },
    computed: {
        ...mapState('authentication', ['currentuser']),
        ...mapState('networkTeam', ['networkmembers']),
        ...mapState('network', ['network']),
        ...mapState('user', ['users']),
        permission () {
            if (this.network.accesLevel) {
                const accesLevel = this.network.accesLevel
                if (accesLevel === 'admin' || accesLevel === 'network admin') {
                    return true
                }
            }
            return false
        },
        filteredMembers () {
            return this.networkmembers.filter(member => {
                return (
                    member.user_name.toLowerCase().includes(this.search.toLowerCase()) ||
                    member.role_name.toLowerCase().includes(this.search.toLowerCase()) ||
                    member.invitation.toLowerCase().includes(this.search.toLowerCase())
                )
            })
        }
    },
    created () {
        this.getData()
    },
    methods: {
        ...mapActions('networkTeam', ['fetchNetworkMembers', 'createNetworkMember', 'updateNetworkMember', 'deleteNetworkMember']),
        ...mapActions('user', ['fetchUsers', 'setUser']),
        ...mapActions('network', ['fetchNetwork']),
        async getData () {
            await this.fetchNetworkMembers({ nId: this.$route.params.NetworkId })
            await this.fetchNetwork({ id: this.$route.params.NetworkId })
        },
        async openInviteDialog () {
            await this.fetchUsers({ query: `?excludenetwork=${this.$route.params.NetworkId}` })
            this.inviteDialog = true
        },
        async inviteUser (data) {
            await this.createNetworkMember({ nId: this.$route.params.NetworkId, data: { user: data.id } })
            this.getData()
            this.inviteDialog = false
        },
        changeRole (data) {
            console.log(data)
            this.member = data
            if (this.checkNetworkAdminCount(data)) {
                this.changeDialog = true
            } else {
                this.messageDialog = true
            }
        },
        checkNetworkAdminCount (data) {
             if (this.networkmembers.filter(element => element.user_name !== data.user_name).find(element => element.role_name === 'network admin')) {
                console.log('===', this.networkmembers.filter(element => element.user_name !== data.user_name).find(element => element.role_name === 'network admin'))
                return true
            }
            return false
        },
        async updateRole () {
            await this.updateNetworkMember({ nId: this.$route.params.NetworkId, id: this.member.id, data: { user: this.member.user, role: this.member.role } })
            this.getData()
            this.changeDialog = false
        },
        deleteRole (data) {
            this.member = data
            this.deleteDialog = true
        },
        async deleteUser () {
            if (this.checkNetworkAdminCount(this.member)) {
                await this.deleteNetworkMember({ nId: this.$route.params.NetworkId, id: this.member.id })
                this.fetchNetwork({ id: this.$route.params.NetworkId })
                this.deleteDialog = false
            } else {
                this.deleteDialog = false
                this.messageDialog = true
            }
        },
        closeInvitationDialog () {
            this.inviteDialog = false
            this.getData()
        },
        async goToUser (user) {
            if (user?.data?.id) {
                await this.setUser(user)
                this.$router.push({ name: 'userdetails', params: { id: user.data.id } })
            }
        }
    }
}
</script>
