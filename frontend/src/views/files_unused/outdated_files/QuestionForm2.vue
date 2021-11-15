<template>
        <form ref="form" class="p-grid p-m-0 p-p-5 p-fluid p-input-filled" :style="[(!v$.lazyQuestion.$invalid && lazyQuestion.id > 0) ? 'border: 1px solid #00695C;': 'border: 1px solid rgba(255, 0, 0, 0.3);']" >

            <div class="p-col-8 p-m-0 p-my-1 p-field">
                <span class="p-float-label">
                    <InputText ref="questionname" id="questionname" type="text" v-model="lazyQuestion.name"  :class="{'borderless': nameErrors.length }"  @blur="v$.lazyQuestion.name.$touch()" :disabled="!active" /> <!-- nameErrors.length -->
                    <label for="questionname">Question</label>
                </span>
                <div class="p-error p-text-italic" v-for="error in nameErrors" :key="error"><small>{{error}}</small></div>
            </div>
            <div class="p-col-4">
                <span class="p-float-label">
                    <Dropdown id="questionuicomponent" v-model="lazyQuestion.uiComponent" :options="uiComponentsList" optionLabel="text" optionValue="value" :class="{'p-invalid': uiComponentErrors.length}" @change="changeUIComponent" :disabled="!active" />
                    <label v-if="active" for="questionuicomponent">Select ui Component...</label>
                </span>
            </div>

            <template v-if="active" class="p-grid p-col-12">

                    <div class="p-col-12 p-m-1 p-field">
                        <span class="p-float-label">
                            <InputText id="questiondescription" type="text" v-model="lazyQuestion.description" :disabled="!active" />
                            <label for="questiondescription">Description</label>
                        </span>
                    </div>

                    <div class="p-col-12 p-m-1 p-field">
                        <span class="p-float-label">
                            <InputText id="questioninstruction" type="text" v-model="lazyQuestion.instruction" :disabled="!active" />
                            <label for="questioninstruction">Instruction</label>
                        </span>
                    </div>

                <Divider />
                <div class="p-col-12 p-d-flex p-ai-center p-jc-end">
                    <Button v-if="!lazyQuestion.direct_indicator.length" label="Add Indicator" class="p-button-outlined p-col" @click="addIndicator" />
                    <div class="p-d-flex p-ai-center p-ml-5"><p class="p-mr-2">Required</p> <InputSwitch v-model="lazyQuestion.isMandatory" style="" /></div>
                    <i class="pi pi-trash p-mx-5" style="font-size: 25px; color: red; cursor: not-allowed;" />
                    <i class="pi pi-ellipsis-v" style="font-size: 25px; cursor: not-allowed;" />
                </div>

                <div v-if="lazyQuestion.direct_indicator.length" class="p-grid p-col-12" :style="[(lazyQuestion.direct_indicator[0].id > 0) ? 'border: 1px solid #00695C;': 'border: 1px solid rgba(255, 0, 0, 0.3);']">
                    <h3 class="p-col-12 p-text-bold p-text-center">Direct Indicator</h3>
                        <div class="p-col-5 p-m-1 p-field">
                            <span class="p-float-label">
                                <InputText id="questionkey" type="text" v-model="lazyQuestion.direct_indicator[0].key"  :class="{'borderless': keyError}"  @blur="questionKeyFilter(lazyQuestion.direct_indicator[0].key)" :disabled="!active" />
                                <label for="questionkey">Question Key</label>
                            </span>
                            <div class="p-error p-text-italic" v-for="error in keyErrors" :key="error"><small>{{error}}</small></div>
                        </div>
                        <div class="p-col-5 p-m-1 p-field">
                            <Dropdown v-model="lazyQuestion.direct_indicator[0].datatype" :options="dataTypesList" optionLabel="text" optionValue="value" placeholder="Select datatype..." :class="{'p-invalid': datatypeError }" @change="changeDataTypeComponent" :disabled="!active" />
                        </div>
                        <Button label="Delete Indicator" class="p-col p-button-danger p-button-text" @click="deleteIndicator" />
                        <div class="p-col-12 p-m-1 p-field">
                            <span class="p-float-label">
                                <InputText id="indicatorname" type="text" v-model="lazyQuestion.direct_indicator[0].name" />
                                <label for="indicatorname">Name</label>
                            </span>
                        </div>
                            <div class="p-col-12 p-m-1 p-field">
                            <span class="p-float-label">
                                <InputText id="indicatordescription" type="text" v-model="lazyQuestion.direct_indicator[0].description" />
                                <label for="indicatordescription">Description</label>
                            </span>
                        </div>
                        <div v-if="lazyQuestion.direct_indicator[0].datatype && !datatypeWithOptions" class="p-col-12 p-grid p-m-0 p-p-0">
                            {{datatypesWithOptions}}
                            <div class="p-col-6">
                                <span class="p-float-label">
                                    <InputText id="pre_unt" type="text" v-model="lazyQuestion.direct_indicator[0].pre_unit" />
                                    <label for="pre_unit">pre unit</label>
                                </span>
                            </div>
                            <div class="p-col-6">
                                <span class="p-float-label">
                                    <InputText id="post_unit" type="text" v-model="lazyQuestion.direct_indicator[0].post_unit" />
                                    <label for="post_unit">post unit</label>
                                </span>
                            </div>
                        </div>
                        <div v-if="lazyQuestion.direct_indicator[0].datatype && datatypeWithOptions" class="p-grid p-col-12 p-mx-0 p-px-0"> <!-- v-if="active && lazyQuestion.direct_indicator[0].options && lazyQuestion.direct_indicator[0].options.length" -->
                            <option-form v-for="(option, index) in lazyQuestion.direct_indicator[0].options" :key="`option-${index}`" :option="option" @delete="deleteOption(option)" />
                            <Button label="Add Option" class="p-button-text" @click="newOption" />
                        </div>
                </div>
            </template>
        </form>
</template>
<script>
import { mapActions, mapGetters } from 'vuex'
import useVuelidate from '@vuelidate/core'
import { DATA_TYPES, UI_COMPONENTS } from '../utils/constants'
import HandleValidationErrors from '../utils/HandleValidationErrors'
import { isEqual, cloneDeep } from 'lodash'
import { required, maxLength } from '../utils/validators'
import Dropdown from 'primevue/dropdown'
import OptionForm from '../../components/forms/OptionForm'
import InputSwitch from 'primevue/inputswitch'

export default {
    components: {
        OptionForm,
        Dropdown,
        InputSwitch
    },
    props: {
        question: {
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
        }
    },
    data () {
        return {
            lazyQuestion: cloneDeep(this.question) || { },
            dataTypes: DATA_TYPES,
            uiComponents: UI_COMPONENTS,
            indicator: false,
            additionalInfo: false,
            keyError: false,
            datatypeError: false,
            requiredList: [{ name: 'Required', value: true }, { name: 'Optional', value: 'false' }]
        }
    },
    computed: {
        ...mapGetters('question', ['getValidQuestionKeyNumber']),
        dataTypesList () {
                // const acceptedDataTypes = this.dataTypes.reduce((result, option) => option.possibleUI.includes(this.lazyQuestion.uiComponent) ? result.concat({ text: option.text, value: option.value }) : result, []) // Object.entries(this.dataTypes).reduce((result, datatype, {includes(datatype.value)}))
                // return acceptedDataTypes
            return this.dataTypes // Object.entries(this.dataTypes).map((element) => ({ text, value }))
        },
        uiComponentsList () {
            if (this.lazyQuestion.direct_indicator?.[0]?.datatype) {
                const acceptedUIComponents = this.uiComponents.reduce((result, option) => option.possibleDataTypes.includes(this.lazyQuestion.direct_indicator[0].datatype) ? result.concat({ text: option.text, value: option.value }) : result, []) // Object.entries(this.dataTypes).reduce((result, datatype, {includes(datatype.value)}))
                console.log(acceptedUIComponents)
                return acceptedUIComponents
            }
            return this.uiComponents // return Object.entries(this.uiComponents).map(([text, value]) => ({ text, value }))
        },
        datatypeWithOptions () {
            let datatypeWithOptions = false
            if (this.lazyQuestion?.direct_indicator?.[0].datatype) {
                const datatypesWithOptions = ['boolean', 'singlechoice', 'multiplechoice']
                datatypeWithOptions = datatypesWithOptions.includes(this.lazyQuestion.direct_indicator[0].datatype)
            }
            return datatypeWithOptions
        },
        keyErrors () {
            // if (this.lazyQuestion.direct_indicator.length) {
            //     console.log('ée;')
            //     for (const v in this.v$.lazyQuestion.direct_indicator.$each?.$iter) {
            //         return HandleValidationErrors(v.key, this.errors.direct_indicator?.[0].key)
            //     }
            // }
            return false
        },
        nameErrors () {
            return HandleValidationErrors(this.v$.lazyQuestion.name, this.errors.name)
        },
        uiComponentErrors () {
            return HandleValidationErrors(this.v$.lazyQuestion.uiComponent, this.errors.uiComponent)
        },
        cssProps () {
            const props = { border: '1px solid lightgrey' }
            if (this.active) {
                props.border = '2px solid #9ecaed'
                props['background-color'] = '#f7f7f7'
            }
            return props
        }
    },
    watch: {
        question (val) {
            // if (val?.direct_indicator?.[0].datatype) {
            //             const datatypesWithOptions = ['boolean', 'singlechoice', 'multiplechoice']
            //             this.datatypeWithOptions = datatypesWithOptions.includes(val.direct_indicator[0].datatype)
            //         }
            if (isEqual(this.lazyQuestion, val)) { return }
            console.log('reee')
            this.lazyQuestion = cloneDeep(val)
        },
        lazyQuestion: {
            handler (val) {
                setTimeout(() => {
                    console.log('refs:', this.$refs)
                if (!this.uiComponentsList.find(element => element.value === this.lazyQuestion.uiComponent)) {
                    this.lazyQuestion.uiComponent = null
                }
                this.v$.lazyQuestion.$touch()
                if (val.direct_indicator.length) {
                    if (!val.direct_indicator[0].key) {
                        this.keyError = true
                        return
                    } else {
                        this.keyError = false
                    }
                    if (!val.direct_indicator[0].datatype) {
                        this.datatypeError = true
                        return
                    } else {
                        this.datatypeError = false
                    }
                }
                if (this.v$.$invalid) { return }
                if (this.lazyQuestion.direct_indicator.length) {
                    if (this.lazyQuestion.direct_indicator?.[0].options.length) {
                        this.lazyQuestion.direct_indicator[0].options.forEach((option, index) => { option.order = index + 1 })
                    }
                }
                // if (val) { return }
                if (isEqual(this.question, val)) { return }
                console.log('+++', val)
                this.$emit('input', val) // cloneDeep(val)
                }, 200)
            },
            deep: true
        },
        active (val) {
            if (!val) {
                console.log('naayyy')
                this.v$.$touch()
            } else {
                console.log('yeay')
                this.$nextTick(() => this.$refs.questionname.$el.focus()) // this.$refs.name &&
            }
        }
    },
    mounted () {
        if (this.lazyQuestion) {
            console.log('empy name')
            this.$refs.questionname.$el.focus()
            // this.$refs.name.focus()
        }
    },
    created () {
    },
    setup: () => ({ v$: useVuelidate() }),
    validations: {
        lazyQuestion: {
            name: { required, maxLength: maxLength(120) },
            uiComponent: { required },
            isMandatory: { required }
            // direct_indicator: {
            //     $each: {
            //         key: { required },git a
            //         datatype: { required }
            //     }
            // }
        }
    },
    methods: {
        ...mapActions('directIndicator', ['deleteDirectIndicator']),
            // if (!this.lazyQuestion.key && !this.lazyQuestion.name) {
            //     this.lazyQuestion.key = `direct_indicator_${this.getValidQuestionKeyNumber}`
            //     this.lazyQuestion.name = `question_${this.getValidQuestionKeyNumber}`
            // }
            // if (!this.lazyQuestion.options) {
            //     this.lazyQuestion.options = []
            // }
        changeUIComponent (e) {
            console.log('dddddd')
            this.v$.lazyQuestion.uiComponent.$touch()
            console.log(e.value)
            const uiComponentsWithOptions = ['dropdown', 'checkbox', 'radiobutton']
            if (uiComponentsWithOptions.includes(e.value)) {
                if (!this.lazyQuestion.direct_indicator.length) {
                    this.addIndicator()
                }
            }
        },
        changeDataTypeComponent (e) {
            // console.log('++', e)
            console.log('dddddd')
            const datatypesWithOptions = ['boolean', 'singlechoice', 'multiplechoice']
            if (!datatypesWithOptions.includes(e.value)) {
                // this.datatypeWithOptions = false
                this.lazyQuestion.direct_indicator[0].options = []
            } else if (!this.lazyQuestion.direct_indicator[0].options.length) {
                this.lazyQuestion.direct_indicator[0].options = [
                    { text: 'Option 1', order: 1 },
                    { text: 'Option 2', order: 2 }
                ]
            }
        },
        addIndicator () {
            this.lazyQuestion.direct_indicator = []
            const baseDirectIndicator = { key: '', name: 'new direct indicator', description: '', isMandatory: '', pre_unit: '', post_unit: '', options: [] }
            this.lazyQuestion.direct_indicator.push(baseDirectIndicator)
        },
        async deleteIndicator () {
            const indicator = this.lazyQuestion.direct_indicator?.[0]
            this.lazyQuestion.direct_indicator = []
            await this.deleteDirectIndicator({ mId: indicator?.method, id: indicator?.id })
        },
        newOption () {
            this.lazyQuestion.direct_indicator[0].options.push({ text: `option ${this.lazyQuestion.direct_indicator[0].options.length + 1}`, order: this.lazyQuestion.direct_indicator[0].options.length + 1 })
        },
        deleteOption (event) {
            if (this.lazyQuestion.direct_indicator[0].options && this.lazyQuestion.direct_indicator[0].options.length > 2) {
                this.lazyQuestion.direct_indicator[0].options = this.lazyQuestion.direct_indicator[0].options.filter(option => option !== event)
            }
        },
        questionKeyFilter (val) {
            console.log(val)
            if (val.includes(' ')) {
                this.lazyQuestion.key = val.replace(' ', '_')
            }
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
<!-- <div v-else class="p-grid p-jc-center p-ai-center p-px-5" :style="cssProps">
    <i class="pi pi-question p-col-1" style="fontSize: 2rem"></i>
    <div class="p-col-11">
    <p><span class="p-text-bold">Question:</span> {{ question.name }}</p>
    <div class="p-d-flex p-jc-between p-mr-5 p-pr-5">
    <p><span class="p-text-bold">Key:</span> {{ question.key }}</p>
    <p><span class="p-text-bold">Type:</span> {{ questionType }}</p>
    </div>
    </div>
    <Divider />
    <div v-if="!question.options.length" class="p-d-flex p-jc-between p-col-10">
        <p v-if="question.min_number"><span class="p-text-bold">Minimum:</span> {{ question.min_number }}</p>
        <p><span class="p-text-bold">Default:</span> {{ question.default }}</p>
        <p v-if="question.max_number"><span class="p-text-bold">Maximum:</span> {{ question.max_number }}</p>
    </div>
    <template v-else>
        <div v-for="(option, index) in question.options" :key="index" class="p-field-checkbox p-col-12">
            <Checkbox :id="index" name="option" :value="text" v-model="ss" />
            <label :for="index"><span class="p-text-bold">Text:</span> '{{option.text}}'<span class="p-text-bold"> - Value:</span> '{{option.value}}'</label>
        </div>
    </template>
</div> -->
<!-- <div v-if="active && lazyQuestion.answertype === 'NUMBER'" class="p-grid p-col-12 p-mx-0 p-px-0">
    <div class="p-col-4">
        <span class="p-float-label">
            <InputText id="minvalue" type="number" v-model="lazyQuestion.min_number" />
            <label for="minvalue">Minimum</label>
        </span>
    </div>
    <div class="p-col-6">
        <span class="p-float-label">
            <InputText id="defaultvalue" type="number" v-model="lazyQuestion.default" />
            <label for="defaultvalue">Default</label>
        </span>
    </div>
    <div class="p-col-6">
        <span class="p-float-label">
            <InputText id="maxvalue" type="number" v-model="lazyQuestion.max_number" />
            <label for="maxvalue"><small>Maximum</small></label>
        </span>
    </div>
</div> -->
<!-- <div class="p-col-4">
    <span class="p-float-label">
        <InputText id="questionkey" type="text" v-model="lazyQuestion.key"  :class="{'borderless': keyErrors.length}"  @blur="questionKeyFilter(lazyQuestion.key)" :disabled="!active" v$.lazyQuestion.name.$touch() />
        <label for="questionkey">Question Key</label>
    </span>
    <div class="p-error p-text-italic" v-for="error in keyErrors" :key="error"><small>{{error}}</small></div>
</div> -->

<!--
            <div class="p-grid p-col-12 p-mx-0 p-px-0 p-field" >
                <div class="p-col-4">
                    <ToggleButton v-model="lazyQuestion.isMandatory" onLabel="Requires Answer" offLabel="Optional Answer" :disabled="!active" />  onIcon="pi pi-check" offIcon="pi pi-times"
                    <span class="p-float-label">
                        <Dropdown id="questionismandatory" v-model="lazyQuestion.isMandatory" :options="requiredList" optionLabel="name" optionValue="value" :class="{'p-invalid': v$.lazyQuestion.isMandatory.$error}" :disabled="!active" />
                        <label for="questionismandatory">Select whether answer is needed...</label>
                    </span>
                </div>
            </div> -->
