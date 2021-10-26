    <template>
    <h1>Networks Overview</h1>
    <!-- <div class="networks">

        <Toast position="top-right"/>
        <div class="card p-m-5 p-shadow-2">
          <Toolbar>
                <template #left>
                        <ToggleButton v-model="selectionToggle" onLabel="Selecting: Enabled" offLabel="Selecting: Disabled" onIcon="pi pi-check" offIcon="pi pi-times" />
                        <Button label="Create Network" icon="pi pi-plus" class="p-button-success p-mx-2" @click="openCreateNetworkDialog" />
                </template>
                <template #right>
                    <span class="p-input-icon-left">
                        <i class="pi pi-search" />
                        <InputText v-model="filters['global']" placeholder="Search..." />
                    </span>
                </template>
            </Toolbar>
            <personalised-datatable table-name="networks" selectionToggle :columns="NetworkColumns" :filters="filters"
            :custom-data="networks" @item-redirect="goToNetwork"/>

            <DataTable ref="dt" :value="networks" v-model:selection="selectedNetworks" selectionMode="single" dataKey="id" @row-select="goToNetwork"
            :paginator="true" :rows="10" :filters="filters" paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
            :rowsPerPageOptions="[5,10,25]" currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products" class="p-datatable-striped">

              <template #header>
                <div class="table-header p-d-flex p-jc-between p-ai-center">
                  <Button label="Create Network" icon="pi pi-plus" class="p-button-success p-mr-2" @click="openCreateNetworkDialog" />
                  <span class="p-input-icon-left">
                    <i class="pi pi-search" />
                    <InputText v-model="filters['global']" placeholder="Search..." />
                  </span>
                </div>
              </template>

              <Column field="ispublic" header="Public" :sortable="true"></Column>
              <Column field="name" header="Name" :sortable="true"></Column>
              <Column field="description" header="Description" :sortable="true"></Column>
              <Column field="organisations.length" header="Organisations" :sortable="true"></Column>
              <Column field="created_by.username" header="Created by" :sortable="true"></Column>
            </DataTable>
        </div>
    </div> -->

    <Dialog v-model:visible="networkDialog" :style="{width: '450px'}" header="Network Details" :modal="true" class="p-fluid">
        <div class="p-field">
            <label for="name">Name</label>
            <InputText id="name" v-model.trim="network.name" required="true" autofocus :class="{'p-invalid': submitted && !network.name}"
            @blur="updateNetworkForm({ name: $event.target.value })" />
            <small class="p-error" v-if="submitted && !network.name">Name is required.</small>
        </div>
        <div class="p-field">
            <label for="description">Description</label>
            <Textarea id="description" v-model="network.description" required="true" rows="3" cols="20"
            @blur="updateNetworkForm({ description: $event.target.value })" />
        </div>
        <div class="p-field">
            <label for="ispublic">Should this network be public? </label>
            <SelectButton id="ispublic" v-model="network.ispublic" required="true" :options="ispublicbool"
            @blur="updateNetworkForm({ ispublic: false })" />
        </div>
        <template #footer>
            <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="hideDialog"/>
            <Button label="Save" icon="pi pi-check" class="p-button-text" @click="saveNetwork" :disabled="!network.name" />
        </template>
    </Dialog>

</template>

 <script>
// Potentially remove @blur if it won't be used
 import { mapState, mapActions } from 'vuex'
 // import PersonalisedDatatable from '../components/PersonalisedDatatable'

 export default {
     components: {
         // PersonalisedDatatable
     },
     data () {
        return {
            NetworkColumns: [
                { field: 'ispublic', header: 'Public' },
                { field: 'name', header: 'Name' },
                { field: 'description', header: 'Description' },
                { field: 'organisations.length', header: 'Organisations' },
                { field: 'created_by.username', header: 'Created by' }
            ],
            selectionToggle: false,
            filters: {},
            ispublicbool: [true, false],
            networkDialog: false,
            submitted: false
        }
     },
     computed: {
        ...mapState('network', ['networks', 'network'])
      },
     created () {
       this.initialize()
     },
     methods: {
       ...mapActions('network', ['fetchNetworks', 'setNetwork', 'createNetwork', 'updateNetworkForm']),
       async initialize () {
         await this.fetchNetworks({})
       },
       async openCreateNetworkDialog () {
         this.setNetwork({})
         this.submitted = false
         this.networkDialog = true
       },
       saveNetwork () {
         this.submitted = true
         if (this.network.name.trim()) {
             this.createNetwork({})
             this.$toast.add({ severity: 'success', summary: 'Succesful', detail: 'Network created', life: 3000 })
         this.networkDialog = false
         }
       },
       hideDialog () {
         this.networkDialog = false
         // this.submitted = false
       },
       goToNetwork (event) {
         this.setNetwork({ ...event.data })
         this.$toast.add({ severity: 'info', summary: 'Network Selected', detail: 'Name: ' + event.name, life: 3000 })
         this.$router.push({ name: 'networkdetails', params: { id: this.network.id } })
       }
     }
 }
       //  editNetwork (network) {
      //    this.network = { ...network }
      //    this.networkDialog = true
      //  },
      //  confirmDeleteNetwork (network) {
      //    this.network = network
      //    this.deleteNetworkDialog = true
      //  },

      //  async removeNetwork (network) {
      //    this.deleteNetworkDialog = false
      //    this.deleteNetwork({ id: network.id })
      //    // this.network = {}
      //    this.$toast.add({ severity: 'success', summary: 'Succesful', detail: 'Network Deleted', life: 3000 })
      //  },

            //  deleteNetwork () {
      //    this.deleteNetworkDialog = true
      //    this.$store.state.networks = this.$store.state.networks.filter(val => val.id !== this.network.id)
      //    this.network = {}
      //    this.$toast.add({ severity: 'success', summary: 'Succesful', detail: 'Network Deleted', life: 3000 })
      //  },

          //  if (this.network.id) {
          //    this.$store.state.networks[this.findIndexById(this.network.id)] = this.network
          //    this.$toast.add({ severity: 'success', summary: 'Succesful', detail: 'Network updated', life: 3000 })
          //  } else {

      //  findIndexById (id) {
      //      let index = -1
      //      for (let i = 0; i < this.$store.state.networks.length; i++) {
      //          if (this.$store.state.networks[i].id === id) {
      //            index = i
      //              break
      //          }
      //      }
        //    return index
        //  },
 </script>
