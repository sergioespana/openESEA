// Used by DirectindicatorEditForm.vue

<template>
    <div class="p-grid p-col-12">
        <div class="p-col-1">
            {{ order }}
        </div>
        <div class="p-col-10">
            <InputText id="optiontext" type="text" v-model="lazyOption.text" :class="{'borderless': v$.lazyOption.text.$invalid}" :disabled="disabled" />
        </div>
        <Button v-if="!disabled" icon="pi pi-times" class="p-col p-button-danger p-button-text" @click="deleteOption" />
    </div>
</template>

<script>
    import { required } from '../../utils/validators'
    import useVuelidate from '@vuelidate/core'

    export default {
        props: {
            option: {
                type: Object,
                required: true
            },
            order: {
                type: Number,
                required: true
            },
            disabled: {
                type: Boolean,
                required: true
            }
        },
        data () {
            return {
                lazyOption: this.option
            }
        },
        watch: {
            option (val) {
                this.lazyOption = val
            },
            lazyOption (val) {
                if (this.v$.lazyOption.$invalid) { return }
                if (val !== this.option && val.text && val.value) {
                    this.$emit('update', this.lazyOption)
                }
            }
        },
        setup: () => ({ v$: useVuelidate() }),
        validations: {
            lazyOption: {
                text: { required }
            }
        },
        methods: {
            deleteOption () {
                this.$emit('delete')
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
</style>
