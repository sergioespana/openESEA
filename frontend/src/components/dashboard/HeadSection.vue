<template>
    <div class="head-section">
        <OverviewSelection
            :overviewId="this.overviewId">
        </OverviewSelection>
        <EditableText
            class="headsectiontitle"
            :hidden="headsectionTitle === null"
            :initialValue="headsectionTitle"
            :componentType="'h1'"
            @enteredValue="(value) => updateTitle(value)">
        </EditableText>
        <EditableText
            class="headsectiontext"
            :hidden="headsectionText === null"
            :initialValue="headsectionText"
            @enteredValue="(value) => updateText(value)">
        </EditableText>
    </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'

import OverviewSelection from './OverviewSelection.vue'
import EditableText from './EditableText.vue'

export default {
    name: 'HeadSection',
    components: {
        OverviewSelection,
        EditableText
    },
    props: {
        overviewId: { type: Number, required: true }
    },
    computed: {
        headsectionTitle () {
            return this.getHeadSectionTitle()(this.overviewId)
        },
        headsectionText () {
            return this.getHeadSectionText()(this.overviewId)
        }
    },
    methods: {
        ...mapGetters('dashboardModel', { getHeadSectionTitle: 'getHeadSectionTitle', getHeadSectionText: 'getHeadSectionText' }),
        ...mapMutations('dashboardModel', { setHeadSectionTitle: 'setHeadSectionTitle', setHeadSectionText: 'setHeadSectionText' }),
        updateText (text) {
            const payload = { overviewId: this.overviewId, containerId: this.containerId, visualisationId: this.visualisationId, text: text }
            this.setHeadSectionText(payload)
        },
        updateTitle (title) {
            const payload = { overviewId: this.overviewId, containerId: this.containerId, visualisationId: this.visualisationId, title: title }
            this.setHeadSectionTitle(payload)
        }
    }
}
</script>

<style>
.head-section {
    position: absolute;
    height: 25%;
    width: 100%;
}
.headsectiontitle {
    height: 50%;
    width: 100%;
}
.headsectiontext {
    top: 50%;
    height: 50%;
    width: 100%;
}
</style>
