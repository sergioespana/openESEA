// used by Users.vue

<template>
    <list-bar v-model:tabledisplay="tableDisplay" v-model:allitems="allOrganisations" :includecheckbox="false" v-model:search="customSearch" name="Organisations">
        <slot></slot>
    </list-bar>
    <ProgressSpinner v-if="loading && !failedLoad" />
    <div v-else-if="loading && failedLoad" class="p-text-italic">Users could not be retrieved!</div>
    <div v-else-if="users.length">
        <div v-if="tableDisplay" class="p-grid p-m-5">
            <div v-for="user in filteredUsers" :key="user.id" class="p-col-12 p-md-6 p-lg-4" style="width: 220px; height: auto;">
                <div class="p-p-3" :class="user.hover ? 'p-shadow-1 p-m-0' : 'p-m-0'" :style="(user.hover ? styleObject: '')" @mouseover="user.hover = true" @mouseleave="user.hover = false" @click="goToUser(user)">
                    <img :src="user.image" alt="Profile Avatar" style="max-width: 100px; max-height: 100px; border-radius: 50%;" format="PNG">
                    <p class="p-text-italic">{{user.username}}</p>
                </div>
            </div>
        </div>
         <DataTable v-else :value="filteredUsers" v-model:selection="selectedRows" :selectionMode="selectionToggle? 'multiple' : 'single'" dataKey="id" :metaKeySelection="false" @row-select="goToUser" showGridlines autoLayout
        :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

            <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field" />
            <Column header="Full Name" headerStyle="width: 15rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                <template #body="{data}">
                        {{data.first_name}} {{data.last_name_prefix}} {{data.last_name}}
                </template>
            </Column>
        </Datatable>
    </div>
</template>

<script>
    import ProgressSpinner from 'primevue/progressspinner'
    import ListBar from '@/components/lists/ListBar'

    export default {
        components: {
            ProgressSpinner,
            ListBar
        },
        props: {
            users: {
                type: Array,
                default: () => []
            },
            loading: {
                type: Boolean,
                default: false
            }
        },
        data () {
            return {
                tableDisplay: false,
                customSearch: '',
                // loading: true,
                failedLoad: false,
                allOrganisations: false,
                styleObject: { backgroundColor: '#EFEEEE', cursor: 'pointer' },
                columns: [
                    { field: 'username', header: 'Username' },
                    { field: 'email', header: 'E-mail' }
                ]
            }
        },
        computed: {
            filteredUsers () {
                return this.users.filter(user => { return user.username.toLowerCase().includes(this.customSearch.toLowerCase()) })
            }
        },
        created () {
            setTimeout(() => { this.failedLoad = true }, 10000)
        },
        methods: {
            goToUser (user) {
                if (user?.data) {
                    user = user.data
                }
                this.$emit('clicked-user', user)
            }
        }
    }
</script>
