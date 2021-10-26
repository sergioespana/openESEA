<template>
    <div class="p-text-left p-px-5 p-shadow-2"> <!-- #dcdcdc"> -->
        <h3 class="p-text-italic">
            {{ title || 'No Section title'}}
        </h3>
    </div>
</template>

<script>
export default {
    props: {
        title: {
            type: String,
            required: true
        }
    }
}
</script>
