<template>
    <div class="flex flex-column">

        <!-- Edit area title -->
        <div class="edit-area-title">Suggestions</div>
        <div class="edit-area-field">Suggestions: </div>
        <div v-if="dashboardSuggestions === []">
            <div class="edit-area-field">No suggestions as of yet!</div>
        </div>
        <div v-else>
            <div v-for="(item, index) in dashboardSuggestions"
                :key="index"> {{ item }}
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
    computed: {
        dashboardSuggestions: {
            get () { return this.getDashboardSuggestions() }
        }
    },
    methods: {
        ...mapGetters('dashboardSuggestions', ['getDashboardSuggestions'])
    }
}
</script>
