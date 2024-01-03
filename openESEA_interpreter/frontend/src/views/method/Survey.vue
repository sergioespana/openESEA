// http://localhost:8081/method-wizard/3/surveys/6/
// A specific Survey's subpages are also part of this component, as you can see <router-view/> on line 15. e.g. http://localhost:8081/method-wizard/3/surveys/6/settings/

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
