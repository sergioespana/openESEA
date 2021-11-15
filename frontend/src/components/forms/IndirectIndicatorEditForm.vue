// used by MethodIndicatorCreation.vue, MethodTopicCreation.vue

<template>
    <div>
        <form v-if="active" ref="form" class="p-grid p-fluid p-input-filled p-m-3 p-px-5 p-pb-3 p-text-center" :style="[(active) ? 'border: 2px solid #9ecaed;':'border: 1px solid lightgrey;', (valid) ? '':'border: 2px solid rgba(255, 0, 0, 0.3)', (hover) ? 'background-color: white;':'background-color: #F2F2F2;']" @mouseover="hover=true" @mouseleave="hover=false">
            <div class="p-d-flex p-col-12">
                <h3 class="p-col p-text-cente">Indirect Indicator</h3>
                <div class="p-d-flex p-ai-center p-jc-end">
                    <i class="pi pi-trash p-mx-5" style="font-size: 30px; color: red; cursor: pointer;" @click="removeIndicator()" />
                    <i class="pi pi-ellipsis-v" style="font-size: 30px; cursor: not-allowed;" />
                </div>
            </div>
            <div class="p-grid p-col-12 p-mx-0 p-px-0 p-text-left">
                <div class="p-col-4 p-field p-my-2">
                    <span class="p-float-label">
                        <InputText id="calculationkey" ref="keyinput" type="text" v-model="lazyIndirectIndicator.key"  :class="{'borderless': keyErrors.length}" :disabled="!active" />
                        <label for="calculationkey">indicator Key</label>
                    </span>
                    <div class="p-error p-text-italic" v-for="error in keyErrors" :key="error">{{error}}</div>
                </div>
                <div class="p-col-8 p-field p-my-2">
                    <span class="p-float-label">
                        <InputText id="calculationame" type="text" v-model="lazyIndirectIndicator.name" :class="{'borderless': nameErrors.length}" :disabled="!active" />
                        <label for="calculationname">Name</label>
                    </span>
                    <div class="p-error p-text-italic p-pt-1" v-for="error in nameErrors" :key="error">{{error}}</div>
                </div>
            </div>
            <div v-if="active" class="p-col-12 p-field">
                <span class="p-float-label">
                    <InputText id="calculationdescription" type="text" v-model="lazyIndirectIndicator.description" :disabled="!active" />
                    <label for="calculationdescription">Description</label>
                </span>
            </div>

            <div  v-if="active" class="p-col-12">
                <p class="p-mr-3">Formula</p>
                <Divider />
                <formula-form-correct :formula="lazyIndirectIndicator.formula" :keyy="lazyIndirectIndicator.key" @output="updateFormula" />
                <div class="p-error p-text-left p-text-italic p-pt-1" v-for="error in formulaErrors" :key="error">{{error}}</div>
            </div>
        </form>
        <calculation-card v-if="!active" :keyy="indirectIndicator.key" :name="indirectIndicator.name" :formula="indirectIndicator.formula" :valid="valid" :hover="hover" @mouseover="hover=true" @mouseleave="hover=false" />
    </div>
</template>

<script>
    import { mapState, mapGetters } from 'vuex'
    import useVuelidate from '@vuelidate/core'
    import HandleValidationErrors from '../../utils/HandleValidationErrors'
    import { required, maxLength } from '../../utils/validators'
    import { isEqual, cloneDeep } from 'lodash'
    import CalculationCard from '@/components/cards/CalculationCard'
    import FormulaFormCorrect from '@/components/forms/FormulaFormCorrect'

    export default {
        components: {
            FormulaFormCorrect,
            CalculationCard
        },
        props: {
            indirectIndicator: {
                type: Object,
                required: true
            },
            active: {
                type: Boolean,
                default: false
            },
            errors: {
                type: Object,
                default: () => ({})
            },
            checkSavingStatus: {
                type: Boolean
            }
        },
        setup: () => ({ v$: useVuelidate() }),
        validations: {
            lazyIndirectIndicator: {
                key: { required },
                name: { required, maxLength: maxLength(255) },
                formula: { required }
            }
        },
        data () {
            return {
                lazyIndirectIndicator: cloneDeep(this.indirectIndicator) || {},
                hover: false
            }
        },
        computed: {
            ...mapGetters('indirectIndicator', ['getValidIndirectIndicatorNumber']),
            ...mapState('directIndicator', ['directIndicators']),
            ...mapState('indirectIndicator', ['indirectIndicators', 'errors']),
            indicators () {
                const selectableIndirectIndicators = this.indirectIndicators.filter(item => item.id !== this.indirectIndicator.id)
                return this.directIndicators.concat(selectableIndirectIndicators)
            },
            keyErrors () {
                return HandleValidationErrors(
                    this.v$.lazyIndirectIndicator.key,
                    this.errors.key
                )
            },
            nameErrors () {
                return HandleValidationErrors(
                    this.v$.lazyIndirectIndicator.name,
                    this.errors.name
                )
            },
            formulaErrors () {
                return HandleValidationErrors(
                    this.v$.lazyIndirectIndicator.formula,
                    this.errors.formula
                )
            },
            valid () {
                return (!this.v$.lazyIndirectIndicator.$invalid && (this.lazyIndirectIndicator.id > 0))
            }
        },
        watch: {
            indirectIndicator: {
                handler (val) {
                    if (isEqual(this.lazyIndirectIndicator, val)) { return }
                    this.lazyIndirectIndicator = cloneDeep(val)
                },
                deep: true
            },
            lazyIndirectIndicator: {
                handler (val) {
                    setTimeout(() => {
                    this.v$.lazyIndirectIndicator.$touch()
                    if (this.v$.lazyIndirectIndicator.$invalid) { return }
                    if (isEqual(this.indirectIndicator, val)) { return }
                    this.$emit('input', val)
                    }, 500)
                },
                deep: true
            },
            active () {
                this.v$.lazyIndirectIndicator.$touch()
            },
            checkSavingStatus (val) {
                this.$emit('savingstatus', this.v$.lazyIndirectIndicator.$invalid)
            }
        },
        methods: {
            removeIndicator () {
                this.$emit('delete', this.indirectIndicator)
            },
            updateFormula (formula) {
                this.v$.lazyIndirectIndicator.formula.$touch()
                this.lazyIndirectIndicator.formula = formula
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
