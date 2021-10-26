<template>
    <div class="p-d-flex p-ai-center p-m-0" style="">
        <div ref="focuswindow" style="position: relative; width: 100%;">
            <Textarea ref="expression" :autoResize="true" rows="1" v-model="lazyFormula" :placeholder="(assignment) ? 'Type #ife  or #iff for either an empty or filled if/else statement. Type [ to insert an indicator.' : 'Write any expression you want here. Typing [ will pop up an autocomplete list.'" style="width: 100%; position: relative;" autocomplete="off" />
            <div id="autocomplete" v-if="autoComplete" style="width: 100%; position: absolute; z-index: 50;">
                <div v-for="indicator in indicators" :key="indicator" class="autocomplete-item" style="padding: 4px; border: 0.5px solid lightgrey; cursor: pointer; position: relative;" @click="chooseIndicator(indicator)">{{indicator.key}}</div>
            </div>
        </div>
    </div>
</template>
<script>
import { mapState } from 'vuex'

export default {
    components: {
    },
    props: {
        formula: {
            type: String,
            default: ''
        },
        keyy: {
            type: String
        }
    },
    data () {
        return {
            lazyFormula: this.formula || '',
            autoComplete: false,
            positionLeft: null,
            positionRight: null
        }
    },
    computed: {
        ...mapState('directIndicator', ['directIndicators']),
        ...mapState('indirectIndicator', ['indirectIndicators', 'indirectIndicator']),
        indicators () {
            return this.directIndicators.concat(this.indirectIndicators)
        }
    },
    watch: {
        lazyFormula (val) {
            this.lazyFormula = val.replace(' then', '\nthen')
            this.lazyFormula = val.replace(' else', '\nelse')
            console.log(val)
            this.$emit('output', val)
        }
    },
    mounted () {
        const self = this
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
                    const userPosition = e.target.selectionStart

                    if (this.lazyFormula.includes('#iff')) {
                        this.lazyFormula = this.lazyFormula.replace('#iff', `if ([indicator_key] = null)\nthen [${this.keyy}] = null\nelse [${this.keyy}] = null`)
                    }
                    if (this.lazyFormula.includes('#ife')) {
                        this.lazyFormula = this.lazyFormula.replace('#ife', 'if () \nthen \nelse')
                    }

                    // Following three for loops look for the 1). left bracket and 2). right bracket or 3). empty space
                    for (var i = userPosition - 1; i >= 0; i--) {
                        if (this.lazyFormula[i] === ']') { break }
                        if (this.lazyFormula[i] === '[') {
                            this.positionleft = i
                            break
                        }
                    }
                    for (i = userPosition; i <= this.lazyFormula.length; i++) {
                        if (this.lazyFormula[i] === '[') { break }
                        if (this.lazyFormula[i] === ']') {
                            this.positionright = i + 1
                            break
                        }
                    }
                    if (Number.isInteger(this.positionleft) && !this.positionright) {
                        for (i = this.positionleft; i <= this.lazyFormula.length; i++) {
                            if ((this.lazyFormula[i] === ')') || (this.lazyFormula[i] === ' ')) {
                                this.positionright = i
                                break
                            }
                        }
                    }
                    console.log('left: ', this.positionleft, 'right: ', this.positionright)
                    if (Number.isInteger(this.positionleft)) {
                        this.showIndicators()
                        return
                    }
                    this.removeAutoComplete()
        },
        chooseIndicator (indicator) {
            const tempString = this.lazyFormula.split('')
            let removablePart = this.lazyFormula.length - this.positionleft
            if (Number.isInteger(this.positionright)) {
                removablePart = (this.positionright) - (this.positionleft)
            }
            tempString.splice((this.positionleft), removablePart, `[${indicator.key}]`)
            this.lazyFormula = tempString.join('')
            this.removeAutoComplete()
        }
    }
}
// findIndicators (string) {
//     let results = []
//     this.getAllResults()

// },
// getAllResults (string) {
//      if(string.indexOf('[') >= 0 || string.indexOf(']') >= 0) {

//      }
// }
// const selectableIndirectIndicators = this.indirectIndicators.filter(item => item.id !== this.indirectIndicator.id)
// (this.positionright - (this.positionLeft + 1)) (this.positionright - (this.positionLeft + 1))
// comparisonOperators: [
//     { id: 0, value: '==', component: null },
//     { id: 1, value: '!-', component: null },
//     { id: 2, value: '>', component: null },
//     { id: 3, value: '<', component: null },
//     { id: 4, value: '>=', component: null },
//     { id: 5, value: '<=', component: null }
// ],
// if (val.length) {
//     const pattern = /[\s?[\w\s]*\s?]/g
//     this.result = [...val.matchAll(pattern)]
// }
</script>

<style lang="scss" scoped>
    .autocomplete-item {
        background-color: white;
    }
    .autocomplete-item:hover {
        background-color: lightgrey;
    }
</style>
