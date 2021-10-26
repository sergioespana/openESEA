<template>
    <div v-if="stakeholders">
        <my-reports></my-reports>
    </div>
    <div v-else class="p-text-italic">
        Your organisation has no reports to display.<br> Join a network and fill in surveys to get reports!
    </div>
</template>

<script>
export default {
    components: {
    }
}
</script>
