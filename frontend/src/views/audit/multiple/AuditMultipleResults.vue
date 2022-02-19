<template>
    <div class="p-p-3">
        <h2 class="p-text-left">Results</h2>
        <Checkbox id="card1" v-model="card1" :binary="true" class="p-ml-2" />
        <label for="card1">Card1</label>
        <Checkbox id="card2" v-model="card2" :binary="true" class="p-ml-2" />
        <label for="card2">Card2</label>
        <Card v-if="card1" class="p-text-left p-m-2">
            <template #title>
            Audit Result
            </template>
            <template #content class="p-col-12">
            <div class="p-mr-5">
                <div class="p-grid">
                    <div class="p-col-2 p-text-center"><i class="pi pi-check" style="font-size: 3rem; background-color: #689F38; color: white; border-radius: 50%; padding: 30px;"></i></div>
                    <div class="p-col-10">
                        <h3 class="p-mt-0 p-pt-0">Multi stakeholder survey</h3>
                        The auditor has verified the survey responses.
                    </div>
                </div>
            </div>
            </template>
        </Card>

    <Card v-if="card2" class="p-text-left p-m-2">
            <template #title>
            Audit Result
            </template>
            <template #content class="p-col-12">
            <div class="p-mr-5">
                <div class="p-grid">
                    <div class="p-col-2 p-text-center"><i class="pi pi-times" style="font-size: 3rem; background-color: red; color: white; border-radius: 50%; padding: 30px;"></i></div>
                    <div class="p-col-10">
                        <h3 class="p-mt-0 p-pt-0">Multi stakeholder survey</h3>
                        Unfortunately, the auditor has rejected the survey responses.
                    </div>
                </div>
            </div>
            </template>
        </Card>
    </div>
</template>

<script>
export default {
    data () {
        return {
            card1: true,
            card2: true
        }
    }
}
</script>
