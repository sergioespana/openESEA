<template>
    <div class="p-m-1" style="min-width: 1000px;">
        <h1>Methods Overview</h1>
        <div class="p-d-flex p-jc-between p-m-5">
            <Button label="Create Method" icon="pi pi-plus" class="p-button-success p-button-sm" @click="goToMethodCreate()" />
        </div>
        <method-list :methods="methods" />
    </div>
</template>

<script>
import { mapState } from 'vuex'
import MethodList from '../../components/lists/MethodList'

export default {
    components: {
        MethodList
    },
    data () {
        return {
            createMethodDialog: false
        }
    },
    computed: {
        ...mapState('method', ['methods', 'method'])
    },
    methods: {
        async goToMethodCreate () {
            this.$router.push({ name: 'methodcreation' })
        }
    }
}
    // <!-- <Dialog v-model:visible="createMethodDialog" style="width: 500px" header="Method Details" :modal="true" :dismissableMask="true">
    //     <method-form @closedialog="createMethodDialog=false" />
    // </Dialog> -->
    // <!-- <div class="methods">
    //     <h1>Methods Overview</h1>
    //     <Button label="Method Wizard" @click="goToMethodCreate" />
    //     <Toast position="top-right"/>
    //     <div class="card p-m-5 p-shadow-2">
    //         <my-methods :columns="columns" selection-enabled></my-methods>
    //     </div>
    // </div> -->
    // <!-- <Dialog v-model:visible="methodDialog" :style="{width: '450px'}" header="Method Details" :modal="true" class="p-fluid">
    //     <div class="p-field">
    //         <label for="name">Name</label>
    //         <InputText id="name" v-model.trim="method.name" required="true" autofocus :class="{'p-invalid': submitted && !method.name}"
    //         @blur="updateMethodForm({ name: $event.target.value })" />
    //         <small class="p-error" v-if="submitted && !method.name">Name is required.</small>
    //     </div>
    //     <div class="p-field">
    //         <label for="description">Description</label>
    //         <Textarea id="description" v-model="method.description" required="true" rows="3" cols="20"
    //         @blur="updateMethodForm({ description: $event.target.value })" />
    //     </div>
    //     <div class="p-field">
    //         <label for="ispublic">Should this method be public? </label>
    //         <SelectButton id="ispublic" v-model="method.ispublic" required="true" :options="ispublicbool"
    //         @blur="updateMethodForm({ ispublic: $event.target.value })" />
    //     </div>
    //     <template #footer>
    //         <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="hideDialog"/>
    //         <Button label="Save" icon="pi pi-check" class="p-button-text" @click="saveMethod" :disabled="!method.name" />
    //     </template>
    // </Dialog> -->
</script>
