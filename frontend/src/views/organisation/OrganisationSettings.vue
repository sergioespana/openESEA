<template>
    <div class="p-px-5" style="width: 500px">
        <form id="settingsform" v-on:submit.prevent="updateDetails" class="p-grid p-fluid p-text-left p-my-5">
            <div class="p-col-12 p-field p-d-flex p-ai-center p-jc-center p-mb-5">
                <img :src="organisation.image" alt="Organisation Image" style="width: 150px; height: 150px; border-radius: 50%;" format="image/jpeg">
                <div class="p-col p-grid p-ml-5">
                    <input id="uploadfile" type="file" accept="image/*" @change="validateImage" hidden />
                    <label for="uploadfile" class="p-col-12 imageupload p-text-center">Change Organisation Image</label>
                    <div class="p-col-12">{{file.name}}</div>
                </div>
            </div>
            <div class="p-col-12 p-field">
                <span class="p-float-label">
                     <InputText id="organisationname" v-model.trim="organisation.name" :class="{'p-invalid': !organisation.name}" class="p-text-italic" />
                     <label for="organisationname">Name</label>
                </span>
                <div class="p-error p-text-italic" v-if="!organisation.name">Name is required.</div>
            </div>
            <div class="p-col-12 p-field">
                <span class="p-float-label">
                    <Textarea id="organisationdescription" v-model="organisation.description" class="p-text-italic" :autoResize="true" rows="3" />
                    <label for="organisationdescription">Description</label>
                </span>
            </div>
            <div class="p-col-12 p-d-flex p-ai-center p-jc-between p-mb-2">
                <span>Organisation Status</span>
                <SelectButton id="ispublic" v-model="organisation.ispublic" :options="ispublicbool" optionLabel="name" optionValue="value" />
            </div>
            <small class="p-text-italic">*Public organisations are visible to anyone. Explicitly granted access is still required for certain operations.</small>
        </form>
        <div class="p-col-12 p-d-flex p-jc-between">
            <Button type="submit" form="settingsform" :label="loading? 'Save...' : 'Save Details'" class="p-button-primary" :loading="loading" :disabled="v$.$invalid" style="width: 150px;" />
            <Button label="Delete Organisation" class="p-button-danger" @click="deleteOrganisationDialog = true" />
        </div>
    </div>

    <Dialog v-model:visible="ispublicDialog" :style="{width: '450px'}" header="Premium Feature" :modal="true" :dismissableMask="true">
        <i class="pi pi-star p-mr-3" style="font-size: 1.5rem" />
        <span>Go premium to make your organisation private!</span>
        <template #footer>
            <Button label="No thanks" icon="pi pi-times" class="p-button-text" @click="ispublicDialog = false" />
            <Button label="What's Premium?" icon="pi pi-question" class="p-button-text" @click="ispublicDialog = false" />
        </template>
    </Dialog>

    <Dialog v-if="organisation" v-model:visible="deleteOrganisationDialog" :style="{width: '450px'}" header="Confirm" :modal="true" :dismissableMask="true">
        <div class="confirmation-content">
            <i class="pi pi-exclamation-triangle p-mr-3" style="font-size:1.5rem" />
            <span>Are you sure you want to delete <b>{{organisation.name}}</b>?</span>
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" class="p-button-text" @click="deleteOrganisationDialog = false" />
            <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="removeOrganisation()" />
        </template>
    </Dialog>

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
                deleteOrganisationDialog: false,
                file: false
            }
        },
        computed: {
            ...mapState('organisation', ['organisation'])
        },
        setup: () => ({ v$: useVuelidate() }),
        validations: {
            organisation: {
                name: { required },
                description: {}
            }
        },
        created () {
            if (this.organisation.accesLevel !== 'admin' && this.organisation.accesLevel !== 'organisation admin') {
                console.log('You may not change settings!')
                this.$router.push({ name: 'organisationoverview', params: { OrganisationId: this.organisation.id } })
            }
        },
        methods: {
            ...mapActions('organisation', ['fetchOrganisation', 'updateOrganisation', 'deleteOrganisation']),
            async validateImage (e) {
                this.file = await imageValidator(e)
            },
            async updateDetails () {
                if (this.v$.organisation.$invalid) { return }
                this.loading = true
                console.log('orgg', this.organisation)

                var formData = new FormData()
                formData.append('name', this.organisation.name)
                formData.append('description', this.organisation.description)
                formData.append('ispublic', this.organisation.ispublic)

                if (this.file) {
                    formData.append('image', this.file)
                }
                await this.updateOrganisation(formData)
                await this.fetchOrganisation({ id: this.$route.params.OrganisationId })
                this.loading = false
            },
            async removeOrganisation () {
                this.deleteOrganisationDialog = false
                await this.deleteOrganisation({ id: this.organisation?.id || 0 })
                this.$toast.add({ severity: 'success', summary: 'Succesful', detail: 'Organisation Deleted', life: 3000 })
                this.$router.push({ name: 'organisations' })
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
