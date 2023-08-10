<template>
    <div class="edit-element">

        <!-- Editing sidebar with icons -->
        <div class="edit-sidebar p-p-0">

            <!-- Arrow for folding/unfolding editing area  -->
            <div class="edit-sidebar-angle" v-on:click="goIntoEdit(selectedEditElement)">
                <i class="pi pi-angle-right larger-icon" v-if="editing"></i>
                <i class="pi pi-angle-left larger-icon" v-else></i>
            </div>

            <div :style="{ height: '40px' }"></div>

            <!-- Icon for different edit elements -->
            <div v-for="editElement in editElements" v-bind:key="editElement.name">
                <i :class='editElement.icon' v-on:click="goIntoEdit(editElement.name)"></i>

                <div :style="{ height: '20px' }"></div>
            </div>

            <div :style="{ 'flex-grow': '1' }">
                <!-- Edit Dashboard model directly -->
                <ModifyDashboardModel></ModifyDashboardModel>
                <!-- Save button -->
                <div class="edit-sidebar-discard" v-on:click="this.$emit('discardButtonClicked')">
                    <i class="pi pi-times"></i>
                </div>
                <div class="edit-sidebar-save" v-on:click="this.$emit('saveButtonClicked')">
                    <i class="pi pi-save"></i>
                </div>
            </div>
        </div>

        <!-- Editing area which is shown in editing mode -->
        <div v-if="editing" class="edit-area-position edit-area-style">
            <div v-for="editElement in editElements" v-bind:key="editElement.name">
                <div v-if="editElement.name === selectedEditElement">
                    <div v-for="component in editElement.components" v-bind:key="component">
                        <component :is="component"></component>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import EditDashboard from './editing/EditDashboard.vue'
import EditOverview from './editing/EditOverview.vue'
import EditContainer from './editing/EditContainer.vue'
import EditVisualisation from './editing/EditVisualisation.vue'
import EditImage from './editing/EditImage.vue'
import ModifyDashboardModel from './editing/ModifyDashboardModel.vue'

export default {
    components: {
        EditDashboard,
        EditOverview,
        EditContainer,
        EditVisualisation,
        EditImage,
        ModifyDashboardModel
    },
    data () {
        return {
            editing: false,
            selectedEditElement: 'Dashboard',
            editElements: [
                {
                    name: 'Dashboard',
                    icon: 'pi pi-chart-line',
                    components: [EditDashboard, EditOverview]
                },
                {
                    name: 'Container',
                    icon: 'pi pi-clone',
                    components: [EditContainer]
                },
                {
                    name: 'Visualisation',
                    icon: 'pi pi-chart-bar',
                    components: [EditVisualisation]
                },
                {
                    name: 'Image',
                    icon: 'pi pi-image',
                    components: [EditImage]
                }
            ]
        }
    },
    methods: {
        goIntoEdit (targetEditElement) {
            // Toggle editing mode or go to selected edit element
            if (targetEditElement !== this.selectedEditElement) {
                this.selectedEditElement = targetEditElement
                this.editing = true
            } else {
                this.editing = !this.editing
            }

            // Width of edit area in pixels
            const pixels = this.editing ? 200 : 0

            // Get dashboard element and set edit area to this given width
            const dashboardElement = document.querySelector('.organisation-dashboard')
            dashboardElement.style.setProperty('--edit-area-current-width', pixels + 'px')
        }
    }
}
</script>

<style>
.edit-sidebar {
    width: calc(var(--edit-sidebar-width));
    height: 100%;
    right: 0;
    position: absolute;
    border-color: gray;
    border-style: solid;
    background-color: #c0c0c0;
    border-width: 1px;
}
.edit-sidebar-angle {
    top: 2px;
    left: -1px;
    position: relative;
}
.edit-sidebar-save {
    bottom: 0;
    left: 1px;
    position: absolute;
}
.edit-sidebar-discard {
    bottom: 25px;
    left: 1px;
    position: absolute;
}
.edit-sidebar-model {
    position: absolute;
    bottom: 50px;
    left: 1px;
    cursor: pointer;
}
.edit-sidebar i {
    color: gray;
    cursor: pointer;
}
.edit-area-style {
    border-color: gray;
    border-style: solid;
    background-color: #e8e8e8;
}
.larger-icon {
    font-size: calc(var(--edit-sidebar-width));
}

/* Styling for edit areas */
.full-width {
    width: 100%
}
.near-width {
    width: 98%
}
.edit-area-field {
    text-align: left;
    color: gray;
    font-size: small;
}
.edit-area-title {
    background-color: gray;
    height: 23px;
    /* vertical-align: middle; */
    display: flex;
    align-items:center;
    justify-content:center;
}
.edit-area-position {
    right: calc(var(--edit-sidebar-width) - 1px); /* -1px such that there is no double border from edit area and edit sidebar */
    width: calc(var(--edit-area-current-width));
    height: 100%;
    position: absolute;
    overflow-y: auto;
}
</style>
