<template>
<div class="p-px-5" style="border-color: #00008B; border-radius: 5px;" :style="[(checkanswerrequired && (requiredBorder || requiredStatus)) ? 'border: 1px solid red': 'border: 1px solid lightgrey', (active && !requiredBorder) ? 'border: 1px solid green' : '']">
            <p class="p-text-left"><span v-if="checkanswerrequired" style="color: red; font-size: 25px">*</span>{{question.name}} <i v-if="question.description" class="pi pi-question p-ml-2 p-p-1" v-tooltip="question?.description" style="background-color: green; color: white; border-radius: 50%;" /></p>
            <answer-input
            :value="answer || question.default"
            :type="question.answertype"
            :uiComponent="question.uiComponent"
            :indicator="question.direct_indicator[0]"
            :options="question.direct_indicator[0].options"
            :readonly="readonly"
            :checkanswerrequired="checkanswerrequired"
            option-value-key="text"
            required
            @input="changeAnswer"
            />
            {{question.required}}
            -- {{foo}} >>
            {{requiredQuestion}}
            <!-- <div v-if="question.description">
                <p class="p-text-justify p-text-italic p-text-light p-m-0" style="color: grey;"><span class="p-text-bold">Description:</span><br>
                <small>{{question.description}}</small></p>
            </div>
            <div v-else>
                <p class="p-text-left p-m-0" style="color: lightgrey;"><small>No Description</small>
                </p></div> -->
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
        question: {
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
        readonly: {
            type: Boolean,
            default: false
        },
        checkanswerrequired: {
            type: Boolean,
            default: false
        },
        checkrequiredfields: {
            type: Boolean
        }
    },
    data () {
        return {
            requiredBorder: false,
            requiredStatus: false,
            requiredQuestion: false
        }
    },
    computed: {
        primaryBorder () {
            return { 'border-color': '#00008B' }
        },
        foo () {
            return this.question.required
        }
        // goodanswer () {
        //     console.log(this.answer)
        //     if (this.question.answertype === ('RADIO' || 'CHECKBOX')) {
        //         return this.answer[0]
        //     }
        //     return this.answer[1]
        // }
    },
    watch: {
        checkrequiredfields () {
            this.requiredStatus = this.checkrequiredfields
        },
        foo (val) {
            console.log('this question is required')
            this.requiredQuestion = val
        }
    },
    methods: {
        changeAnswer (answer) {
            this.requiredQuestion = false
            console.log('eee')
            if (!answer.length || answer[0] === null) {
                this.requiredBorder = true
            } else {
                this.requiredBorder = false
                this.requiredStatus = false
            }
            this.$emit('input', { answer: answer, answertype: this.question.answertype })
        }
    }
}
</script>
