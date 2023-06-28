<template>
    <div :id="'overview_' + this.overviewId + '_sidepanel'"></div>
</template>

<script>
    export default {
        name: 'SidePanel',
        props: {
            overviewId: { type: Number, required: true }
        }
    }
</script>
