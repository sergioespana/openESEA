<template>
    <div class="p-p-3 p-py-1 p-shadow-2" :style="[(hover) ? 'background-color: white;':'background-color: #F7F7F7;']" style="border: 1px solid lightgrey; width: 100%;" @mouseover="hover=true" @mouseleave="hover=false"> <!-- #dcdcdc"> -->
        <div class="p-d-flex p-jc-between p-jc-between p-ai-center" style="width: 100%;">
            <div class="p-col p-d-flex p-jc-between p-ai-center">
                <div class="attribute-name p-text-left">{{ indirectIndicator.key || 'None' }}</div>
                <small class="p-text-right">{{ indirectIndicator.formula || 'No Formula' }}</small>
            </div>
            <i class="pi pi-times p-d-flex p-jc-center p-ai-center p-ml-5" style="font-size: 20px; color: red; cursor: pointer;" @click="removeFromTopic()" />
        </div>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
    props: {
        indirectIndicator: {
            type: String,
            required: undefined
        }
    },
    data () {
        return {
            hover: false
        }
    },
    computed: {
        ...mapState('method', ['method'])
    },
    methods: {
        ...mapActions('indirectIndicator', ['patchIndirectIndicator']),
        async removeFromTopic () {
            await this.patchIndirectIndicator({ mId: this.method.id, id: this.indirectIndicator.id, data: { topic: null } })
        }
    }
}
</script>

<style lang="scss" scoped>
.attribute-name {
    min-width: 400px;
    margin-right: 50px;
    font-size: 16px;
    font-weight: bold;
}
.value {
    font-weight: normal;
}
</style>
