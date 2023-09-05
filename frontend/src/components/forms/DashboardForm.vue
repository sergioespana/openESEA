// used by OrganisationDashboards.vue

<template>
    <form id="dashboardform" @submit.prevent="createNewEseaMethod" class="p-input-filled p-fluid p-text-left">
        <div class="p-field">
            <label for="methods">Methods<span style="color:red">*</span></label>
            <MultiSelect id="methods" v-model="dashboardform.methods" :options="methods" optionLabel="name" placeholder="Select ESEA Methods" :class="{'p-invalid': v$.dashboardform.methods.$error}" />
        </div>
        <div class="p-field p-m-0">
            <label for="Name">Name</label>
            <InputText id="name" v-model="dashboardform.name"></InputText>
        </div>

        <div class="p-d-flex p-jc-between p-mt-5">
            <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="closeDialog" style="width: 100px" />
            <Button label="Create" icon="pi pi-check" class="p-button-text" type="submit" form="dashboardform" :disabled="v$.dashboardform.$error" style="width: 100px" />
        </div>
    </form>
</template>

<script>
    import useVuelidate from '@vuelidate/core'
    import { required } from 'vuelidate/lib/validators'

    import MultiSelect from 'primevue/multiselect'
    import InputText from 'primevue/inputtext'

    import { mapActions, mapState } from 'vuex'

    export default {
        components: {
            MultiSelect,
            InputText
        },
        data () {
            return {
                dashboardform: {
                    methods: [],
                    name: null
                }
            }
        },
        computed: {
            ...mapState('method', ['methods']),
            ...mapState('dashboard', ['dashboard, dashboards'])
        },
        setup: () => ({ v$: useVuelidate() }),
        validations: {
            dashboardform: {
                methods: { required },
                name: { required }
            }
        },
        async created () {
            await this.fetchMethods({})
        },
        methods: {
            ...mapActions('method', ['fetchMethods']),
            ...mapActions('dashboard', ['createDashboard']),
            async createNewEseaMethod () {
                this.v$.dashboardform.$touch()
                if (this.v$.$invalid) { return }
                const data = {
                    Name: this.dashboardform.name,
                    Methods: this.dashboardform.methods.map((method) => method.id),
                    Overviews: [{ Name: 'New Overview' }]
                }
                await this.createDashboard({ data: data })
                this.$emit('dashboardCreated')
                if (this.dashboard.id) {
                    this.$router.push({ name: 'organisationdashboard', params: { DashboardId: this.dashboard.id } })
                }
            },
            closeDialog () {
                this.$emit('closedialog')
            }
        }
    }
</script>
