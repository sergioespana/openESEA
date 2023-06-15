<template>
    <div :id="'overview_' + this.overviewId + '_bodysection'" class="body-section">
    </div>
</template>

<script>
    import createDivWrapper from '../../utils/createDivWrapper'
    import Container from './Container.vue'

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
                const containers = this.yamlData.constructor.name === 'Array' ? this.yamlData : []
                console.log(this.yamlData)
                this.$nextTick(() => {
                    var parent = document.getElementById('overview_' + this.overviewId + '_bodysection')
                    const length = containers.length
                    for (var index = 0; index < length; index++) {
                        var containerId = index
                        createDivWrapper(parent, Container, { yamlData: containers[index], overviewId: overviewId, containerId: containerId }, { id: 'wrapper_overview_' + overviewId + '_container_' + containerId })
                    }
                })
            }
        }
    }
</script>

<style>
.body-section {
    position: absolute;
    width: 100%;
    height: 100%;
}
</style>
