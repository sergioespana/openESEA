<template>
    <Splitter style="height: 100%;">
        <SplitterPanel :size="70" minSize="30" class="p-d-flex p-flex-column">
            <div style="background-color: white; width: 100%;">
                <div class="p-d-flex p-ai-center" @click="goToAuditAudit">
                    <i class="pi pi-angle-left p-mx-3" style="fontSize: 2rem"></i>
                    <h4>Responses</h4>
                </div>
            </div>
            <div class="p-d-flex p-flex-column p-jc-between p-my-5" style="width: 100%; height: 100%;">
                    <Paginator :rows="10"></Paginator>
                    <Galleria :value="images" :responsiveOptions="responsiveOptions" :numVisible="5" containerStyle="max-width: 90%; margin: 0px auto;" class="p-mt-auto"
                        :showThumbnails="false" :showIndicators="true">
                        <template #item="slotProps">
                            <img :src="slotProps.item.itemImageSrc" :alt="slotProps.item.alt" style="width: 100%; display: block;" />
                        </template>
                    </Galleria>
                </div>
        </SplitterPanel>
        <SplitterPanel :size="30" minSize="25" style="display: flex;">
            <div class="p-d-flex p-flex-column" style="height: 100%; width: 100%;">
                <h2>{{indicator.name}}</h2>
                <Accordion :multiple="true" class="accordion-custom">
                    <AccordionTab header="Response Information">
                        <div v-for="list in lists" :key="list.item" class="p-grid p-m-0 p-px-2 p-text-left" style="border: 1px solid #E9E9E9;">
                            <div class="p-col p-mr-2" style="border-right-width: 1px; border-right-color: #E9E9E9; border-right-style: solid;">
                                {{list.item}}
                            </div>
                            <div class="p-col">
                                <div v-if="list.item === 'Recommendation'">
                                    <Tag v-if="list.info" severity="danger" value="Recommendation"></Tag>
                                    <span v-else>None</span>
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
</template>

<script>
    import { mapState } from 'vuex'
    import Splitter from 'primevue/splitter'
    import SplitterPanel from 'primevue/splitterpanel'
    import Paginator from 'primevue/paginator'
    import Galleria from 'primevue/galleria'
    import Accordion from 'primevue/accordion'
    import AccordionTab from 'primevue/accordiontab'
    import Tag from 'primevue/tag'

    export default {
        components: {
            Splitter,
            SplitterPanel,
            Paginator,
            Galleria,
            Accordion,
            AccordionTab,
            Tag
        },
        data () {
            return {
                uploadDocumentationDialog: false,
                images: [{ alt: 'Image 1' }, { alt: 'Image 2' }, { alt: 'Image 3' }], // 'What is the total number of men staff?',
                documents: [{ name: 'employee_db_excerpt.png' }, { name: 'employee_db.xslx' }]
            }
        },
        computed: {
            ...mapState('auditIndicators', ['indicator']),
            lists () {
                return ([{ item: 'Question', info: this.indicator.name }, { item: 'Response', info: this.indicator.value }, { item: 'Message to Organisation', info: this.indicator.message }, { item: 'Comment', info: this.indicator.comment }, { item: 'Recommendation', info: true }])
            }
        },
        methods: {
            goToAuditAudit () {
                console.log('go to auditaudit')
                this.$router.push({ name: 'singleauditaudit', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } })
            },
            changeAuditStatus (status) {
                console.log('change auditstatus to', status)
            }
        }
    }
</script>
