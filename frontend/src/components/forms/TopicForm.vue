<template>
    <form v-if="active" ref="form" class="p-d-flex p-m-0 p-fluid p-text-left"
        :style="[(active) ? 'border: 2px solid #9ecaed;':'border: 1px solid lightgrey;', (valid) ? '': 'border: 2px solid rgba(255, 0, 0, 0.5);']"> <!-- @submit.prevent="!v$.$invalid" -->
        <!-- {{activeTopic}} <hr> {{topic}} <hr> {{activeTopic}} {{v$.$invalid}} -->
        <div class="p-pl-2" style="width: 40px;">
            <ProgressSpinner v-if="(loading && !failedToUpDate)" style="width: 35px;"/>
            <i v-else-if="!valid" class="pi pi-refresh p-d-flex p-jc-center p-ai-center" style="font-size: 30px; height: 100%; color: #ff6666; cursor: pointer;" @click="updateThisTopic()" />
            <i v-if="valid" class="pi pi-check p-d-flex p-jc-center p-ai-center" style="font-size: 30px; height: 100%; color: #9ecaed;" /> <!-- rgba(0, 153, 51, 1) -->
        </div>
        <div class="p-grid" style="width: 100%;">
            <div class="p-pl-3 p-pt-3" style="width: 90%;">
                <div class="p-field">
                    <span class="p-float-label">
                        <InputText id="topicname" ref="input" v-model.lazy="lazyTopic.name" :placeholder="nameLabel" :class="{'borderless': nameErrors.length }" @blur="v$.lazyTopic.name.$touch()" />
                    </span>
                    <div class="p-error p-text-italic" v-for="error in nameErrors" :key="error"><small>{{error}}</small></div>
                </div>
                <div class="p-field">
                    <span class="p-float-label">
                        <InputText v-model.lazy="lazyTopic.description" placeholder="Topic Description" class="p-inputtext-sm" @blur="v$.lazyTopic.description.$touch()" />
                    </span>
                    <div class="p-error p-text-italic" v-for="error in descriptionErrors" :key="error"><small>{{error}}</small></div>
                </div>
            </div>
            <i class="pi pi-trash p-d-flex p-jc-center p-ai-center" style="width: 10%; font-size: 30px; color: #ff6666; cursor: pointer;" @click="removeTopic()" />
        </div>
                <!-- <i class="pi pi-ellipsis-v" style="font-size: 30px; cursor: not-allowed;" <div class="p-d-flex p-ai-center p-jc-end"> /> -->
    </form>
    <topic-card v-else :name="lazyTopic.name" :description="lazyTopic.description" :is-sub-topic="!isMainTopic" :style="[(!v$.lazyTopic.$invalid && lazyTopic.id > 0) ? 'border: 1px solid green;': 'border: 1px solid rgba(255, 0, 0, 0.3);']" />
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { isEqual } from 'lodash'
import HandleValidationErrors from '../../utils/HandleValidationErrors'
import { required, maxLength } from '../../utils/validators'
import useVuelidate from '@vuelidate/core'
import TopicCard from '../../components/cards/TopicCard'
import ProgressSpinner from 'primevue/progressspinner'

export default {
    emits: [''],
    components: {
        TopicCard,
        ProgressSpinner
    },
    props: {
        topic: {
            type: Object,
            required: true
        },
        active: {
            type: Boolean,
            default: false
        },
        errors: {
            type: Object,
            default: () => ({})
        },
        checkSavingStatus: {
            type: Boolean
        }
    },
    setup: () => ({ v$: useVuelidate() }),
    validations: {
        lazyTopic: {
            name: { required, maxLength: maxLength(120) }, // $lazy: true
            description: { maxLength: maxLength(255) }
        }
    },
    data () {
        return {
            lazyTopic: { ...this.topic } || {},
            loading: false,
            failedToUpDate: false
        }
    },
    computed: {
        ...mapState('topic', { activeTopic: 'topic' }),
        isMainTopic () {
            return !this.lazyTopic.parent_topic
        },
        nameLabel () {
            return this.isMainTopic ? 'Topic name' : 'Sub topic name'
        },
        nameErrors () {
            return HandleValidationErrors(
                this.v$.lazyTopic.name,
                this.errors.name
            )
        },
        descriptionErrors () {
            return HandleValidationErrors(
                this.v$.lazyTopic.description,
                this.errors.description
            )
        },
        valid () {
            return (!this.v$.lazyTopic.$invalid && (this.lazyTopic.id > 0) && this.uptodate)
        },
        uptodate () {
            return (isEqual(this.topic, this.lazyTopic))
        }
    },
    watch: {
        topic (val) {
            this.loading = false
            if (isEqual(this.lazyTopic, val)) { return }
            this.lazyTopic = { ...val }
        },
        lazyTopic: {
            handler (val) {
                this.failedToUpDate = false
            setTimeout(() => {
                if (isEqual(this.topic, this.lazyTopic) && this.lazyTopic.id > 0) { return }
                this.v$.lazyTopic.$touch()
                if (this.v$.lazyTopic.$invalid) { return }
                this.updateThisTopic()
                }, 200)
            },
            deep: true
        },
        active (val) {
            this.v$.lazyTopic.$touch()
        },
        checkSavingStatus (val) {
            this.$emit('savingstatus', this.v$.lazyTopic.$invalid)
        }
    },
    methods: {
        ...mapActions('topic', ['updateTopic', 'deleteTopic']),
        async updateThisTopic () {
            this.loading = true
            this.failedToUpDate = false
            setTimeout(() => { this.failedToUpDate = true }, 5000)
            await this.updateTopic({
                mId: this.$route.params.id,
                topic: this.lazyTopic
            })
        },
        updateName () {
            this.v$.lazyTopic.name.$touch()
        },
        updateDescription () {
            this.v$.lazyTopic.description.$touch()
        },
        async removeTopic () {
            await this.deleteTopic({ mId: this.$route.params.id, id: this.lazyTopic.id })
            this.$emit('refreshsidebar', true)
        }
    }
}
// else {
//     this.$nextTick(() => this.$refs.input && this.$refs.input.focus())
// }
// mounted () {
//     if (!this.activeTopic.name) {
//         this.$refs.topicname.focus()
//     }
// },
// initialize () {
// if (this.activeTopic.name === 'topic') {
//     const name = this.activeTopic.parent_topic ? 'subtopic' : 'topic'
//     this.activeTopic.name = `Untitled ${name}`
// }
// },
// @focus="$event.target.select()"
</script>

<style lang="scss" scoped>
.p-inputtext {
    border: none;
    border-bottom: 1px solid lightgrey;
}
.borderless {
    border-bottom: 1px solid red;

}
</style>
