<template>
    <div class="flex flex-column">

        <!-- Edit area title -->
        <div class="edit-area-title">Suggestions</div>
        <div v-if="recommendations === null || recommendations === undefined || recommendations.length === 0">
            <div class="edit-area-field">Waiting for suggestions...</div>
        </div>
        <div v-else>
            <!-- <div class="edit-area-field">Suggestions: </div> -->
            <div class="edit-area-style"></div>
            <div v-for="(item, index) in recommendations"
                :key="index">
                <div :style="(() => { if (clicked === index) return { 'background-color': '#ffffff' } })()">
                    <!-- v-on:click="toggleRecommendation(index)"> -->
                    <div><i>{{ item?.['Type'] }}</i></div>
                    <div>Visualisation: <i>{{ item?.['Visualisation Title']}}</i></div>
                    <div v-if="item?.['Item Limit']">Item Limit: <i>{{ item?.['Item Limit'] }}</i></div>
                    <div v-if="item?.['Visualisation Type']">Visualisation Type: <i>{{ item?.['Visualisation Type'] }}</i></div>
                    <div>
                        <Button label="Preview" icon="pi pi-search"
                            @click="toggleRecommendation(index)" text>
                        </Button>
                        <Button label="Dismiss" icon="pi pi-times" class="p-element p-button-rounded p-button-danger p-button p-component"
                            @click="dismissSuggestion(index)" text>
                        </Button>
                        <Button label="Accept" icon="pi pi-check" class="p-element p-button-rounded p-button-success p-button p-component"
                            @click="acceptSuggestion(index)" text>
                        </Button>
                    </div>
                </div>
                <!-- <div v-if="item?.['Selection Configuration']">Selection Configuration: {{ item?.['Selection Configuration'] }}</div> -->
            <div class="edit-area-style"></div>
            </div>
        </div>
    </div>
</template>

<script>
import { cloneDeep } from 'lodash'

import { mapGetters, mapMutations, mapActions } from 'vuex'

export default {
    computed: {
        dashboard: {
            get () {
                return this.getDashboardModel()()
            },
            set (dashboard) {
                this.setDashboardModel({ value: dashboard })
            }
        },
        dashboardRecommendations: {
            get () {
                return this.getDashboardSuggestions()
            }
        }
    },
    watch: {
        dashboardRecommendations: {
            handler: 'updateRecommendations',
            deep: false
        }
    },
    data () {
        return {
            oldDashboard: null,
            clicked: null,
            testing: true,
            manualRecommendations: [
    {
        Type: 'Add Item Limit',
        'Visualisation Index': 1,
        'Item Limit': 3,
        Explanation: 'Action chosen because of higher rewards w.r.t.:\n\tDecluttering\tReward difference: 0.019345238095238138\tWeighted: 0.019345238095238138\n',
        'Visualisation Title': 'GHG Emissions by Scopes over Time',
        'Selection Configuration': {
            overviewId: 0,
            containerId: 0,
            visualisationId: 1
        }
    },
    {
        Type: 'Add Item Limit',
        'Visualisation Index': 0,
        'Item Limit': 3,
        Explanation: 'Action chosen because of higher rewards w.r.t.:\n\tDecluttering\tReward difference: 0.005952380952380931\tWeighted: 0.005952380952380931\n',
        'Visualisation Title': 'Water Consumption by Region over Time',
        'Selection Configuration': {
            overviewId: 0,
            containerId: 0,
            visualisationId: 0
        }
    },
    {
        Type: 'Add Item Limit',
        'Visualisation Index': 3,
        'Item Limit': 3,
        Explanation: 'Action chosen because of higher rewards w.r.t.:\n\tDecluttering\tReward difference: 0.005952380952380931\tWeighted: 0.005952380952380931\n',
        'Visualisation Title': 'Energy Consumption over Time',
        'Selection Configuration': {
            overviewId: 0,
            containerId: 0,
            visualisationId: 3
        }
    },
    {
        Type: 'Add Item Limit',
        'Visualisation Index': 9,
        'Item Limit': 3,
        Explanation: 'Action chosen because of higher rewards w.r.t.:\n\tDecluttering\tReward difference: 0.005952380952380931\tWeighted: 0.005952380952380931\n',
        'Visualisation Title': 'Employee - Contract Types',
        'Selection Configuration': {
            overviewId: 0,
            containerId: 2,
            visualisationId: 0
        }
    },
    {
        Type: 'Change Visualisation Type',
        'Visualisation Index': 3,
        'Visualisation Type': 'Table',
        Explanation: 'Action chosen because of higher rewards w.r.t.:\n',
        'Visualisation Title': 'Energy Consumption over Time',
        'Selection Configuration': {
            overviewId: 0,
            containerId: 0,
            visualisationId: 3
        }
    },
    {
        Type: 'Add Item Limit',
        'Visualisation Index': 5,
        'Item Limit': 3,
        Explanation: 'Action chosen because of higher rewards w.r.t.:\n\tDecluttering\tReward difference: 0.00952380952380949\tWeighted: 0.00952380952380949\n',
        'Visualisation Title': 'Board Diversity - Age',
        'Selection Configuration': {
            overviewId: 0,
            containerId: 1,
            visualisationId: 1
        }
    }
],
            recommendations: this.testing ? this.manualRecommendations : []
        }
    },
    created () {
        this.recommendations = this.testing ? this.manualRecommendations : []
    },
    methods: {
        ...mapGetters('dashboardSuggestions', ['getDashboardSuggestions']),
        ...mapGetters('dashboardModel', ['getDashboardModel', 'getDataConfiguration']),
        ...mapMutations('dashboardModel', ['setCategoryLimit', 'setDashboardModel']),
        ...mapActions('dashboardModel', ['changeVisualisationType']),
        async updateRecommendations () {
            if (!this.testing) {
                this.recommendations = this.dashboardRecommendations
            } else {
                // this.recommendations = this.manualRecommendations
            }
        },
        async acceptSuggestion (index) {
            // Reset previous action if this is still shown
            await this.resetDashboard()
            // Perform action on real dashboard
            const action = await this.getSuggestion(index)
            await this.performAction(action)
            // Remove the suggestion once implemented
            await this.removeSuggestion(index)
        },
        async dismissSuggestion (index) {
            // Reset previous action if this is still shown
            await this.resetDashboard()
            // Remove the suggestion
            await this.removeSuggestion(index)
        },
        async removeSuggestion (index) {
            // Remove recommendation at index
            this.recommendations.splice(index, 1)
        },
        async getSuggestion (index) {
            return this.recommendations[index]
        },
        async toggleRecommendation (index) {
            // Determine which item is wanted
            this.clicked = this.clicked === index ? null : index
            // Show action if clicked
            await this.showAction(index)
        },
        async showRecommendation (index) {
            // Set current item to
            this.clicked = index
            // Show the clicked action
            await this.showAction(index)
        },
        async showAction (index) {
            // Reset previous action if this is still shown
            await this.resetDashboard()
            // If an action is clicked show this action
            if (this.clicked !== null) {
                // Save old dashboard if we want to reset
                await this.saveDashboard()
                // Perform action on temp dashboard
                const action = await this.getSuggestion(index)
                await this.performAction(action)
            }
            // Wait such that the action is performed
            await this.$nextTick()
        },
        async resetDashboard () {
            // Reset to old dashboard
            if (this.oldDashboard !== null && this.oldDashboard !== undefined) {
                this.dashboard = await cloneDeep(this.oldDashboard)
            }
            // Set the old dashboard after resetting
            this.oldDashboard = null
        },
        async saveDashboard () {
            // Save dashboard into old dashboard
            if (this.oldDashboard === null || this.oldDashboard === undefined) {
                this.oldDashboard = await cloneDeep(this.dashboard)
            }
        },
        async performAction (action) {
            // Get selection config from action
            var payload = action['Selection Configuration']
            // Perform action
            const actionType = action?.Type
            switch (actionType) {
                case 'Add Item Limit':
                    payload.value = action['Item Limit']
                    await this.setCategoryLimit(payload)
                    break
                case 'Remove Item Limit':
                    payload.value = null
                    await this.setCategoryLimit(payload)
                    break
                case 'Change Visualisation Type':
                    payload.value = action['Visualisation Type']
                    await this.changeVisualisationType(payload)
                    break
                default:
                    break
            }
        },
        async getText (action) {
            // Get selection config from action
            const selectionConfig = action['Selection Configuration']
            const dataConfiguration = await this.getDataConfiguration()(selectionConfig)
            var field = null
            field = dataConfiguration?.['Value Field']
            if (field?.Name) { return field.Name }
            field = dataConfiguration?.['Fractional Value Field']
            if (field?.Name) { return field.Name }
            field = dataConfiguration?.['Current Value Field']
            if (field?.Name) { return field.Name }
            field = dataConfiguration?.['Value Fields']?.[0]
            return 'Unknown'
        }
    }
}
</script>
