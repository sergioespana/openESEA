<template>
    <div class="p-grid p-jc-center p-text-center p-p-5">
        <h1 class="p-col-12">Method Creation Options</h1>
                <Divider />
        <div v-for="option in creationOptions" :key="option.action" class="p-col-4 p-jc" style="width: 400px; height: 250px;">
            <div :class="option.hover ? 'p-shadow-10 p-p-1' : 'p-shadow-3 p-m-1'" style="background-color: #F1F1F1; border: 1px solid lightgrey; height: 100%;" :style="option.hover ? 'background-color: white; cursor: pointer;': 'background-color: #EDEDED;'" @mouseover="option.hover=true" @mouseleave="option.hover=false" @click="createNewMethod(option.action)">
                <div style="height: 50%;">
                    <h3>{{option.title}}</h3>
                    <p class="p-m-5 p-text-justify">{{option.description}}</p>
                </div>
                <!-- <Button :label="option.button" @click="createNewMethod(option.action)" class="p-button-lg p-button-outlined p-m-5" style="width: 80%;" /> -->
            </div>
        </div>
    </div>
    <Dialog v-model:visible="createMethodDialog" :style="{width: '450px'}" header="Create Method" :modal="true" :dismissableMask="true" class="p-fluid">
        <method-form @closedialog="createMethodDialog = false" />
    </Dialog>
        <!-- <div class="p-field">
            <label for="name">Name</label>
            <InputText id="name" v-model.trim="method.name" required="true" autofocus :class="{'p-invalid': submitted && !method.name}"
            @blur="updateMethodForm({ name: $event.target.value })" />
            <small class="p-error" v-if="submitted && !method.name">Name is required.</small>
        </div>
        <div class="p-field">
            <label for="description">Description</label>
            <Textarea id="description" v-model="method.description" required="true" rows="3" cols="20"
            @blur="updateMethodForm({ description: $event.target.value })" />
        </div>
        <div class="p-field">
            <label for="ispublic">Should this method be public? </label>
            <SelectButton id="ispublic" v-model="method.ispublic" required="true" :options="ispublicbool"
            @blur="updateMethodForm({ ispublic: $event.target.value })" />
        </div> -->
    <Dialog v-model:visible="uploadMethodDialog" :style="{width: '700px'}" header="Upload Method" :modal="true" :dismissableMask="true">
        <FileUpload name="myfile" :customUpload="true" @uploader="onUpload" :fileLimit="1" accept=".txt" :maxFileSize="10000000" class="p-jc-between">
            <template #empty>
                <p>Drag and drop your Text file here to upload.</p>
            </template>
        </FileUpload>
        <template #footer>
            <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="uploadMethodDialog = false"/>
        </template>
    </Dialog>
    <Dialog v-model:visible="copyMethodDialog" :style="{width: '700px'}" header="Copy Method" :modal="true" :dismissableMask="true">
        <p> In the near future it will be possible to copy a method instance, including its related objects to be able to modify it freely without being the owner.</p>
    </Dialog>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import MethodForm from '../../components/forms/createMethodForm'
import { AxiosInstance } from '../../plugins/axios'
import store from '../../store'

export default {
    components: {
        MethodForm
    },
    data () {
        return {
            createMethodDialog: false,
            uploadMethodDialog: false,
            copyMethodDialog: false,
            creationOptions: [
                {
                    title: 'Upload a Method',
                    description: 'Pick this option if you have a .yaml file which can be used as a model. You can modify this later through the editor.',
                    button: 'Upload Method',
                    action: 'upload'
                },
                {
                    title: 'Create a Method',
                    description: 'Pick this option if you don\'t have a model that can be imported directly. You\'ll be able to create the method manually.',
                    button: 'Create Method',
                    action: 'create'
                },
                {
                    title: 'Copy a Method',
                    description: 'Pick this option if you want to copy a publicly available method to be able to modify it freely.',
                    button: 'Copy Method',
                    action: 'copy'
                }
            ]
        }
    },
    computed: {
        ...mapState('method', ['method'])
    },
    methods: {
        ...mapActions('method', ['fetchMethod', 'createMethod']),
        ...mapActions('authentication', ['refreshAccessToken']),
        async createNewMethod (action) {
            console.log(action)
            if (action === 'upload') {
                this.uploadMethodDialog = true
            } else if (action === 'create') {
                // this.createMethodDialog = true
                await this.createMethod({})
                this.$router.push({ name: 'method-general', params: { id: this.method.id } })
            } else if (action === 'copy') {
                this.copyMethodDialog = true
            }
        },
        async onUpload (event) {
            await this.refreshAccessToken()
            for (const file of event.files) {
                console.log(file)
            }
            var formData = new FormData()
            formData.append('file', event.files[0])

            const config = {
                headers: {
                    'Content-type': 'application/json',
                    Authorization: `Bearer ${store.getters['authentication/AuthenticationToken']}`
                }
            }
            return new Promise((resolve, reject) => {
                AxiosInstance.post('/import-method/', formData, config)
                .then(response => {
                    const id = response?.data?.id
                    this.goToMethod(id)
                    console.log(response)
                     this.$toast.add({ severity: 'success', summary: 'Method created', detail: 'New method', life: 3000 })
                })
                .catch(console.log)
            })
        },
        async goToMethod (id) {
            await this.fetchMethod({ id: id })
            this.$router.push({ name: 'method-general', params: { id: this.method?.id } })
        }
    }
}
</script>
