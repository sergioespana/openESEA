// http://localhost:8081/organisations/4/esea-accounts/4/report/

<template>
    <div class="p-d-flex p-jc-center p-ai-center" style="height: 150px; background-color: #dcedc8;">
        <h1>Report - {{eseaAccount.organisation}}</h1>
    </div>
    <div class="p-d-flex p-grid p-nested-grid p-jc-center p-p-5" style="background-color: #F5F5F5;">
        <div class="p-grid p-col-6" style="min-width: 1000px;">
            <div v-for="indicator in surveyResult.indicators" :key="indicator.id" class="p-grid p-col-12">
                <div class="p-grid p-col-12 p-p-5" style="background-color: white; border-radius: 10px;">
                    <div class="p-d-flex p-jc-between p-col-12">
                        <h4>Topic: <span class="p-text-light p-text-italic">'{{indicator.topic}}'</span></h4>
                        <h4>Name: <span class="p-text-light p-text-italic">'{{indicator.name}}'</span></h4>
                        <h4>Key: <span class="p-text-light p-text-italic">'[{{indicator.key}}]'</span></h4>
                    </div>
                    <div v-if="indicator.formula" class="p-grid p-col-12 p-text-left p-ml-2">
                        <div class="p-grid p-col-12 p-my-2" style="border: 1px solid lightgrey;">
                            <div class="p-col-fixed p-text-bold" style="width: 150px;">Formula:</div>
                            <div class="p-col">{{indicator.formula}}</div>
                        </div>
                        <div class="p-grid p-col-12 p-text-left p-my-2" style="border: 1px solid lightgrey;">
                            <div class="p-col-fixed p-text-bold" style="width: 150px">Calculation:</div>
                            <div class="p-col">{{indicator.calculation}}</div>
                        </div>
                    </div>
                    <div class="p-col-12 p-d-flex p-jc-between">
                        <h3>{{indicator.formula? 'Indirect Indicator value': 'Direct Indicator value'}}: <span class="p-text-light p-text-italic p-ml-5">'{{decimalrounder(indicator.value) || 'No Value to Display'}}'</span></h3>
                        <Button label="Learn more about this Indicator" class="p-button-info  p-button-outlined" @click="goesnowhere" />
                    </div>
                </div>
                <Divider class="p-m-5"/>
            </div>
        </div>
    </div>
</template>

<script>
    import { mapActions, mapState } from 'vuex'

    export default {
        data () {
            return {
            }
        },
        computed: {
            ...mapState('surveyResults', ['surveyResult']),
            ...mapState('eseaAccount', ['eseaAccount'])
        },
        created () {
            this.initialize()
        },
        methods: {
            ...mapActions('surveyResults', ['fetchSurveyResults']),
            async initialize () {
                await this.fetchSurveyResults({ oId: this.$route.params.OrganisationId, eaId: this.$route.params.EseaAccountId })
            },
            decimalrounder (number) {
                if (number === null) { return }
                if (!isNaN(number)) {
                    number = +number
                    if (Math.floor(number)) { return Math.abs(number) }
                    return number.toFixed(2)
                }
                return number
            }
        }
    }
</script>
