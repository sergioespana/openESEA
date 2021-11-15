// http://localhost:8081/methods/3/topic-creation/

<template>
    <div class="p-d-flex" style="height: calc(100vh - 145px); width: 100%; border-top: solid lightgrey; display: flex;">
        <method-tree-sidebar :topicsdisplay="true" style="height: 100%; width: 400px; flex: 0 0 400px;" />
        <div v-if="methodTopics.length" class="" style="width: 100%; height: calc(100vh - 145px); background-color: white; overflow-y: auto;">
            <div class="p-m-5">
                 <div v-for="(topic, topicIndex) in items2" :key="`topic-${topicIndex}`" class="p-my-5 p-shadow-5" style="width: 100%; background-color: #f8f9fe; border: 1px solid lightgrey;"> <!-- #f7f7f7 #e6f3ff-->
                    <topic-form
                        :topic="topic"
                        :active="activeItem.objType === topic.objType && activeItem.id === topic.id"
                        :check-saving-status="checkSavingStatus"
                        @savingstatus="savingStatus(topic, $event)"
                        @refreshsidebar="refreshSidebar()"
                        @click="toggleActive(topic)"
                    />
                    <h3 v-if="(topic.id > 0)"
                        class="p-col p-text-center p-text-italic p-text-light p-m-4 p-p-5"
                        style="border: 2px dashed rgba(192,192,192,0.7); background-color:rgba(192,192,192,0.25); color: grey;"
                        @drop='onDrop($event, topic)'
                        @dragover.prevent
                        @dragenter.prevent>
                        'Add Indicator to the main topic by dragging it into the box'
                    </h3>
                    <div v-for="(topicChild, index) in topic.children" :key="`topicChild-${index}`" >
                        <div class="p-ml-5">
                                <component
                                    :is="`${topicChild.objType}-form`"
                                    :topic="topicChild"
                                    :direct-indicator="topicChild"
                                    :indirect-indicator="topicChild"
                                    :errors="errors[topicChild.objType] && errors[topicChild.objType][topicChild.id]"
                                    :active="activeItem.objType === topicChild.objType && activeItem.id === topicChild.id"
                                    :check-saving-status="checkSavingStatus"
                                    @click="toggleActive(topicChild)"
                                    @refreshsidebar="refreshSidebar()"
                                    @savingstatus="savingStatus(topicChild, $event)"
                                    @dragstart="startDrag($event, topicChild)"
                                    @dragover.prevent @dragenter.prevent :draggable="true"
                                />
                                <div v-for="(subTopicChild, index) in topicChild.children" :key="`subTopicChild-${index}`" class="p-ml-5">
                                    <component
                                        :is="`${subTopicChild.objType}-form`"
                                        :direct-indicator="subTopicChild"
                                        :indirect-indicator="subTopicChild"
                                        :errors="errors[subTopicChild.objType] && errors[subTopicChild.objType][subTopicChild.id]"
                                        :active="activeItem.objType === subTopicChild.objType && activeItem.id === subTopicChild.id"
                                        @input="saveActive(subTopicChild.objType, $event)"
                                        @click="toggleActive(subTopicChild)"
                                        @dragstart="startDrag($event, subTopicChild)"
                                        @dragover.prevent @dragenter.prevent :draggable="true"
                                    />
                                </div>
                                <h3
                                    v-if="(topicChild.objType === 'topic' && topicChild.id > 0)"
                                    class="p-col p-text-center p-text-italic p-text-light p-m-4 p-p-5"
                                    style="border: 2px dashed rgba(192,192,192,0.7); background-color:rgba(192,192,192,0.25);color: grey;"
                                    @drop='onDrop($event, topicChild)'  @dragover.prevent @dragenter.prevent>
                                    'Add Indicator by dragging it into the box'
                                </h3>
                            <!-- <Button label="Add Question" icon="pi pi-plus" class="p-button-text p-text-left p-p-5" @click="addQuestion()" /> :class="(topicChild?.children?.length ? 'p-p-0': 'p-p-0')" -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div
            v-else class="p-m-5"
            style="display: flex; width: 100%; height: 50px; background-color: #00695C; border-radius: 5px; cursor: pointer;"
            @click="addTopic">
            <span style="margin: auto; color: white; font-weight: bold;">Add Topic</span>
        </div>
    </div>

    <div class="p-d-flex p-ai-center p-shadow-5" style="position: fixed; top: 45%; right: 0px; width: 100px; background-color: #fcfcfc; border: 2px solid grey;">
        <div>
            <div v-for="option in addBar" :key="option.choice"
                class="p-d-flex p-jc-center p-ai-center"
                style="height: 100px; width: 100px; border: 1px solid lightgrey" :style="(option.hover ? 'background-color: lightgrey;' : '')"
                @mouseover="option.hover=true" @mouseleave="option.hover=false">
                <div v-if="!(option.choice ==='SubTopic' && !items2.length)" @click="addBarMethod(option.choice)">
                    <i :class="option.icon? option.icon : 'pi pi-plus'" />
                    <p class="p-text-italic p-m-2">{{option.choice}}</p>
                </div>
            </div>
        </div>
    </div>
    <Dialog v-model:visible="unsavedChangesDialog" style="width: 600px;" header="Unsaved Changes" :modal="true" :dismissableMask="true">
        <div class="confirmation-content">
            This page contains unsaved changes, leaving the page now will destroy these. Do you still wish to leave the page?
        </div>
        <template #footer>
            <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="unsavedChangesChoice(true)" />
            <Button label="No" icon="pi pi-times" class="p-button-text" @click="unsavedChangesChoice(false)"/>
        </template>
    </Dialog>
</template>

<script>
    import MethodTreeSidebar from '@/components/MethodTreeSideBar'
    import { mapState, mapActions, mapGetters } from 'vuex'
    import getMethodItems2 from '@/utils/getMethodItems2'
    import TopicForm from '@/components/forms/TopicForm'
    import DirectIndicatorForm from '@/components/cards/DirectIndicatorForm'
    import IndirectIndicatorForm from '@/components/cards/IndirectIndicatorForm'

    export default {
        components: {
            MethodTreeSidebar,
            TopicForm,
            DirectIndicatorForm,
            IndirectIndicatorForm
        },
        data () {
            return {
                checkSavingStatus: false,
                TopicSavingStatus: {},
                to: null,
                allowRouting: false,
                unsavedChangesDialog: false,
                discardUnsavedChanges: false,
                addBar: [
                    { choice: 'Topic' },
                    { choice: 'SubTopic' }
                ],
                currentTopic: null
            }
        },
        computed: {
            ...mapState('method', ['method', 'error']),
            ...mapState('topic', { topics: 'topics', activeTopic: 'topic', topicErrors: 'errors' }),
            ...mapGetters('topic', ['methodTopics', 'subTopics']),
            ...mapState('directIndicator', { activeDirectIndicator: 'directIndicator', directIndicatorErrors: 'errors' }),
            ...mapGetters('directIndicator', ['topicDirectIndicators']),
            ...mapState('indirectIndicator', { activeIndirectIndicator: 'indirectIndicator', indirectIndicatorErrors: 'errors' }),
            ...mapGetters('indirectIndicator', ['topicIndirectIndicators']),
            // Get's Method items in the proper format
            items2 () {
                return getMethodItems2(
                    this.methodTopics,
                    this.subTopics,
                    this.topicDirectIndicators,
                    this.topicIndirectIndicators
                )
            },
            activeItem () {
                let objType = 'topic'
                let { id } = this.activeTopic
                if (this.activeDirectIndicator.id) {
                    objType = 'direct-indicator'
                    id = this.activeDirectIndicator.id
                }
                if (this.activeIndirectIndicator.id) {
                    objType = 'indirect-indicator'
                    id = this.activeIndirectIndicator.id
                }
                return { objType, id }
            },
            errors () {
                return {
                    indicator: this.directIndicatorErrors,
                    topic: this.topicErrors,
                    calculation: this.indirectIndicatorErrors
                }
            }
        },
        watch: {
            TopicSavingStatus: {
                handler (val) {
                    if ((Object.keys(val).length === this.topics.length) & (!Object.keys(this.topicErrors).length)) {
                        for (const key in val) {
                            if (val[key]) {
                                this.TopicSavingStatus = {}
                                this.unsavedChangesDialog = true
                                return
                            }
                        }
                        this.allowRouting = true
                        this.$router.push(this.to)
                    }
                },
                deep: true
            }
        },
        beforeRouteLeave (to, from, next) {
            if (!this.topics.length) { this.allowRouting = true }
            if (this.allowRouting || this.discardUnsavedChanges) { //  & !this.discardUnsavedChanges
                next(true)
            } else {
                this.to = to
                this.allowRouting = false
                this.checkSavingStatus = !this.checkSavingStatus
                next(false)
            }
        },
        methods: {
            ...mapActions('method', ['fetchMethod', 'updateMethod', 'saveMethod']),
            ...mapActions('topic', ['fetchTopics', 'setTopic', 'createTopic', 'updateTopic', 'addNewTopic', 'deleteTopic']),
            ...mapActions('directIndicator', ['fetchDirectIndicators', 'setDirectIndicator', 'addNewDirectIndicator', 'updateDirectIndicator', 'patchDirectIndicator', 'deleteDirectIndicator']),
            ...mapActions('indirectIndicator', ['fetchIndirectIndicators', 'setIndirectIndicator', 'addNewIndirectIndicator', 'updateIndirectIndicator', 'patchIndirectIndicator', 'deleteIndirectIndicator']),
            // Handles the dragging of an item (from e.g. sidebar)
            startDrag (evt, item) {
                evt.dataTransfer.dropEffect = 'move'
                evt.dataTransfer.effectAllowed = 'move'
                if (typeof item === 'object') {
                    item = JSON.stringify(item)
                }
                evt.dataTransfer.setData('draggedItem', item)
            },
            // Handles the Dropping of a dragged item
            async onDrop (evt, topic) {
                const myitem = evt.dataTransfer.getData('draggedItem')
                const parseditem = JSON.parse(myitem)
                if (!topic.id || !parseditem.id) { return }
                if ((parseditem.objType === 'direct-indicator')) {
                    await this.patchDirectIndicator({ mId: this.method.id, id: parseditem.id, data: { topic: topic.id } })
                } else if (parseditem.objType === 'indirect-indicator') {
                    await this.patchIndirectIndicator({ mId: this.method.id, id: parseditem.id, data: { topic: topic.id } })
                }
            },
            addBarMethod (choice) {
                if (choice === 'Topic') { this.addTopic() }
                if (choice === 'SubTopic') { this.addSubTopic() }
            },
            async addTopic () {
                await this.createTopic({ mId: this.method.id }) // addNewTopic()
                this.setDirectIndicator()
                this.setIndirectIndicator()
            },
            async addSubTopic () {
                let parentTopic = this.activeTopic.id
                if (this.activeTopic.parent_topic) {
                    parentTopic = this.activeTopic.parent_topic
                }
                await this.createTopic({ mId: this.method.id, parent: parentTopic })
                // this.addNewTopic({ parent: this.currentTopic.id || this.activeTopic.parent_topic }) // this.activeTopic.parent_topic || this.activeTopic.id
                this.setDirectIndicator()
                this.setIndirectIndicator()
            },
            async refreshSidebar () {
                await this.fetchDirectIndicators({ mId: this.method.id })
                await this.fetchIndirectIndicators({ mId: this.method.id })
            },
            toggleActive (item) {
                const { objType } = item
                const topic = { id: item.topic || item.id }
                if (objType === 'topic') {
                    this.setTopic(topic)
                    this.setDirectIndicator()
                    this.setIndirectIndicator()
                } else if (objType === 'direct-indicator' && item.id !== this.activeDirectIndicator.id) {
                    console.log('check')
                    this.setDirectIndicator(item)
                    this.setIndirectIndicator()
                } else if (objType === 'indirect-indicator' && item.id !== this.activeIndirectIndicator.id) {
                    this.setIndirectIndicator(item)
                    this.setDirectIndicator()
                }
            },
            deleteActive () {
                const objType = this.activeItem.objType
                const id = this.activeItem.id
                if (objType === 'topic') {
                    this.deleteTopic({ mId: this.method.id, id })
                }
                if (objType === 'direct-indicator') {
                    this.deleteDirectIndicator({ mId: this.method.id, SuId: 0, SeId: 0, id: id })
                }
                if (objType === 'indirect-indicator') {
                    this.deleteIndirectIndicator({ mId: this.method.id, id })
                }
            },
            savingStatus (topic, status) {
                const key = topic.objType + topic.id
                this.TopicSavingStatus[key] = status
            },
            unsavedChangesChoice (choice) {
                this.unsavedChangesDialog = false
                this.discardUnsavedChanges = choice
                if (choice) {
                    this.$router.push(this.to)
                }
            }
        }
    }
</script>

<style lang="scss" scoped>
    .topicTabs {
        padding: 0px 20px 0px 20px;
        font-weight: bold;
        font-size: 20px;
        line-height: 50px;
        // background-color: #fcfcfc;
        border-right: 1px solid lightgrey;
        color: grey;
        // color: #00695C;
        // border-bottom: 3px solid #00695C;
    }
    .topicTabs:hover {
        color: #00695C;
        border-bottom: 3px solid #00695C;
    }
    .topic-add-button {
        line-height: 50px;
        padding: 0px 20px;
        width: 20px;
        font-size: 18px;
        font-weight: bold;
    }
    .topic-add-button:hover {
        color: #00695C;
        font-size: 22px;
        border-radius: 40%;
    }
    .topic-remove-button {
        font-size: 16px;
        padding-left: 10px;
    }
    .topic-remove-button:hover {
        color: red;
    }
</style>
