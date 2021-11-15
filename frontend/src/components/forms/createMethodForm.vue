// Used by MethodCreation.vue

<template>
    <form id="methodform" @submit.prevent="createNewMethod" class="p-input-filled p-fluid p-text-left">
        <div class="p-field">
            <label for="name">Name<span style="color:red">*</span></label>
            <InputText id="name" v-model.trim="methodForm.name" :class="{'p-invalid': v$.methodForm.name.$error}" />
            <div class="p-error p-text-italic" v-for="error in nameErrors" :key="error">{{ error }}</div>
        </div>
        <div class="p-field">
            <label for="description">Description</label>
            <Textarea id="description" v-model="methodForm.description" :autoResize="true" rows="3" />
            <div class="p-error p-text-italic" v-for="error in descriptionErrors" :key="error">{{ error }}</div>
        </div>
        <div class="p-field">
            <label for="ispublic">Should this method be public? </label>
            <SelectButton id="ispublic" v-model="methodForm.ispublic" :options="ispublicbool" />
        </div>
        <div class="p-d-flex p-jc-between">
            <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="closeDialog" style="width: 100px" />
            <Button type="submit" form="methodform" label="Save" icon="pi pi-check" class="p-button-text" :disabled="v$.methodForm.$error" style="width: 100px" />
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
            ispublicbool: [true, false],
            methodForm: {
                name: null,
                description: '',
                ispublic: true
            }
        }
    },
    validations: {
        methodForm: {
            name: { required, maxLength: maxLength(255) },
            description: { maxLength: maxLength(1000) },
            ispublic: { required }
        }
    },
    computed: {
        ...mapState('method', ['method', 'error']),
        nameErrors () {
            return HandleValidationErrors(this.v$.methodForm.name, this.error.name)
        }
    },
    created () {
        this.initialize()
    },
    methods: {
        ...mapActions('method', ['setMethod', 'createMethod']),
        async initialize () {
            this.setMethod({})
        },
        async createNewMethod () {
            this.v$.methodForm.$touch()
            if (this.v$.$invalid) { return }

            await this.createMethod({ data: this.methodForm })

            if (this.method?.id) {
                this.$router.push({ name: 'method-create', params: { id: this.method?.id || 0 } })
            }
        },
        closeDialog () {
            this.$emit('closedialog')
        }
    }
}
</script>
