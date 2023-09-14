<template>
    <div class="flex flex-column">

        <!-- Edit area title -> overview -->
        <div class="edit-area-title">Overview</div>

        <div :style="{ height: '5px' }"></div>

        <div class="full-width" :style="{ position: 'relative', width: '100%' }">
            <Button label="Add Overview" icon="pi pi-plus" class="p-button-success p-button-sm"
                @click="addOverview">
            </Button>
        </div>

        <div :style="{ height: '5px' }"></div>

        <!-- Display current overview information-->
        <div v-if="overviews.length === 0">
            <div class="edit-area-field">Add an Overview to view information about the Overview</div>
        </div>
        <div v-else>
            <div class="edit-area-field">Current Overview:</div>
            <InputText class="near-width"
                v-model="overviewName">
            </InputText>
            <div class="edit-area-field">Title:</div>
            <InputText class="near-width"
                v-model="headsectionTitle">
            </InputText>
            <div class="edit-area-field">Text:</div>
            <InputText class="near-width"
                v-model="headsectionText">
            </InputText>

            <div :style="{ height: '5px' }"></div>

            <div class="full-width" :style="{ position: 'relative', width: '100%' }">
                <Button label="Delete Overview" icon="pi pi-trash" class="p-button-danger p-button-sm" @click="deleteOverview">
                </Button>
            </div>

            <div :style="{ height: '5px' }"></div>

        </div>
    </div>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from 'vuex'

import InputText from 'primevue/inputtext'

export default {
    components: {
        InputText
    },
    computed: {
        overviews: {
            get () { return this.getOverviews()() }
        },
        overviewName: {
            get () { return this.getOverviewName()() },
            set (value) { this.setOverviewName({ value: value }) }
        },
        headsectionTitle: {
            get () { return this.getHeadSectionTitle()() },
            set (value) { this.setHeadSectionTitle({ value: value }) }
        },
        headsectionText: {
            get () { return this.getHeadSectionText()() },
            set (value) { this.setHeadSectionText({ value: value }) }
        }
    },
    methods: {
        ...mapGetters('dashboardModel', ['getOverviews', 'getOverviewName', 'getHeadSectionTitle', 'getHeadSectionText']),
        ...mapMutations('dashboardModel', ['setOverviewName', 'setHeadSectionTitle', 'setHeadSectionText']),
        ...mapActions('dashboardModel', ['deleteOverview', 'addOverview'])
    }
}
</script>
