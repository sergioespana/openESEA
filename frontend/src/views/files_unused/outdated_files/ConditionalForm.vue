<template>

    <div v-if="assignment" class="p-px-2">
        <div v-if="(active || v$.AssignmentValue.$invalid)" class="p-d-flex p-ai-center conditional">
            <span class="p-mr-2">{{indicator}} = </span>
            <InputText type="text" v-model="AssignmentValue.right_value" style="width: 150px;" :class="{'p-invalid': v$.AssignmentValue.right_value.$error}" />
            <i class="pi pi-check Icon" style="color: green;" @click="changeActive(false)" />
            <i class="pi pi-times Icon" @click="deleteConditional()"/>
            </div>
        <div v-else class="conditional" @click="active=true">( {{indicator}} = {{AssignmentValue.right_value}} )</div>
    </div>
    <div v-else style="display: inline-block;">
        <div v-if="(active || v$.conditionalValues.$invalid)" class="conditional" style="height: 50px; margin: 0px 10px;">
            <div><Dropdown id="first_if" class="p-ml-2" v-model="conditionalValues.left_value" :options="indicatorList" placeholder="Select Indicator" :class="{'p-invalid': v$.conditionalValues.left_value.$error}"  /></div>
            <Dropdown class="p-m-2" v-model="conditionalValues.operator" :options="OperatorsList" style="width: 70px;" :class="{'p-invalid': v$.conditionalValues.operator.$error}" />
            <!-- <span id="text"><InputText type="text" v-model="conditionalValues.right_value" :style="widthStyl" /></span> -->
            <input id="txt" v-model="conditionalValues.right_value" class="p-inputtext" type="text" onkeypress.enter="this.style.width = (((this.value.length + 1) * 8) + 40) + 'px'" style="min-width: 50px;" :class="{'border': v$.conditionalValues.right_value.$error}">

            <i class="pi pi-check Icon" style="color: green;" @click="changeActive(false)" />
            <i class="pi pi-times Icon" @click="deleteConditional()"/>
        </div>
        <p v-else @click="active=true" style="background-color: #ededed; padding: 15px 20px; margin: 0px 10px; height: 50px; border-radius: 10px">( {{conditionalValues.left_value}}  {{conditionalValues.operator}}  {{conditionalValues.right_value}} )</p>
    </div>
</template>

<script>
import useVuelidate from '@vuelidate/core'
import { required } from '../utils/validators'
import Dropdown from 'primevue/dropdown'

export default {
    components: {
        Dropdown
    },
    props: {
        mykey: {
            type: String
        },
        index: {
            type: Number
        },
        nested: {
            type: Boolean,
            default: false
        },
        indicator: {
            type: String
        },
        assignment: {
            type: String
        }
    },
    setup: () => ({ v$: useVuelidate() }),
    validations: {
        conditionalValues: {
            left_value: { required },
            operator: { required },
            right_value: { required }
        },
        AssignmentValue: {
            right_value: { required }
        }
    },
    data () {
        return {
            active: false,
            isEmpty: true,
            OperatorsList: ['<', '<=', '=', '!=', '>', '>='],
            indicatorList: ['Indicator 1', 'Indicator 2', 'Indicator 3', 'Indicator 4'],
            conditionalValues: { left_value: null, operator: null, right_value: null },
            AssignmentValue: { right_value: null },
            widthStyle: 'width: 100px;'
        }
    },
    watch: {
        conditionalValues: {
            handler (val) {
                this.isEmpty = Object.values(val).some(x => x === null || x === '')
                console.log(this.isEmpty)
                // this.valueLength = val.right_value?.length
                // var textWidth = document.getElementById('text').clientWidth
                // console.log(textWidth)
                // if (val.right_value?.length > 6) {
                //     this.widthStyle = `width: ${((val.right_value?.length + 1) * 10 + 20)}px;`
                // }
                if (!this.assignment) {
                    if (this.v$.conditionalValues.$invalid) {
                    this.active = true
                }
                }
                console.log('return Conditional...')
            },
            deep: true
        },
        AssigmentValue: {
            handler (val) {
                if (this.assignment) {
                    if (this.v$.AssignmentValue.$invalid) {
                        this.active = true
                    }
                }
                this.$emit('update', this.AssigmentValue)
            },
            deep: true
        }
    },
    methods: {
        changeActive (value) {
            if (this.assignment) {
                console.log('-----', this.assigment)
                this.v$.AssignmentValue.$touch()
            } else {
                this.v$.conditionalValues.$touch()
            }
            this.active = value || false
        },
        deleteConditional () {
            console.log('Remove Conditional')
            this.$emit('delete', this.index, this.mykey, this.nested)
        }
    }
}
</script>

<style lang="scss" scoped>
    .conditional {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #ededed;
        height: 50px;
        border-radius: 10px;
        margin: 0px 0px;
        padding: 5px 10px;
    }
    .Icon {
        cursor: pointer;
        color: red;
        font-size: 20px;
        margin: 0px 0px;
        padding: 15px 15px;
        width: 40px;
    }
    .Icon:hover {
        font-size: 25px;
    }
    .p-inputtext {
        width: 100px;
    }
    .border {
        border: 1px solid red;
    }
</style>
    // formulaEditableFields.first_if || !formulaFields.first_if.first_statement.left_side || !formulaFields.first_if.first_statement.operator || !formulaFields.first_if.first_statement.right_side)
    // @mouseenter="active=true" @mouseleave="active=false"
    <!-- <div v-if="active" class="p-d-flex p-ai-center conditional"  @mouseleave="formulaEditableFields.first_if=false">
    <Dropdown id="first_if" class="p-ml-2" v-model="formulaFields.first_if.first_statement.left_side" :options="indicatorList" placeholder="Select Indicator"  />
    <Dropdown class="p-m-2" v-model="formulaFields.first_if.first_statement.operator" :options="OperatorsList" style="width: 100px;" />
    <InputText type="text" v-model="formulaFields.first_if.first_statement.right_side" style="width: 150px;" />
    <i class="pi pi-times Icon" />
    </div>
    <div v-else class="conditional p-px-3" @click="formulaEditableFields.first_if=true">{{formulaFields.first_if.first_statement.left_side}} {{formulaFields.first_if.first_statement.operator}} {{formulaFields.first_if.first_statement.right_side}}</div> -->
    <!-- <span class="input p-inputtext" v-model="conditionalValues.right_value" :style="widthStyle" role="text" contenteditable>99</span> -->
