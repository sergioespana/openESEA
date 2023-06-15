<template>
    <div :id="'overview_' + this.overviewId + '_headsection'" class="head_section">
        <h1 :id="'overview_' + this.overviewId + '_headsection_title'"></h1>
        <h1 :id="'overview_' + this.overviewId + '_headsection_text'"></h1>
    </div>
</template>

<script>
    export default {
        name: 'HeadSection',
        props: {
            yamlData: {
                type: Object,
                required: true
            },
            overviewId: {
                type: Number,
                required: true
            }
        },
        mounted () {
            this.updateElements()
        },
        methods: {
            updateElements () {
                const overviewId = this.overviewId
                const title = this.yamlData.Title || null
                const text = this.yamlData.Text || null
                this.$nextTick(() => {
                    document.getElementById(`overview_${overviewId}_headsection_title`).innerHTML = title

                    if (text) document.getElementById(`overview_${overviewId}_headsection_text`).innerHTML = text
                    else document.getElementById(`overview_${overviewId}_headsection_text`).hidden = true
                })
            }
        }
    }
</script>

<style>
.head-section {
    position: absolute;
    height: 20%; /*calc(100vh - 14px);*/
}
</style>
