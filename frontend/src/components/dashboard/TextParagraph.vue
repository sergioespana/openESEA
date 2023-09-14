<template>
    <div class="text-paragraph" v-on:click="isClicked" :style="styleObject">
        <span v-if="textParagraphTitle !== null && textParagraphTitle !== undefined">
            <b>{{ textParagraphTitle }}</b>
        </span>
        <br>
        <span v-if="textParagraphText !== null && textParagraphText !== undefined">
            {{ textParagraphText }}
        </span>
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
    props: {
        config: { type: Object, required: true }
    },
    computed: {
        textParagraphTitle: {
            get () { return this.getTextParagraphTitle()(this.config) }
        },
        textParagraphText: {
            get () { return this.getTextParagraphText()(this.config) }
        },
        position: {
            get () { return this.getTextParagraphPosition()(this.config) }
        },
        styleObject () {
            var styleObject = {}
            const position = this.position
            if (position) {
                styleObject.position = 'absolute'
                styleObject.left = position['X Start'].toString() + '%'
                styleObject.right = (100 - position['X End'].toString()) + '%'
                styleObject.bottom = position['Y Start'].toString() + '%'
                styleObject.top = (100 - position['Y End'].toString()) + '%'
            }
            return styleObject
        }
    },
    methods: {
        ...mapGetters('dashboardModel', ['getTextParagraphTitle', 'getTextParagraphText', 'getTextParagraphPosition']),
        ...mapActions('dashboardModel', ['updateSelectionConfig']),
        async isClicked (event) {
            event.stopPropagation()
            console.log('Clicked!')
            await this.updateSelectionConfig(this.config)
        }
    }
}
</script>
