<template>
    <div class="p-text-left p-px-5 p-shadow-2"> <!-- #dcdcdc"> -->
        <h3 v-if="isSubTopic">
            <span class="p-text-light p-text-italic">{{ name || 'No name'}}</span>
        </h3>
        <h2 v-else>
            <span class="p-text-light p-text-italic">{{ name || 'No name' }}</span>
        </h2>
        <p v-if="description">
            Description: {{ description }}
        </p>
    </div>
</template>

<script>
export default {
    props: {
        name: {
            type: String,
            required: true
        },
        description: {
            type: String,
            default: undefined
        },
        isSubTopic: {
            type: Boolean,
            default: false
        }
    }
}
</script>
// style="border-bottom: 2px solid lightgrey; background-color: #f1f1f1;"
