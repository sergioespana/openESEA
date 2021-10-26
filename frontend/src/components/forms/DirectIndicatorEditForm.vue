<template>
<div>
    <form v-if="active" ref="form" class="p-grid p-m-3 p-px-5 p-pb-3 p-fluid p-text-left" :style="[(active) ? 'border: 2px solid #9ecaed;': 'border: 1px solid lightgrey;', (valid) ? '': 'border: 2px solid rgba(255, 0, 0, 0.3);', (hover) ? 'background-color: white;':'background-color: #F2F2F2;']" @mouseover="hover=true" @mouseleave="hover=false">
        <!-- {{errors}} {{valid}} {{directIndicator}} {{v$.$invalid}} -->
        <div class="p-d-flex p-col-12">
            <h3 class="p-col p-text-center">Direct Indicator</h3>
            <div class="p-d-flex p-ai-center p-jc-end">
                <i class="pi pi-trash p-mx-5" style="font-size: 30px; color: red; cursor: pointer;" @click="removeIndicator()" />
                <i class="pi pi-ellipsis-v" style="font-size: 30px; cursor: not-allowed;" />
            </div>
        </div>
        <div class="p-col-6 p-field p-my-2">
            <span class="p-float-label">
                <InputText id="indicator-key" type="text" v-model="lazyIndicator.key" :class="{'borderless': v$.lazyIndicator.key.$error}" @blur="v$.lazyIndicator.key.$touch()" :disabled="!active" /> <!--  @blur="questionKeyFilter(lazyIndicator.key)" -->
                <label for="indicator-key">Indicator Key</label>
            </span>
            <div class="p-error p-text-italic" v-for="error in keyErrors" :key="error"><small>{{ error }}</small></div>
        </div>

        <div class="p-col-6 p-field p-my-2">
            <Dropdown v-model="lazyIndicator.datatype" :options="dataTypesList" optionLabel="text" optionValue="value" placeholder="Select Datatype..." :class="{'p-invalid': v$.lazyIndicator.datatype.$error }" :disabled="!active" @change="changeDataTypeComponent" />
        </div>

        <div class="p-col-12 p-field p-my-2">
            <span class="p-float-label">
                <InputText ref="indicatorname" id="indicatorname" type="text" v-model="lazyIndicator.name" :class="{borderless: nameErrors.length }" @blur="v$.lazyIndicator.name.$touch()" :disabled="!active" />
                <label for="indicatorname">Name</label>
            </span>
            <div class="p-error p-text-italic" v-for="error in nameErrors" :key="error"><small>{{ error }}</small></div>
        </div>
        <div v-if="active" class="p-col-12 p-m-0 p-p-0">
            <div class="p-col-12 p-field p-my-2">
                <span class="p-float-label">
                    <InputText id="indicatordescription" type="text" v-model="lazyIndicator.description" />
                    <label for="indicatordescription">Description</label>
                </span>
            </div>

            <div v-if="lazyIndicator.datatype && !datatypeWithOptions" class="p-col-12 p-grid p-m-0 p-p-0">
                <div class="p-col-6 p-field p-my-2">
                    <span class="p-float-label">
                        <InputText id="pre_unit" type="text" v-model="lazyIndicator.pre_unit" />
                        <label for="pre_unit">pre unit</label>
                    </span>
                </div>
                <div class="p-col-6 p-field p-my-2">
                    <span class="p-float-label">
                        <InputText id="post_unit" type="text" v-model="lazyIndicator.post_unit" />
                        <label for="post_unit">post unit</label>
                    </span>
                </div>
            </div>
            <div v-if="lazyIndicator.datatype && datatypeWithOptions" class="p-grid p-col-12 p-m-0 p-p-0" style="border: 1px solid lightgrey;">
                <div class="p-col-1">Order</div>
                <div class="p-col-10 p-text-left">Text</div>
                <Divider />
                <div v-if="(lazyIndicator.datatype === 'boolean')" class="p-col-12">
                    <option-form v-for="(option, index) in lazyIndicator.options" :key="`option-${index}`" :option="option" :order="index+1" :disabled="true" />
                </div>
                <div v-else class="p-col-12">
                    <option-form v-for="(option, index) in lazyIndicator.options" :key="`option-${index}`" :option="option" :order="index+1" @delete="deleteOption(option)" />
                    <Button label="Add Option" class="p-button-text" @click="addOption" />
                </div>
            </div>
        </div>
   </form>
   <indicator-card v-if="!active" :keyy="directIndicator.key" :datatype="directIndicator.datatype" :name="directIndicator.name" :valid="valid" :hover="hover" @mouseover="hover=true" @mouseleave="hover=false" />
   </div>
</template>

<script>
import IndicatorCard from '@/components/cards/IndicatorCard/'
import { isEqual, cloneDeep } from 'lodash'
import HandleValidationErrors from '../../utils/HandleValidationErrors'
import useVuelidate from '@vuelidate/core'
import { required, maxLength } from '@/utils/validators'
import Dropdown from 'primevue/dropdown'
import OptionForm from '@/components/forms/OptionForm'
import { DATA_TYPES } from '@/utils/constants'

export default {
    setup () { return { v$: useVuelidate() } },
    components: {
        IndicatorCard,
        OptionForm,
        Dropdown
    },
    props: {
        directIndicator: {
            type: Object,
            required: true
        },
        active: {
            type: Boolean
        },
        errors: {
            type: Object,
            default: () => ({})
        },
        checkSavingStatus: {
            type: Boolean
        }
    },
    data () {
        return {
            lazyIndicator: cloneDeep(this.directIndicator) || {},
            dataTypes: DATA_TYPES,
            hover: false
        }
    },
    computed: {
        dataTypesList () {
            return this.dataTypes
        },
        datatypeWithOptions () {
            if (this.lazyIndicator.datatype) {
                const datatypesWithOptions = ['boolean', 'singlechoice', 'multiplechoice']
                return datatypesWithOptions.includes(this.lazyIndicator.datatype)
            }
            return false
        },
        keyErrors () {
            return HandleValidationErrors(this.v$.lazyIndicator.key, this.errors.key)
        },
        nameErrors () {
            return HandleValidationErrors(this.v$.lazyIndicator.name, this.errors.name)
        },
        valid () {
            return ((Object.entries(this.errors).length === 0) && !this.v$.lazyIndicator.$invalid && (this.lazyIndicator.id > 0))
        }
    },
    watch: {
        directIndicator: {
            handler (val) {
                if (isEqual(this.lazyIndicator, this.directIndicator)) { return }
                this.lazyIndicator = cloneDeep(val)
            },
            deep: true
        },
        lazyIndicator: {
            handler (val) {
                setTimeout(() => {
                    this.v$.$touch()
                    if (this.v$.$invalid) { return }
                    if (isEqual(this.directIndicator, this.lazyIndicator)) { return }
                    this.$emit('input', val)
                }, 500)
            },
            deep: true
        },
        active () {
            this.v$.$touch()
        },
        checkSavingStatus (val) {
            this.$emit('savingstatus', this.v$.lazyIndicator.$invalid)
        }
    },
    validations: {
        lazyIndicator: {
            key: { required },
            datatype: { required },
            name: { required, maxLength: maxLength(120) }
        }
    },
    methods: {
        changeDataTypeComponent (e) {
            const datatypesWithOptions = ['boolean', 'singlechoice', 'multiplechoice']
            if (!datatypesWithOptions.includes(e.value)) {
                this.lazyIndicator.options = []
            } else if (this.lazyIndicator.datatype === 'boolean') {
                this.lazyIndicator.options = [
                    { text: 'True', order: 1 },
                    { text: 'False', order: 2 }
                ]
            } else if (!this.lazyIndicator.options.length) {
                this.lazyIndicator.options = [
                    { text: '', order: 1 },
                    { text: '', order: 2 }
                ]
            }
        },
        addOption () {
            this.lazyIndicator.options.push({ text: '', order: this.lazyIndicator.options.length + 1 })
            this.sortOptions()
        },
        deleteOption (option) {
            if (this.lazyIndicator.options && this.lazyIndicator.options.length > 2) {
                this.lazyIndicator.options = this.lazyIndicator.options.filter(choice => choice.text !== option.text)
                this.sortOptions()
            }
        },
        sortOptions () {
            this.lazyIndicator.options.forEach((option, index) => { option.order = index + 1 })
            this.lazyIndicator.options = this.lazyIndicator.options.sort(function sortiItems (a, b) {
                return (a.order - b.order)
            })
        },
        removeIndicator () {
            this.$emit('delete', this.directIndicator)
        }
    }

}
// mounted () {
//     if (this.lazyIndicator) {
//         // console.log('-->', this.$refs)
//         //  this.$refs.indicatorname.$el.focus()
//     }
// },
// if (!this.lazyIndicator.key) {
//     this.lazyIndicator.key = `indicator_${this.getValidDirectIndicatorNumber}`
// }
// if (!this.lazyIndicator.name) {
//     this.lazyIndicator.name = `indicator_${this.getValidDirectIndicatorNumber}`
// }
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
