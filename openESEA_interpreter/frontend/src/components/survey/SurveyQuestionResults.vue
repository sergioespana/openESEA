<template>
    <div class="p-p-5" style="border-color: #00008B; border: 1px solid lightgrey; border-radius: 5px;">
        <p class="p-text-left">{{ question.name }}</p>
        <Divider class="p-mb-4" />
    <div class="p-p-3 p-pt-5 p-my-3" style="border: 1px solid lightgrey;">
    <div v-if="answertype === questionTypes.RADIO || questionTypes.CHECKBOX">
        <div v-for="(amount, option) in answers" :key="option" class="p-grid p-d-flex p-ai-center p-m-1">
            <div class="p-col-fixed" style="width:80px">
                <div v-if="amountdisplaychoice.value">
                    {{ Math.round(amount / answersum * 100 ) }}%
                </div>
                <div v-else>
                    {{ amount }}
                </div>
            </div>
            <div class="p-col p-text-left p-field-radiobutton p-m-0 p-p-0">
                <RadioButton  v-if="answertype === questionTypes.RADIO" :id="`${index}-option`" name="option" :value="option" :disabled="true" />
                <Checkbox v-if="answertype === questionTypes.CHECKBOX" :id="`${index}-option`" name="option" :value="option" :disabled="true" />
                <label :for="`${index}-option`" class="p-text-left">{{option}}</label>
            </div>
        </div>
    </div>
    <div v-else>
        <div v-for="(amount, value) in answers" :key="value">
            {{amount}}
        </div>
        <p>
            average: {{ average }}
        </p>
    </div>
    </div>
        <div v-if="question.description">
                    <p class="p-text-justify p-text-light p-m-0" style="color: lightgrey;"><small>Description:</small><br>
                    <small><small>{{question.description}}</small></small></p>
        </div>
        <div v-else>
            <p  class="p-text-left p-m-0" style="color: lightgrey;"><small>No Description</small></p>
        </div>
        <div class="p-d-flex p-jc-center">
        <Chart v-if="answertype === questionTypes.RADIO" type="pie" :data="chartData" class="p-col" />
    </div>
        <!-- <Chart v-if="answertype === questionTypes.CHECKBOX" type="bar" :data="chartData" /> -->
    </div>
</template>

<script>
import { QUESTION_TYPES } from '../../utils/constants'
import Chart from 'primevue/chart'
export default {
    components: {
        Chart
    },
    props: {
        question: {
            type: Object,
            required: true
        },
        answers: {
            type: Array,
            default: () => []
        },
        amountdisplaychoice: {
            type: Boolean,
            default: false
        }
    },
    data () {
        return {
            questionTypes: QUESTION_TYPES,
            chartData: {
				labels: [],
				datasets: [
					{
                        label: 'Visualisation',
						data: [],
						backgroundColor: [
                            '#42A5F5',
                            '#66BB6A',
                            '#FFA726',
                            '#26C6DA',
                            '#7E57C2',
                            '#7AC142',
                            '#007CC3',
                            '#00529B',
                            '#377B2B'
                        ],
                        hoverBackgroundColor: [
                            '#64B5F6',
                            '#81C784',
                            '#FFB74D'
                        ]
					}
				]
			}
        }
    },
    computed: {
        answertype () {
            return this.question.answertype
        },
        average () {
            if (!this.answers.length || this.type !== this.questionTypes.NUMBER) {
                return 0
            }
            const total = this.answers.reduce(
                (a, b) => parseInt(a, 10) + parseInt(b, 10), 0)

            return total / this.answers.length
		},
        answersum () {
            var answersum = 0
            for (var key in this.answers) {
                answersum += this.answers[key]
            }
            return answersum
        },
        optionMappedAnswers () {
            console.log(this.answers)
            const optionMappedAnswers = {}
            // if (!this.question.options.length || !this.answers) {
			// 	return optionMappedAnswers
            // }
            // console.log('b')
            // this.question.options.forEach(
			// 	option => (optionMappedAnswers[option.text] = 0)
			// )
			// let allAnswers = []
            // console.log(this.answertype)
			// if (this.answertype === this.questionTypes.CHECKBOX) {
            //     for (var key in this.answers) {
            //         console.log('//')
            //         if (Object.prototype.hasOwnProperty.call(this.answers, key)) {
            //             console.log(key, this.answers[key])
            //         }
            //     }
			// 	this.answers.forEach((answer) => {
            //         console.log('>>', answer)
			// 		const list = answer.split(',')
			// 		allAnswers = [...allAnswers, ...list]
			// 	})
			// } else if (this.answertype === this.questionTypes.RADIO) {
            //     console.log(this.answers)
			// 	allAnswers = this.answers
			// }
			// allAnswers.forEach(answer => (optionMappedAnswers[answer] += 1))
			return Object.entries(optionMappedAnswers)
		}
    },
    created () {
        this.initialize()
    },
    methods: {
        initialize () {
            var i = 0
            for (const key in this.answers) {
                i += i
                if (this.answers[key] > 0) {
                    var val = Math.round(this.answers[key] / this.answersum * 100)
                    if (key.length > 100) {
                        var label = `Label ${key.slice(0, 20)}`
                        this.chartData.labels.push(label)
                    } else {
                        this.chartData.labels.push(key)
                    }
                this.chartData.datasets[0].data.push(val)
                }
            }
            // this.answers.forEach((answer) => {
            //     if (answer[1] > 0) {
            //     var val = Math.round(answer[1] / this.answers.length * 100)
            //     console.log(val)
            //     if (answer[0].length > 100) {
            //         var label = 'A'
            //         this.chartData.labels.push(label)
            //     } else {
            //         this.chartData.labels.push(answer[0])
            //     }
            //     this.chartData.datasets[0].data.push(val)
            //     }
            // })
        },
        changeAnswer (answer) {
            this.$emit('input', answer)
        }
    }
}
</script>

<style scoped>
.p-chart {
    width: 500px;
}
</style>
