<template>
    <div class="p-d-flex p-ai-center p-m-0" style="height: 40px;">
        <div v-if="assignment" class="p-d-flex p-ai-center p-mx-2">
            <p class="">{{ indirectIndicator.key || 'indicator_value' }}</p>
            <p class="p-mx-2" style="font-size: 30px;">=</p>

        </div>
        <div v-else class="p-d-flex p-mx-2">
            <Dropdown class="p-mr-2" v-model="leftSide" :options="indicators" optionLabel="key" optionValue="key" placeholder="Select Indicator" />
            <Dropdown v-model="comparisonValue" :options="comparisonOperators" optionLabel="value" optionValue="value" placeholder="Select Indicator" />
        </div>
        <div ref="focuswindow" style="position: relative; width: 100%;">
            <InputText ref="expression" v-model="rightSide" :placeholder="(assignment) ? 'set Indicator value here' : 'Write any expression you want here. Typing [ will pop up an autocomplete list.'" style="width: 100%; position: relative;" autocomplete="off" />
            <div id="autocomplete" v-if="autoComplete" style="width: 100%; position: absolute; z-index: 50;">
                <div v-for="indicator in indicators" :key="indicator" class="autocomplete-item" style="padding: 4px; border: 0.5px solid lightgrey; cursor: pointer; position: relative;" @click="chooseIndicator(indicator)">{{indicator.key}}</div>
            </div>
        </div>
    </div>
</template>
<script>
import { mapState } from 'vuex'
import Dropdown from 'primevue/dropdown'

export default {
    components: {
        Dropdown
    },
    props: {
        assignment: {
            type: Boolean,
            default: false
        },
        formula: {
            type: String,
            default: ''
        }
    },
    data () {
        return {
            // indicators: [
            //         { key: 'indicator_1' },
            //         { key: 'indicator_2' },
            //         { key: 'indicator_3' },
            //         { key: 'indicator_4' },
            //         { key: 'indicator_5' }
            // ],
            comparisonOperators: [
                    { id: 0, value: '==', component: null },
                    { id: 1, value: '!-', component: null },
                    { id: 2, value: '>', component: null },
                    { id: 3, value: '<', component: null },
                    { id: 4, value: '>=', component: null },
                    { id: 5, value: '<=', component: null }
                ],
            leftSide: null,
            rightSide: this.formula || '',
            months: '',
            comparisonValue: '==',
            autoComplete: false,
            positionLeft: null,
            positionRight: null,
            result: null
        }
    },
    computed: {
        ...mapState('directIndicator', ['directIndicators']),
        ...mapState('indirectIndicator', ['indirectIndicators', 'indirectIndicator']),
        indicators () {
            const selectableIndirectIndicators = this.indirectIndicators.filter(item => item.id !== this.indirectIndicator.id)
            return this.directIndicators.concat(selectableIndirectIndicators)
        }
    },
    watch: {
        rightSide (val) {
            this.$emit('expression', val)
            this.positionleft = null
            this.positionright = null
            this.autoComplete = false
            if (val.length) {
                console.log(val)
                const pattern = /[\s?[\w\s]*\s?]/g
                // const result = val.matchAll(pattern)
                this.result = [...val.matchAll(pattern)]
            }
        }
    },
    mounted () {
        console.log('==', this.$refs)
        const self = this
        // const focuswindow = document.getElementById('focuswindow')
        this.$refs.expression.$el.addEventListener('keyup', self.checkUserPosition, false)
        this.$refs.expression.$el.addEventListener('click', self.checkUserPosition, false)
        document.addEventListener('click', function (event) {
            if (self.$refs.focuswindow !== event.target && !self.$refs.focuswindow?.contains(event.target)) { self.removeAutoComplete() }
        })
    },
    methods: {
        showIndicators () {
            this.autoComplete = true
        },
        removeAutoComplete () {
            this.autoComplete = false
        },
        checkUserPosition (e) {
            console.log('user is moving!')
                    this.positionleft = null
                    this.positionright = null
                    this.autoComplete = false

                    const userPosition = e.target.selectionStart
                    console.log('-->', userPosition)
                    for (var i = userPosition - 1; i >= 0; i--) {
                        console.log(i)
                        if (this.rightSide[i] === ']') { break }
                        if (this.rightSide[i] === '[') {
                            this.positionleft = i
                        }
                    }
                    for (i = userPosition; i <= this.rightSide.length; i++) {
                        if (this.rightSide[i] === '[') { break }
                        if (this.rightSide[i] === ']') {
                            this.positionright = i
                        }
                    }
                    console.log('left: ', this.positionleft, 'right: ', this.positionright)
                    if (Number.isInteger(this.positionleft)) { //  && Number.isInteger(this.positionright)
                        this.showIndicators()
                    }
        },
        chooseIndicator (indicator) {
            const tempString = this.rightSide.split('')
            console.log('---------->', this.rightSide.slice((this.positionleft + 1), (this.positionLeft + (this.positionright - (this.positionLeft + 1)))))
            console.log('==', tempString)
            console.log(this.positionleft, this.positionright)
            let removablePart = 1
            if (Number.isInteger(this.positionright)) {
                removablePart = (this.positionright + 1) - (this.positionleft)
            }
            console.log(removablePart)
            tempString.splice((this.positionleft), removablePart, `[${indicator.key}]`) // (this.positionright - (this.positionLeft + 1)) (this.positionright - (this.positionLeft + 1))
            console.log('!!', tempString)
            this.rightSide = tempString.join('')
        }
        // findIndicators (string) {
        //     let results = []
        //     this.getAllResults()

        // },
        // getAllResults (string) {
        //      if(string.indexOf('[') >= 0 || string.indexOf(']') >= 0) {

        //      }
        // }
    }
}
</script>

<style lang="scss" scoped>
    .autocomplete-item {
        background-color: white;
    }
    .autocomplete-item:hover {
        background-color: lightgrey;
    }
</style>
