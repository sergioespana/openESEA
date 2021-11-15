// Used by MethodCreation.vue

<template>
    <form ref="form"  class="p-fluid p-p-5 p-input-filled p-inputtext-lg">
        <div class=" p-mb-5">
            <span class="p-float-label">
                <InputText id="methodname" type="text" v-model="lazyMethod.name"  :class="{'borderless': nameErrors.length}" @blur="v$.lazyMethod.name.$touch()"  />
                <label for="methodname"><span class="p-text-bold" style="font-size: 18px;">Method Name</span></label>
            </span>
            <div class="p-error p-text-italic" v-for="error in nameErrors" :key="error">{{error}}</div>
        </div>
        <div>
            <span class="p-float-label">
                <InputText id="methoddescription" type="text" v-model="lazyMethod.description" :class="{'borderless': descriptionErrors.length}" @blur="this.v$.lazyMethod.description.$touch()" />
                <label for="methoddescription"><span class="p-text-bold" style="font-size: 16px;">Method Description</span></label>
            </span>
            <div class="p-error p-text-italic" v-for="error in descriptionErrors" :key="error">{{error}}</div>
        </div>
    </form>
</template>

<script>
    import { isEqual } from 'lodash'
    import useVuelidate from '@vuelidate/core'
    import { required, minLength, maxLength } from '../../utils/validators'
    import HandleValidationErrors from '../../utils/HandleValidationErrors'

    export default {
        props: {
            method: {
                type: Object,
                default: () => ({})
            },
            errors: {
                type: Object,
                default: () => ({})
            }
        },
        data () {
            return {
                lazyMethod: { ...this.method } || {}
            }
        },
        computed: {
            nameErrors () {
                return HandleValidationErrors(
                    this.v$.lazyMethod.name,
                    this.errors.name
                    )
            },
            descriptionErrors () {
                return HandleValidationErrors(
                    this.v$.lazyMethod.description,
                    this.errors.description
                )
            }
        },
        watch: {
            method (val) {
                if (!isEqual(this.lazyMethod, val)) {
                    this.lazyMethod = { ...val }
                }
            },
            lazyMethod: {
                handler (val) {
                    if (this.v$.lazyMethod.$invalid) { return }
                    if (isEqual(this.method && val)) { return }
                    this.$emit('input', this.lazyMethod)
                },
                deep: true,   
            }
        },
        setup: () => ({ v$: useVuelidate() }),
        validations: {
            lazyMethod: {
                id: { required },
                name: { required, minLength: minLength(2), maxLength: maxLength(255) },
                description: { required }
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
