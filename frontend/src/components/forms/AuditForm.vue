// used by NetworkCampaigns.vue

<template>
    <form id="auditform" @submit.prevent="createNewAudit" class="p-input-filled p-text-left">
        <h2>{{survey}}</h2>

        <div class="p-field p-col-12 p-mx-0 p-px-0">
            <span class="p-float-label p-mt-3">
                <InputText type="text" class="p-col-12 p-mx-0" id="name" v-model.trim="name" />
                <label for="name">Name</label>
            </span>
        </div>

        <div class="p-field-checkbox">
            <Checkbox id="binary" v-model="checked" :binary="true" />
            <label for="binary">Deadline</label>
        </div>

        <div v-if="checked" class="p-field">
                <Calendar id="opendate" v-model="auditdate" placeholder="Calendar" appendTo="body" :showIcon="true" :inline="true" />
                <!-- <div class="p-error p-text-italic" v-for="error in openingDateErrors" :key="error"><small>{{error}}</small></div> -->
            </div>

        <div class="p-d-flex p-jc-between">
            <Button label="Cancel" icon="pi pi-times" class="" @click="closeDialog" style="width: 100px" />
            <Button type="submit" form="auditform" label="Save" icon="pi pi-check" style="width: 100px" />
        </div>
    </form>
</template>

<script>
    // :disabled="v$.campaignForm.$error"
    import { mapActions } from 'vuex'
    // import useVuelidate from '@vuelidate/core'
    // import { required, minLength, maxLength } from 'vuelidate/lib/validators'
    // import HandleValidationErrors from '../../utils/HandleValidationErrors'
    import Calendar from 'primevue/calendar'

    export default {
        components: {
            Calendar
        },
        props: {
            survey: {
                type: Number
            }
        },
        data () {
            return {
                name: '',
                checked: false,
                auditdate: new Date()
            }
        },
        // computed: {
        //     ...mapState('auditIndicators', ['indicators'])
        // },
        methods: {
            ...mapActions('auditIndicators', ['fetchIndicators']),
            async createNewAudit () {
                await this.fetchIndicators({ id: this.$route.params.EseaAccountId }) //  oId: this.$route.params.OrganisationId, eaId: this.$route.params.EseaAccountId
                this.$router.push({ name: 'questionselection', params: { EseaAccountId: this.$route.params.EseaAccountId, SurveyId: this.survey } })
                console.log('yess!', this.survey)
            },
            closeDialog () {
                this.$emit('closedialog')
            }
        }
    }
</script>

<style lang="scss" scoped>
    .borderless {
        border-bottom: 1px solid red;

    }
</style>
