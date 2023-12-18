<template>
    <div class="flex flex-column">

        <!-- Edit area title -->
        <div class="edit-area-title">Text Paragraph</div>

        <!-- Add Text Paragraph -->
        <div :style="{ height: '5px' }"></div>

        <div class="full-width" :style="{ position: 'relative', width: '100%' }">
            <Button label="Add Text Paragraph" icon="pi pi-plus" class="p-button-success p-button-sm"
                @click="addTextParagraph">
            </Button>
        </div>

        <!-- If no text paragraph selected, display this message -->
        <div v-if="textParagraphId === null">
            <div class="edit-area-field">Select a Text Paragraph to display its information!</div>
        </div>
        <!-- Otherwise display text paragraph information -->
        <div v-else>
            <!-- Title -->
            <div class="edit-area-field">Title:</div>
            <InputText class="near-width"
                v-model="textParagraphTitle">
            </InputText>
            <!-- Text -->
            <div class="edit-area-field">Text:</div>
            <InputText class="near-width"
                v-model="textParagraphText">
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
                    v-model="textParagraphXStart">
                </InputNumber>
                <InputNumber class="near-width"
                    v-model="textParagraphXEnd">
                </InputNumber>
                <InputNumber class="near-width"
                    v-model="textParagraphYStart">
                </InputNumber>
                <InputNumber class="near-width"
                    v-model="textParagraphYEnd">
                </InputNumber>
            </div>
        </div>

        <!-- Delete Text Paragraph -->
        <div :style="{ height: '5px' }"></div>

        <div class="full-width" :style="{ position: 'relative', width: '100%' }">
            <Button label="Delete Text Paragraph" icon="pi pi-trash" class="p-button-danger p-button-sm" @click="deleteTextParagraph">
            </Button>
        </div>

        <div :style="{ height: '5px' }"></div>
    </div>
</template>

<script>
import { mapState, mapGetters, mapMutations, mapActions } from 'vuex'

export default {
    components: {
    },
    data () {
        return {
            showPosition: false
        }
    },
    computed: {
        ...mapState('dashboardModel', ['selectionConfig']),
        textParagraphId: {
            get () { return this.selectionConfig.textParagraphId ?? null }
        },
        textParagraphTitle: {
            get () { return this.getTextParagraphTitle()() },
            set (value) { this.setTextParagraphTitle({ value: value }) }
        },
        textParagraphText: {
            get () { return this.getTextParagraphText()() },
            set (value) { this.setTextParagraphText({ value: value }) }
        },

        textParagraphXStart: {
            get () { return this.getTextParagraphXStart()() },
            set (value) { this.setTextParagraphXStart({ value: value }) }
        },
        textParagraphXEnd: {
            get () { return this.getTextParagraphXEnd()() },
            set (value) { this.setTextParagraphXEnd({ value: value }) }
        },
        textParagraphYStart: {
            get () { return this.getTextParagraphYStart()() },
            set (value) { this.setTextParagraphYStart({ value: value }) }
        },
        textParagraphYEnd: {
            get () { return this.getTextParagraphYEnd()() },
            set (value) { this.setTextParagraphYEnd({ value: value }) }
        }
    },
    methods: {
        ...mapGetters('dashboardModel', [
            'getTextParagraphTitle', 'getTextParagraphText',
            'getTextParagraphXStart', 'getTextParagraphXEnd', 'getTextParagraphYStart', 'getTextParagraphYEnd'
        ]),
        ...mapMutations('dashboardModel', [
            'setTextParagraphTitle', 'setTextParagraphText',
            'setTextParagraphXStart', 'setTextParagraphXEnd', 'setTextParagraphYStart', 'setTextParagraphYEnd'
        ]),
        ...mapActions('dashboardModel', ['addTextParagraph', 'deleteTextParagraph']) // Add / Delete
    }
}
</script>
