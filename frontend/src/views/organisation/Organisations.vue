<template>
    <div class="p-m-1" style="min-width: 1000px;">
        <h1>Organisations Overview</h1>
        <Button label="Create Organisation" icon="pi pi-plus" class="p-button-success p-button-sm p-d-flex p-m-5" @click="createOrganisationDialog=true" />
        <organisation-list :organisations="organisations">
        </organisation-list>
    </div>
    <Dialog v-model:visible="createOrganisationDialog" style="width: 500px" header="Organisation Details" :modal="true" :dismissableMask="true">
        <organisation-form @closedialog="createOrganisationDialog=false" />
    </Dialog>
</template>

<script>
    import OrganisationList from '../../components/lists/OrganisationList'
    import OrganisationForm from '../../components/forms/OrganisationForm'

    export default {
        components: {
            OrganisationList,
            OrganisationForm

        },
        data () {
            return {
                createOrganisationDialog: false
            }
        }
    }
</script>
