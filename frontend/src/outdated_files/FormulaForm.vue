<template>
    <div>
        <!-- {{ formula}} - {{openItem}} -->

        <div v-if="(type === 'Average' || type === 'Sum')" class="p-d-flex p-ai-center p-ml-5">
            <span v-if="type === 'Average'">Average of</span><span v-if="type === 'Sum'">Sum of</span>
            <Dropdown id="questionuicomponent" class="p-ml-2" v-model="indicator" :options="indicatorList" placeholder="Select Indicator"  />
        </div>
        <div id="conditionals" v-if="type === 'Conditionals'" class="p-text-bold" style="font-size: 20px;">
            {{formulastring}}
            <div v-for="(key, idx) in formula" :key="idx">
                <div v-if="(key.type === 'if')">
                    <div class="p-d-flex p-ai-start p-m-2">
                        <span class="p-mt-3">If</span>
                        <div style="display: flex; flex-wrap: wrap;">
                            <div v-for="(component) in key.value" :key="component.name" class="p-d-flex p-ai-center">
                                <div :id="component.name" v-if="component.name.startsWith('operator')">
                                    <Dropdown v-if="openItem[component.name]" class="p-p-0" v-model="component.val" :options="conditionalChainingList"  style="width: 70px;" />
                                    <div v-else :id="component.name" >{{component.val}}</div>
                                </div>
                                <conditional-form v-if="component.name.startsWith('constraint')" :mykey="component.name" :index="idx" @delete="removeConstraint"> </conditional-form>
                            </div>
                        </div>
                        <i class="pi pi-plus Icon p-mt-2" style="color: grey;" @click="addConditional(idx)"/>
                    </div>
                    <div v-if="(key.then)" class="p-d-flex p-ai-start p-m-2">
                        <div :id="key.then">
                            <Dropdown  v-if="openItem[key.then]" class="p-m-2" v-model="key.then.type" :options="thenChoices" placeholder="Select option" @change="changeThenSection(idx)" style="height: 40px;" />
                            <div v-else :id="key.then" class="p-mt-3">{{ (key.then.type === 'Assignment') ? 'then': 'then'}}</div>
                        </div>
                        <conditional-form v-if="key.then?.type === 'Assignment'" assignment="assignment" :indicator="indicatorkey" @update="updateFormula()" />
                        <div v-if="key.then?.type === 'nested if statement'">
                            <div class="p-d-flex p-ai-start p-mx-2">
                                <span style="" class="p-mt-3">If</span>
                                <div style="display: flex; flex-wrap: wrap;">
                                    <div v-for="(component) in key.then.value" :key="component.name" class="p-d-flex p-ai-center">
                                        <div :id="component.name" v-if="component.name.startsWith('operator')">
                                            <Dropdown v-if="openItem[component.name]" class="p-p-0" v-model="component.val" :options="conditionalChainingList"  style="width: 70px;" />
                                            <div v-else :id="component.name" >{{component.val}}</div>
                                        </div>
                                        <conditional-form v-if="component.name.startsWith('constraint')" :mykey="component.name" :index="idx" :nested="true" @delete="removeConstraint"> </conditional-form>
                                    </div>
                                </div>
                                <i class="pi pi-plus Icon p-mt-2" style="color: grey;" @click="addNestedConditional(idx)"/>
                            </div>
                            <div v-if="(key.then.then)" class="p-d-flex p-ai-center p-m-2">
                                <span style="width: 60px;">Then</span>
                                <conditional-form v-if="key.then.then.type === 'Assignment'" assignment="assignment" :indicator="indicatorkey" />
                            </div>
                            <div v-if="(key.then.else)" class="p-d-flex p-ai-center p-m-2">
                                <span style="width: 60px;">Else</span>
                                <conditional-form v-if="key.then.else.type === 'Assignment'" assignment="assignment" :indicator="indicatorkey" />
                            </div>
                        </div>
                    </div>
                    <i class="pi pi-trash Icon p-text-right" style="width: 100%; font-size: 30px;" @click="deleteConditional(idx)"/>
                    <Divider />
                </div>
                <div v-if="(key.type === 'else')">
                    <Button label="Add If Statement" class="p-button-outlined" @click="addIfStatement" />

                    <div class="p-d-flex p-ai-center p-m-2">
                     <span style="width: 60px;">Else</span>
                        <conditional-form assignment="assignment" :indicator="indicatorkey" />
                    </div>
                </div>
            </div>
<!--
-->
            <!-- <div id="check" class="p-d-flex p-ai-center p-m-2">
                <span style="width: 60px;">If</span>
                <div style="display: flex; flex-wrap: wrap;">
                    <div v-for="(key, index) in formula[0].if" :key="key.name" class="p-d-flex p-ai-center p-my-2">
                        <div :id="key.name" v-if="key.name.startsWith('operator')">
                            <Dropdown v-if="openItem[key.name]" class="p-p-0" v-model="formula[0].if[index].val" :options="conditionalChainingList"  style="width: 70px;" />
                            <div v-else :id="key.name" >{{formula[0].if[index].val}}</div>
                        </div>
                        <conditional-form v-if="key.name.startsWith('constraint')" :mykey="key.name" @delete="removeConstraint"> </conditional-form>
                    </div>
                </div>
                <i class="p-col pi pi-plus Icon" style="color: grey;" @click="add"/>
            </div>
            <div id="then" class="p-d-flex p-ai-center p-m-2" style="width: fit-content;">
                <span  style="width: 60px;">Then</span>
                <Dropdown id="thenoption" class="p-m-2" v-model="then" :options="thenChoices" placeholder="Select option"  />
                <div id="innerconditional" v-if="then === 'nested if statement'">
                    <div id="check" class="p-d-flex p-ai-center p-m-2">
                        <span style="width: 60px;">If</span>
                        <div style="display: flex; flex-wrap: wrap;">
                            <div v-for="(key, index) in formula[1].then[0].if" :key="key.name" class="p-d-flex p-ai-center p-my-2">
                                <div :id="key.name" v-if="key.name.startsWith('operator')">
                                    <Dropdown v-if="openItem[key.name]" class="p-p-0" v-model="formula[1].then[0].if[index].val" :options="conditionalChainingList"  style="width: 70px;" />
                                    <div v-else :id="key.name" >{{formula[1].then[0].if[index].val}}</div>
                                </div>
                                <conditional-form v-if="key.name.startsWith('constraint')" :mykey="key.name" @delete="removeConstraint"> </conditional-form>
                            </div>
                        </div>
                        <i class="p-col pi pi-plus Icon" style="color: grey;" @click="addConditional()"/>
                    </div>
                    </div>
                <div style="display: flex; flex-wrap: wrap;">
                    <conditional-form v-if="then === 'Assignment'" assignment="assignment" :indicator="indicatorkey" />
                    <Dropdown v-if="false" v-model="formula[0].if[`operator_${val}`]" :options="conditionalChainingList" style="width:70px;" @blur="formulaEditableFields.operator = false"/>
                </div>
                <i class="pi pi-plus Icon" style="color: grey;"/>
                <div v-if="(formulaEditableFields.first_then || !formulaFields.first_then.indicator_value.assigned_value)" class="p-d-flex p-ai-center conditional"  @mouseleave="formulaEditableFields.first_then=false">
                    <span class="p-mr-2">{{indicatorkey}} = </span>
                    <InputText type="text" v-model="formulaFields.first_then.indicator_value.assigned_value" style="width: 150px;" />
                    <i class="pi pi-times Icon" @click="addConditional()"/>
                </div>
                <div v-else class="conditional" @click="formulaEditableFields.first_then=true">{{indicatorkey}} = {{formulaFields.first_then.indicator_value.assigned_value}}</div> @click="formulaEditableFields.operator = true"
            </div>
            <div class="p-d-flex p-ai-center p-m-2" style="width: fit-content;">
                <span  style="width: 60px;">Else</span>
                <conditional-form assignment="assignment" :indicator="indicatorkey" />
            </div> -->
            <!-- <input id="first_if" v-if="formulaEditableFields.first_if" v-model="formulaFields.first_if" @blur="formulaEditableFields.first_if=false" @keyup.enter="formulaEditableFields.first_if=false" class="p-inputtext" /> -->
            <!-- <div @click="delayedfocus('first_if')">{{formulaFields.first_if}}</div> @blur="formulaEditableFields.operator = false"  @keyup="formulaEditableFields.operator=false" -->
        </div>
    </div>
</template>
//:class="{'p-invalid': uiComponentErrors.length}" @change="changeUIComponent" :disabled="!active"

<script>
import ConditionalForm from '@/components/forms/ConditionalForm'
import Dropdown from 'primevue/dropdown'
import buildFormula from '@/utils/buildFormula'

export default {
    components: {
        ConditionalForm,
        Dropdown
    },
    props: {
        type: {
            type: String
        },
        indicatorkey: {
            type: String
        }
    },
    data () {
        return {
            OperatorsList: ['<', '<=', '=', '!=', '>', '>='],
            conditionalChainingList: ['AND', 'OR'],
            thenChoices: ['Assignment', 'nested if statement'],
            then: null,
            indicator: null,
            indicatorList: ['Indicator 1', 'Indicator 2', 'Indicator 3', 'Indicator 4'],
            formulaEditableFields: { first_if: true, operator: false, first_then: false },
            openItem: {},
            test: {},
            formula: [
                { type: 'if', value: [{ name: 'constraint_0', val: true }], then: { type: 'Assignment', value: [{ name: 'assignment_1', val: true }] } }, // then: { type: 'nested if statement', value: [{ name: 'constraint_0', val: true }]}
                { type: 'then', value: [{ if: [{ name: 'constraint_0', val: true }] }, { then: null }, { else: null }] }, // then: { assignment: { name: 'assignment_1', val: true } }
                { type: 'else', value: { assignment: { name: 'assignment_1', val: true } } }
                // { else if: [{ name: 'constraint_0', val: true }] },
                // then: { assignment: { name: 'assignment_1', val: true } }
                ]
            // formulaFields: { first_if: { first_statement: { left_side: 'indicator 1', operator: '<', right_side: 10 } }, first_then: { indicator_value: { assigned_value: null } } }
        }
    },
    computed: {
        formulastring () {
            return buildFormula(this.formula)
        }
    },
    mounted () {
        var self = this
        document.addEventListener('click', function (event) {
            console.log(event.target)
            if (event.target.id) {
            console.log('event:', event.target.id)
            self.openItem = {}
            self.openItem[event.target.id] = true
            }
            console.log('hello', this.openItem)
        })
        // window.clickOutSide = (element, clickOutside, clickInside) => {
        //     document.addEventListener('click', (event) => {
        //     if (!element.contains(event.target)) {
        //     if (typeof clickInside === 'function') {
        //         clickOutside()
        //     }
        //     } else {
        //     if (typeof clickInside === 'function') {
        //         clickInside()
        //     }
        //     }
        // })
        // }
        // window.clickOutSide(document.querySelector('.block'), () => alert('clicked outside'), () => alert('clicked inside'))
    },
    methods: {
        delayedfocus (id) {
            this.editablefields[`${id}`] = true
            setTimeout(() => { document.getElementById(`${id}`).focus() }, 50)
        },
        addConditional (index) {
            let val = this.formula[index].value.length
            if (val !== 0) {
                const correctionval = -Math.round(-(val / 2))
                val = val - correctionval
                const arrayOfNumbers = []
                for (const component of this.formula[0].value || []) {
                    arrayOfNumbers.push(parseInt(component.name.slice(-1)))
                }

                while (arrayOfNumbers.includes(val)) {
                    val = val + 1
                }

                this.formula[index].value.push({ name: `operator_${val}`, val: 'AND' })
            }
            this.formula[index].value.push({ name: `constraint_${val}`, val: true })
        },
        addNestedConditional (index) {
            let val = this.formula[0].then.value.length
            if (val !== 0) {
                const correctionval = -Math.round(-(val / 2))
                val = val - correctionval
                const arrayOfNumbers = []
                for (const component of this.formula[index].then.value || []) {
                    arrayOfNumbers.push(parseInt(component.name.slice(-1)))
                }

                while (arrayOfNumbers.includes(val)) {
                    val = val + 1
                }
                this.formula[index].then.value.push({ name: `operator_${val}`, val: 'AND' })
            }
            this.formula[index].then.value.push({ name: `constraint_${val}`, val: true })
        },
        changeThenSection (index) {
            if (this.formula[index].then.type === 'nested if statement') {
                this.formula[index].then.value = [{ name: 'constraint_0', val: true }]
                this.formula[index].then.then = { type: 'Assignment', value: [{ name: 'assignment_1', val: true }] }
                this.formula[index].then.else = { type: 'Assignment', value: [{ name: 'assignment_1', val: true }] }
            }
        },
        addIfStatement () {
            this.formula.splice(-1, 0, { type: 'if', value: [{ name: 'constraint_0', val: true }], then: { type: 'Assignment', value: [{ name: 'assignment_1', val: true }] } })
        },
        removeConstraint (...args) {
            const [index, name, nested] = args
            console.log('>>>', nested)
            if (nested) {
                this.formula[index].then.value = this.formula[index].then.value.filter((item) => !item.name.includes(name.slice(-1)))
                return
            } else {
                this.formula[index].value = this.formula[index].value.filter((item) => !item.name.includes(name.slice(-1)))
            }
            console.log(args, index, name)
        },
        deleteConditional (index) {
            this.formula.splice(index, 1)
        }
    }
}
</script>

<style lang="scss" scoped>
    .conditional {
        background-color: #ededed;
        border-radius: 10px;
        margin: 0px 10px;
        padding: 5px 5px;
    }
    .Icon {
        cursor: pointer;
        color: red;
        font-size: 20px;
        margin: 0px 10px;
        width: 30px;
    }
    .Icon:hover {
        font-size: 25px;
    }
</style>
// <div v-if="(formulaEditableFields.first_if || !formulaFields.first_if.first_statement.left_side || !formulaFields.first_if.first_statement.operator || !formulaFields.first_if.first_statement.right_side)" class="p-d-flex p-ai-center conditional"  @mouseleave="formulaEditableFields.first_if=false">
// <Dropdown id="first_if" class="p-ml-2" v-model="formulaFields.first_if.first_statement.left_side" :options="indicatorList" placeholder="Select Indicator"  />
// <Dropdown class="p-m-2" v-model="formulaFields.first_if.first_statement.operator" :options="OperatorsList" style="width: 100px;" />
// <InputText type="text" v-model="formulaFields.first_if.first_statement.right_side" style="width: 150px;" />
// <i class="pi pi-times Icon" />
// </div>
// <div v-else class="conditional p-px-3" @click="formulaEditableFields.first_if=true">{{formulaFields.first_if.first_statement.left_side}} {{formulaFields.first_if.first_statement.operator}} {{formulaFields.first_if.first_statement.right_side}}</div>
            <!-- <div onclick="console.log('Outside?',event.composedPath()[0]===this)" style="background-color: green;" class="block">eeeee</div>
            <div id="aaa" class="" style="background-color: red;">aaaa</div> -->
