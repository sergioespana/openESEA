<template>
    <div class="p-d-flex p-jc-center p-ai-center" style="height: 100vh; "> <!-- #e9ecef -->
        <div class="p-p-5 p-shadow-5" style="width: 700px; border-radius: 5px; background-color: white;">
            <h3 class="p-text-left">Thank You very much for participating in this survey, {{surveyResponse.respondent}}!</h3>
            <Divider />
            <div class="p-text-justify p-my-3">
                This survey response, among others, will be used to examine how well your organisation is doing in the environmental, social and ethical fields.
                Once enough stakeholders filled in the survey a report will be created, which will be made publicly available after its validation.
            </div>
            <Button label="Learn more about ESEA" class="p-button-success" disabled="true" @click="informationAboutESEA()"></Button>
        </div>
    </div>
</template>

<script>
    import { mapState } from 'vuex'
    export default {
        computed: {
            ...mapState('surveyResponse', ['surveyResponse'])
        },
        methods: {
            informationAboutESEA () {
                // insert link to ESEA information page
            }
        }
    }
</script>
