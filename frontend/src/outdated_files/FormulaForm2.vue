<template>
    <div style="min-height: 300px; background-color: white; position:relative; padding-top: 5px;">
        <div class="p-d-flex p-ai-center">
            <span class="formula-text">IF</span>
            <div class="statement p-d-flex">
                <div v-for="(component, index) in formula.if" :key="component" class="logic-check p-d-flex p-ai-center">
                    <div class="insert-padding" @drop='onDrop($event, (index))'  @dragover.prevent @dragenter.prevent></div>
                    <div @drop='onDrop($event, index, (replace=true))' style="min-width: 50px;" draggable="true" @dragstart="startDrag($event, index)" @dragover.prevent @dragenter.prevent>{{component.value}}</div>
                    <div v-if="index === (formula.if.length - 1)" class="insert-padding" @drop='onDrop($event, (index + 1))'  @dragover.prevent @dragenter.prevent></div> <!--  @dragover.prevent @dragenter.prevent -->
                </div>
                <i class="pi pi-check Icon" style="color: green;" @click="changeActive(false)" />
                <i class="pi pi-times Icon" @click="deleteConditional()"/>
            </div>
             <i class="pi pi-plus Icon" style="color: grey;" @click="addConditional(idx)"/>
            <span class="formula-text">THEN</span>
             <div class="statement"></div>
        </div>
        <div class="p-d-flex p-ai-center">
            <span class="formula-text">ELSE</span>
            <div class="statement"></div>
        </div>
        {{formula.if}}
        <div class="building-blocks">
            <div class="p-grid p-m-0 p-p-0 p-text-center" style="width: 100%; height: 100%;">
                <div class="p-col-4 p-m-0 p-p-0">
                    <div class="header">Indicators | Search Bar</div>
                    <div class="items-box">
                        <div v-for="indicator in indicators" :key="indicator" class="item">
                            {{indicator}}
                        </div>
                    </div>
                </div>
                <div class="p-col-2 p-m-0 p-p-0">
                    <div class="header">Logical Operators</div>
                    <div class="items-box">
                        <div v-for="item in logicalOperators" :key="item" draggable="true" @dragstart="startDrag($event, item)" class="item">
                            {{item.value}}
                        </div>
                    </div>
                </div>
                <div class="p-col-3 p-m-0 p-p-0">
                    <div class="header">Comparison Operators</div>
                    <div class="items-box">
                        <div v-for="item in comparisonOperators" :key="item" draggable="true" @dragstart="startDrag($event, item)" class="item">
                            {{item.value}}
                        </div>
                    </div>
                </div>
                <div class="p-col-3 p-m-0 p-p-0">
                    <div class="header">Arithmetic Operators</div>
                    <div class="items-box">
                        <div v-for="operator in arithmeticOperators" :key="operator" class="item">
                            {{operator}}
                        </div>
                    </div>
                </div>
            </div>
            <!-- <div class="p-grid p-m-0 p-text-center">
                <div class="p-grid p-m-0 p-p-0 p-col-4" style="border: 1px solid black;">
                    <div class="p-col-6 item">Direct Indicator</div>
                    <div class="p-col-6 item">Indirect Indicator</div>
                </div>
                <div class="p-grid p-m-0 p-p-0 p-col-2 operators"  style="border: 1px solid black;">
                    <div class="p-col-6 item">AND</div>
                    <div class="p-col-6 item">OR</div>
                </div>
                <div class="p-grid p-m-0 p-p-0 p-col-3 operators"  style="border: 1px solid black;">
                    <div class="p-col-2 item">==</div>
                    <div class="p-col-2 item">!=</div>
                    <div class="p-col-2 item">&gt;</div>
                    <div class="p-col-2 item">&lt;</div>
                     <div class="p-col-2 item">&gt;=</div>
                    <div class="p-col-2 item">&lt;=</div>
                </div>
                <div class="p-grid p-m-0 p-p-0 p-col-3 operators"  style="border: 1px solid black;">
                    <div class="p-col-2 item">+</div>
                    <div class="p-col-2 item">-</div>
                    <div class="p-col-2 item">*</div>
                    <div class="p-col-2 item">/</div>
                    <div class="p-col-2 item">%</div>
                    <div class="p-col-2 item">**</div>
                    <div class="p-col-2 item">//</div>
                </div>
            </div> -->
        </div>
        <!-- <div class="p-col-8">ee</div>
        <div class="p-col-4" style="border-left: 1px solid lightgrey;">
            <div class="p-text-center p-mt-2">
                <h3>Building Blocks</h3>
                <Divider />
            </div>
                <Accordion>
                    <AccordionTab header="Indicators">
                        Content
                    </AccordionTab>
                    <AccordionTab header="Comparison Operators">
                        Content
                    </AccordionTab>
                    <AccordionTab header="Logical Operators">
                        Content
                    </AccordionTab>
                </Accordion>
        </div> -->

    </div>
</template>

<script>

export default {
    data () {
        return {
            formula: {
                if:
                    [
                        { id: 0, value: '5', type: null },
                        { id: 1, value: '==', type: null },
                        { id: 2, value: '5', type: null }
                    ],
                then: [
                ],
                else: [
                ]
                }, // {'if': [], 'then': {'if': [], 'then': { }, else: [] }, else: [] }
            indicators: [
                'Direct Indicator',
                'Indirect Indicator'
            ],
            logicalOperators: [
                { id: 0, value: 'AND', component: null },
                { id: 1, value: 'OR', component: null }
            ],
            comparisonOperators: [
                { id: 0, value: '==', component: null },
                { id: 1, value: '!-', component: null },
                { id: 2, value: '>', component: null },
                { id: 3, value: '<', component: null },
                { id: 4, value: '>=', component: null },
                { id: 5, value: '<=', component: null }
            ],
            arithmeticOperators: [
                '+',
                '-',
                '*',
                '/',
                '%',
                '**'
            ]
        }
    },
    methods: {
        startDrag (evt, item) {
            console.log(item)
            evt.dataTransfer.dropEffect = 'move'
            evt.dataTransfer.effectAllowed = 'move'
            if (typeof item === 'object') {
                item = JSON.stringify(item)
            }
            evt.dataTransfer.setData('draggedItem', item)
        },
        onDrop (evt, ...args) {
            const [index, replace] = args
            const myitem = evt.dataTransfer.getData('draggedItem')
            const parseditem = JSON.parse(myitem)

            if (typeof parseditem === 'object') {
                console.log('e')
                if (replace) {
                    this.formula.if.splice(index, 1, parseditem)
                } else {
                    this.formula.if.splice(index, 0, parseditem)
                }
            } else {
                if (replace) {
                    var temp = this.formula.if[parseditem]
                    this.formula.if[parseditem] = this.formula.if[index]
                    this.formula.if[index] = temp
                } else {
                        var temp2 = this.formula.if[parseditem]
                        if (parseditem < index) {
                            this.formula.if.splice((index), 0, temp2)
                            this.formula.if.splice(parseditem, 1)
                        } else {
                            console.log('yyy')
                            this.formula.if.splice((index), 0, temp2)
                            this.formula.if.splice((parseditem + 1), 1)
                        }
                }
            }
            // const item = this.items.find(item => item.id === itemID)
            // item.list = list
        }
    }
}
// import Accordion from 'primevue/accordion'
// import AccordionTab from 'primevue/accordiontab'
// export default {
//     components: {
//         Accordion,
//         AccordionTab
//     }
// }
</script>

<style lang="scss" scoped>
.formula-text {
    font-size: 25px;
    font-weight: bold;
    padding: 0px 10px;
}
.statement {
    border: 1px dotted lightgrey;
    min-height: 50px;
    min-width: 150px;
    margin: 5px 0px;
}
.insert-padding {
    width: 30px;
    height: 50px;
    background-color: rgba(100, 107, 107, 0.05);
    border: 1px dashed rgba(100, 107, 107, 0.05);
}
.logic-check {
    // height: 50px;
    line-height: 50px;
    text-align: center;
    flex-grow: 1;
}
.insert-padding:hover {
    background-color: rgba(112, 107, 107, 0.35)
}
.building-blocks {
    position: absolute;
    bottom: 0px;
    width: 100%;
    height: 100px;
    background-color: #F2F2F2;
    padding-bottom: 10px;
}
.header {
    // width: 100%;
    height: 40px;
    line-height: 40px;
    border: 1px solid #D8D8D8;
    background-color: white;
}
.items-box {
    height: 60px;
    // border: 1px solid black;
    display: flex;
    align-items: stretch;
}
.item {
    flex-grow: 1;
    line-height: 60px;
    border: 1px solid lightgray;
    // width: 100%; height: 100%; flex-grow-1; line-height: 60px;"
}
.item:hover {
    background-color: lightgrey;
    cursor: grab;
}
.Icon {
    font-size: 20px;
    padding: 15px 10px 10px 10px;
    cursor: pointer;
    color: red;
    margin: 0px 10px;
    width: 30px;
}
.Icon:hover {
    font-size: 25px;
}
// style="
// .item-header {
//     text-align: center;
//     font-size: 20px;
//     font-weight: bold;
//     border: 1px solid grey;
// }
// .item {
//     border: 1px solid lightgrey;
//     flex-grow: 1;
//     text-align: center;
//     font-weight: bold;
//     display: table-cell;
//     vertical-align: middle;
// }
// .operators {
//     font-size: 30px;
//     font-weight: bold;
// }

// console.log(parseditem.id)
// console.log(this.formula.if)
// console.log(this.formula.if.findIndex(x => x === parseditem))
// console.log('>>', this.formula.if.find((element) => element.id === parseditem.id))
//  if (this.formula.if.findIndex(x => x.value === parseditem.value) >= 0) {
//     const oldIndex = this.formula.if.findIndex(x => x.value === parseditem.value)
//     if (replace) {
//         console.log('check')
//         // const oldIndex = this.formula.if.findIndex(x => x.id === parseditem.id)
//         var temp = this.formula.if[oldIndex]
//         this.formula.if[oldIndex] = this.formula.if[index]
//         this.formula.if[index] = temp
//         console.log('===', this.formula.if)
//     } else {
//         console.log('eeee')
//         this.formula.if.splice(oldIndex, 1)
//         if (oldIndex < index) {
//             this.formula.if.splice((index - 1), 0, parseditem)
//         } else {
//              this.formula.if.splice((index), 0, parseditem)
//         }
//     }
//     console.log('===', this.formula.if)
// }
</style>
