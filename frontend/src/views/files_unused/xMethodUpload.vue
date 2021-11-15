// No View, maybe it can be put in 


<template>
    <div class="p-mx-5" style="min-width: 1000px;">
        <h1>Upload Method</h1>
        <FileUpload name="myfile" :customUpload="true" @uploader="onUpload" :fileLimit="1" accept=".txt" :maxFileSize="10000000">
            <template #empty>
                <p>Drag and drop your YAML file here to upload.</p>
            </template>
        </FileUpload>
    </div>
</template>

<script>
    import { mapState, mapActions } from 'vuex'
    import { AxiosInstance } from '../../plugins/axios'
    import store from '../../store'

    export default {
        data () {
            return {
                response: false
            }
        },
        computed: {
            ...mapState('method', ['method'])
        },
        methods: {
            ...mapActions('method', ['fetchMethod']),
            async onUpload (event) {
                for (const file of event.files) {
                    console.log(file)
                }
                var formData = new FormData()
                formData.append('file', event.files[0])
                // const config = { headers: { Authorization: 'Bearer ' + store.getters['authentication/AuthenticationToken'] } }
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
                console.log('--->', this.method.id)
                this.$router.push({ name: 'method-general', params: { id: this.method?.id } })
            }
        }
    }
</script>
