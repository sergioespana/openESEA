<template>
    <div style="height: 100%; width: 100%; display: flex; flex-direction: column;">
        <method-header />
        <router-view />
    </div>
</template>

<script>
    import MethodHeader from '@/components/MethodHeader'

    export default {
        components: {
            MethodHeader
        }
    }
</script>
