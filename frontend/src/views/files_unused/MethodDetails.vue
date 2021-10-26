<template>
    <div class="p-d-flex p-grid p-jc-center p-m-0">
        <div class="p-col-12 p-p-3" style="background-color: #dcedc8;">
            <h1>{{method.name}}</h1>
            <h3>{{method.description}}</h3>
        </div>
        <div v-if="method.surveys.length" class="p-grid p-col-6 p-p-3" style="min-width: 800px;">
            <div class="p-col-12 p-d-flex p-jc-between p-p-5">
            <SelectButton v-model="amountDisplayButtonValue" :options="amountDisplayButtonOptions" optionLabel="name" />
            <Button icon="pi pi-external-link" label="Download as pdf" class="p-button-info" @click="exportMethod($event)" />
            </div>
            <TabView v-if="amountDisplayButtonValue.value === 1" class="p-col-12 p-shadow-5">
                <TabPanel v-for="survey in method.surveys" :key="survey.id" :header="survey.name">
                    <h4 class="p-text-left">Name: <span class="p-text-light">{{survey.name}}</span></h4>
                    <h4 class="p-text-left">Stakeholdergroup: <span class="p-text-light">{{survey.stakeholdergroup}}</span></h4>
                    <h4 class="p-text-left">Required Responserate: <span class="p-text-light">{{survey.min_threshold}}%</span></h4>
                    <h4 v-if="survey.description" class="p-text-left">Description: <span class="p-text-light">{{survey.description}}</span></h4>

                    <div v-for="topic in survey.topics" :key="topic.id" class="p-grid p-col-12">
                        <h2 class="p-col-12">Parenttopic: <span class="p-text-light">{{topic.name}}</span></h2>

                        <div v-for="subtopic in topic.sub_topics" :key="subtopic.id" class="p-col-12 p-mb-5" style="background-color: #F8F9FA; border-radius: 10px;">
                            <h3 class="p-text-left">Topic: <span class="p-text-light">{{subtopic.name}}</span></h3>

                            <div v-for="question in subtopic.questions" :key="question.id" class="p-p-5" style="border: 1px solid lightgrey">
                                <p class="p-text-left"><span v-if="question.isMandatory" style="color: red; font-size: 25px">*</span><span class="p-text-bold">Question:</span> {{question.name}}</p>
                                <Divider />
                                <div v-if="question.answertype === 'SCALE' ||'RADIO'">
                                    <div v-for="(option, index) in question.options" :key="`${index}-option`" class="p-field-radiobutton">
                                        <RadioButton :id="`${index}-option`" name="option" :value="option[optionValueKey]" v-model="lazyValue" :disabled="readonly" required/>
                                        <label :for="`${index}-option`" class="p-text-left">{{option.text}}</label>
                                    </div>
                                </div>
                                <div v-if="question.answertype === 'CHECKBOX'">
                                    <div v-for="(option, index) in question.options" :key="`${index}-option`" class="p-field-checkbox">
                                        <Checkbox :id="`${index}-option`" name="option" :value="option[optionValueKey]" v-model="lazyValue" disabled="true" required/>
                                        <label :for="`${index}-option`" class="p-text-left">{{option.text}}</label>
                                    </div>
                                </div>
                                <div v-if="question.answertype === ('NUMBER' || 'TEXT')">
                                    <InputText type="text" :placeholder="question.answertype.toLowerCase()" disabled class="p-field-checkbox"></InputText>
                                </div>
                                <Divider />
                                <div v-if="question.description">
                                    <p class="p-text-justify p-text-light p-m-0" style="color: lightgrey;"><small>Description:</small><br>
                                    <small><small>{{question.description}}</small></small></p>
                                </div>
                                <div v-else>
                                    <p class="p-text-left p-m-0" style="color: lightgrey;"><small>No Description</small></p>
                                </div>
                            </div>
                        </div>
                    </div>
                </TabPanel>
            </TabView>
            <div v-else>
                <div v-for="indicator in method.indicators" :key="indicator.id" class="p-grid p-col-12">
                <div class="p-grid p-col-12 p-p-5" style="background-color: white; border-radius: 10px;">
                    <div class="p-d-flex p-jc-between p-col-12">
                        <h4>Topic: <span class="p-text-light p-text-italic">'{{indicator.topic}}'</span></h4>
                        <h4>Name: <span class="p-text-light p-text-italic">'{{indicator.name}}'</span></h4>
                        <h4>Key: <span class="p-text-light p-text-italic">'[{{indicator.key}}]'</span></h4>
                    </div>
                    <div v-if="indicator.formula" class="p-grid p-col-12 p-text-left p-ml-2">
                        <div class="p-grid p-col-12 p-my-2" style="border: 1px solid lightgrey;">
                            <div class="p-col-fixed p-text-bold" style="width: 150px;">Formula:</div>
                            <div class="p-col">{{indicator.formula}}</div>
                        </div>
                        <div class="p-grid p-col-12 p-text-left p-my-2" style="border: 1px solid lightgrey;">
                            <div class="p-col-fixed p-text-bold" style="width: 150px">Calculation:</div>
                            <div class="p-col">{{indicator.calculation}}</div>
                        </div>
                    </div>
                    <div class="p-col-12 p-d-flex p-jc-between">
                        <h3>{{indicator.formula? 'Indirect Indicator value': 'Direct Indicator value'}}: <span class="p-text-light p-text-italic p-ml-5">'{{decimalrounder(indicator.value) || 'No Value to Display'}}'</span></h3>
                        <Button label="Learn more about this Topic" class="p-button-info  p-button-outlined" @click="goesnowhere" />
                    </div>
                </div>
                <Divider class="p-m-5"/>
            </div>

                <h1>Indicators of the method TBC</h1>
            </div>
            <!-- <Button label="Go to surveys" class="p-button-success p-mt-4" style="width: 100%" @click="goToSurveys"/> -->
        </div>
    </div>

<!-- <div class="p-d-flex p-jc-center">
    <div>
        <div class="p-grid nested-grid" style="width: 1000px">
                  <h1 class="p-col-12">{{method.name}}</h1>
        {{method}}
            <div class="p-col-12">
                {{method.ispublic}} {{method.name}} {{method.description}} {{surveys}}
            </div>
        <Divider />
            <div class="p-col-12" v-for="topic in topics" :key="topic.id">

                <div v-if="topic.parent_topic === null" class="p-shadow-5 p-m-2 p-p-5">
                    Topic: {{topic.name}}
                    <Divider />
                    <div class="p-col-12" v-for="subtopic in topics" :key="subtopic.id">
                        <div v-if="subtopic.parent_topic === topic.id">
                         Topic: {{subtopic.name}}
                    <Divider />
                    <div v-for="question in subtopic.questions" :key="question.id">
                        <p class="p-text-left">Question: {{question.name}}</p>
                        <div v-if="question.options > 0"><h3>options</h3>
                            <div v-for="option in question.options" :key="option.id">
                                <div class="p-shadow-2 p-p-3 p-m-2">{{option.text}}</div>
                            </div>
                        </div>
                    </div>
                    </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div> -->
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
    data () {
        return {
            amountDisplayButtonValue: { name: 'Surveys', value: 1 },
            amountDisplayButtonOptions: [
                { name: 'Surveys', value: 1 },
                { name: 'Indicators', value: 0 }
                ]
        }
    },
    computed: {
        ...mapState('method', ['method']),
        ...mapState('topic', ['topics'])
    },
    created () {
        this.initialize()
    },
    methods: {
        ...mapActions('method', ['fetchMethod']),
        ...mapActions('topic', ['fetchTopics']),
        async initialize () {
            await this.fetchMethod({ id: this.method?.id })
            await this.fetchTopics({ mId: this.method.id })
        }
    }

}
</script>

<style scoped>
/* $tabviewNavBg: black; */
.p-tabview {
    border: 1px solid lightgrey;
}
.p-tabview >>> .p-tabview-panels {
    background-color: #F8F9FA;
}
>>> .p-tabview-nav {
    background-color: #F8F9FA;
}
::v-deep(.p-highlight) {
    background-color: blue;
}
</style>
