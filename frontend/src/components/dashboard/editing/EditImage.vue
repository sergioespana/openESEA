<template>
    <div class="flex flex-column">

        <!-- Edit area title -->
        <div class="edit-area-title">Image</div>

        <!-- If no image selected, display this message -->
        <div v-if="imageId === null">
            <div class="edit-area-field">Select an Image to display its information!</div>
        </div>
        <!-- Otherwise display image information -->
        <div v-else>
            <div class="edit-area-field">Image information</div>
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
        imageId: {
            get () { return this.selectionConfig.imageId ?? null }
        }
    },
    created () {
        // console.log(this.selectionConfig?.imageId)
    }
}
</script>
