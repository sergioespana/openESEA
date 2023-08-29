<template>
    <!-- Icon for opening dashboard model edit text dialog -->
    <div class="edit-sidebar-model">
        <i class="pi pi-user-edit" v-on:click="openDialog"></i>
    </div>
    <!-- Dialog screen for editing dashboard model -->
    <Dialog class="dialog-screen" modal
        header="Edit Dashboard Model"
        :visible="visible"
        @update:visible="closeDialog">
        <!-- Area for editing dashboard model -->
        <TextArea class="dashboard-model-text-area"
            v-model="dashboardModel" >
        </TextArea>
        <!-- Footer for cancel or save buttons -->
        <template #footer>
            <Button label="Cancel" icon="pi pi-times" @click="closeDialog" text></Button>
            <Button label="Apply Changes" icon="pi pi-check" @click="saveModel" autofocus></Button>
        </template>
    </Dialog>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'

import Dialog from 'primevue/dialog'
import TextArea from 'primevue/textarea'

export default {
    components: {
        Dialog,
        TextArea
    },
    data () {
        return {
            visible: false,
            dashboardModel: ''
        }
    },
    computed: {
        ...mapState('dashboardModel', ['dashboard'])
    },
    methods: {
        ...mapGetters('dashboardModel', ['getDashboardModel']),
        ...mapActions('dashboardModel', ['createDashboardModel']),
        showDialog () {
            this.visible = true
        },
        closeDialog () {
            this.visible = false
        },
        async openDialog () {
            const dashboardModel = await this.getDashboardModel()()
            this.dashboardModel = JSON.stringify(dashboardModel, null, '\t')
            this.showDialog()
        },
        async saveModel () {
            const dashboardModel = JSON.parse(this.dashboardModel)
            const payload = { value: dashboardModel }
            await this.createDashboardModel(payload)
            this.closeDialog()
        }
    }
}
</script>

<style>
.dialog-screen {
    max-width: 60vw;
    max-height: 70vh;

    min-width: 60vw;
    min-height: 70vh;

    width: 60vw;
    height: 70vh;
}
.dashboard-model-text-area {
    max-width: 100%;
    max-height: 100%;

    min-width: 100%;
    min-height: 100%;

    width: 100%;
    height: 100%;
}
</style>
