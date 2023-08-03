// http://localhost:8081/organisation/1/dashboard/

<template>
    <div style="min-width: 1000px;">
    <DashboardList @goToDashboard="navigateToDashboard">
    <Button v-if="permission" label="Create Dashboard" icon="pi pi-plus" class="p-button-success p-button-sm" @click="createNewDashboard" />
    </DashboardList>
    </div>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex'
    import DashboardList from '../../components/lists/DashboardList.vue'
    export default {
        components: {
            DashboardList
        },
        data () {
            return {
                styleObject: { backgroundColor: '#EFEEEE' }
            }
        },
        computed: {
            ...mapState('dashboard', ['dashboards']),
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
        methods: {
            ...mapGetters('dashboard', ['getDashboard']),
            ...mapActions('dashboard', ['setDashboard', 'createDashboard']),
            async createNewDashboard () {
                // create dashboard and retrieve id
                const data = { Name: 'New Dashboard' }

                await this.createDashboard({ data: data }) // this sets current dashboard to the newly created one
                const dashboard = await this.getDashboard()
                console.log('Created the following Dashboard:', dashboard)
                await this.navigateToDashboard(dashboard)
            },
            async navigateToDashboard (dashboard) {
                console.log('Dashboard:', dashboard)
                await this.setDashboard(dashboard)
                this.$router.push({ name: 'organisationdashboard', params: { DashboardId: dashboard.id } })
            }
        }
    }
</script>
