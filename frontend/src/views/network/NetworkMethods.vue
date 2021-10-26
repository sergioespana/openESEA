<template>
    <method-list :permission="permission" v-model:refresh="refresh" :networkmethods="true" :importablemethods="importableMethods" @import-method="importMethod" @drop-method="dropChosenMethod">
    <div v-if="permission">
        <Button label="Create Method" icon="pi pi-plus" class="p-button-success p-button-sm p-mr-2" @click="goToMethodCreation()" />
        <Button v-if="permission" :label="(importableMethods) ? 'Show owned Methods':'Import Method'" :class="(importableMethods) ? 'p-button-warning':'p-button-success'" class="p-button-sm" @click="importableMethods= !importableMethods" />
    </div>
    </method-list>

    <Dialog v-model:visible="dropDialog" style="width: 500px" header="Confirm Action" :modal="true"  :dismissableMask="true">
            Are you sure you want to remove the following methods?
            <div class="p-shadow-1 p-p-3 p-m-5">{{selectedMethod.name}}</div>
        <template #footer>
        <Button label="No" icon="pi pi-times" class="p-button-text" @click="dropDialog=false" />
        <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="dropMethod()" />
      </template>
    </Dialog>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import MethodList from '../../components/lists/MethodList'

export default {
    components: {
        MethodList
    },
    data () {
        return {
            importableMethods: false,
            refresh: false,
            selectedMethod: null,
            dropDialog: false
        }
    },
    computed: {
        ...mapState('network', ['network']),
        ...mapState('authentication', ['currentuser']),
        permission () {
            if (this.network.accesLevel) {
                const accesLevel = this.network.accesLevel
                if (accesLevel === 'admin' || accesLevel === 'network admin') {
                    return true
                }
            }
            return false
        }
    },
    watch: {
        importableMethods () {
            this.refresh = !this.refresh
        }
    },
    methods: {
        ...mapActions('network', ['patchNetwork']),
        async importMethod (method) {
            this.importableMethods = false
            console.log(this.network.methods)
            this.network.methods.push(method.id)
            await this.patchNetwork({ methods: this.network.methods })
            this.refresh = !this.refresh
        },
        dropChosenMethod (method) {
            this.selectedMethod = method
            this.dropDialog = true
        },
        async dropMethod () {
            const newListOfMethods = this.network.methods.filter((item) => item !== this.selectedMethod.id)
            await this.patchNetwork({ methods: newListOfMethods })
            this.dropDialog = false
            this.refresh = !this.refresh
        },
        goToMethodCreation () {
            this.$router.push({ name: 'methodcreation' })
        }
    }
}

// async getMethods () {
//     if (this.addMode) {
//         await this.fetchMethods({ query: `?excludenetwork=${this.$route.params.NetworkId}` })
//     } else {
//         await this.fetchMethods({ query: `?network=${this.$route.params.NetworkId}` })
//     }
//     this.loading = false
// },
// <!-- <Dialog v-model:visible="removeDialog" style="width: 500px" header="Confirm Action" modal="true"  dismissableMask="true">
//         Are you sure you want to <span v-if="removeMode"><b>delete</b></span><span v-if="addMode"><b>Add</b></span> the following methods(s)?
//         <div v-for="method in selectedMethods" :key="method.id" class="p-shadow-1 p-p-3 p-m-5">{{method}}</div>
//     <template #footer>
//     <Button label="No" icon="pi pi-times" class="p-button-text" @click="actionDialog=false" />
//     <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="addMode ? addMethods() : removeMethods()" />
//   </template>
// </Dialog>

//  <Dialog v-model:visible="inviteDialog" style="width: 500px" modal="true" dismissableMask="true" class="p-fluid">
//      <div class="p-field">
//         <MultiSelect id="organisations" v-model="organisationsToInvite" :options="organisations" optionLabel="name" optionValue="name" placeholder="Select Organisations" :filter="true" class="multiselect-custom">
//             <template #value="slotProps">
//                 <div v-for="option of slotProps.value" :key="option.id">
//                     <div>{{option}}</div>
//                 </div>
//                 <template v-if="!slotProps.value || slotProps.value.length === 0">
//                     Select Organisations
//                 </template>
//             </template>
//             <template #option="slotProps">
//                 <div>{{slotProps.option.name}}</div>
//             </template>
//         </MultiSelect>
//      </div>
//         <div class="p-field">
//         <label for="message">Message to Organisations</label>
//         <Textarea id="message" v-model="something" required="true" rows="3" cols="20" />
//         </div>
//     <template #footer>
//             <Button label="Invite Organisations" icon="pi pi-plus" @click="addOrganisations"/>
//             <Button label="Cancel" icon="pi pi-check" class="p-button-text" @click="inviteDialog=false" />
//     </template>
// </Dialog> -->

// columns:
// [
//     { field: 'name', header: 'Name' },
//     { field: 'description', header: 'Description' },
//     { field: 'surveys.length', header: 'Surveys' }
// ]
//     <!-- my-methods :columns=columns network-methods selection-enabled></my-methods> -->
// async addMethods () {
//     this.actionDialog = false
//     console.log('eeee', this.addMode, this.removeMode, this.selectedMethods.length)
//     if (this.addMode && this.removeMode) { return }
//     if (this.selectedMethods.length && this.addMode) {
//         console.log('check')
//         const result = this.selectedMethods.map(a => a.id)
//         const newMethods = this.network.methods.concat(result)
//         await this.patchNetwork({ methods: newMethods })
//     }
//     this.addMode = false
// },
// async removeMethods () {
//     this.actionDialog = false
//     if (this.addMode && this.removeMode) { return }
//     if (this.selectedMethods.length && this.removeMode) {
//         const result = this.selectedMethods.map(a => a.id)
//         const newListOfMethods = this.network.methods.filter((item) => !result.includes(item))
//         await this.patchNetwork({ methods: newListOfMethods })
//     }
//     this.getMethods()
// },
// async goToMethod (method) {
//     this.selectedMethods = []
//     if (this.addMode) {
//         this.selectedMethods.push(method)
//         this.actionDialog = true
//         return
//     }
//     if (this.removeMode) {
//         this.selectedMethods.push(method)
//         this.actionDialog = true
//         return
//     }
//     if (method.id) {
//         await this.setMethod(method)
//         this.$router.push({ name: 'newmethoddetails', params: { id: this.method.id } })
//     }
// },
</script>
