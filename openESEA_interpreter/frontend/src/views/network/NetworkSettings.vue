// http://localhost:8081/network/2/settings/

<template>
    <div class="p-px-5" style="width: 500px;">
        <form id="settingsform" v-on:submit.prevent="updateDetails" class="p-grid p-fluid p-text-left p-my-5">
            <div class="p-col-12 p-field p-d-flex p-ai-center p-jc-center p-mb-5">
                <img :src="network.image" alt="Network Image" style="width: 150px; height: 150px; border-radius: 50%;" format="image/jpeg">
                <div class="p-col p-grid p-ml-5">
                    <input id="uploadfile" type="file" accept="image/*" @change="validateImage" hidden />
                    <label for="uploadfile" class="p-col-12 imageupload p-text-center">Change Network Image</label>
                    <div class="">{{file.name}}</div>
                </div>
            </div>
            <div class="p-col-12 p-field">
                <span class="p-float-label">
                    <InputText id="networkname" v-model.trim="network.name" :class="{'p-invalid': !network.name}" class="p-text-italic" />
                    <label for="networkname">Name</label>
                </span>
                <div class="p-error p-text-italic" v-if="!network.name">Name is required.</div>
            </div>
            <div class="p-col-12 p-field">
                <span class="p-float-label">
                    <Textarea id="networkdescription" v-model.trim="network.description" :autoResize="true" rows="3" />
                    <label for="networkdescription">Description</label>
                </span>
            </div>
            <div class="p-col-12 p-d-flex p-ai-center p-jc-between p-mb-2">
                <span>Network Status</span>
                <SelectButton id="ispublic" v-model="network.ispublic" :options="ispublicbool" optionLabel="name" optionValue="value" />
            </div>
            <small class="p-text-italic">*Public Networks are visible to anyone. Explicitly granted access is still required for cetain operations.</small>
        </form>
        <div class="p-col-12 p-d-flex p-jc-between">
            <Button type="submit" form="settingsform" :label="loading? 'Save...' : 'Save Details'" :loading="loading" class="p-button-primary" style="width: 150px;" :disabled="v$.$invalid" />
            <Button label="Delete Network" class="p-button-danger" @click="deleteNetworkDialog = true" />
        </div>

        <Dialog v-model:visible="ispublicDialog" style="width: 450px;" header="Premium Feature" :modal="true" dismissableMask="true">
            <i class="pi pi-star p-mr-3" style="font-size: 1.5rem" />
            <span>Go premium to make your network private!</span>
            <template #footer>
                    <Button label="No thanks" icon="pi pi-times" class="p-button-text" @click="ispublicDialog = false" />
                    <Button label="What's Premium?" icon="pi pi-question" class="p-button-text" @click="ispublicDialog = false" />
            </template>
        </Dialog>

        <Dialog v-if="network" v-model:visible="deleteNetworkDialog" style="width: 450px;" header="Confirm" :modal="true" dismissableMask="true">
            <div class="confirmation-content">
                <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 1.5rem" />
                <span>Are you sure you want to delete <b>{{network.name}}</b></span>
            </div>
            <template #footer>
                <Button label="No" icon="pi pi-times" class="p-button-text" @click="deleteNetworkDialog = false" />
                <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="removeNetwork()" />
            </template>
        </Dialog>
    </div>
</template>

<script>
    import { mapState, mapActions } from 'vuex'
    import { required } from 'vuelidate/lib/validators'
    import useVuelidate from '@vuelidate/core'
    import imageValidator from '../../utils/imageValidator'

    export default {
        data () {
            return {
                loading: false,
                ispublicbool: [
                    { name: 'Public', value: true },
                    { name: 'Private', value: false }
                    ],
                ispublicDialog: false,
                deleteNetworkDialog: false,
                file: false
            }
        },
        computed: {
            ...mapState('network', ['network']),
            ...mapState('authentication', ['currentuser'])
        },
        setup: () => ({ v$: useVuelidate() }),
        validations: {
            network: {
                name: { required },
                description: {}
            }
        },
        created () {
            if (this.network.accesLevel !== 'admin' && this.network.accesLevel !== 'network admin') {
                console.log('You may not change settings!')
                this.$router.push({ name: 'networkoverview', params: { NetworkId: this.network.id } })
            }
        },
        methods: {
            ...mapActions('network', ['fetchNetwork', 'updateNetwork', 'deleteNetwork']),
            async validateImage (e) {
                this.file = await imageValidator(e)
            },
            // Updates Network Settings when the 'Save Details' button has been clicked
            async updateDetails () {
                if (this.v$.network.$invalid) { return }
                this.loading = true
                var formData = new FormData()
                for (var key in this.network) {
                    console.log('>>>', key, this.network[key])
                    if (key !== 'image' && !Array.isArray(this.network[key])) {
                        formData.append(key, this.network[key])
                    }
                }
                if (this.file) {
                    formData.append('image', this.file)
                }
                await this.updateNetwork(formData)
                await this.fetchNetwork({ id: this.$route.params.NetworkId })
                this.loading = false
            },
            async removeNetwork () {
                this.deleteNetworkDialog = false
                await this.deleteNetwork({ id: this.network?.id || 0 })
                this.$toast.add({ severity: 'success', summary: 'Succesful', detail: 'Network Deleted', life: 3000 })
                this.$router.push({ name: 'networks' })
            }
        }
    }
</script>

<style lang="scss" scoped>
    .imageupload {
    background-color: #2196F3;
    color: white;
    padding: 10px;
    border-radius: 5px;
    cursor: pointer;
    }
</style>
