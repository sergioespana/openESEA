<template>
    <div class="p-grid p-m-5">
        <div class="p-col-12 p-d-flex p-ai-center p-jc-between">
            <h2 class="p-text-left">Documentation Upload</h2>
            <Button @click="(helpDialog = !helpDialog)" label="Help" class="p-button-sm p-button-warning" icon="pi pi-external-link" />
        </div>
        <DataTable class="p-col-12 p-m-0 p-p-0" :value="selectedIndicators" rowGroupMode="rowspan" groupRowsBy="section.name" sortMode="single" sortField="section.name" :sortOrder="1" responsiveLayout="scroll"
        v-model:expandedRowGroups="expandedRowGroups" @rowgroupExpand="onRowGroupExpand" @rowgroupCollapse="onRowGroupCollapse" dataKey="name">
            <Column field="topic" header="Topic"></Column>
            <Column field="name" header="Name" sortable></Column>
            <Column field="value" header="Value" sortable></Column>
            <Column field="message" header="Message" />
            <Column headerStyle="width: 10rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                <template #body="row">
                    <Button label="Comment" icon="pi pi-plus" class="p-button-sm p-button-success" @click="openComment(row.data)" />
                </template>
            </Column>
            <Column headerStyle="width: 10rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                <template #body="">
                    <Button label="Upload" icon="pi pi-upload" class="p-button-sm p-button-warning" @click="uploadDocumentationDialog = true" />
                </template>
            </Column>
        </DataTable>
        <div class="p-text-right p-col-12">
            <Button class="p-my-5" label="Submit" icon="pi pi-check" />
        </div>

    </div>

    <Dialog v-model:visible="helpDialog" style="width: 500px;" header="Help" :modal="true" dismissableMask="true">
        <p>Your auditor has requested documentation on the listed questions. Please provide documentation that supports your question responses.</p>
        <template #footer>
            <Button label="Ok" icon="pi pi-check" @click="(helpDialog = !helpDialog)" />
        </template>
    </Dialog>

    <Dialog v-model:visible="messageToAuditorDialog" style="width: 500px;" header="Message to Auditor" :modal="true" dismissableMask="true">
        <Textarea class="p-col-12" id="description" v-model="comment" :autoResize="true" rows="3" />
        <template #footer>
            <Button label="Cancel" class="p-button-sm" icon="pi pi-times" @click="(messageToAuditorDialog = false)" />
            <Button label="Save" class="p-button-sm p-button-success" icon="pi pi-check" @click="saveMessage()" />
        </template>
    </Dialog>

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

    export default {
        data () {
            return {
                helpDialog: false,
                messageToAuditorDialog: false,
                uploadDocumentationDialog: false,
                comment: '',
                CommentedIndicator: null,
                questions: [
                    {
                        name: 'What is the total number of men staff?',
                        response: 5,
                        recommendations: '',
                        section: { name: 'Gender' }
                    },
                    {
                        name: 'What is the total number of women staff?',
                        response: 7,
                        recommendations: '',
                        section: { name: 'Gender' }

                    },
                    {
                        name: 'What is the average monthly salary per employee?',
                        response: '$4000',
                        recommendations: '',
                        section: { name: 'Salary' }
                    }
                ]
            }
        },
        computed: {
        ...mapState('auditIndicators', ['selectedIndicators'])
        },
        methods: {
            openComment (indicator) {
                this.CommentedIndicator = indicator
                this.messageToAuditorDialog = true
            },
            saveMessage () {
                console.log('saving message')
                this.CommentedIndicator.comment = this.comment
                this.selectedIndicators = this.selectedIndicators.map((item) => {
                if (item.id !== this.CommentedIndicator.id) { return item }
                return Object.assign(item, this.CommentedIndicator)
            })
            this.messageToAuditorDialog = false
            },
            // Needs to be rewritten to the appropriate backend endpoint/location!
            async onUpload (event) {
                    // await this.refreshAccessToken()
                    // for (const file of event.files) {
                    //     console.log(file)
                    // }
                    // var formData = new FormData()
                    // formData.append('file', event.files[0])

                    // const config = {
                    //     headers: {
                    //         'Content-type': 'application/json',
                    //         Authorization: `Bearer ${store.getters['authentication/AuthenticationToken']}`
                    //     }
                    // }
                    // return new Promise((resolve, reject) => {
                    //     AxiosInstance.post('/some-place/', formData, config)
                    //     .then(response => {
                    //         const id = response?.data?.id
                    //         this.goToMethod(id)
                    //         console.log(response)
                    //         this.$toast.add({ severity: 'success', summary: 'Method created', detail: 'New method', life: 3000 })
                    //     })
                    //     .catch(console.log)
                    // })
            }
        }
    }
</script>
