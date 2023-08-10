<template>
    <div class="flex flex-column">

        <!-- Edit area title -->
        <div class="edit-area-title">Container</div>

        <!-- If no container selected, display this message -->
        <div v-if="containerId === null">
            <div class="edit-area-field">Select a Container to display its information!</div>
        </div>
        <!-- Otherwise display container information -->
        <div v-else>
            <!-- Title -->
            <div class="edit-area-field">Title:</div>
            <InputText class="near-width"
                v-model="containerTitle">
            </InputText>

            <!-- Position -->
            <div class="edit-area-field">
                Position:
                <i v-on:click="showPosition = !showPosition">
                    <i v-if="showPosition" class="pi pi-angle-up"></i>
                    <i v-else class="pi pi-angle-down"></i>
                </i>
            </div>
            <div v-if="showPosition">
                <InputNumber class="near-width"
                    v-model="containerXStart">
                </InputNumber>
                <InputNumber class="near-width"
                    v-model="containerXEnd">
                </InputNumber>
                <InputNumber class="near-width"
                    v-model="containerYStart">
                </InputNumber>
                <InputNumber class="near-width"
                    v-model="containerYEnd">
                </InputNumber>
            </div>
        </div>
    </div>
</template>

<script>
import { mapState, mapGetters, mapMutations } from 'vuex'

import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'

export default {
    components: {
        InputText,
        InputNumber
    },
    data () {
        return {
            showPosition: false
        }
    },
    computed: {
        ...mapState('dashboardModel', ['selectionConfig']),
        containerId: {
            get () { return this.selectionConfig?.containerId ?? null }
        },
        containerTitle: {
            get () { return this.getContainerTitle()() },
            set (value) { this.setContainerTitle({ value: value }) }
        },
        containerXStart: {
            get () { return this.getContainerXStart()() },
            set (value) { this.setContainerXStart({ value: value }) }
        },
        containerXEnd: {
            get () { return this.getContainerXEnd()() },
            set (value) { this.setContainerXEnd({ value: value }) }
        },
        containerYStart: {
            get () { return this.getContainerYStart()() },
            set (value) { this.setContainerYStart({ value: value }) }
        },
        containerYEnd: {
            get () { return this.getContainerYEnd()() },
            set (value) { this.setContainerYEnd({ value: value }) }
        }
    },
    methods: {
        ...mapGetters('dashboardModel', ['getContainerTitle', 'getContainerXStart', 'getContainerXEnd', 'getContainerYStart', 'getContainerYEnd']),
        ...mapMutations('dashboardModel', ['setContainerTitle', 'setContainerXStart', 'setContainerXEnd', 'setContainerYStart', 'setContainerYEnd'])
    }
}
</script>
