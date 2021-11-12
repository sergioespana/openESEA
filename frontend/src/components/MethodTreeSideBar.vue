<template>
    <div style="width: 400px; border-right: 1px solid lightgrey;" @drop='onDrop($event)'  @dragover.prevent @dragenter.prevent>
        <div class="p-d-flex p-mt-2">
            <div v-for="item in libraryComponents" :key="item" class="p-col-6" style="font-size: 20px;" :style="(item === activeComponentType) ? 'border-bottom: 3px solid  #00695C; font-weight: bold;':'border-bottom: 3px solid lightgrey;'" @click="activeComponentType = item">
                {{item}}
            </div>
        </div>
        <method-sidebar-component v-if="activeComponentType === 'Indicators'" :items="filteredDirectIndicators" :active-item="activeDirectIndicator" v-model:searchbar="searchbar" item-type="direct" />
        <method-sidebar-component v-if="activeComponentType === 'Calculations'" :items="filteredIndirectIndicators" :active-item="activeIndirectIndicator" v-model:searchbar="searchbar" item-type="indirect" />
        <method-sidebar-component v-if="activeComponentType === 'Topics' && topicsdisplay" :items="filteredTopics" :active-item="activeTopic" v-model:searchbar="searchbar" item-type="topic" />
    </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
import MethodSidebarComponent from '@/components/MethodSidebarComponent'

export default {
    components: {
        MethodSidebarComponent
    },
    props: {
        topicsdisplay: {
            type: Boolean,
            default: false
        }
    },
    data () {
        return {
            libraryComponents: ['Indicators', 'Calculations'], // , 'Topics'
            activeComponentType: 'Indicators',
            searchbar: ''
        }
    },
    computed: {
        ...mapState('method', ['method']),
        ...mapState('topic', { topics: 'topics', activeTopic: 'topic' }),
        ...mapState('question', { activeQuestion: 'question', methodQuestions: 'questions' }),
        ...mapState('directIndicator', { activeDirectIndicator: 'directIndicator', directIndicators: 'directIndicators' }),
		...mapState('indirectIndicator', { activeIndirectIndicator: 'indirectIndicator', indirectIndicators: 'indirectIndicators' }),

        ...mapGetters('topic', ['methodTopics', 'subTopics']),
		...mapGetters('question', { topicQuestions: 'topicQuestions' }),
		...mapGetters('indirectIndicator', ['topicIndirectIndicators']),
        filteredTopics () {
            return this.topics.filter((topic) => { return (topic.name.toLowerCase().includes(this.searchbar.toLowerCase())) })
        },
        // For searching direct indicators
        filteredDirectIndicators () {
            const directindicators = this.directIndicators.filter((indicator) => { return (indicator.key?.toLowerCase().includes(this.searchbar.toLowerCase())) })
            if (this.activeComponentOption === 'Unused') {
                return directindicators.filter(indicator => !(indicator.topic > 0))
            } else if (this.activeComponentOption === 'Used') {
                return directindicators.filter(indicator => indicator.topic > 0)
            } else {
                return directindicators
            }
        },
        // For searching indirect indicators
        filteredIndirectIndicators () {
            if (this.indirectIndicators.length) {
            return this.indirectIndicators.filter((indicator) => {
                return (indicator.key?.toLowerCase().includes(this.searchbar.toLowerCase()))
            })
            } else { return [] }
        }
    },
    watch: {
    },
    created () {
        this.fetchItems()
    },
    methods: {
        ...mapActions('topic', ['fetchTopics', 'setTopic', 'patchTopic']),
		...mapActions('question', ['fetchQuestions', 'setQuestion']),
        ...mapActions('directIndicator', ['fetchDirectIndicators']),
		...mapActions('indirectIndicator', ['fetchIndirectIndicators', 'setIndirectIndicator', 'updateIndirectIndicator']),
        // Used when dragging and dropping an indicator into the method
        async onDrop (evt) {
            const myitem = evt.dataTransfer.getData('draggedItem')
            const parseditem = JSON.parse(myitem)
            if (!parseditem.id) { return }
            console.log('-->', parseditem)
            if (parseditem.objType === 'indicator') {
                const topicIndicators = this.directIndicators.filter(indicator => (indicator.topic === parseditem.topic && indicator.id !== parseditem.id))
                const ids = topicIndicators.map(indicator => indicator.id)
                await this.patchTopic({ mId: this.method.id, id: parseditem.topic, data: { direct_indicators: ids } })
            } else if (parseditem.objType === 'calculation') {
                const topicIndirectIndicators = this.indirectIndicators.filter(indicator => (indicator.topic === parseditem.topic && indicator.id !== parseditem.id))
                const ids = topicIndirectIndicators.map(indicator => indicator.id)
                await this.patchTopic({ mId: this.method.id, id: parseditem.topic, data: { indirect_indicators: ids } })
            }
            this.fetchItems()
        },
        async fetchItems () {
            await this.fetchQuestions({ mId: this.method.id, SuId: 0, SeId: 0 })
            await this.fetchTopics({ mId: this.method.id })
            await this.fetchDirectIndicators({ mId: this.method.id })
            await this.fetchIndirectIndicators({ mId: this.method.id })
        }
    }
}
</script>

<style lang="scss" scoped>
.p-tree {
    background: none;
    border: 1px solid lightgray;
}
.directIndicators:hover {
    background-color: #EEEEEE;
}
// setActiveItem (active) {
// 	const [type, id] = active.split('_')
// 	const parsedId = parseInt(id, 10)
// 	if (type === 'topic') {
// 		this.setTopic({ id: parsedId })
// 		this.setQuestion()
// 		this.setIndirectIndicator()
// 	} else if (type === 'question') {
// 		this.setQuestion({ id: parsedId })
// 		this.setIndirectIndicator()
// 	} else if (type === 'calculation') {
// 		this.setIndirectIndicator({ id: parsedId })
// 		this.setQuestion()
// 	}
// },
// addToCalculation (item) {
// 	this.updateIndirectIndicator({
// 		mId: this.method.id,
// 		indirectIndicator: {
// 			...this.activeIndirectIndicator,
// 			formula: `${this.activeIndirectIndicator.formula} [${item.key}]`
// 		}
// 	})
// }
// activeItem () {
//     if (this.activeQuestion.id) {
// 		this.itemsOpen.push(`topic_${this.activeQuestion.topic}`)
// 	}
// 	if (this.activeIndirectIndicator.id) {
// 		this.itemsOpen.push(`topic_${this.activeIndirectIndicator.topic}`)
// 	}
// 	if (this.activeTopic.parent_topic) {
// 		this.itemsOpen.push(`topic_${this.activeTopic.parent_topic}`)
// 	}
// }
// searchbarDirect (val) {
//     if (val) {
//         this.$nextTick(() => this.$refs.searchbardirect.$el.focus())
//     }
// },
// searchbarIndirect (val) {
//     if (val) {
//         this.$nextTick(() => this.$refs.searchbarindirect.$el.focus())
//     }
// }
//     <div style="width: 300px; justify-content: between;">
//             <h2 class="height: 500px;">Indicator Libary</h2>
//             <!-- <div v-if="items.length">
//             <Tree :value="items" v-model:selectionKeys="selectedKey1" selectionMode="single" :expandedKeys="expandedKeys" @nodeSelect="activateItem" style="border-top: 3px solid lightgrey;" />
//             </div>
//             <div v-else> No components to display!</div> -->
//             <!-- <TreeSelect /> -->
//             <div class="p-ml-1 p-mt-5" style="height: 50px;">
//             <div v-if="!searchbarDirect" class="p-px-3 p-d-flex p-jc-between p-ai-center" @click="searchbarDirect = !searchbarDirect"><h3>Direct Indicators</h3><i class="pi pi-search" /></div>
//             <span v-else class="p-input-icon-left" style="width: 100%;">
//                             <i class="pi pi-search" /><InputText ref="searchbardirect" v-model="searchDirect" @blur="checkSearchbarContentDirect" placeholder="Search Direct Indicators..." style="width: 100%;" />
//                         </span>
//             </div>
//             <hr>
//             <div v-for="indicator in filteredDirectIndicators" :key="indicator.id" class="directIndicators" style="height: 50px; line-height: 50px; border: 1px solid white; cursor: grab;" :style="(indicator.key === activeDirectIndicator.key) ? 'background-color: #EEEEEE;':''" :draggable="true">
//                 {{indicator.key}}
//             </div>

//             <div class="p-ml-1 p-mt-5" style="height: 50px;">
//             <div v-if="!searchbarIndirect" class="p-px-3 p-d-flex p-jc-between p-ai-center" @click="searchbarIndirect = !searchbarIndirect"><h3>Indirect Indicators</h3><i class="pi pi-search" /></div>
//             <span v-else class="p-input-icon-left" style="width: 100%;">
//                             <i class="pi pi-search" /><InputText ref="searchbarindirect" v-model="searchIndirect" @blur="checkSearchbarContentIndirect" placeholder="Search Indirect Indicators..." style="width: 100%;" />
//                         </span>
//             </div>
//             <hr>
//             <div v-for="indicator in filteredIndirectIndicators" :key="indicator.id" class="directIndicators" style="height: 50px; line-height: 50px; border-bottom: 1px solid lightgrey; cursor: grab;" :style="(indicator.key === activeIndirectIndicator.key) ? 'background-color: #EEEEEE;':''" :draggable="true">
//                 {{indicator.key}}
//             </div>
//          <div class="p-d-flex p-ai-center p-shadow-5" style="position: relative; margin-top: 300px; margin-top: 1500; background-color: yellow;">
//             <div v-for="option in addBar" :key="option.choice" class="p-d-flex p-jc-center p-ai-center" style="height: 70px; width: 150px; border: 1px solid lightgrey;" :style="(option.hover) ? 'background-color: lightgrey': ''"  @mouseover="option.hover=true" @mouseleave="option.hover=false" @click="addBarMethod(option.choice)">
//                 <div>
//                     <i :class="option.icon ? option.icon : 'pi pi-plus'" />
//                     <p class="p-text-italic p-m-2">{{option.choice}}</p>
//                 </div>
//             </div>
//         </div>
//     </div>
// const arr = []
// console.log('::', data)
// data.forEach(el => console.log(el)) // arr.push({ label: el.name, key: el.name }))
// return arr
// return arr
// return getMethodItems(
//     this.methodTopics,
//     this.subTopics,
//     this.topicQuestions,
//     this.topicIndirectIndicators
// )
// checkSearchbarContentDirect () {
//     if (this.searchDirect === '') {
//         this.searchbarDirect = false
//     }
// },
// checkSearchbarContentIndirect () {
//     if (this.searchIndirect === '') {
//         this.searchbarIndirect = false
//     }
// }
// expandAll () {
//     for (const node of this.items) {
//         this.expandNode(node)
//     }

//     this.expandedKeys = { ...this.expandedKeys }
// },
// expandNode (node) {
//     this.expandedKeys[node.key] = true
//     if (node.children && node.children.length) {
//         for (const child of node.children) {
//             this.expandNode(child)
//         }
//     }
// }
</style>
