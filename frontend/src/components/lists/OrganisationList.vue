<template>
    <list-bar v-model:tabledisplay="tableDisplay" v-model:allitems="allOrganisations" :includecheckbox="!networkorganisations" v-model:search="customSearch" name="Organisations">
        <slot></slot>
    </list-bar>

    <ProgressSpinner v-if="loading && !failedLoad" />
    <div v-else-if="loading && failedLoad" class="p-text-italic">Organisations could not be retrieved!</div>
    <div v-else-if="organisations.length">
        <div v-if="tableDisplay" class="p-grid p-m-5">
            <div v-for="organisation in filteredOrganisations" :key="organisation.id" class="p-col-12 p-md-6 p-lg-4" style="width: 300px; height: auto;">
                <div class="p-p-3" :class="organisation.hover ? 'p-shadow-2 p-m-1' : 'p-shadow-1 p-m-2'" :style="(organisation.hover ? styleObject : '')" @mouseover="organisation.hover=true" @mouseleave="organisation.hover=false" @click.left="goToOrganisation(organisation)">
                    <img :src="organisation.image" alt="Organisation Image" style="max-width: 150px; max-height: 150px; border-radius: 50%;" format="PNG" />
                    <p class="p-text-italic">{{organisation.name}}</p>
                </div>
            </div>
        </div>
        <DataTable v-else :value="filteredOrganisations" datakey="id" selectionMode="single" @row-select="goToOrganisation" showGridlines autoLayout
        :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

            <Column field="ispublic" header="Public" headerStyle="width: 5rem">
                <template #body="slotProps">
                    <i class="pi p-text-center p-text-bold" style="width:100%; font-size: 20px;" :class="{'true-icon pi-check': slotProps.data.ispublic, 'false-icon pi-times': !slotProps.data.ispublic}" :style="(slotProps.data.ispublic ? 'color: green;':'color: red;')"></i>
                </template>
            </Column>
            <Column v-for="col of columns" :field="col.field" :header="col.header" :key="col.field" bodyStyle="" /> <!-- text-align: center; overflow: visible  contentStyle="width: 500px;" -->
            <Column field="owner" header="Owner">
                <template #body="slotProps">
                    <div v-if="slotProps.data.owner !== currentuser">{{slotProps.data.owner}}</div> <div v-else class="p-text-bold">You</div>
                </template>
            </Column>

            <div v-if="networkorganisations">
            <Column headerStyle="width: 15rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                <template #body="{data}">
                    <div v-if="(networkorganisations && permission)">
                        <Button v-if="invitableorganisations" label="Invite Organisation" class="p-button-success p-button-sm" @click="inviteOrganisation(data)" />
                        <Button v-if="!invitableorganisations" label="Remove Organisation" class="p-button-danger p-button-sm" @click="removeOrganisation(data)" />
                    </div>
                </template>
            </Column>
            </div>
            <div v-else><Column bodyStyle="width: 0rem;" /></div>
        </Datatable>
    </div>
    <div v-else class="p-text-italic">No Organisations to display.</div>
</template>

<script>
    import { mapState, mapActions } from 'vuex'
    import ProgressSpinner from 'primevue/progressspinner'
    import ListBar from '@/components/lists/ListBar'

    export default {
        components: {
            ProgressSpinner,
            ListBar
        },
        props: {
            refresh: {
                type: Boolean,
                default: false
            },
            permission: {
                type: Boolean,
                default: false
            },
            invitableorganisations: {
                type: Boolean,
                default: false
            },
            networkorganisations: {
                type: Boolean,
                default: false
            }
        },
        data () {
            return {
                customSearch: '',
                loading: true,
                failedLoad: false,
                tableDisplay: false,
                allOrganisations: false,
                styleObject: { backgroundColor: '#EFEEEE', cursor: 'pointer' },
                columns: [
                    { field: 'name', header: 'Name' },
                    { field: 'description', header: 'Description' },
                    { field: 'networks.length', header: 'Networks' }
                ]
            }
        },
        computed: {
            ...mapState('authentication', ['currentuser']),
            ...mapState('organisation', ['organisations', 'organisation']),
            filteredOrganisations () {
                return this.organisations.filter(organisation => {
                    return (
                        organisation.name.toLowerCase().includes(this.customSearch.toLowerCase()) ||
                        organisation.description.toLowerCase().includes(this.customSearch.toLowerCase())
                    )
                })
            }
        },
        watch: {
            refresh: {
                immediate: true,
                handler () {
                    this.getOrganisations()
                }
            },
            allOrganisations () {
                this.getOrganisations()
            },
            invitableorganisations () {
                this.getOrganisations()
            }
        },
        methods: {
            ...mapActions('organisation', ['fetchOrganisations', 'setOrganisation', 'deleteOrganisation']),
            async getOrganisations () {
                this.loading = true
                setTimeout(() => { this.failedLoad = true }, 10000)
                if (this.networkorganisations) {
                    if (this.invitableorganisations) {
                        await this.fetchOrganisations({ query: `?excludenetwork=${this.$route.params.NetworkId}` })
                    } else {
                        await this.fetchOrganisations({ query: `?network=${this.$route.params.NetworkId}` })
                    }
                } else {
                    if (this.allOrganisations) {
                        await this.fetchOrganisations({ query: '?allorganisations=1' })
                    } else {
                        await this.fetchOrganisations({ query: '?myorganisations=1' })
                    }
                }
                this.loading = false
                this.$emit('update: refresh', true)
            },
            async goToOrganisation (organisation) {
                if (organisation?.data) {
                    organisation = organisation.data
                }
                if (organisation.id) {
                    await this.setOrganisation(organisation)
                     this.$router.push({ name: 'organisationoverview', params: { OrganisationId: this.organisation.id } })
                }
            },
            inviteOrganisation (organisation) {
                if (organisation.id) {
                    this.$emit('invite-organisation', organisation)
                }
            },
            removeOrganisation (organisation) {
                if (organisation.id) {
                    this.$emit('remove-organisation', organisation)
                }
            }

            //  async goToOrganisation (organisation) {
            // if (this.removeMode) {
            //     this.selectedOrganisations = []
            //     this.selectedOrganisations.push(organisation)
            //     this.removeDialog = true
            // } else {
            // await this.setOrganisation({ ...organisation })
            // this.$router.push({ name: 'organisationoverview', params: { OrganisationId: organisation.id } })
            // }
            // async destroyOrganisation () {
            //     if (this.selectedOrganisation) {
            //         this.deleteOrganisation({ id: this.selectedOrganisation?.id })
            //     }
            //     this.selectedOrganisation = null
            //     this.destroyOrganisationDialog = false
            // }
    //             <!-- <Dialog v-model:visible="destroyOrganisationDialog" :style="{width: '450px'}" header="Confirm Organisation Deletion" :modal="true">
    //     <div class="confirmation-content">
    //         <i class="pi pi-exclamation-triangle p-mr-3" style="font-size:1.5rem" />
    //         <span>Are you sure you want to completely delete the following Organisation: <b>{{selectedOrganisation.name}}</b>?</span>
    //     </div>
    //     <template #footer>
    //         <Button label="No" icon="pi pi-times" class="p-button-text" @click="destroyOrganisationDialog = false"/>
    //         <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="destroyOrganisation()" />
    //     </template>
    // </Dialog>
        }
    }
</script>
