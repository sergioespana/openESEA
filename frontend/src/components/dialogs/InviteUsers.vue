<template>
    <div class="p-d-flex p-jc-between p=ai-center p-my-5">
        <span>Select the users that you would like to invite to your team.</span>
        <span class="p-input-icon-left">
            <i class="pi pi-search" /><InputText v-model="search" placeholder="Search Users..." />
        </span>
    </div>
    <DataTable :value="filteredUsers" v-model:selection="selectedRows" :selectionMode="selectionToggle? 'multiple' : 'single'" dataKey="id" :metaKeySelection="false" @row-select="goToUser" showGridlines autoLayout
    :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
    :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

        <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field" />
        <Column header="Actions" headerStyle="width: 10rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
            <template #body="{data}">
                <div class="p-d-flex">
                    <Button label="Invite" class="p-button-info p-button-sm p-mr-2" @click="inviteUser(data)" />
                </div>
            </template>
        </Column>
    </Datatable>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
    props: {
        users: {
            type: Array,
            default: () => []
            }
    },
    data () {
        return {
            columns: [
                { field: 'username', header: 'Username' },
                { field: 'email', header: 'E-mail' },
                { field: 'first_name', header: 'First Name' }
            ],
            search: ''
        }
    },
    computed: {
        ...mapState('network', ['network']),
        filteredUsers () {
            return this.users.filter(user => { return user.username.toLowerCase().includes(this.search.toLowerCase()) })
        }
    },
    // async created () {
    //     await this.fetchUsers({ query: `?excludenetwork=${this.$route.params.NetworkId}` })
    // },
    methods: {
        ...mapActions('user', ['fetchUsers']),
        // ...mapActions('networkTeam', ['createNetworkMember']),
        async inviteUser (data) {
            this.$emit('inviteduser', data)
            // await this.createNetworkMember({ nId: this.$route.params.NetworkId, data: { user: data.id } })
            // this.$emit('closedialog')
        }
    }
}
</script>
