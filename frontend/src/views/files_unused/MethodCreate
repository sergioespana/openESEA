<template>
<div style="height: calc (100vh - 500px;); display: flex; flex-direction: column; background-color: lightgrey;">
    <!-- <method-form :method="method" @input="updateMethod($event)" style="box-shadow: rgba(0, 0, 0, 0.16) 0px 0px 6px, rgba(0, 0, 0, 0.23) 0px 3px 6px; z-index: 0;" /> --> <!-- #f7f7f7 #e6f3ff-->  <!-- @click.native="toggleActive(topic)" @click="toggleActive(subTopicChild)-->
    <div class="p-d-flex" style="height: calc(100vh -300px); border-top: 1px solid lightgrey;">
        <div class="p-d-flex p-flex-column p-jc-between" style="height: calc(100vh - 140px); width: 300px; border: 1px solid lightgrey; background-color: white;">
            <method-tree-sidebar />
            <Button label="Open ESEA Method Creation Guide" class="p-button-info p-button-lg p-p-5" />
        </div>
        <div class="p-m-4" style="width: 100%; height: calc(100vh - 200px); background-color: white; overflow-y: scroll;">
            <div class="p-d-flex" style="height: 50px; background-color: #f6f6f6; border-bottom: 2px solid lightgrey;">
                <div v-for="(topic, topicIndex) in methodTopics" :key="`topic_${topicIndex}`" class="topicTabs" @click="switchTopic(topic)" @dblclick="changeName(topic.edit = true)" :style="(currentTopic.id === topic.id) ? 'border-bottom: 3px solid #00695C; color: #00695C;':''">
                    <InputText v-if="topic.edit" v-model="topic.name" @blur="(topic.edit=false && this.saveActive('topic', topic))" /> <span v-else>{{topic.name}}</span> <icon class="topic-remove-button pi pi-times" @click="removeTopic(topic)" />
                </div>
                <i class="pi pi-plus topic-add-button" @click="addTopic" />
            </div>
            <div class="p-m-5 p-d-flex p-ai-center p-field p-fluid">
                <label for="networkadmin" class="p-mr-2">Description</label>
                <InputText v-if="currentTopic" v-model="currentTopic.description" />
            </div>
            <!-- {{currentTopic}} {{activeTopic}} <hr> {{items.children}} -->
            <div v-if="Object.getOwnPropertyNames(currentTopic).length > 0"> <!-- Object.getOwnPropertyNames(currentTopic).length > 0" -->
                <div v-for="(topicChild, index) in items.children" :key="`topicChild_${index}`">
                    <div class="p-m-5" :class="(topicChild?.children?.length ? 'p-pb-2': 'p-p-0')" style="background-color: #fcfcfc; border: 1px solid lightgrey;">
                        <component :is="`${topicChild.objType}-form`" :errors="errors[topicChild.objType] && errors[topicChild.objType][topicChild.id]" ref="items" :topic="topicChild" :question="topicChild" :direct-indicator="topicChild" :indirect-indicator="topicChild" :active="activeItem.objType === topicChild.objType && activeItem.id === topicChild.id" @input="saveActive(topicChild.objType, $event)" @click="toggleActive(topicChild)" @delete="deleteActive(topicChild.objType, $event)" />
                        <div v-for="(subTopicChild, idx) in topicChild.children" :key="`subTopicChild-${idx}`">
                            <component :is="`${subTopicChild.objType}-form`" ref="items" :errors="errors[subTopicChild.objType] && errors[subTopicChild.objType][subTopicChild.id]" :topic="subTopicChild" :question="subTopicChild" :direct-indicator="subTopicChild" :indirect-indicator="subTopicChild"  :active="activeItem.objType === subTopicChild.objType && activeItem.id === subTopicChild.id" @input="saveActive(subTopicChild.objType, $event)"  @click="toggleActive(subTopicChild)" @delete="deleteActive(subTopicChild.objType, $event)" class="p-ml-5" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- <div class="p-col p-d-flex p-jc-center" style="height: calc(100vh - 135px); text-align: center; overflow-y: scroll;">
            <div class="p-m-2 p-text-left p-fluid" style="width: 1200px;">
                 <div v-for="(topic, topicIndex) in items" :key="`topic-${topicIndex}`" style="background-color: #fcfcfc; border: 1px solid lightgrey;">
                    <topic-form ref="items" :topic="topic" :active="activeItem.objType === topic.objType && activeItem.id === topic.id" @input="saveActive('topic', $event)" @click="toggleActive(topic)" />
                    <div v-for="(topicChild, index) in topic.children" :key="`topicChild-${index}`" >
                        <div class="p-m-5" :class="(topicChild?.children?.length ? 'p-pb-2': 'p-p-0')" style="background-color: #fcfcfc; border: 1px solid lightgrey;">
                            <component :is="`${topicChild.objType}-form`" :errors="errors[topicChild.objType] && errors[topicChild.objType][topicChild.id]" ref="items" :topic="topicChild" :question="topicChild" :direct-indicator="topicChild" :indirect-indicator="topicChild" :active="activeItem.objType === topicChild.objType && activeItem.id === topicChild.id" @input="saveActive(topicChild.objType, $event)" @click=" toggleActive(topicChild)" />
                            <div v-for="(subTopicChild, index) in topicChild.children" :key="`subTopicChild-${index}`">
                                <component :is="`${subTopicChild.objType}-form`" ref="items" :errors="errors[subTopicChild.objType] && errors[subTopicChild.objType][subTopicChild.id]" :topic="subTopicChild" :question="subTopicChild" :direct-indicator="subTopicChild" :indirect-indicator="subTopicChild"  :active="activeItem.objType === subTopicChild.objType && activeItem.id === subTopicChild.id" @input="saveActive(subTopicChild.objType, $event)"  @click="toggleActive(subTopicChild)" class="p-ml-5" />
                            </div>
                        </div>
                    </div>
                </div>
                <Button label="Add New Topic" icon="pi pi-plus" class="p-col-12 p-button-text p-text-left p-p-5 p-mb-5" @click="addTopic" />
            </div>
        </div> -->
        <div class="p-d-flex p-ai-center p-shadow-5" style="position: fixed; top: 35%; right: 0px; width: 100px; background-color: #fcfcfc; border: 2px solid grey;">
            <div>
                <div v-for="option in addBar" :key="option.choice" class="p-d-flex p-jc-center p-ai-center" style="height: 100px; width: 100px; border: 1px solid lightgrey" :style="(option.hover ? 'background-color: lightgrey;' : '')" @mouseover="option.hover=true" @mouseleave="option.hover=false" @click="addBarMethod(option.choice)">
                    <div>
                        <i :class="option.icon? option.icon : 'pi pi-plus'" />
                        <p class="p-text-italic p-m-2">{{option.choice}}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<!-- Method creation wizard -->
<!-- {{subTopicChild}} {{index}} {{activeItem.objType === subTopicChild.objType}}  {{ activeItem.id === subTopicChild.id }} -->
<!-- <indicator-form v-if="subTopicChild.objType === 'indicator'" :active="true" :direct-indicator="subTopicChild" @click="checker" /> -->
<!-- <Button label="Add Question" icon="pi pi-plus" class="p-button-text p-text-left p-p-5" @click="addQuestion()" /> -->
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
import MethodTreeSidebar from '../../components/MethodTreeSideBar'
// import MethodForm from '../../components/forms/MethodForm'
import TopicForm from '../../components/forms/TopicForm'
// import QuestionForm from '../../components/forms/QuestionForm'
import IndicatorForm from '@/components/forms/IndicatorForm'
import CalculationForm from '../../components/forms/CalculationForm'
// import getMethodItems from '../../utils/getMethodItems'
import getTopicItems from '../../utils/getTopicItems'

export default {
    components: {
        MethodTreeSidebar,
        // MethodForm,
        TopicForm,
        // QuestionForm,
        IndicatorForm,
        CalculationForm
    },
    data () {
        return {
            currentTopic: this.items || null,
            updateToolbar: 0,
            numberOfClicks: 0,
            time: null,
            addBar: [
                // { choice: 'question' },
                { choice: 'subtopic' },
                { choice: 'indicator' },
                { choice: 'calculation' },
                { choice: 'delete', icon: 'pi pi-trash' }
            ]
        }
    },
    watch: {
        currentTopic: {
            handler (val) {
                setTimeout(() => {
                    if (val && !val?.name?.length) {
                        val.name = 'Nameless Topic'
                    }
                }, 5000)
            },
            deep: true
        }
    },
    computed: {
        ...mapState('method', ['method', 'error']),
        ...mapState('topic', { topics: 'topics', activeTopic: 'topic', topicErrors: 'errors' }),
        ...mapGetters('topic', ['methodTopics', 'subTopics']),
        // ...mapState('question', { activeQuestion: 'question', questionErrors: 'errors' }),
        // ...mapGetters('question', ['topicQuestions']),
        ...mapState('directIndicator', { activeDirectIndicator: 'directIndicator', directIndicatorErrors: 'errors' }),
        ...mapGetters('directIndicator', ['topicDirectIndicators']),
        ...mapState('indirectIndicator', { activeIndirectIndicator: 'indirectIndicator', indirectIndicatorErrors: 'errors' }),
        ...mapGetters('indirectIndicator', ['topicIndirectIndicators']),
        items () {
            return getTopicItems(
                this.currentTopic, // this.methodTopics,
                this.subTopics,
                this.topicDirectIndicators,
                this.topicIndirectIndicators
            )
        },
        activeItem () {
            let objType = 'topic'
            let { id } = this.activeTopic
            if (this.activeDirectIndicator.id) {
                objType = 'indicator'
                id = this.activeDirectIndicator.id
            }
            if (this.activeIndirectIndicator.id) {
                objType = 'calculation'
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
    created () {
        if (!this.currentTopic) {
            this.currentTopic = this.methodTopics?.[0] || {}
        }
        this.initialize()
    },
    methods: {
        ...mapActions('method', ['fetchMethod', 'updateMethod', 'saveMethod']),
        ...mapActions('topic', ['fetchTopics', 'setTopic', 'createTopic', 'updateTopic', 'addNewTopic', 'deleteTopic']),
        ...mapActions('directIndicator', ['fetchDirectIndicators', 'setDirectIndicator', 'addNewDirectIndicator', 'updateDirectIndicator', 'deleteDirectIndicator']),
        ...mapActions('indirectIndicator', ['fetchIndirectIndicators', 'addNewIndirectIndicator', 'updateIndirectIndicator', 'setIndirectIndicator', 'deleteIndirectIndicator']),
        async initialize () {
            const methodId = parseInt(this.$route.params.id, 10)
            console.log(this.method.id, '&&', methodId)
            if (this.method.id !== methodId) {
                await this.fetchMethod({ id: methodId })
                if (this.error) {
                    this.$router.push({ name: 'methods' })
                }
            }
            await this.fetchTopics({ mId: this.method.id })
            await this.fetchDirectIndicators({ mId: this.method.id })
            await this.fetchIndirectIndicators({ mId: this.method.id })
            // this.toggleActive({ objType: 'topic' })
        },
        async addTopic () {
            await this.createTopic({ mId: this.method.id }) // addNewTopic()
            this.currentTopic = this.activeTopic
            this.setDirectIndicator()
            this.setIndirectIndicator()
        },
        addSubTopic () {
            this.addNewTopic({ parent: this.currentTopic.id || this.activeTopic.parent_topic }) // this.activeTopic.parent_topic || this.activeTopic.id
            this.setDirectIndicator()
            this.setIndirectIndicator()
        },
        addDirectIndicator () {
            this.addNewDirectIndicator({ topic: this.activeTopic.id })
            this.setIndirectIndicator()
        },
        addIndirectIndicator () {
            this.addNewIndirectIndicator({ topic: this.activeTopic.id })
            this.setDirectIndicator()
        },
        switchTopic (topic) {
            console.log('single clicking')
            this.currentTopic = topic
            this.setTopic(topic)
        },
        changeName (topic) {
            clearTimeout(this.time)

            console.log('double clicking')
            // const goodtopic = this.topics.find(element => element.id === topic.id )
            // if (goodtopic) {

            // }
        },
        removeTopic (topic) {
            this.deleteTopic({ mId: this.method.id, id: topic.id })
        },
        deleteChild (objType, item) {
            console.log('yeha')
            console.log(objType, item)
        },
        toggleActive (item) {
            console.log('breee')
            const { objType } = item
            const topic = { id: item.topic || item.id }
            if (objType === 'topic') {
                this.setTopic(topic)
                this.setDirectIndicator()
                this.setIndirectIndicator()
            } else if (objType === 'indicator' && item.id !== this.activeDirectIndicator.id) {
                console.log('check')
                this.setDirectIndicator(item)
                this.setIndirectIndicator()
            } else if (objType === 'calculation' && item.id !== this.activeIndirectIndicator.id) {
                this.setIndirectIndicator(item)
                this.setDirectIndicator()
            }
        },
        saveActive (type, object) {
            console.log('!!', 'type:', type, 'object:', object)
            if (object.target) { return } // Checks whether the $event contains an object or only an inputEvent
            console.log('saving object...')
            if (type === 'topic') {
                this.updateTopic({
                    mId: this.method.id,
                    topic: object
                })
            }
            if (type === 'indicator') {
                this.updateDirectIndicator({
                    mId: this.method.id,
                    directIndicator: object
                })
            }
            if (type === 'calculation') {
                console.log(';reee')
                this.updateIndirectIndicator({
                    mId: this.method.id,
                    indirectIndicator: object
                })
            }
        },
        deleteActive () {
            const objType = this.activeItem.objType
            const id = this.activeItem.id
            console.log('{{{{{', objType, id)
            // const { objType, id } = this.activeitem
            if (objType === 'topic') {
                this.deleteTopic({ mId: this.method.id, id })
            }
            if (objType === 'indicator') {
                this.deleteDirectIndicator({ mId: this.method.id, SuId: 0, SeId: 0, id: id })
            }
            if (objType === 'calculation') {
                this.deleteIndirectIndicator({ mId: this.method.id, id })
            }
        },
        addBarMethod (choice) {
            if (choice === 'question') { this.addQuestion() }
            if (choice === 'subtopic') { this.addSubTopic() }
            if (choice === 'indicator') { this.addDirectIndicator() }
            if (choice === 'calculation') { this.addIndirectIndicator() }
            if (choice === 'delete') { this.deleteActive() }
        },
        checker () {
            console.log('test')
        }
    }
}
</script>

<style lang="scss" scoped>
.p-divider {
}
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
