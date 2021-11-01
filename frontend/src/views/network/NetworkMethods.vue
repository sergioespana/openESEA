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
</script>
