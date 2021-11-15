<template>
    <BreadCrumb :home="home" :model="items" />
</template>
<script>
import BreadCrumb from 'primevue/breadcrumb'
import { mapState } from 'vuex'

export default {
    components: {
        BreadCrumb
    },
    props: {
    },
    data () {
        return {
            home: { icon: 'pi pi-home', to: '/' },
            items: []
        }
    },
    watch: {
        '$route' () {
            var bread = this.$route.meta.breadcrumb || {}
            this.changeBreadCrumb(bread)
        }
    },
    computed: {
        ...mapState('organisation', ['organisation'])
    },
    methods: {
        changeBreadCrumb (bread) {
            const paths = this.$route.path.split('/').slice(1)
            paths.forEach((path, i) => {
                if (bread[i]) {
                    if (bread[i].to.params) {
                        if (parseInt(path)) {
                            bread[i].label = this.organisation.name
                        }
                        bread[i] = { label: bread[i].label, to: { name: bread[i].to.name, params: { id: parseInt(this.$route.params.id) } } }
                    }
                 }
            })
            this.items = bread
        }
    }
}
</script>
