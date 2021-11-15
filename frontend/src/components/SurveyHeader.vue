// Used by Survey.vue

<template>
<div class="p-d-flex p-ai-center p-jc-between" style="width: 100%; height: 60px; border: 1px solid lightgrey;">
    <div class="p-d-flex p-ai-center">
        <h3 class="p-mx-5">{{ this.survey.name }} <span class="p-text-italic p-text-light p-ml-5"><small><template v-if="upToDate">All changes saved</template><template v-else>...</template></small></span></h3>
    </div>
    <div class="p-d-flex p-ai-center p-m-0 p-p-0" style="height: 100%;">
        <div :style="[($route.name === steps[0].to.name) ? 'border-bottom: 4px solid #00695C; color: #00695C;':'']" style="height: 60px; line-height: 60px;" class="p-px-5" @click="(this.survey.id > 0) ? goToPage('settings'):''">Survey Information</div>
        <div :style="[($route.name === steps[1].to.name) ? 'border-bottom: 4px solid #00695C; color: #00695C;':'', (survey.id > 0 ? 'cursor: pointer;':'color: lightgrey; cursor; cursor: not-allowed;')]" style="height: 60px; line-height: 60px;" class="p-px-5" @click="(this.survey.id > 0) ? goToPage('design'):''">Questions</div>
        <!-- <div class="p-px-5 p-d-flex p-ai-center p-text-bold" style="height: 100%; border-bottom: 4px solid #00695C; color: #00695C;" @click="goToPage('method-wizard-survey-settings')">Survey Information</div>
        <div class="p-px-5 p-d-flex p-ai-center" @click="goToPage('method-wizard-survey-design')">Questions</div> -->
    </div>
    <div></div>
</div>
    <!-- <div class="p-d-flex" style="height: 100%; border-top: 1px solid lightgrey;">
        <div class="p-d-flex p-flex-column p-jc-between" style="width: 300px; border: 1px solid lightgrey;">
            <method-tree-sidebar />
            <Button label="Open ESEA Method Creation Guide" class="p-button-info p-button-lg p-p-5" />
        </div>
        </div> -->
</template>

<script>
import { mapState } from 'vuex'
export default {
    data () {
        return {
            steps: [
                { text: 'Survey Information', to: { name: 'method-wizard-survey-settings' } },
                { text: 'Questions', to: { name: 'method-wizard-survey-design' } }
                ]
        }
    },
    computed: {
        ...mapState('survey', ['survey'])
    },
    methods: {
        goToPage (path) {
            if (this.survey?.id > 0) {
                if (path === 'design') {
                console.log('-->', this.$route.params)
                this.$router.push({ name: 'method-wizard-survey-design', params: { SurveyId: this.survey.id } })
                } else { this.$router.push({ name: 'method-wizard-survey-settings', params: { SurveyId: this.survey.id } }) }
            }
        }
    }
}
</script>
