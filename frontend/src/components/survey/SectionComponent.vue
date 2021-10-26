<template>
<div class="p-p-0">
    <div v-if="item.text" class="p-col-12 p-p-2" style="background-color: #F1F1F1; border: 1px solid #D8D8D8;">
        <p class="p-text-left p-text-bold">{{item.text}}</p>
    </div> <!-- {{requireStatus}} {{item.required}} {{answer}} {{focused}} {{refresh}} -- {{activeField}} active: {{active}} -->
    <div class="p-px-2" v-if="item.direct_indicator" style="background-color: white; border-radius: 5px;" :style="[(active) ? 'border: 1px solid blue;' : 'border: 1px solid lightgrey', (((requireStatus && item.isMandatory) || item.required) && (!active)) ? 'border: 1px solid red' : '', hover ? 'background-color: #F1F1F1;' : '']" @mouseover="hover = true" @mouseleave="hover = false">
        <p class="p-text-left"><span v-if="item.isMandatory" style="color: red; font-size: 25px">*</span>{{item.name}} <i v-if="item.description" class="pi pi-question p-ml-2 p-p-1" v-tooltip="(item?.description && item?.instruction)" style="background-color: green; color: white; border-radius: 50%;" /></p>
       <!-- {{answer}} {{requireStatus}} {{active}} {{item.required}} ?? {{answer}} {{item}} -->
        <answer-input
        :value="answer"
        :uiComponent="item.uiComponent"
        :indicator="item.direct_indicator?.[0]"
        option-value-key="text"
        @input="changeAnswer"
        @focuscheck="fieldFocus"
        />
    </div>
    </div>
</template>
<script>
    import AnswerInput from './AnswerInput'
    import Tooltip from 'primevue/tooltip'

export default {
    directives: {
        tooltip: Tooltip
    },
    components: {
        AnswerInput
    },
    props: {
        item: {
            type: Object,
            required: true
        },
        answer: {
            type: String,
            default: undefined
        },
        active: {
            type: Boolean,
            default: false
        },
        refresh: {
            type: Boolean
        }
    },
    data () {
        return {
            requireStatus: false,
            focused: false,
            hover: false
        }
    },
    computed: {
        someAnswer () {
            return this.answer
        }
    },
    watch: {
        refresh () {
            this.checkRequirementStatus()
        },
        active () {
            this.focused = true
            this.checkRequirementStatus()
        }
    },
    methods: {
        changeAnswer (answer) {
            console.log('====', answer)
            this.$emit('input', { answer: answer })
        },
        checkRequirementStatus () {
            console.log('check Requirements', this.item, this.answer, this.focused)
            if (this.focused && this.item.isMandatory) {
                if (!this.answer?.[0].length && (!this.answer?.[1].length || this.answer?.[1] === null) && !this.item.text) { // === ('' || null))
                    this.requireStatus = true
                } else {
                    this.requireStatus = false
                }
            }
        },
        fieldFocus (val) {
            this.$emit('focuschecking', val)
        }
    }
}
</script>
