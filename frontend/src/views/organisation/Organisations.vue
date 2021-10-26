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
// <div class="p-d-flex p-jc-between p-m-5">
//     <div>
//         <Button :label="(allOrganisations ? 'All Organisations' : 'My Organisations')" class="p-button-sm p-mr-2" @click="allOrganisations = !allOrganisations"/>
//         <Button label="Change Display" class="p-button-sm p-mr-2" @click="tableDisplay = !tableDisplay" />
//         <Button label="Create Organisation" icon="pi pi-plus" class="p-button-success p-button-sm" @click="createOrganisationDialog=true" />
//     </div>
//     <span class="p-input-icon-left">
//         <i class="pi pi-search" /><InputText v-model="search" placeholder="Search Organisations..." />
//     </span>
// </div>
// <Divider />
// async goToOrganisation (organisation) {
//     if (organisation.id) {
//         await this.setOrganisation(organisation)
//         this.$router.push({ name: 'organisationoverview', params: { OrganisationId: organisation.id } })
//     }
// }
</script>
