<template>
    <form v-if="active" ref="form" class="p-fluid p-input-filled p-p-3 p-text-left" :style="[(active) ? 'border: 2px solid #9ecaed;':'border: 1px solid lightgrey;', (valid) ? '': 'border: 2px solid rgba(255, 0, 0, 0.3);']"> <!-- @submit.prevent="!v$.$invalid" -->
        {{topic}} <hr> {{lazyTopic}} {{v$.$invalid}}
        <div class="p-d-flex p-col-12">
            <h3 class="p-col p-text-center">Topic</h3>
            <div class="p-d-flex p-ai-center p-jc-end">
                <i class="pi pi-trash p-mx-5" style="font-size: 30px; color: red; cursor: pointer;" @click="removeTopic()" />
                <i class="pi pi-ellipsis-v" style="font-size: 30px; cursor: not-allowed;" />
            </div>
        </div>
        <div class="p-field">
            <span class="p-float-label">
                <InputText id="topicname" ref="input" v-model.lazy="lazyTopic.name" :placeholder="nameLabel" :class="{'borderless': nameErrors.length }" @blur="v$.lazyTopic.name.$touch()" />
            </span>
            <div class="p-error p-text-italic" v-for="error in nameErrors" :key="error"><small>{{error}}</small></div>
        </div>
        <div class="p-field">
            <span class="p-float-label">
                <InputText v-model="lazyTopic.description" placeholder="Topic Description" class="p-inputtext-sm" @blur="v$.lazyTopic.description.$touch()" />
            </span>
            <div class="p-error p-text-italic" v-for="error in descriptionErrors" :key="error"><small>{{error}}</small></div>
        </div>
    </form>
    <topic-card v-else :name="lazyTopic.name" :description="lazyTopic.description" :is-sub-topic="!isMainTopic" :style="[(!v$.lazyTopic.$invalid && lazyTopic.id > 0) ? 'border: 1px solid green;': 'border: 1px solid rgba(255, 0, 0, 0.3);']" />
</template>

<script>
import { isEqual } from 'lodash'
import HandleValidationErrors from '../../utils/HandleValidationErrors'
import { required, maxLength } from '../../utils/validators'
import useVuelidate from '@vuelidate/core'
import TopicCard from '../../components/cards/TopicCard'

export default {
    emits: [''],
    components: {
        TopicCard
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
            lazyTopic: { ...this.topic } || {}
        }
    },
    computed: {
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
            return (!this.v$.lazyTopic.$invalid && (this.lazyTopic.id > 0))
        }
    },
    watch: {
        topic (val) {
            if (isEqual(this.lazyTopic, val)) { return }
            this.lazyTopic = { ...val }
        },
        lazyTopic: {
            handler (val) {
            setTimeout(() => {
                console.log('cheeeck')
                if (this.v$.lazyTopic.$invalid) { return }
                if (isEqual(this.topic, this.lazyTopic) && this.lazyTopic.id > 0) { return }
                 console.log('cheeeck')
                this.$emit('input', val)
                }, 500)
            },
            deep: true,
            immediate: true
        },
        active (val) {
            this.v$.lazyTopic.$touch()
        }
    },
    methods: {
        updateName () {
            this.v$.lazyTopic.name.$touch()
        },
        updateDescription () {
            this.v$.lazyTopic.description.$touch()
        },
        removeTopic () {
            this.$emit('delete', this.topic)
        }
    }
}
// else {
//     this.$nextTick(() => this.$refs.input && this.$refs.input.focus())
// }
// mounted () {
//     if (!this.lazyTopic.name) {
//         this.$refs.topicname.focus()
//     }
// },
// initialize () {
// if (this.lazyTopic.name === 'topic') {
//     const name = this.lazyTopic.parent_topic ? 'subtopic' : 'topic'
//     this.lazyTopic.name = `Untitled ${name}`
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
