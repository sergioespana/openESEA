// Used by Organisations.vue

<template>
    <form id="organisationform" @submit.prevent="createNewOrganisation" class="p-input-filled p-fluid p-text-left">
        <div class="p-field">
            <label for="name">Name<span style="color:red">*</span></label>
            <InputText id="name" v-model.trim="organisationForm.name" :class="{'p-invalid': v$.organisationForm.name.$error}" />
            <div class="p-error p-text-italic" v-for="error in nameErrors" :key="error">{{ error }}</div>
        </div>
        <div class="p-field">
            <label for="description">Description</label>
            <Textarea id="description" v-model="organisationForm.description" :autoResize="true" rows="3" />
            <div class="p-error p-text-italic" v-for="error in descriptionErrors" :key="error">{{ error }}</div>
        </div>
        <div class="p-field">
            <label for="ispublic">Should this organisation be public? </label>
            <SelectButton id="ispublic" v-model="organisationForm.ispublic" optionLabel="display" optionValue="value" :options="ispublicbool" />
        </div>
        <div class="p-d-flex p-jc-between">
            <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="closeDialog" style="width: 100px" />
            <Button type="submit" form="organisationform" label="Save" icon="pi pi-check" class="p-button-text" :disabled="v$.organisationForm.$error" style="width: 100px" />
        </div>
    </form>
</template>

<script>
    import { mapState, mapActions } from 'vuex'
    import useVuelidate from '@vuelidate/core'
    import { required, maxLength } from 'vuelidate/lib/validators'
    import HandleValidationErrors from '../../utils/HandleValidationErrors'

    export default {
        setup: () => ({ v$: useVuelidate() }),
        data () {
            return {
                ispublicbool: [
                    { display: 'Public', value: true },
                    { display: 'Private', value: false }
                ],
                organisationForm: {
                    name: null,
                    description: '',
                    ispublic: true
                }
            }
        },
        validations: {
            organisationForm: {
                name: { required, maxLength: maxLength(255) },
                description: { maxLength: maxLength(1000) },
                ispublic: { required }
            }
        },
        computed: {
            ...mapState('organisation', ['organisation', 'error']),
            nameErrors () {
                return HandleValidationErrors(this.v$.organisationForm.name, this.error.name)
            }
        },
        created () {
            this.setOrganisation({})
        },
        methods: {
            ...mapActions('organisation', ['setOrganisation', 'createOrganisation']),
            async createNewOrganisation () {
                this.v$.organisationForm.$touch()
                if (this.v$.$invalid) { return }

                await this.createOrganisation({ data: this.organisationForm })
                if (this.organisation?.id) {
                    this.$router.push({ name: 'organisationoverview', params: { OrganisationId: this.organisation.id } })
                }
            },
            closeDialog () {
                this.$emit('closedialog')
            }
        }
    }
</script>
