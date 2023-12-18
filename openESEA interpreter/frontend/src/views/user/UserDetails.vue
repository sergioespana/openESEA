// http://localhost:8080/users/user_id/

<template>
    <div class="p-grid p-m-0 p-p-0" style="height: 100%;">
        <div class="p-col-fixed p-m-0 p-p-0" style="height: 100%;">
            <!-- <organisation-sidebar :links="links" :name="network.name" @reroute="goToPage"/> -->
            <sub-sidebar :links="links" />
        </div>
        <div class="p-col">
            <div class="p-col-12 p-text-left p-text-italic p-m-0 p-px-5">
            </div>
            <router-view />
        </div>
    </div>
    <!-- <input v-if="usernameedit && editing" v-model="user.username" @focus="usernameedit" @blur="usernameedit=false && console.log('check')" @keyup.enter="usernameedit=false" class="p-col-12 p-inputtext" />
                            <div v-else @click="usernameedit=true">{{user.username}}</div> --> <!--@focusin="true" @focusout="usernameedit=false" -->
    <div class="p-d-flex p-jc-center" style="width: 100%; height: 100%;">
        <div style="width: 100%;">
            <!-- <h1> {{user.username}}'s Profile</h1> -->
            <!-- <Divider /> -->
            <TabView class="p-shadow-2" style="height: 80%;">
                <TabPanel header="Contact Information" style="height: 80%;">'
                    a'
                </TabPanel>
                <TabPanel header="User Settings">
                </TabPanel>
                <TabPanel header="Permissions and Teams">
                </TabPanel>
            </TabView>
            <!-- <form id="userform" v-on:submit.prevent="updateProfile" class="p-grid p-fluid p-p-5" style="width: 1000px">
                <div class="p-col-7 p-grid p-ai-center p-text-left p-p-3">
                        <div class="p-col-6 p-text-bold"> Username </div>
                        <div class="p-col-6">
                            <input id="username" v-if="editablefields.username" v-model="user.username" @blur="editablefields.username=false" @keyup.enter="editablefields.username=false" class="p-inputtext" />
                            <div v-else @click="delayedfocus('username')">{{user.username}}</div>
                            <div class="p-error p-text-italic" v-for="error in usernameErrors" :key="error"><small>{{error}}</small></div>
                        </div>
                        <div class="p-col-6 p-text-bold"> Full name </div>
                        <div class="p-col-6 ">
                            <div v-if="editablefields.fullname">
                            <input id="firstname" v-if="editablefields.fullname" v-model="user.first_name"  @focus="editablefields.fullname=true" placeholder="first name" @blur="editablefields.fullname=false" class="p-inputtext" />
                            <input id="prefix" v-if="editablefields.fullname" v-model="user.last_name_prefix" @focus="editablefields.fullname=true" placeholder="last name prefix" @blur="editablefields.fullname=false" class="p-inputtext" />
                            <input id="lastname" v-if="editablefields.fullname" v-model="user.last_name" @focus="editablefields.fullname=true" placeholder="last name" @blur="editablefields.fullname=false" class="p-inputtext" />
                            </div>
                            <div v-else @click="delayedfocus('fullname')">{{ (user.firstname || user.last_name_prefix || user.last_name) ? `${user.first_name} ${user.last_name_prefix} ${user.last_name}` : 'no name'}}</div>
                        </div>
                        <div class="p-col-6 p-text-bold"> Email </div>
                        <div class="p-col-6">
                            <input id="email" v-if="editablefields.email || emailErrors.length" type="email" v-model="user.email" @blur="editablefields.email=false" @keyup.enter="editablefields.email=false" placeholder="email" class="p-inputtext" :class="{'borderless': emailErrors.length}" />
                            <div v-else @click="delayedfocus('email')">{{user.email}}</div>
                            <div class="p-error p-text-italic" v-for="error in emailErrors" :key="error"><small>{{error}}</small></div>
                        </div>
                        <div class="p-col-6 p-text-bold"> Account Creation </div>
                        <div class="p-col-6"> {{ user?.date_joined?.slice(0, 10) }} </div>
                        <div class="p-col-12" >
                            <div class="p-text-bold p-mb-2" >Bio</div>
                            <textarea id="bio" v-if="editablefields.bio" type="text" rows="5" @blur="editablefields.bio=false" @keyup.enter="editablefields.bio=false" class="p-inputtext" />
                            <div v-else @click="delayedfocus('bio')">
                                Hello this is my Bio! Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                            </div>
                        </div>
                </div>
                <div class="p-col-1"></div>
                <div class="p-col p-grid">
                    <div class="p-col-12">
                        <img class="p-shadow-5" :src="user.image" alt="Profile Avatar" style="max-width: 200px; max-height: 200px; border-radius: 50%;" format="image/jpeg">
                    </div>
                    <div v-if="editing" class="p-grid p-col-12 p-px-5">
                        <input id="uploadfile" type="file" accept="image/*" @change="validateImage" hidden />
                        <label for="uploadfile" class="p-col imageupload p-text-center"> Change your Avatar</label>
                        <div class="p-col-12">{{file.name}}</div>
                    </div>
                </div>
            </form>
            <Divider />
            <div v-if="currentuser === user.username" class="p-d-flex p-jc-start">
                <Button type="submit" form="userform" label="Save Profile" class="p-button-raised p-button-primary p-mr-2" :loading="loading" />
                <Button label="Delete Account" class="p-button-raised p-button-danger" @click="deleteAccountDialog = true" />
            </div> -->
        </div>
    </div>

    <Dialog v-if="user" v-model:visible="deleteAccountDialog" :style="{width: '450px'}" header="Confirm" :modal="true">
        <div class="confirmation-content">
            <i class="pi pi-exclamation-triangle p-mr-3" style="font-size:1.5rem" />
            <span>Are you sure you want to delete the following account: '<b>{{user.username}}</b>'?</span>
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" class="p-button-text" @click="deleteAccountDialog = false" />
            <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="deleteAccount()" />
        </template>
    </Dialog>

</template>

<script>
    import useVuelidate from '@vuelidate/core'
    import { required, minLength, maxLength, email } from 'vuelidate/lib/validators'
    import HandleValidationErrors from '../../utils/HandleValidationErrors'
    import { mapActions, mapState } from 'vuex'
    import imageValidator from '../../utils/imageValidator'
    import SubSidebar from '@/components/SubSidebar'

    export default {
        components: {
            SubSidebar
        },
        data () {
            return {
                deleteAccountDialog: false,
                editing: false,
                activatefocus: false,
                loading: false,
                file: false,
                editablefields: {
                    username: false,
                    fullname: false,
                    email: false,
                    accountcreation: false,
                    bio: false
                    },
                links: [
                    {
                        name: 'Contact Information',
                        icon: 'pi pi-user',
                        path: 'profileoverview'
                    },
                    {
                        name: 'Socials',
                        icon: 'pi pi-comments',
                        path: 'profilesocials'
                    },
                    {
                        name: 'User Settings',
                        icon: 'pi pi-cog',
                        path: 'profilesettings'
                    }
                ]
            }
        },
        computed: {
            ...mapState('user', ['user', 'error']),
            ...mapState('authentication', ['currentuser', 'authenticatedUser']),
            usernameErrors () {
                return HandleValidationErrors(this.v$.user.username, this.error.username)
            },
            emailErrors () {
                return HandleValidationErrors(this.v$.user.email, this.error.email)
            }
        },
        setup: () => ({ v$: useVuelidate() }),
        validations: {
            user: {
                username: { required, minLength: minLength(4), maxLength: maxLength(50) },
                fullname: {},
                email: { email, required }
                // bio: {} Isn't an attribute in the user Model yet (backend).
            }
        },
        async created () {
            await this.fetchUser({ id: this.$route.params.id })
            this.initialize()
        },
        mounted  () {
            /*
                this.$refs.myref.focus()
            */
        },
        methods: {
            ...mapActions('user', ['fetchUser', 'updateUser', 'deleteUser']),
            initialize () {
                if (this.currentuser === this.user.username) {
                    this.editing = true
                }
            },
            async updateProfile () {
                this.v$.user.$touch()
                if (this.v$.user.$invalid) { return }
                this.loading = true
                setTimeout(() => { this.loading = false }, 1000)

                // formData can be used to construct objects to send through a Post Request.
                var formData = new FormData()
                for (var key in this.user) {
                    if (key !== 'image') {
                        if (this.user[key].length) {
                            formData.append(key, this.user[key])
                        }
                    }
                }
                // Add image file to formData object if an image was uploaded.
                if (this.file) {
                    formData.append('image', this.file)
                }
                await this.updateUser(formData)
                await this.fetchUser({ id: this.$route.params.id })
                setTimeout(() => { this.loading = false }, 1000)
            },
            async deleteAccount () {
                if (this.currentuser === this.user.username) {
                    await this.deleteUser({ id: this.user.id })
                    this.$router.push({ name: 'logout' })
                }
            },
            // Used to change an attribute (e.g. bio) to an input field in order for it to be changed.
            delayedfocus (id) {
                if (this.editing) {
                    this.editablefields[`${id}`] = true
                    setTimeout(() => { document.getElementById(`${id}`).focus() }, 50)
                }
            },
            async validateImage (e) {
                this.file = await imageValidator(e)
            }
        }
    }
</script>

<style lang="scss" scoped>
    .p-inputtext {
        border: none;
        border-bottom: 1px solid lightgrey;
    }
    .borderless {
        border-bottom: 1px solid red;

    }
    .imageupload {
    background-color: #2196F3;
    color: white;
    padding: 5px;
    margin: 0px 50px;
    border-radius: 5px;
    cursor: pointer;
    }
</style>

// <div class="p-col-4 p-shadow-1" style="border-style: solid; border-color: #f2f2f2; border-width: thin; opacity: 0.6"></div>
