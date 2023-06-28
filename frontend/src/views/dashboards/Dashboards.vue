<template>
    <div class="wrapper-dropdown">
        <div class="dropdown-trigger" v-on:click="$event => toggleDropdown()">
            <i class="pi pi-ellipsis-v"></i>
        </div>
        <div class="dropdown-content" v-show="showDropdown">
            <UploadFileButton :fileInputId="'modelInput'" @fileUploaded="$event => handleModelUploaded($event)" iconClass="pi pi-chart-bar" />
            <UploadFileButton :fileInputId="'dataInput'" @fileUploaded="$event => handleDataUploaded($event)" iconClass="pi pi-upload" />
        </div>
    </div>
    <Dashboard v-if="modelUploaded"></Dashboard>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'

import UploadFileButton from '../../components/buttons/UploadFileButton.vue'
import Dashboard from './Dashboard.vue'

import { load as yamlLoad } from 'yaml'

export default {
    name: 'Dashboards',
    components: {
        UploadFileButton,
        Dashboard
    },
    methods: {
        ...mapGetters('dashboard', { getDashboard: 'getDashboard' }),
        ...mapMutations('dashboard', { setDashboard: 'setDashboard', setCurrentOverview: 'setCurrentOverview' }),
        toggleDropdown () { this.showDropdown = !this.showDropdown },
        async saveDashboard (model) {
            await this.setDashboard(model)
            await this.setCurrentOverview(0)
        },
        async loadDashboard (fileContents) {
            const model = yamlLoad(fileContents)
            await this.saveDashboard(model)
            this.modelUploaded = true
        },
        saveData (data) {
            // data = '{"Hello":"Goodbye"}'
            // var jsonData = JSON.parse(data)
            // console.log(jsonData)
            // this.data = vl.jsonFormat(jsonData)
            // console.log(d3.autoType(jsonData))
        },
        handleDataUploaded (file) {
            const fr = new FileReader()
            fr.onload = () => { this.saveData(fr.result) }
            fr.readAsText(file)
        },
        handleModelUploaded (file) {
            const fr = new FileReader()
            fr.onload = () => { this.loadDashboard(fr.result) }
            fr.readAsText(file)
        }
    },
    data () {
        return {
            showDropdown: true,
            modelUploaded: false,
            data: null
        }
    }
}
</script>

<style>
.wrapper-dropdown {
  position: absolute;
  top: 50%;
  right: 0;
  z-index: 5;
}

.dropdown-trigger {
  cursor: pointer;
}

.dropdown-content {
  border: 1px solid #ddd;
    padding: 2vh;
}
</style>
