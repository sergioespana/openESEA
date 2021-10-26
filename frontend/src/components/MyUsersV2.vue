<template>
    <div class="p-d-flex p-jc-between p-m-5" style="min-width: 600px;">
        <Button label="Send Message" icon="pi pi-plus" class="p-button-success p-mr-2" @click="messageDialog = true" :disabled="!users.length" />
        <span class="p-input-icon-left">
            <i class="pi pi-search" /><InputText v-model="search" placeholder="Search user by name or email..." style="width: 300px;" />
        </span>
    </div>
    <Divider />
    <div class="p-grid p-m-5">
        <div v-for="user in filteredList" :key="user.id" class="p-col-12 p-md-6 p-lg-4" style="width: 220px; height: auto;">
            <div class="p-p-3" :class="user.hover ? 'p-shadow-1 p-m-0' : 'p-m-0'" :style="(user.hover ? styleObject: '')" @mouseover="user.hover = true" @mouseleave="user.hover = false" @click="goToUser(user)">
                <img :src="user.image" alt="Profile Avatar" style="max-width: 100px; max-height: 100px; border-radius: 50%;" format="PNG">
                <p class="p-text-italic">{{user.username}}</p>
                 <!-- {{user.first_name || 'first_name'}} {{user.last_name_prefix}} {{user.last_name_prefix || 'last_name'}} -->
            </div>
        </div>
    </div>

     <Dialog v-model:visible="messageDialog"  modal="true" header="Send Message" :dismissableMask="true" class="p-fluid">
         <div class="p-field">
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
                    <Textarea id="message" v-model="something" required="true" rows="3" cols="20" />
        </div>
        <template #footer>
                <Button label="Send Message" icon="pi pi-plus" @click="SendMessage()"/>
                <Button label="Cancel" icon="pi pi-check" class="p-button-text" @click="messageDialog = false" />
        </template>
    </Dialog>
</template>
<script>
import { mapActions, mapState } from 'vuex'
import MultiSelect from 'primevue/multiselect'

export default {
    components: {
        MultiSelect
    },
    data () {
        return {
            search: '',
            messageDialog: false,
            usersToMessage: []
        }
    },
    computed: {
        ...mapState('user', ['users']),
        filteredList () {
            return this.users.filter(user => { return user.username.toLowerCase().includes(this.search.toLowerCase()) })
        }
    },
    created () {
        this.initialize()
    },
    methods: {
        ...mapActions('user', ['fetchUsers', 'setUser']),
        async initialize () {
            await this.fetchUsers({})
        },
        sendMessage () {
            // send message
        },
        async goToUser (user) {
            await this.setUser({ ...user })
            console.log(user)
            this.$router.push({ name: 'userdetails', params: { id: user.id } })
        }
    }
}
</script>
