<template>
    <div class="flex flex-column">

        <!-- Edit area title -->
        <div class="edit-area-title">Suggestions</div>
        <div v-if="dashboardSuggestions === null || dashboardSuggestions === undefined || dashboardSuggestions.length === 0">
            <div class="edit-area-field">Waiting for suggestions...</div>
        </div>
        <div v-else>
            <div class="edit-area-field">Suggestions: </div>
            <div class="edit-area-style"></div>
            <div v-for="(item, index) in dashboardSuggestions"
                :key="index">
                <div :style="(() => { if (clicked === index) return { 'background-color': '#ffffff' } })()"
                    v-on:click="this.clicked = this.clicked === index ? null : index; if (this.clicked) { this.showAction(item) } else { this.resetAction() }">
                    <div>Visualisation: {{ item?.['Visualisation Title'] }}</div>
                    <div>Action: {{ item?.['Type'] }}</div>
                    <div v-if="item?.['Item Limit']">Item Limit: {{ item?.['Item Limit'] }}</div>
                    <div v-if="item?.['Visualisation Type']">Visualisation Type: {{ item?.['Visualisation Type'] }}</div>
                </div>
                <!-- <div v-if="item?.['Selection Configuration']">Selection Configuration: {{ item?.['Selection Configuration'] }}</div> -->
            <div class="edit-area-style"></div>
            </div>
        </div>
    </div>
</template>

<script>
import { cloneDeep } from 'lodash'

import { mapState, mapGetters, mapMutations } from 'vuex'

export default {
    computed: {
        ...mapState('dashboardModel', 'dashboard'),
        dashboardSuggestions: {
            get () { return this.getDashboardSuggestions() }
        }
    },
    data () {
        return {
            oldDashboard: null,
            clicked: null
        }
    },
    methods: {
        ...mapGetters('dashboardSuggestions', ['getDashboardSuggestions']),
        ...mapMutations('dashboardModel', ['setCategoryLimit', 'setVisualisationType']),
        async resetAction () {
            console.log('reset')
            this.dashboard = cloneDeep(this.oldDashboard)
            this.oldDashboard = null
        },
        async showAction (action) {
            console.log('do action')
            console.log(action)
            const actionType = action?.Type
            var payload = action['Selection Configuration']
            // Save old dashboard
            if (this.oldDashboard === null) {
                this.oldDashboard = cloneDeep(this.dashboard)
            }
            // Perform action
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
                    await this.setVisualisationType(payload)
                    break
                default:
                    break
            }
        }
    }
}
</script>
