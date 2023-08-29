<template>
    <div class="flex flex-column">

        <!-- Edit area title -->
        <div class="edit-area-title">Container</div>

        <!-- Add Container -->
        <div :style="{ height: '5px' }"></div>

        <div class="full-width" :style="{ position: 'relative', width: '100%' }">
            <Button label="Add Container" icon="pi pi-plus" class="p-button-success p-button-sm"
                @click="addContainer">
            </Button>
        </div>

        <div :style="{ height: '5px' }"></div>

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
                <InputNumber class="near-width" :maxFractionDigits="2" :min="0" :max="100"
                    v-model="containerXStart">
                </InputNumber>
                <InputNumber class="near-width" :maxFractionDigits="2" :min="0" :max="100"
                    v-model="containerXEnd">
                </InputNumber>
                <InputNumber class="near-width" :maxFractionDigits="2" :min="0" :max="100"
                    v-model="containerYStart">
                </InputNumber>
                <InputNumber class="near-width" :maxFractionDigits="2" :min="0" :max="100"
                    v-model="containerYEnd">
                </InputNumber>
            </div>

            <!-- Background Color -->
            <div class="edit-area-field">
                Background Color:
                <InputSwitch
                    v-model="hasBackgroundColor"
                    @click="initializeBackgroundColor">
                </InputSwitch>
            </div>
            <div>
                <ColorPicker v-if="hasBackgroundColor" class="near-width"
                    v-model="containerBackgroundColor">
                </ColorPicker>
            </div>

            <!-- Delete Container -->
            <div :style="{ height: '5px' }"></div>

            <div class="full-width" :style="{ position: 'relative', width: '100%' }">
                <Button label="Delete Container" icon="pi pi-trash" class="p-button-danger p-button-sm" @click="deleteContainer">
                </Button>
            </div>

            <div :style="{ height: '5px' }"></div>
        </div>
    </div>
</template>

<script>
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'

import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import InputSwitch from 'primevue/inputswitch'
import ColorPicker from 'primevue/colorpicker'

export default {
    components: {
        InputText,
        InputNumber,
        InputSwitch,
        ColorPicker
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
        },
        containerBackgroundColor: {
            get () { const color = this.getContainerBackgroundColor()(); console.log(color); return color },
            set (value) { this.updateContainerBackgroundColor({ value: '#' + value }) }
        },
        hasBackgroundColor: {
            get () { return !(!this.containerBackgroundColor) }
        }
    },
    methods: {
        ...mapGetters('dashboardModel', ['getContainerTitle', 'getContainerXStart', 'getContainerXEnd', 'getContainerYStart', 'getContainerYEnd', 'getContainerBackgroundColor']),
        ...mapMutations('dashboardModel', ['setContainerTitle', 'setContainerXStart', 'setContainerXEnd', 'setContainerYStart', 'setContainerYEnd']),
        ...mapActions('dashboardModel', ['addContainer', 'deleteContainer', 'updateContainerBackgroundColor']),
        initializeBackgroundColor () {
            this.updateContainerBackgroundColor({ value: this.hasBackgroundColor ? null : '#ffffff' })
        }
    }
}
</script>
