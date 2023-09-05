<template>
    <div class="flex flex-column">

        <!-- Edit area title -->
        <div class="edit-area-title">Text Paragraph</div>

        <!-- If no text paragraph selected, display this message -->
        <div v-if="imageId === null">
            <div class="edit-area-field">Select a Text Paragraph to display its information!</div>
        </div>
        <!-- Otherwise display text paragraph information -->
        <div v-else>
            <div class="edit-area-field">Text Paragraph information</div>
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    components: {
    },
    computed: {
        ...mapState('dashboardModel', ['selectionConfig']),
        textParagraphId: {
            get () { return this.selectionConfig.textParagraphId ?? null }
        }
    },
    created () {
        // console.log(this.selectionConfig?.textParagraphId)
    }
}
</script>
