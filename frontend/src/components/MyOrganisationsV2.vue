<template>
    <!-- <my-organisations network-organisations selection-enabled></my-organisations> -->
    <div class="p-d-flex p-jc-between p-mx-5" style="min-width: 600px;">
        <div v-if="networkOrganisations">
            <Button :label="'Invite Organisation'" icon="pi pi-plus" class="p-button-success p-button-sm p-mr-2" @click="addableOrganisations()" />
            <Button :label="removeMode ? 'Select the organisation to remove': 'Enable Remove Mode'" icon="pi pi-trash" class="p-button-danger p-button-sm" :disabled="!organisations.length" @click="removeMode = !removeMode" />
        </div>
        <div v-else>
            <Button label="Create Organisation" icon="pi pi-plus" class="p-button-success" @click="createDialog = true" />
        </div>
        <span class="p-input-icon-left">
            <i class="pi pi-search" /><InputText v-model="search" placeholder="Search Organisations..." />
        </span>
    </div>
    <Divider />
    <div v-if="organisations.length" class="p-grid p-m-5">
        <div v-for="organisation in filteredList" :key="organisation.id" class="p-col-12 p-md-6 p-lg-4" style="width: 300px; height: auto;">
            <div class="p-p-3" :class="organisation.hover ? 'p-shadow-2 p-m-1' : 'p-shadow-2 p-m-2'" :style="(organisation.hover ? styleObject: '')" @mouseover="organisation.hover=true" @mouseleave="organisation.hover = false" @click="goToOrganisation(organisation)">
                <img :src="organisation.image" alt="Profile Avatar" style="max-width: 150px; max-height: 150px; border-radius: 50%;" format="PNG">
                <p class="p-text-italic">{{organisation.name}}</p>
            </div>
        </div>
    </div>
    <div v-else class="p-text-italic">There are no Organisations to display!</div>

    <Dialog v-model:visible="createDialog" style="width: 450px" header="Organisation Details" modal="true" dismissableMask="true" class="p-fluid">
        <div class="p-field">
            <label for="name">Name</label>
            <InputText id="name" v-model.trim="organisationForm.name" required="true" autofocus :class="{'p-invalid': submitted && !organisationForm.name}" />
            <small class="p-error" v-if="submitted && !organisationForm.name">Name is required.</small>
        </div>
        <div class="p-field">
            <label for="description">Description</label>
            <Textarea id="description" v-model="organisationForm.description" required="true" rows="3" cols="20" />
        </div>
        <div class="p-field">
            <label for="ispublic">Should this organisation be public? </label>
            <SelectButton id="ispublic" v-model="organisationForm.ispublic" required="true" :options="ispublicbool" />
        </div>
        <template #footer>
            <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="createDialog = false" />
            <Button label="Save" icon="pi pi-check" class="p-button-text" @click="createNewOrganisation" :disabled="!organisationForm.name" />
        </template>
    </Dialog>

    <Dialog v-model:visible="removeDialog" style="width: 500px" header="Confirm Deletion" modal="true"  dismissableMask="true">
            Are you sure you want to <b>delete</b> the following organisation(s)?
            <div class="p-shadow-1 p-p-3 p-m-5">{{selectedOrganisations.name}}</div>
        <template #footer>
        <Button label="No" icon="pi pi-times" class="p-button-text" @click="(removeDialog = false) && (selectedRows = null)"/>
        <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="removeOrganisation()" />
      </template>
    </Dialog>

     <Dialog v-model:visible="inviteDialog" style="width: 500px" modal="true" dismissableMask="true" class="p-fluid">
         <div class="p-field">
            <MultiSelect id="organisations" v-model="organisationsToInvite" :options="organisations" optionLabel="name" placeholder="Select Organisations" :filter="true" class="multiselect-custom">
                <template #value="slotProps">
                    <div v-for="option of slotProps.value" :key="option.id">
                        <div>{{option.name}}</div>
                    </div>
                    <template v-if="!slotProps.value || slotProps.value.length === 0">
                        Select Organisations
                    </template>
                </template>
                <template #option="slotProps">
                    <div>{{slotProps.option.name}}</div>
                </template>
            </MultiSelect>
         </div>
            <div class="p-field">
            <label for="message">Message to Organisations</label>
            <Textarea id="message" v-model="something" required="true" rows="3" cols="20" />
            </div>
        <template #footer>
                <Button label="Invite Organisations" icon="pi pi-plus" @click="addOrganisations"/>
                <Button label="Cancel" icon="pi pi-check" class="p-button-text" @click="inviteDialog = false" />
        </template>
    </Dialog>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import MultiSelect from 'primevue/multiselect'

export default {
    components: {
        MultiSelect
    },
    props: {
     networkOrganisations: {
            type: Boolean,
            default: false
        }
    },
    data () {
        return {
            styleObject: { backgroundColor: '#EFEEEE' },
            search: '',
            selectedOrganisations: [],
            organisationsToInvite: '',
            inviteDialog: false,
            removeMode: false,
            removeDialog: false,
            createDialog: false,
            submitted: false,
            ispublicbool: [true, false],
            organisationForm: {
                name: null,
                description: '',
                ispublic: true
            }
        }
    },
    computed: {
        ...mapState('organisation', ['organisations', 'organisation']),
        filteredList () {
            return this.organisations.filter(organisation => { return organisation.name.toLowerCase().includes(this.search.toLowerCase()) })
        }
    },
    watch: {
        inviteDialog () {
            if (!this.inviteDialog) { this.initialize() }
        }
    },
    created () {
        this.initialize()
    },
    methods: {
        ...mapActions('organisation', ['fetchOrganisations', 'setOrganisation', 'createOrganisation']),
        async initialize () {
            if (this.networkOrganisations) {
                await this.fetchOrganisations({ query: `?network=${this.network?.id || 0}` })
            } else {
                await this.fetchOrganisations({})
            }
            // await this.fetchOrganisations({ query: `?network=${this.$route.params.NetworkId}` })
        },
        async createNewOrganisation () {
            this.submitted = false
            if (this.organisationForm.name.trim()) {
                await this.createOrganisation({ data: this.organisationForm })
                this.$toast.add({ severity: 'success', summary: 'Organisation created', detail: `organisation: ${this.organisation.name}`, life: 3000 })
            this.createDialog = false
            this.submitted = true
            this.$router.push({ name: 'organisationoverview', params: { OrganisationId: this.organisation.id } })
            }
        },
        async removeOrganisation () {
            // remove Organisation
        },
        async addOrganisations () {
            this.inviteDialog = false
            // add Organisation
        },
        async addableOrganisations () {
            await this.fetchOrganisations({ query: `?excludenetwork=${this.$route.params.NetworkId}` })
            this.inviteDialog = true
        },
        async goToOrganisation (organisation) {
            if (this.removeMode) {
                this.selectedOrganisations = organisation
                this.removeDialog = true
            } else {
            await this.setOrganisation({ ...organisation })
            this.$router.push({ name: 'organisationoverview', params: { OrganisationId: organisation.id } })
            }
        }
    }
}
</script>
