// http://localhost:8081/organisation/1/dashboard/

<template>
    <div style="min-width: 1000px;">
    <DashboardList @goToSelectedDashboard="goToDashboard">
    <Button v-if="permission" label="Create Dashboard" icon="pi pi-plus" class="p-button-success p-button-sm" @click="createDashboardDialog = true" />
    </DashboardList>
    </div>

    <Dialog v-model:visible="createDashboardDialog" style="width: 700px" header="Dashboard Details" :modal="true" :dismissableMask="true">
        <DashboardForm @dashboardCreated="loadDashboard" @closedialog="createDashboardDialog = false" />
    </Dialog>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex'

    import DashboardList from '../../components/lists/DashboardList.vue'
    import DashboardForm from '../../components/forms/DashboardForm.vue'

    export default {
        components: {
            DashboardList,
            DashboardForm
        },
        data () {
            return {
                createDashboardDialog: false
            }
        },
        computed: {
            ...mapState('dashboard', ['dashboard', 'dashboards']),
            ...mapState('organisation', ['organisation']),
            permission () {
                if (this.organisation.accesLevel) {
                    const accesLevel = this.organisation.accesLevel
                    if (accesLevel === 'admin' || accesLevel === 'organisation admin') {
                        return true
                    }
                }
                return false
            }
        },
        async created () {
            await this.fetchDashboards()
        },
        methods: {
            ...mapGetters('dashboard', ['getDashboard']),
            ...mapActions('dashboard', ['setDashboard', 'fetchDashboards', 'createDashboard']),
            async createNewDashboard () {
                // create dashboard and retrieve id
                const data = { Name: 'New Dashboard' }

                await this.createDashboard({ data: data }) // this sets current dashboard to the newly created one
                const dashboard = await this.getDashboard()
                await this.navigateToDashboard(dashboard)
            },
            async goToDashboard (dashboard) {
                await this.setDashboard(dashboard)
                await this.loadDashboard()
            },
            async loadDashboard () {
                // console.log(this.dashboard?.id)
                this.$router.push({ name: 'organisationdashboard', params: { DashboardId: this.dashboard?.id } })
            }
            // ,
            // async dialogClosed () {
            //     this.createDashboardDialog = false
            //     await this.createNewDashboard()
            // }
        }
    }
</script>
