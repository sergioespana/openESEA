<template>
    <div :id="topLevelId()">
    </div>
</template>

<script>
    // import createElement from '../../utils/createElement.js'

    export default {
        name: 'Visualisation',
        props: {
            yamlData: {
                type: Object,
                required: true
            },
            overviewId: {
                type: Number,
                required: true
            },
            containerId: {
                type: Number,
                required: true
            },
            visualisationId: {
                type: Number,
                required: true
            }
        },
        mounted () {
            this.updateElements()
        },
        methods: {
            topLevelId () {
                return 'overview_' + this.overviewId + '_container_' + this.containerId + '_visualisationId_' + this.visualisationId
            },
            updateElements () {
                const overviewId = this.overviewId
                const containerId = this.containerId
                this.$nextTick(() => {
                    console.log(overviewId, containerId)
                })
            }
        }
    }
</script>

<style>
</style>
