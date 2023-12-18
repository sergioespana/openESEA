// http://localhost:8081/methods/3/creation/
// A specific Method's subpages are also part of this component, as you can see <router-view/> on line 15. e.g. http://localhost:8080/methods/2/method-general/

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
