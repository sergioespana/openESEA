// used by Method.vue

<template>
    <div class="p-d-flex p-ai-center p-jc-between" style="height: 60px; background-color: #f1f1f1; border-bottom: 1px solid lightgrey;">
        <div style="display: flex; align-items: center; flex-grow: 1; flex-shrink: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
            <i class="pi pi-arrow-left p-px-5" style="font-size: 30px; cursor: pointer;" @click="goToMethods()"></i>
            <div style="display: flex; align-items: center; flex-grow: 1; flex-shrink: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                <h2 class="p-text-left" style="flex-grow: 1; flex-shrink: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{{ title }}</h2>
                <span class="p-text-italic p-p-5" style="font-size: 16px; flex-shrink: 0;"><template v-if="upToDate">All changes saved</template><template v-else>...</template></span>
            </div>
        </div>
        <div class="p-d-flex p-ai-center" style="height: 100%; flex-shrink: 0; cursor: pointer;">
            <div v-for="step in steps" :key="step.text" class="p-d-flex p-ai-center" @mouseover="step.hover = true" @mouseleave="step.hover = false" :style="[($route.name.startsWith(step.to.name.slice(0, -1))) ? 'background-color: grey; color: white;' :'', step.hover ? styleObject : '', ]" style="height: 100%;">
                <div class="p-text-light p-p-5" @click="goToPage(step.to)"  style="text-align: center;">{{step.text}}</div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
    data () {
        return {
        steps: [
            { text: 'Method Information', to: { name: 'method-general' } },
            { text: 'Create Indicators', to: { name: 'method-indicator-creation' } },
            { text: 'Create Topics', to: { name: 'method-topic-creation' } },
            // { text: 'Set Indicators 2', to: { name: 'method-create' } },
            { text: 'Create Surveys', to: { name: 'method-wizard-surveys' } },
            { text: 'Finish method', to: { name: 'method-wizard-finish' } }
            ],
        styleObject: { 'background-color': '#00695C', color: 'white' }
        }
    },
    computed: {
        ...mapState('method', ['method']),
		...mapState('topic', { topicsSaved: 'isSaved' }),
		...mapState('question', { questionsSaved: 'isSaved' }),
        ...mapState('directIndicator', { DirectIndicatorsSaved: 'isSaved' }),
		...mapState('indirectIndicator', { IndirectIndicatorsSaved: 'isSaved' }),
		// ...mapState('survey', { SurveysSaved: 'isSaved' }),
        title () {
            return this.method.id ? this.method.name : 'New Method'
        },
        upToDate () {
            const all = {
                ...this.topicsSaved,
                ...this.questionsSaved,
                ...this.IndirectIndicatorsSaved
                // ...this.SurveysSaved,
            }
            const found = Object.values(all).find(value => value === false)
            return found === undefined
        }
    },
    methods: {
        ...mapActions('method', ['setMethod']),
        goToMethods () {
            this.$router.push({ name: 'methods' })
        },
        async goToPage (page) {
            console.log('is saved:', this.DirectIndicatorsSaved)
            if (page.name === 'method-wizard-finish') {
                if (this.method.id) {
                    await this.setMethod({ id: this.method.id })
                    this.$router.push({ name: 'newmethoddetails', params: { id: this.method.id } })
                }
                // this.goToMethods()
                return
            }
            page.params = { id: this.$route.params.id }
            this.$router.push(page)
        }
    }
}
</script>
