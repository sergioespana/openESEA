// used by Networks.vue, OrganisationNetworks.vue

<template>
    <list-bar v-model:tabledisplay="tableDisplay" v-model:allitems="allNetworks" v-model:search="customSearch" :includecheckbox="!organisationnetworks" name="Networks">
        <slot></slot>
    </list-bar>
    <ProgressSpinner v-if="loading && !failedLoad" />
    <div v-else-if="loading && failedLoad" class="p-text-italic">Networks could not be retrieved</div>
    <div v-else-if="networks.length">
         <div v-if="tableDisplay" class="p-grid p-m-5">
            <div v-for="network in filteredNetworks" :key="network.id" class="p-col-12 p-md-6 p-lg-4" style="width: 300px; height: auto;">
                <div class="p-p-3" :class="network.hover ? 'p-shadow-2 p-m-1' : 'p-shadow-1 p-m-2'" :style="(network.hover ? styleObject : '')" @mouseover="network.hover=true" @mouseleave="network.hover=false" @click.left="goToNetwork(network)">
                    <img :src="network.image" alt="Network Image" style="max-width: 150px; max-height: 150px; border-radius: 50%;" format="PNG" />
                    <p class="p-text-bold p-text-italic">{{network.name}}</p>
                </div>
            </div>
         </div>
        <DataTable v-else :value="filteredNetworks"  dataKey="id" :loading="loading" selectionMode="single" @row-select="goToNetwork" showGridlines autoLayout
        :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped"> <!-- p-datatable-sm -->

            <template #loading>
                Loading records, please wait...
            </template>
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
            <div v-if="organisationnetworks && permission">
            <Column headerStyle="width: 15rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                <template #body="{data}">
                    <div v-if="(organisationnetworks && permission)">
                        <Button v-if="joinableNetworks" label="Join Network" class="p-button-success p-button-sm" @click="joinNetwork(data)" />
                        <Button v-if="!joinableNetworks" label="Leave Network" class="p-button-danger p-button-sm" @click="leaveNetwork(data)" />
                    </div>
                </template>
            </Column>
            </div>
            <div v-else><Column bodyStyle="width: 0rem;" /></div>
        </Datatable>
    </div>
    <div v-else class="p-text-italic">No Networks to display!</div>
</template>

<script>
    import { mapActions, mapState } from 'vuex'
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
            joinableNetworks: {
                type: Boolean,
                default: false
            },
            organisationnetworks: {
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
                allNetworks: false,
                styleObject: { backgroundColor: '#EFEEEE', cursor: 'pointer' },
                columns: [
                    { field: 'name', header: 'Name' },
                    { field: 'description', header: 'Description' },
                    { field: 'organisations.length', header: 'Organisations' }
                ]
            }
        },
        computed: {
            ...mapState('network', ['networks', 'network']),
            ...mapState('authentication', ['currentuser']),
            filteredNetworks () {
                return this.networks.filter(network => {
                    return (
                        network.name.toLowerCase().includes(this.customSearch.toLowerCase()) ||
                        network.description.toLowerCase().includes(this.customSearch.toLowerCase())
                    )
                })
            }
        },
        watch: {
            refresh: {
                immediate: true,
                handler () {
                    this.getNetworks()
                }
            },
            allNetworks () {
                this.getNetworks()
            }
        },
        created () {
            this.getNetworks()
            setTimeout(() => { this.failedLoad = true }, 10000)
        },
        methods: {
            ...mapActions('network', ['fetchNetworks', 'setNetwork', 'deleteNetwork']),
            async getNetworks () {
                this.loading = true
                if (this.organisationnetworks) {
                    if (this.joinableNetworks) {
                        await this.fetchNetworks({ query: `?excludeorganisation=${this.$route.params.OrganisationId}` })
                    } else {
                        await this.fetchNetworks({ query: `?organisation=${this.$route.params.OrganisationId}` })
                    }
                }
                if (!this.organisationnetworks) {
                    if (this.allNetworks) {
                        await this.fetchNetworks({ query: '?allnetworks=1' })
                    } else {
                        await this.fetchNetworks({ query: '?mynetworks=1' })
                    }
                }
                this.loading = false
                this.$emit('update:refresh', true)
            },
            async goToNetwork (network) {
                if (network?.data) {
                    network = network.data
                }
                if (network.id) {
                    // this.$emit('clicked-network', network)
                    await this.setNetwork(network)
                    this.$router.push({ name: 'networkoverview', params: { NetworkId: this.network.id } })
                }
            },
            joinNetwork (network) {
                if (network.id) {
                    this.$emit('join-network', network)
                }
            },
            leaveNetwork (network) {
                if (network.id) {
                    this.$emit('leave-network', network)
                }
            }

        }
    }
// destroyNetwork () {
//     if (this.selectedNetwork) {
//         this.deleteNetwork({ id: this.selectedNetwork?.id })
//     }
//     this.selectedNetwork = null
//     this.destroyNetworkDialog = false
// }
// <Dialog v-model:visible="destroyNetworkDialog" :style="{width: '450px'}" header="Confirm Network Deletion" :modal="true">
//         <div class="confirmation-content">
//             <i class="pi pi-exclamation-triangle p-mr-3" style="font-size:1.5rem" />
//             <span>Are you sure you want to delete <b>{{selectedNetwork.name}}</b>?</span>
//         </div>
//         <template #footer>
//             <Button label="No" icon="pi pi-times" class="p-button-text" @click="destroyNetworkDialog = false"/>
//             <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="destroyNetwork()" />
//         </template>
//     </Dialog>
</script>
