// http://localhost:8081/organisation/1/overview/
// A specific Organisation's subpages are also part of this component, as you can see <router-view/> on line 14. e.g. http://localhost:8080/organisation/1/overview/

<template>
    <div class="p-grid p-m-0 p-p-0" style="height: 100%;">
        <div class="p-col-fixed p-m-0 p-p-0" style="height: 100%;">
            <sub-sidebar :links="links" />
        </div>
        <div class="p-col">
            <div class="p-col-12 p-text-left p-text-italic p-m-0 p-px-5" v-if="!this.$route.path.endsWith('dashboards')">
                <p>{{organisation.name}}</p>
                <h3>{{pagename || this.$route.meta.breadcrumb[this.$route.meta.breadcrumb.length-1].label}}</h3>
            </div>
            <router-view />
        </div>
    </div>
</template>

<script>
    import { mapState } from 'vuex'
    import SubSidebar from '../../components/SubSidebar'

    export default {
        components: {
        SubSidebar
        },
        data () {
            return {
                links: [
                    {
                        name: 'Overview',
                        icon: 'pi pi-desktop',
                        path: 'organisationoverview'
                    },
                    {
                        name: 'Networks',
                        icon: 'pi pi-cloud',
                        path: 'organisationnetworks'
                    },
                    {
                        name: 'Esea Accounts',
                        icon: 'pi pi-book',
                        path: 'organisationeseaaccounts'
                    },
                    {
                        name: 'Reports',
                        icon: 'pi pi-chart-bar',
                        path: 'organisationreports'
                    },
                    {
                        name: 'Dashboards',
                        icon: 'pi pi-chart-line',
                        path: 'organisationdashboards'
                    },
                    {
                        name: 'Team',
                        icon: 'pi pi-users',
                        path: 'organisationteam'
                    },
                    {
                        name: 'Settings',
                        icon: 'pi pi-cog',
                        path: 'organisationsettings'
                    }
                ]
            }
        },
        computed: {
            ...mapState('organisation', ['organisation'])
        },
        methods: {
            goToPage (name) {
                this.pagename = name
                this.$router.push({ name: `organisation${name.toLowerCase()}`, params: { OrganisationId: this.organisation?.id } })
            }
        }
    }
</script>
