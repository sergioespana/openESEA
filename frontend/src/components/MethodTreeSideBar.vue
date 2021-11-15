// used by MethodIndicatorCreation.vue, MethodTopicCreation.vue

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
</style>
