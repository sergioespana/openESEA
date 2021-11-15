<template>
    <!--
        uiComponent: field, line, textBox, checkBox, dropDown, radioButton
        datatype: Text, Integer, Double, Date, Boolean, SingleChoice, MultipleChoice

    -->
    <div class="p-p-0 p-my-3 p-text-left p-d-flex p-ai-center p-fluid p-input-filled">
        <!-- {{lazyValue}} -- {{value}} ++ {{ checkboxvals }} -->
        <span class="p-mr-2"> {{indicator?.pre_unit}} </span>
        <div v-if="uiComponent === 'field'">
            <div v-if="indicator.datatype === 'text'">
                <InputText type="text" v-model="lazyValue" :disabled="readonly" required style="border: none;" @focus="focusedField()" />
            </div>
            <div v-if="indicator.datatype === 'integer'" >
                <InputNumber class="inputnumber" v-model="lazyValue" :disabled="readonly" required style="border: none;" @focus="focusedField()" />
                <!-- <input type="number" step="1" v-model="lazyValue" :disabled="readonly" required /> -->
            </div>
            <div v-if="indicator.datatype === 'double'">
                <InputNumber class="inputnumber" v-model="lazyValue" mode="decimal" :minFractionDigits="2" :maxFractionDigits="5" :disabled="readonly" required style="border: none;" @focus="focusedField()" />
            </div>
            <div v-if="indicator.datatype === 'date'">
                <!-- <input type="date" v-model="lazyValue" :disabled="readonly" required /> -->
                <!-- <InputMask mask="99/99/9999" v-model="lazyValue" placeholder="99/99/9999" slotChar="mm/dd/yyyy" /> -->
                <Calendar id="dateformat" v-model="lazyValue" placeholder="Calendar" appendTo="body" dateFormat="mm-dd-yy" :disabled="readonly" @focus="focusedField()" />
            </div>
        </div>

        <div v-if="uiComponent === 'line'" style="width: 100%;">
            <!-- <input type="text" v-model="lazyValue" :disabled="readonly" required style="width: 100%;" /> -->
            <InputText type="text" v-model="lazyValue" :disabled="readonly" required @focus="focusedField()" />
        </div>

        <Textarea v-if="uiComponent === 'textbox'" id="description" v-model="lazyValue" :disabled="readonly" :autoResize="true" rows="3" @focus="focusedField()" />

        <div v-if="uiComponent === 'radiobutton'">
            <div v-for="(option, index) in indicator.options" :key="`${index}-option`" class="p-field-radiobutton">
                <RadioButton :id="`${index}-option`" name="option" :value="option[optionValueKey]" v-model="lazyValue" :disabled="readonly" required @focus="focusedField()" />
                <label :for="`${index}-option`" class="p-text-left">{{option[optionTextKey]}}</label>
            </div>
        </div>

        <div v-if="uiComponent === 'checkbox'">
            <div v-for="(option, index) in indicator.options" :key="`${index}-option`" class="p-field-checkbox">
                <Checkbox :id="`${index}-option`" name="option" :value="option[optionValueKey]" v-model="lazyValue" :disabled="readonly" required @focus="focusedField()" />
                <label :for="`${index}-option`" class="p-text-left">{{option[optionTextKey]}}</label>
            </div>
        </div>

        <div v-if="uiComponent === 'dropdown'" style="width: 100%;">
            <Dropdown v-model="lazyValue" :options="indicator.options"  optionLabel="text" optionValue="text" placeholder="Select option"  style="width: 100%" @focus="focusedField()" />
        </div>

        <span class="p-ml-2">{{indicator?.post_unit}}</span>
    </div>
</template>

<script>
    // import { QUESTION_TYPES } from '../../utils/constants'
    // import InputMask from 'primevue/inputmask'
    import Calendar from 'primevue/calendar'
    import Dropdown from 'primevue/dropdown'
    import { isEqual } from 'lodash'

    export default {
        model: {
            prop: 'value',
            event: 'input'
        },
        components: {
            Dropdown,
            // InputMask
            Calendar
        },
        props: {
            value: {
                type: [String, Number, Array, Boolean],
                default: null
            },
            // required: {
            //     type: Boolean,
            //     default: false
            // },
            indicator: {
                type: Object,
                default: () => { return { } }
            },
            uiComponent: {
                type: String
            },
            optionTextKey: {
                type: String,
                default: 'text'
            },
            optionValueKey: {
                type: String,
                default: 'value'
            },
            readonly: {
                type: Boolean,
                default: false
            }
        },
        data () {
            return {
                lazyValue: []
            }
        },
        watch: {
            value (val) {
                setTimeout(() => {
                    this.getValues()
                }, 5000)
            },
            lazyValue: {
                handler (val) {
                    setTimeout(() => {
                    console.log('cheeeck', val)
                    if ((val === 'undefined') || (val === this.value)) {
                        console.log('value is undefined or same as this.value')
                        return
                    }

                    if (this.indicator.datatype === 'date') {
                        val.setDate(val.getDate() + 1)
                    }
                    console.log('+++', val)
                    if (!Array.isArray(val)) {
                        this.$emit('input', [val])
                        return
                    }

                    if (typeof (val || val?.[0]) === 'undefined') {
                        return
                    }
                    console.log('--->', val)
                    this.$emit('input', val)
                    }, 1000)
                },
                deep: true
            }
        },
        created () {
            console.log('this vlaue', this.value)
            this.getValues()
        },
        methods: {
            focusedField () {
                this.$emit('focuscheck', true)
            },
            getValues () {
                if (
                    !this.value ||
                    this.value[1] === null ||
                    (!this.value?.[0].length && this.value[1] === '') ||
                    this.value?.[0] === this.lazyValue ||
                    this.value?.[1] === this.lazyValue
                    ) {
                        return
                    }

                if (this.value) {
                    if (this.indicator.datatype === 'text') {
                        if (isEqual(this.lazyValue, this.value?.[1])) { return true }
                        this.lazyValue = this.value?.[1]
                    }
                    if (this.indicator.datatype === 'integer') {
                        if (isEqual(this.lazyValue, parseInt(this.value?.[1]))) { return }
                        this.lazyValue = parseInt(this.value?.[1]) || null
                    }
                    if (this.indicator.datatype === 'double') {
                        if (isEqual(this.lazyValue, parseFloat(this.value?.[1]))) { return }
                        this.lazyValue = parseFloat(this.value?.[1]) || null
                    }
                    if (this.indicator.datatype === 'date') {
                        if (this.value[1].length) {
                            var tempval = new Date(this.value?.[1])
                            }
                        if (isEqual(this.lazyValue, tempval)) { return }
                        console.log(this.lazyValue, tempval)
                        this.lazyValue = tempval || null
                    }
                    const questionWithSingleChoices = ['singlechoice', 'boolean']
                    if (questionWithSingleChoices.includes(this.indicator.datatype)) {
                        if (isEqual(this.lazyValue, this.value?.[1])) { return }
                        console.log(this.lazyValue, this.value?.[1])
                        this.lazyValue = this.value?.[1] || null
                    }
                    if (this.indicator.datatype === 'multiplechoice') {
                        if (isEqual(this.lazyValue, this.value[0])) { return }
                        this.lazyValue = this.value?.[0] || []
                    }
                }
            }
        }
    }
</script>
