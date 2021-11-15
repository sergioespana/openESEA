// Used by SurveyCreation.vue

<template>
    <div>
        <div class="p-d-flex p-mt-2">
            <div v-for="item in libraryComponents" :key="item" class="p-col-4" style="font-size: 20px;" :style="(item === activeComponentType) ? 'border-bottom: 3px solid  #00695C; font-weight: bold;':'border-bottom: 3px solid lightgrey;'" @click="activeComponentType = item">
                {{item}}
            </div>
        </div>
        <div v-if="activeComponentType === 'Indicators'" class="p-d-flex p-mt-2" style="">
            <div v-for="item in ComponentOptions" :key="item" class="p-col-4" style="font-size: 14px;" :style="(item === activeComponentOption) ? 'border-bottom: 1px solid #00695C; font-size;':'border-bottom: 1px solid lightgrey;'" @click="activeComponentOption = item">
                {{item}}
            </div>
        </div>
        <div v-if="activeComponentType === 'Indicators'" class="p-text-left">
            <div class="p-m-1" style="height: 50px;">
                <!-- <div v-if="!searchbarIndicators" class="p-px-3 p-d-flex p-jc-between p-ai-center" @click="searchbarIndicators = !searchbarIndicators" @blur="searchbarIndicators = false">
                    <h3>Direct Indicators</h3><i class="pi pi-search" />
                </div> -->
                <span class="p-input-icon-left" style="width: 100%">
                    <i class="pi pi-search" /><InputText ref="searchbarQuestions" v-model="searchIndicator" @blur="checksSearchbarContentIndicator" placeholder="Search Direct Indicators..." style="width: 100%;" />
                </span>
            </div>
            <div style="height: calc(100vh - 390px); overflow-y: scroll;">
            <div v-for="indicator in filteredDirectIndicators" :key="indicator.id" class="directIndicators p-m-2" style="font-size: 16px; padding: 10px; overflow: hidden; border: 1px solid lightgrey; cursor: grab;"  @dragstart="startDrag($event, indicator)" @dragover.prevent @dragenter.prevent :draggable="true">
                {{indicator.key}}
            </div>
            </div>
        </div>
        <div v-if="activeComponentType === 'Questions'" class="p-text-left">
            <div class="p-m-1" style="height: 50px;">
                <!-- <div v-if="!searchbarQuestions" class="p-px-3 p-d-flex p-jc-between p-ai-center" @click="searchbarQuestions = !searchbarQuestions">
                    <h3>Questions</h3><i class="pi pi-search" />
                </div> -->
                <span class="p-input-icon-left" style="width: 100%">
                    <i class="pi pi-search" /><InputText ref="searchbarQuestions" v-model="searchQuestion" @blur="checkSearchbarContentQuestion" placeholder="Search Questions..." style="width: 100%;" />
                </span>
            </div>
            <div style="height: calc(100vh - 350px); overflow-y: scroll;">
                <div v-for="question in filteredQuestions" :key="question.id" class="questions p-px-3 p-m-2" style="font-size: 16px; padding: 10px; overflow: hidden; border: 1px solid lightgrey; cursor: grab;" :style="(question.id === activeQuestion?.id) ? 'background-color: #EEEEEE;':''" :draggable="true">
                    {{question.name}}
                </div>
            </div>
        </div>
        <div v-if="activeComponentType === 'Sections'" class="p-text-left">
            <div class="p-m-1" style="height: 50px;">
                <!-- <div v-if="!searchbarQuestions" class="p-px-3 p-d-flex p-jc-between p-ai-center" @click="searchbarQuestions = !searchbarQuestions">
                    <h3>Questions</h3><i class="pi pi-search" />
                </div> -->
                <span class="p-input-icon-left" style="width: 100%">
                    <i class="pi pi-search" /><InputText ref="searchbarSections" v-model="searchSection" @blur="checkSearchbarContentQuestion" placeholder="Search Sections..." style="width: 100%;" />
                </span>
            </div>
            <div style="height: calc(100vh - 350px); overflow-y: scroll;">
                <div v-for="section in filteredSections" :key="section.id" class="questions p-px-3 p-m-2" style="font-size: 16px; padding: 10px; overflow: hidden; border: 1px solid lightgrey; cursor: grab;" :style="(section.id === activeSection?.id) ? 'background-color: #EEEEEE;':''" :draggable="true">
                    {{section.title}}
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
    data () {
        return {
            libraryComponents: ['Indicators', 'Questions', 'Sections'],
            ComponentOptions: ['Unused', 'Used', 'All'],
            activeComponentType: 'Indicators',
            activeComponentOption: 'Unused',
            searchbarQuestions: false,
            searchQuestion: '',
            searchbarIndicators: false,
            searchIndicator: '',
            searchSection: ''
        }
    },
    computed: {
        ...mapState('question', ['questions']),
        ...mapState('directIndicator', ['directIndicators']),
        ...mapState('section', ['sections']),
        filteredSections () {
            return this.sections.filter((section) => { return (section.title.toLowerCase().includes(this.searchSection.toLowerCase())) })
        },
        filteredQuestions () {
            return this.questions.filter((question) => {
                return (question.name.toLowerCase().includes(this.searchQuestion.toLowerCase()))
            })
        },
        filteredDirectIndicators () {
            const directindicators = this.directIndicators.filter((indicator) => { return (indicator.key?.toLowerCase().includes(this.searchIndicator.toLowerCase())) })
            if (this.activeComponentOption === 'Unused') {
                return directindicators.filter(indicator => !(indicator.question > 0))
            } else if (this.activeComponentOption === 'Used') {
                return directindicators.filter(indicator => indicator.question > 0)
            } else {
                return directindicators
            }
        }
    },
    mounted () {
        this.fetchDirectIndicators({ mId: this.$route.params.id })
    },
    async created () {
        this.fetchData()
    },
    methods: {
        ...mapActions('directIndicator', ['fetchDirectIndicators']),
        async fetchData () {
            await this.fetchDirectIndicators({ mId: this.$route.params.id })
        },
        startDrag (evt, item) {
            console.log(item)
            evt.dataTransfer.dropEffect = 'move'
            evt.dataTransfer.effectAllowed = 'move'
            if (typeof item === 'object') {
                item = JSON.stringify(item)
            }
            evt.dataTransfer.setData('draggedItem', item)
            this.directIndicators = this.directIndicators.filter(indicator => indicator.id !== item.id)
        }
    }
}
</script>

<style lang="scss" scoped>
    .questions:hover {
        background-color: #EEEEEE;
    }
</style>
