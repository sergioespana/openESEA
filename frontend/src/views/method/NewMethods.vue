<template>
    <div class="p-d-flex p-grid p-jc-center p-m-0" style="min-width: 800px">
        <div class="p-col-12 p-p-3" style="background-color: #dcedc8;">
            <h1>{{method.name}}</h1>
            <h3>{{method.description}}</h3>
            <div class="p-d-flex p-ai-center p-jc-center p-text-bold">
                <span>Public: <i class="pi p-text-center" :class="{'true-icon pi-check-circle': method.ispublic, 'false-icon pi-times-circle': !method.ispublic}"></i></span>
                <p class="p-mx-5">Version: {{method.version}}</p>
                <p class="p-mr-5">Surveys: {{method.surveys.length}}</p>
                <p>Created by: {{method.created_by}}</p>
            </div>
            <div class="p-col-12 p-d-flex p-jc-between p-p-5">
                <SelectButton v-model="MethodDisplayToggleValue" :options="MethodDisplayToggleOptions" optionLabel="name" />
                <Button icon="pi pi-external-link" label="Download as PDF" class="p-button-info" @click="exportMethod($event)" :disabled="true" />
            </div>
        </div>
        <TabView v-if="MethodDisplayToggleValue.value === 1" class="p-col-12 p-m-0">
            <TabPanel v-for="survey in method.surveys" :key="survey.id" :header="survey.name">
                <h4 class="p-text-left">Name: <span class="p-text-light">{{survey.name}}</span></h4>
                <h4 class="p-text-left">Description: <span class="p-text-light">{{survey.description}}</span></h4>
                <h4 class="p-text-left">Stakeholdergroup: <span class="p-text-light">{{survey.stakeholdergroup}}</span></h4>
                <h4 class="p-text-left">Required Responserate: <span class="p-text-light">{{survey.min_threshold*100}}%</span></h4>
                <h4 class="p-text-left">Response Type: <span class="p-text-light">{{survey.response_type}}</span></h4>
                <h4 class="p-text-left">Anonymous: <i class="pi p-text-center" :class="{'true-icon pi-check-circle': survey.ispublic, 'false-icon pi-times-circle': !survey.ispublic}"></i></h4>

                <h4 v-if="survey.welcome_text?.length" class="p-text-left">Welcome Message: <span class="p-text-light">{{survey.welcome_text}}</span></h4>
                <h4 v-if="survey.closing_text?.length" class="p-text-left">Closing Message: <span class="p-text-light">{{survey.closing_text}}</span></h4>
                <h2>Sections</h2>
                <Divider />
                <div v-if="survey.sections?.length">
                <div v-for="section in survey.sections" :key="section.id" class="p-shadow-2 p-p-3 p-my-5" style="background-color: #F1F1F1;">
                    <h3>{{section.title}}</h3>
                    <h4 class="p-text-left">Questions</h4>
                    <Divider />
                    <div v-for="question in section.questions" :key="question.id" class="p-text-left p-shadow-0 p-px-5 p-py-3 p-my-3" style="background-color: white; border: 1px solid grey;">
                        <h3 class="p-text-center"><span class="p-text-bold"></span> {{question.name}}</h3>
                        <div class="p-grid p-ai-center">
                            <div class="p-col-fixed p-text-bold" style="width:150px;">
                                Description:
                            </div>
                            <div class="p-col">
                                "{{question.description}}"
                            </div>
                        </div>
                        <div class="p-grid p-ai-center">
                            <div class="p-col-fixed p-text-bold" style="width:150px;">
                                Instruction:
                            </div>
                            <div class="p-col">
                                "{{question.instruction}}"
                            </div>
                        </div>
                        <div class="p-grid p-ai-center">
                            <div class="p-col-fixed p-text-bold" style="width:150px;">
                                UI Component:
                            </div>
                            <div class="p-col">
                                "{{question.uiComponent}}"
                            </div>
                        </div>
                        <span class="p-text-bold">Indicator:</span>
                        <div class="p-my-3 p-p-3" style="background-color: #F8F8F8; border: 1px solid lightgrey;">
                            <div class="p-grid p-ai-center">
                                <div class="p-col-fixed p-text-bold" style="width:150px;">
                                    Name:
                                </div>
                                <div class="p-col">
                                    "{{question.direct_indicator[0].name}}"
                                </div>
                            </div>
                            <div class="p-grid p-ai-center">
                                <div class="p-col-fixed p-text-bold" style="width:150px;">
                                    Description:
                                </div>
                                <div class="p-col">
                                    "{{question.direct_indicator[0].description}}"
                                </div>
                            </div>
                            <div v-if="question.direct_indicator[0].pre_unit.length" class="p-grid p-ai-center">
                                <div class="p-col-fixed p-text-bold" style="width:150px;">
                                    Pre_unit:
                                </div>
                                <div class="p-col">
                                    "{{question.direct_indicator[0].pre_unit}}"
                                </div>
                            </div>
                            <div v-if="question.direct_indicator[0].post_unit.length" class="p-grid p-ai-center">
                                <div class="p-col-fixed p-text-bold" style="width:150px;">
                                    Post_unit:
                                </div>
                                <div class="p-col">
                                    "{{question.direct_indicator[0].post_unit}}"
                                </div>
                            </div>
                            <div v-if="question.direct_indicator[0].options.length">
                                <span class="p-text-bold">Options:</span>
                                <ul v-for="option in question.direct_indicator[0].options" :key="option.id">
                                    <li>{{option.text}}</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
                </div>
            </TabPanel>
        </TabView>
        <TabView v-else class="p-col-12">
            <TabPanel v-for="topic in method.topics" :key="topic.id" :header="topic.name">
                <h4 class="p-text-left">Name: <span class="p-text-light">{{topic.name}}</span></h4>
                <h4 class="p-text-left">Description: <span class="p-text-light">{{topic.description}}</span></h4>

                <TabView>
                    <TabPanel v-for="subtopic in topic.sub_topics" :key="subtopic.id" :header="subtopic.name">
                        <h4 class="p-text-left">Name: <span class="p-text-light">{{subtopic.name}}</span></h4>
                        <h4 class="p-text-left">Description: <span class="p-text-light">{{subtopic.description}}</span></h4>
                        <div v-if="subtopic.direct_indicators.length" class="p-shadow-2 p-p-3 p-my-5" style="background-color: #F8F8F8">
                        <h4 class="p-text-left">Direct Indicators</h4>
                        <Divider />
                         <div v-for="direct_indicator in subtopic.direct_indicators" :key="direct_indicator.id" class="p-text-left p-shadow-0 p-px-5 p-py-3 p-my-3" style="background-color: white; border: 1px solid grey;">
                        <h3 class="p-text-center"><span class="p-text-bold"></span> {{direct_indicator.name}}</h3>
                        <div class="p-grid p-ai-center">
                            <div class="p-col-fixed p-text-bold" style="width:150px;">
                                Question:
                            </div>
                            <div class="p-col">
                                "{{direct_indicator.question_name}}"
                            </div>
                        </div>
                        <div class="p-grid p-ai-center">
                            <div class="p-col-fixed p-text-bold" style="width:150px;">
                                Description:
                            </div>
                            <div class="p-col">
                                "{{direct_indicator.description}}"
                            </div>
                        </div>
                        <div class="p-grid p-ai-center">
                            <div class="p-col-fixed p-text-bold" style="width:150px;">
                                Datatype:
                            </div>
                            <div class="p-col">
                                "{{direct_indicator.datatype}}"
                            </div>
                        </div>
                        <div class="p-grid p-ai-center">
                            <div class="p-col-fixed p-text-bold" style="width:150px;">
                                Pre_unit:
                            </div>
                            <div class="p-col">
                                "{{direct_indicator.pre_unit}}"
                            </div>
                        </div>
                        <div class="p-grid p-ai-center">
                            <div class="p-col-fixed p-text-bold" style="width:150px;">
                                Post_unit:
                            </div>
                            <div class="p-col">
                                "{{direct_indicator.post_unit}}"
                            </div>
                        </div>
                        <div v-if="direct_indicator.options.length">
                                <span class="p-text-bold">Options:</span>
                                <ul v-for="option in direct_indicator.options" :key="option.id">
                                    <li>{{option.text}}</li>
                                </ul>
                            </div>
                         </div>
                        </div>
                    </TabPanel>
                </TabView>

                    <!-- <div class="p-my-3 p-p-3" style="background-color: #F8F8F8; border: 1px solid lightgrey;">
                        <div class="p-grid p-ai-center">
                            <div class="p-col-fixed p-text-bold" style="width:150px;">
                                Name:
                            </div>
                            <div class="p-col">
                                "{{direct_indicator.name}}"
                            </div>
                        </div>
                        <div class="p-grid p-ai-center">
                            <div class="p-col-fixed p-text-bold" style="width:150px;">
                                Description:
                            </div>
                            <div class="p-col">
                                "{{direct_indicator.description}}"
                            </div>
                        </div>
                        <div v-if="direct_indicator.pre_unit.length" class="p-grid p-ai-center">
                            <div class="p-col-fixed p-text-bold" style="width:150px;">
                                Pre_unit:
                            </div>
                            <div class="p-col">
                                "{{direct_indicator.pre_unit}}"
                            </div>
                        </div>
                        <div v-if="direct_indicator.post_unit.length" class="p-grid p-ai-center">
                            <div class="p-col-fixed p-text-bold" style="width:150px;">
                                Post_unit:
                            </div>
                            <div class="p-col">
                                "{{direct_indicator.post_unit}}"
                            </div>
                        </div>
                        <div v-if="direct_indicator.options.length">
                            <span class="p-text-bold">Options:</span>
                            <ul v-for="option in direct_indicator.options" :key="option.id">
                                <li>{{option.text}}</li>
                            </ul>
                        </div>
                    </div>
                </div> -->
            </TabPanel>
        </TabView>

    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
    created () {
        this.initialize()
    },
    data () {
        return {
            MethodDisplayToggleValue: { name: 'Surveys', value: 1 },
            MethodDisplayToggleOptions: [
                { name: 'Surveys', value: 1 },
                { name: 'Topics', value: 0 }
            ]
        }
    },
    computed: {
        ...mapState('method', ['method'])
    },

    methods: {
        ...mapActions('method', ['fetchMethod']),
        async initialize () {
            await this.fetchMethod({ id: this.method?.id })
        },
        exportMethod () {
            // Export Method to PDF
        }
    }
}
</script>
