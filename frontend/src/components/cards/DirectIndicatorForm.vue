<template>
    <div class="p-p-3 p-py-1 p-shadow-2" :style="[(hover) ? 'background-color: white;':'background-color: #F7F7F7;']" style="border: 1px solid lightgrey; width: 100%;"  @mouseover="hover=true" @mouseleave="hover=false"> <!-- #dcdcdc"> -->
        <!-- <h3 class="p-col p-text-center p-m-0">Direct Indicator - [{{directIndicator.key || 'No Key'}}]</h3> -->
        <div class="p-d-flex p-jc-between p-ai-center" style="width: 100%;">
            <div class="p-col p-d-flex p-jc-between p-ai-center">
                <div class="attribute-name p-text-left">{{ directIndicator.key || 'None' }}</div>
                <span class="value p-text-right">{{ directIndicator.datatype || 'No Datatype' }}</span>
            </div>
            <i class="pi pi-times p-d-flex p-jc-center p-ai-center p-ml-5" style="font-size: 20px; color: red; cursor: pointer;" @click="removeFromTopic()" />
        </div>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
    props: {
        directIndicator: {
            type: Object,
            required: true
        },
        active: {
            type: Boolean
        },
        valid: {
            type: Boolean,
            default: undefined
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
        ...mapActions('directIndicator', ['patchDirectIndicator']),
        async removeFromTopic () {
            await this.patchDirectIndicator({ mId: this.method.id, id: this.directIndicator.id, data: { topic: null } })
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
