<template>
    <div class="p-p-3">
        <h2 class="p-text-left">Sample Overview</h2>
        <Card class="p-text-left">
            <template #title>
            Survey Response Sample
            </template>
            <template #subtitle>
                Total number of responses:  <br>
                How many responses do you wish to audit?
            </template>
            <template #content class="p-col-12">
                <div class="field-radiobutton p-mb-2">
                    <RadioButton id="choice1" name="choice" value="fixed" class="p-mx-1" v-model="sample_choice" />
                    <label for="city1">Fixed number</label>
                </div>
                <div class="field-radiobutton">
                    <RadioButton id="choice2" name="choice" value="percentage" class="p-mx-1" v-model="sample_choice" />
                    <label for="city2">Percentage of Total Responses</label>
                </div>

                <div class="p-pt-5" style="width: 400px;">
                    <InputNumber v-if="sample_choice ==='fixed'" class="p-col-12 p-m-0 p-p-0" v-model="value" />
                    <div v-if="sample_choice ==='percentage'" class="p-inputgroup">
                        <span class="p-inputgroup-addon">%</span>
                        <InputNumber placeholder="Percentage" :min="0" :max="100" :maxFractionDigits="0" />
                    </div>
                </div>
                <Button class="p-mt-5" label="Sample Responses" @click="sampleResponses()" icon="pi pi-check" />
            </template>
        </Card>
    </div>
</template>

<script>
export default {
    data () {
        return {
            sample_choice: null,
            value: null
        }
    },
    methods: {
        sampleResponses () {
            this.$router.push({ name: 'multiplesampleoverview', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.$route.params.SurveyId } })
            // Get number of sampled responses
            print()
        }
    }
}
</script>
