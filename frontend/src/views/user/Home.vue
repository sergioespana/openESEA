<template>
<div class="p-m-5">
<h1>Dashboard</h1>
</div>
<div class="p-grid nested-grid p-m-5 p-jc-center">
    <div class="p-col-12 p-py-5">
        <div v-if="!tasks">
            <h4>All Done!</h4>
            <p>
                None of your organisations or networks require your attention right now.
            </p>
        </div>
        <div v-else>
            <h4>The following tasks require your attention.</h4>
            <div class="p-shadow-2 p-m-3 p-p-3 p-text-left"><span class="p-text-bold">Task 1:</span> Fill in the survey of network 1.</div>
            <div class="p-shadow-2 p-m-3 p-p-3 p-text-left"><span class="p-text-bold">Task 2:</span> Reply to network participation request on network 2.</div>
        </div>
        <img alt="logo" src="../../assets/tasklist.png" class="p-m-5" style="height: 400px;">
    </div>
    <!-- <div class="p-col-1"><Divider layout="vertical" /></div>
    <div class="p-col-3">
        <div class="p-grid">
            <div class="p-col-12">
                <h3 class="p-mb-2">Your Networks</h3>
                <Divider class="p-m-0" />
                <div class="p-m-3">
                    <div v-if="networks.length">
                        <div v-for="network, num in networks" :key="network.name">
                            {{num+1}}. <router-link :to="{name: 'networkoverview', params: { NetworkId: network.id } }" style="text-decoration: none; color: blue;">{{network.name}}</router-link>
                            <Divider class="p-m-1" />
                        </div>
                    </div>
                    <div v-else>
                        <div class="p-py-5 p-text-italic">No networks to display</div>
                    </div>
                </div>
                <router-link to="/networks" style="text-decoration: none; color: blue;">View all Networks</router-link>
            </div>
            <div class="p-col-12">
                <h3 class="p-mb-2">Your Organisations</h3>
                <Divider class="p-m-0" />
                <div class="p-m-3">
                    <div v-if="organisations.length">
                        <div v-for="organisation, num in organisations" :key="organisation.name">
                            {{num+1}}. <router-link :to="{name: 'organisationoverview', params: { OrganisationId: organisation.id } }" style="text-decoration: none; color: blue;">{{organisation.name}}</router-link>
                            <Divider class="p-m-1" />
                        </div>
                    </div>
                    <div v-else>
                        <div class="p-py-5 p-text-italic">No organisations to display</div>
                    </div>
                </div>
                <router-link to="/organisations" style="text-decoration: none; color: blue;">View all organisations</router-link>
            </div>
        </div>
    </div> -->
</div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
    components: {
    },
    data () {
        return {
            org: [],
            post: {
                title: '',
                content: ''
            },
            submitted: false
        }
    },
    computed: {
    ...mapState('organisation', ['organisations']),
    ...mapState('network', ['networks'])
    },
    created () {
        this.initialize()
    },
    methods: {
        ...mapActions('network', ['fetchNetworks']),
        ...mapActions('organisation', ['fetchOrganisations']),
        ...mapActions('user', ['fetchUsers']),
        async initialize () {
            'checking it'
            await this.fetchNetworks({})
            await this.fetchOrganisations({})
            await this.fetchUsers({})
       }
    }
}
</script>
