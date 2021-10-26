<template>
    <div class="p-d-flex p-ai-center p-m-2" style="width: 100%;">
        <span class="p-mr-2 p-text-bold">IF</span>
        <div class="p-grid p-col p-m-0 p-p-0">
            <div v-for="(expression, index) in if_expressions" :key="expression" class="p-col-12 p-grid p-m-0 p-p-0">
                <expression-form class="p-col-11" />
                <i v-if="index + 1 === if_expressions" class="pi pi-plus p-col-1" @click="addExpression" />
                <Dropdown v-else class="p-p-0 p-col-1" v-model="conditionalChainingChoices[index]" :options="conditionalChainingList" />
            </div>
        </div>
    </div>
    <div class="p-d-flex p-ai-center p-m-2" style="width: 100%;"><span class="p-mr-2 p-text-bold" style="margin-left: 40px; width: 40px;">THEN</span> <expression-form class="p-col" :assignment="true" /></div>
    <div class="p-d-flex p-ai-center p-m-2" style="width: 100%;"><span class="p-mr-2 p-text-bold" style="width: 70px;">ELSE IF </span>
        <div class="p-grid p-col p-m-0 p-p-0">
            <div v-for="(expression, index) in then_expressions" :key="expression" class="p-col-12 p-grid p-m-0 p-p-0">
                <expression-form class="p-col-11" />
                <i v-if="index + 1 === then_expressions" class="pi pi-plus p-col-1" @click="addThenExpression" />
                <Dropdown v-else class="p-p-0 p-col-1" v-model="conditionalChainingChoices[index]" :options="conditionalChainingList" />
            </div>
        </div>
    </div>
     <div class="p-d-flex p-ai-center p-m-2" style="width: 100%;"><span class="p-mr-2 p-text-bold" style="margin-left: 40px; width: 40px;">THEN</span> <expression-form class="p-col" :assignment="true" /></div>
    <div class="p-d-flex p-ai-center p-m-2" style="width: 100%;"><span class="p-mr-2 p-text-bold" style="width: 40px;">ELSE</span> <expression-form class="p-col" :assignment="true" /></div>
<!-- <InputText id="foobar" v-model="formula" placeholder="Write your Formula here." style="width: 100%;" /> -->
    <!-- <div v-if="insideIndicator" style="width: 100%; height: 50px;"><div v-for="indicator in indicatorss" :key="indicator" class="autocomplete-item" style="padding: 2px; border: 1px solid lightgrey; rcursor: pointer;">{{indicator.key}}</div></div></div> THEN </div> -->
    <!-- <Textarea id="description" v-model="formula" :autoResize="true" rows="3" /> -->
</template>

<script>
import formulaProcessor from '@/utils/formulaProcessor'
import ExpressionForm from '@/components/forms/ExpressionForm'
import Dropdown from 'primevue/dropdown'

function autocomplete (inp, arr) {}

var countries = ['Afghanistan', 'Albania', 'Algeria', 'Andorra']
autocomplete(document.getElementById('myInput'), countries)

export default {
    components: {
        ExpressionForm,
        Dropdown
    },
    data () {
        return {
            conditionalChainingList: ['AND', 'OR'],
            if_expressions: 1,
            then_expressions: 1,
            conditionalChainingChoices: [],
            insideIndicator: false,
            formula: 'IF',
            indicatorss: [
                { key: 'indicator_1' },
                { key: 'indicator_2' },
                { key: 'indicator_3' },
                { key: 'indicator_4' }
            ]
        }
    },
    computed: {
        processedFormula () {
            return formulaProcessor(this.formula)
        }
    },
    watch: {
        formula (val) {
            this.insideIndicator = false
            document.getElementById('foobar').addEventListener('keyup', e => {
                let positionleft = null
                let positionright = null
                const userPosition = e.target.selectionStart
                console.log('-->', this.parentNode)
                for (var i = 0; i < userPosition; i++) {
                    if (this.formula[i] === '[') {
                        positionleft = i
                        console.log(positionleft)
                    }
                }
                for (i = userPosition; i <= this.formula.length; i++) {
                    if (this.formula[i] === ']') {
                        positionright = i
                        console.log('dd', positionright)
                    }
                }
                if (positionleft && positionright) {
                    console.log(this.formula.slice(positionleft + 1, positionright))
                    this.showIndicators()
                }
            if (this.formula[e.target.selectionStart - 1] === '[') {
                this.showIndicators()
            }
            console.log('Caret at: ', this.formula[e.target.selectionStart - 1])
            })
            if (val.includes('elsdede')) {
                console.log('A indicator is incoming!')
            } else { console.log('Indicator is not incoming!') }
        }
    },
    methods: {
        showIndicators () {
            this.insideIndicator = true
        },
        addExpression () {
            this.if_expressions++
        },
        addThenExpression () {
            this.then_expressions++
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
.autocomplete-item {
    background-color: white;
}
.autocomplete-item:hover {
    background-color: lightgrey;
}
</style>
