// used by OrganisationEseaAccounts.vue

<template>
    <form id="eseaaccountform" @submit.prevent="createNewEseaMethod" class="p-input-filled p-fluid p-text-left">
        <div class="p-field">
            <label for="method">Method<span style="color:red">*</span></label>
            <Dropdown id="method" v-model="eseaaccountForm.method" :options="methods"  optionLabel="name" placeholder="Select a Method" :class="{'p-invalid': v$.eseaaccountForm.method.$error}" />
            <!-- <div class="p-error p-text-italic" v-for="error in methodErrors" :key="error">{{error}}</div> -->
        </div>

        <div class="p-field p-m-0">
            <label for="year">Year</label>
            <Dropdown id="method" v-model="eseaaccountForm.year" :options="possibleyears" placeholder="Select a Year" :class="{'p-invalid': v$.eseaaccountForm.year.$error}" />
            <!-- <div class="p-error p-text-italic" v-for="error in openingDateErrors" :key="error"><small>{{error}}</small></div> -->
        </div>
        <div v-if="filteredEseaAccounts.length" class="p-error p-text-italic">"This organisation already has an Esea Account for this method and year."</div>

        <div class="p-d-flex p-jc-between p-mt-5">
            <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="closeDialog" style="width: 100px" />
            <Button type="submit" form="eseaaccountform" label="Create" icon="pi pi-check" class="p-button-text" :disabled="v$.eseaaccountForm.$error || filteredEseaAccounts.length" style="width: 100px" />
        </div>
    </form>
</template>

<script>
    import useVuelidate from '@vuelidate/core'
    import { required } from 'vuelidate/lib/validators'
    import Dropdown from 'primevue/dropdown'
    import { mapActions, mapState } from 'vuex'

    export default {
        components: {
            Dropdown
        },
        props: {
            eseaAccounts: {
                type: Array
            }
        },
        data () {
            return {
                eseaaccountForm: {
                    method: null,
                    year: null
                }
            }
        },
        computed: {
            ...mapState('method', ['methods']),
            ...mapState('eseaAccount', ['eseaAccount']),
            filteredEseaAccounts () {
                return this.eseaAccounts.filter(eseaAccount => eseaAccount.year === this.eseaaccountForm.year && eseaAccount.method_name.includes(this.eseaaccountForm.method.name)) // .filter(eseaAccount => { return eseaAccount.year.includes(2020) })
            },
            possibleyears () {
                const currentyear = new Date().getFullYear()
                const minyear = currentyear - 10
                const years = []

                for (let i = minyear; i <= currentyear; i++) {
                    years.push(i)
                }
                return years
            }
        },
        setup: () => ({ v$: useVuelidate() }),
        validations: {
            eseaaccountForm: {
                method: { required },
                year: { required }
            }
        },
        async created () {
            await this.fetchMethods({})
        },
        methods: {
            ...mapActions('method', ['fetchMethods']),
            ...mapActions('eseaAccount', ['createEseaAccount']),
            async createNewEseaMethod () {
                console.log('Validating new Esea Account...')
                this.v$.eseaaccountForm.$touch()
                if (this.v$.$invalid) { return }
                await this.createEseaAccount({ oId: this.$route.params.OrganisationId, data: { method: this.eseaaccountForm.method.id, year: this.eseaaccountForm.year } })

                if (this.eseaAccount.id) {
                    this.$router.push({ name: 'organisationeseaaccount', params: { EseaAccountId: this.eseaAccount.id } })
                }
            },
            closeDialog () {
                this.$emit('closedialog')
            }
        }
    }
</script>

/<!-- <Calendar id="year" v-model="eseaaccountForm.year" placeholder="Year" appendTo="body" :showIcon="true" view="year" dateFormat="yy"  yearRange="2000:2030" />
// <InputNumber id="integeronly" v-model="eseaaccountForm.year" :min="2000" :max="2050" /> -->
