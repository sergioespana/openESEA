<template>
    <div style="height: 100%; width: 100%; display: flex; flex-direction: column;">
        <survey-header />
        <router-view />
    </div>
</template>

<script>
    import { mapState, mapActions } from 'vuex'
    import SurveyHeader from '@/components/SurveyHeader'

    export default {
        components: {
            SurveyHeader
        },
        computed: {
            ...mapState('survey', ['survey']),
            ...mapState('method', ['method'])
        },
        created () {
            this.getQuestions()
        },
        methods: {
            ...mapActions('question', ['fetchQuestions']),
            async getQuestions () {
                await this.fetchQuestions({ mId: this.method.id, SuId: this.survey.id, SeId: 0 })
            }
        }
    }
</script>
