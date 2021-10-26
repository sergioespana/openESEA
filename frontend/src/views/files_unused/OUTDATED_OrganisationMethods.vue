<template>
<Divider />
    <div class="p-d-flex p-ai-stretch p-p-3">
        <div v-for="method in methods" :key="method.id" class="p-grid p-col-12">
            <div class="p-col-3 p-p-3">
                <Card class="p-jc-center p-shadow-5" :class="{ 'p-shadow-10': hover }" @click="goToMethod(method)" @mouseover="hover=true" @mouseleave="hover = false" style="background-color: #EFEEEE; border-radius: 5px">
                    <template #title>
                        {{method.name}}
                    </template>
                    <template #subtitle>
                        {{method.description}}
                        <Divider />
                    </template>
                    <template #content>
                        <div class="p-grid p-text-right p-mx-4 p-px-4">
                            <div class="p-col-6">Surveys:</div>
                            <div class="p-col-3">{{method.surveys.length}}</div>
                            <div class="p-col-6">Networks:</div>
                            <div class="p-col-3">{{method.networks.length}}</div>
                            <div class="p-col-6">Organisations:</div>
                            <div class="p-col-3">{{method.networks.length}}</div>
                        </div>
                    </template>
                </Card>
            </div>
        </div>
    </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
// import MyMethods from '../../components/MyMethods'
export default {
    components: {
        // MyMethods
    },
    data () {
        return {
            hover: false
        }
    },
    computed: {
        ...mapState('method', ['methods'])
    },
    created () {
        this.initialize()
    },
    methods: {
        ...mapActions('method', ['fetchMethods', 'setMethod']),
        async initialize () {
            this.fetchMethods({ }) // query: `?organisation=${this.$route.params.OrganisationId}`
        },
        goToMethod (method) {
            console.log(method)
            console.log(this.$route.params.OrganisationId)
            this.setMethod({ ...method })
            this.$router.push({ name: 'organisationmethod', params: { OrganisationId: this.$route.params.OrganisationId, MethodId: method.id } })
        }
    }
}
</script>
