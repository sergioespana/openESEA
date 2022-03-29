<template>
    <Splitter style="height: 100%;">
        <SplitterPanel :size="70" :minSize="50" class="p-d-flex p-flex-column">
            <div style="background-color: white; width: 100%;">
                <div class="p-d-flex p-ai-center" @click="goToAuditAudit">
                    <i class="pi pi-angle-left p-mx-3" style="fontSize: 2rem"></i>
                    <h4>Responses</h4>
                </div>
            </div>
            <div class="p-d-flex p-flex-column p-jc-between p-my-5" style="width: 100%;">
                    <Galleria :value="images" :responsiveOptions="responsiveOptions" :numVisible="5" containerStyle="max-width: 90%; height: 100%; margin: auto auto; padding-top: 20%;" class=""
                        :showThumbnails="false" :showIndicators="true">
                        <template #item="slotProps">
                            <!-- {{slotProps.item.itemImageSrc}} -->
                            <!-- <img :src="slotProps.item.itemImageSrc" :alt="slotProps.item.alt" style="width: 100%; display: block;" /> -->
                            <img v-if="slotProps.item.alt === 'Image 1'" alt="documentation example 1" src="@/assets/documentation_example_1.png" style="width: 100%; height: 100%:">
                            <img v-if="slotProps.item.alt === 'Image 2'" alt="documentation example 2" src="@/assets/documentation_example_2.png" style="width: 100%; margin: 100px;">
                            <img v-if="slotProps.item.alt === 'Image 3'" alt="documentation example 3" src="@/assets/documentation_example_3.png" style="width: 100%; margin: 100px;">
                        </template>
                    </Galleria>
                    <!-- <img alt="logo" src="@/assets/tasklist.png" class="p-m-5" style="height: 400px;"> -->
                </div>
        </SplitterPanel>
        <SplitterPanel :size="30" :minSize="25" style="display: flex;">
            <div class="p-d-flex p-flex-column" style="height: 100%; width: 100%;">
                <h2>{{indicator.name}}</h2>
                <Accordion :multiple="true" class="accordion-custom">
                    <AccordionTab header="Response Information">
                        <div v-for="list in lists" :key="list.item" class="p-grid p-m-0 p-px-2 p-text-left" style="border: 1px solid #E9E9E9;">
                            <div class="p-col p-mr-2" style="border-right-width: 1px; border-right-color: #E9E9E9; border-right-style: solid;">
                                {{list.item}}
                            </div>
                            <div class="p-col">
                                <div v-if="list.item === 'Critical Impact' || list.item === 'anomaly'">
                                    <Button v-if="list.item === 'Critical Impact' && list.info === true" label="Critical" class="p-button-sm p-button-rounded p-py-1 p-button-danger" @click="openCriticalDialog()" />
                                     <Button v-if="list.item === 'anomaly' && list.info === true" label="Anomaly" class="p-button-sm p-button-rounded p-py-1 p-button-danger" @click="openCriticalDialog()" />

                                    <!-- <Tag v-if="list.info" severity="danger" value="Recommendation"></Tag> -->
                                </div>
                                <div v-else>
                                    {{list.info}}
                                </div>
                            </div>
                        </div>

                    </AccordionTab>
                    <AccordionTab>
                        <template #header>
                            <div class="p-d-flex p-jc-between" style="width: 100%;">
                                <span>Documents</span>
                                <i class="pi pi-upload" @click="uploadDocumentationDialog = true" />
                            </div>
                        </template>
                        <div v-for="document in documents" :key="document.name" class="p-d-flex p-jc-between p-p-3" style="border: 1px solid #E9E9E9;">
                            <div class="">
                                {{ document.name }}
                            </div>
                            <div>
                                <i class="pi pi-download" />
                            </div>
                        </div>
                    </AccordionTab>
                </Accordion>

                <div class="p-p-3 p-mt-auto" style="width: 300px; margin: 60px auto;">
                    <Button @click="changeAuditStatus('Verified')" label="Verify" icon="pi pi-check" class="p-button-success" style="width: 100%;" />
                    <Button @click="changeAuditStatus('Awaiting Correction')" label="Request response correction" icon="pi pi-pencil" class="p-button-warning" style="width: 100%; margin: 10px 0px;" />
                    <Button @click="changeAuditStatus('Rejected')" label="Reject" icon="pi pi-times" class="p-button-danger" style="width: 100%;" />
                </div>
            </div>
        </SplitterPanel>
    </Splitter>

    <Dialog v-model:visible="uploadDocumentationDialog" :style="{width: '700px'}" header="Upload Documentation" :modal="true" :dismissableMask="true">
        <FileUpload name="myfile" :customUpload="true" @uploader="onUpload" :fileLimit="1" :maxFileSize="10000000" class="p-jc-between">
            <template #empty>
                <p>Drag and drop your Text file here to upload.</p>
            </template>
        </FileUpload>
        <template #footer>
            <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="uploadDocumentationDialog = false"/>
        </template>
    </Dialog>

    <Dialog v-model:visible="criticalDialog" style="width: 500px;" :header="`Critical Impact: ${indicator_name}`" :modal="true" dismissableMask="true">
        <p class="p-text-justify">This Indicator was flagged as critical due to it's indirect indicator parent: <b>'{{ criticalDialogIndicator.critical_impact_by.indicator }}'</b> which has an <b>impact of '{{ criticalDialogIndicator.critical_impact_by.impact }}'</b>
        which would lower the <b>total score of '{{ criticalDialogIndicator.critical_impact_by.total_score }}'</b> to <b>'{{ (criticalDialogIndicator.critical_impact_by.total_score - criticalDialogIndicator.critical_impact_by.impact).toFixed(2) }}'</b>, which is below the <b>threshold of '{{method.certification_theshold}}'</b>.
        </p>
    </Dialog>
</template>

<script>
    import { mapState, mapActions } from 'vuex'
    import Splitter from 'primevue/splitter'
    import SplitterPanel from 'primevue/splitterpanel'
    // import Paginator from 'primevue/paginator'
    import Galleria from 'primevue/galleria'
    import Accordion from 'primevue/accordion'
    import AccordionTab from 'primevue/accordiontab'
    // import Tag from 'primevue/tag'

    export default {
        components: {
            Splitter,
            SplitterPanel,
            // Paginator,
            Galleria,
            Accordion,
            AccordionTab
            // Tag
        },
        data () {
            return {
                uploadDocumentationDialog: false, // 'What is the total number of men staff?',
                documents: [{ name: 'employee_db_excerpt.png' }, { name: 'employee_db.xslx' }],
                criticalDialogIndicator: {},
                criticalDialog: false
            }
        },
        computed: {
            ...mapState('auditIndicators', ['indicator']),
            ...mapState('method', ['method']),
            lists () {
                return ([{ item: 'Question', info: this.indicator.name }, { item: 'Status', info: this.indicator.question_response.auditstatus }, { item: 'Response', info: this.indicator.value }, { item: 'Message to Organisation', info: this.indicator.question_response.doc_request_note }, { item: 'Comment', info: this.indicator.question_response.doc_upload_note }, { item: 'Critical Impact', info: this.indicator.critical_impact }, { item: 'anomaly', info: this.indicator.outliers }])
            },
            images () {
                return [{ itemImageSrc: '@/assets/tasklist.png', thumbnailImageSrc: '@/assets/tasklist.png', alt: 'Image 1' }, { alt: 'Image 2' }, { alt: 'Image 3' }]
            },
            indicator_name () {
                if ('name' in this.criticalDialogIndicator) {
                    return this.criticalDialogIndicator.name
                } else {
                    return 'indicator'
                }
            }
        },
        methods: {
            ...mapActions('auditIndicators', ['updateIndicators']),
            ...mapActions('questionResponse', ['updateQuestionResponse']),
            goToAuditAudit () {
                console.log('go to auditaudit')
                this.$router.push({ name: 'singleauditaudit', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } })
            },
            async changeAuditStatus (status) {
                this.indicator.question_response.auditstatus = status
                this.updateIndicators(this.indicator)
                console.log('change auditstatus to', status)
                await this.updateQuestionResponse({ oId: 0, eaId: 0, id: this.indicator.question_response.id, data: this.indicator.question_response })
            },
            openCriticalDialog () {
                this.criticalDialogIndicator = this.indicator
                this.criticalDialog = true
            }
        }
    }
</script>
