<template>
    <div class="wrapper-dropdown">
        <div class="dropdown-trigger" v-on:click="$event => toggleDropdown()">
            <i class="pi pi-ellipsis-v"></i>
        </div>
        <div class="dropdown-content" v-show="showDropdown">
            <div class="wrapper-upload-model">
                <UploadFileButton :fileInputId="'modelInput'" @fileUploaded="$event => handleModelUploaded($event)" iconClass="pi pi-chart-bar" />
            </div>
            <div class="wrapper-upload-data">
                <UploadFileButton :fileInputId="'dataInput'" @fileUploaded="$event => handleDataUploaded($event)" iconClass="pi pi-upload" />
            </div>
        </div>
    </div>
    <div :id="topLevelId()" class="wrapper-dashboard">
    </div>
    <BarChart hidden :chartData="{
                            labels: ['x','y', 'z'],
                            datasets: [ { data: [10, 2, 5] }]
                        }"></BarChart>
</template>

<script>
import UploadFileButton from '../../components/buttons/UploadFileButton.vue'
import Dashboard from './Dashboard.vue'
import BarChart from '../../components/charts/BarChart.vue'

import createDivWrapper from '../../utils/createDivWrapper.js'
import { load as yamlLoad } from 'yaml'
// import * as vl from 'vega-lite-api'
// import * as d3 from 'd3'

export default {
    name: 'Dashboards',
    components: {
        UploadFileButton,
        BarChart
    },
    methods: {
        toggleDropdown () { this.showDropdown = !this.showDropdown },
        topLevelId () { return 'wrapper-dashboard' },
        loadDashboard (fileContents) {
            this.model = yamlLoad(fileContents)
            var model = this.model
            console.log('Dashboard model:', model)

            // Get current dashboard
            var parent = document.getElementById(this.topLevelId())

            // Remove previous dashboard elements
            while (parent.firstChild) {
                parent.removeChild(parent.firstChild)
            }

            // Load new dashboard
            if (model) createDivWrapper(parent, Dashboard, { yamlData: model })
        },
        saveData (data) {
            // data = '{"Hello":"Goodbye"}'
            var jsonData = JSON.parse(data)
            console.log(jsonData)
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
            showDropdown: false,
            model: null,
            data: null
        }
    }
}
</script>

<style>
.wrapper-dropdown {
  position: absolute;
  right: 0;
  /* z-index: 1; */
}

.dropdown-trigger {
  cursor: pointer;
}

.dropdown-content {
  border: 1px solid #ddd;
}

.wrapper-upload-model .wrapper-upload-data {
    padding: 2vh;
}

</style>
