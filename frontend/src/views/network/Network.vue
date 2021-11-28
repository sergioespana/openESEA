// http://localhost:8080/network/1/
// A specific Network's subpages are also part of this component, as you can see <router-view/> on line 15. e.g. http://localhost:8080/network/1/overview/

<template>
    <div class="p-grid p-m-0 p-p-0" style="height: 100%; background-color: red;">
        <div class="p-col-fixed p-m-0 p-p-0">
            <sub-sidebar :links="links" />
        </div>
        <div class="p-col">
            <div class="p-col-12 p-text-left p-text-italic p-m-0 p-px-5">
                <p>{{network.name}}</p>
                <h3>{{pagename || this.$route.meta.breadcrumb[this.$route.meta.breadcrumb.length-1].label}}</h3>
            </div>
            <router-view />
        </div>
    </div>
</template>

<script>
    import { mapState } from 'vuex'
    import SubSidebar from '../../components/SubSidebar.vue'

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
                        path: 'networkoverview'
                    },
                    {
                        name: 'Organisations',
                        icon: 'pi pi-globe',
                        path: 'networkorganisations'
                    },
                    {
                        name: 'Methods',
                        icon: 'pi pi-file',
                        path: 'networkmethods'
                    },
                    {
                        name: 'Campaigns',
                        icon: 'pi pi-calendar',
                        path: 'networkcampaigns'
                    },
                    {
                        name: 'Team',
                        icon: 'pi pi-users',
                        path: 'networkteam'
                    },
                    {
                        name: 'Settings',
                        icon: 'pi pi-cog',
                        path: 'networksettings'
                    }
                ]
            }
        },
        computed: {
            ...mapState('network', ['network'])
        },
        methods: {
            goToPage (name) {
                this.pagename = name
                this.$router.push({ name: `network${name.toLowerCase()}`, params: { NetworkId: this.network?.id || 0 } })
            }
        }
    }
</script>
