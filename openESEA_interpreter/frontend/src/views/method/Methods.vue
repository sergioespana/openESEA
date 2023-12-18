<template>
    <div class="p-m-1" style="min-width: 1000px;">
        <h1>Methods Overview</h1>
        <div class="p-d-flex p-jc-between p-m-5">
            <Button label="Create Method" icon="pi pi-plus" class="p-button-success p-button-sm" @click="goToMethodCreate()" />
        </div>
        <method-list :methods="methods" />
    </div>
</template>

<script>
    import { mapState } from 'vuex'
    import MethodList from '../../components/lists/MethodList'

    export default {
        components: {
            MethodList
        },
        data () {
            return {
                createMethodDialog: false
            }
        },
        computed: {
            ...mapState('method', ['methods', 'method'])
        },
        methods: {
            async goToMethodCreate () {
                this.$router.push({ name: 'methodcreation' })
            }
        }
    }
</script>
