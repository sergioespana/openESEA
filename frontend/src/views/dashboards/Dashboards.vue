<template>
    <div id="dashboard-overview">
        <div class="dashboard-header-section">
            <div class="upload-model-wrapper">
                <UploadFileButton :fileInputId="'modelInput'" @fileUploaded="$event=>handleFileUploaded('model',$event)" iconClass="pi pi-chart-bar"/>
            </div>
            <div class="title-wrapper">
                <h1 class="overview-title">Dashboards Overview</h1>
            </div>
            <div class="upload-data-wrapper">
                <UploadFileButton :fileInputId="'dataInput'" @fileUploaded="$event=>handleFileUploaded('data',$event)" iconClass="pi pi-upload"/>
            </div>
        </div>
        <div id="dashboard-contents-wrapper">
        </div>
    </div>
</template>

<script>
    import BarChart from '../../components/charts/BarChart.vue'
    // import LineChart from '../../components/charts/LineChart.vue'
    import UploadFileButton from '../../components/buttons/UploadFileButton.vue'

    import { createApp, h } from 'vue'
    import { parse as yamlParse } from 'yaml'

    export default {
        name: 'Dashboard',
        components: {
            UploadFileButton
        },
        methods: {
            loadDashboard (result) {
                var dashboardWrapperElement = document.getElementById('dashboard-contents-wrapper')

                // Remove previous dashboard
                while (dashboardWrapperElement.firstChild) {
                    dashboardWrapperElement.removeChild(dashboardWrapperElement.firstChild)
                }

                // Create new dashboard elements
                const fileContents = result
                var yamlData = yamlParse(fileContents)
                var title = yamlData.Overviews[0].Name
                var visualisations = yamlData.Overviews[0].BodySection.Visualisations
                var titleElement = document.createElement('h1')
                titleElement.innerHTML = title
                dashboardWrapperElement.appendChild(titleElement)

                for (var vis of visualisations) {
                    var data = {
                        labels: vis.Query.map(el => el.x), // ['January', 'February', 'August'],
                        datasets: [{ data: vis.Query.map(el => el.y) }] // [{ data: [40, 20, 12] }]
                    }
                    if (this.data) {
                        data = {
                            labels: this.data.map(el => el.Label),
                            datasets: [{ data: this.data.map(el => el.Quantity) }]
                        }
                    }
                    // Display charts
                    var ComponentApp = createApp({
                      setup () {
                        return () => h(BarChart, {
                          chartData: data
                        })
                      }
                    })
                    // Insert new dashboard element
                    var wrapper = document.createElement('div')
                    ComponentApp.mount(wrapper)
                    dashboardWrapperElement.appendChild(wrapper)
                }
            },
            saveData (data) {
                var jsonData = JSON.parse(data)
                console.log(jsonData)
                this.data = jsonData
            },
            handleFileUploaded (type, file) {
                // Access the file data here
                const fr = new FileReader()

                console.log(type, file)

                // If file is loaded, load dashboard or save data
                fr.onload = () => {
                    if (type === 'model') {
                        this.loadDashboard(fr.result)
                    } else if (type === 'data') {
                        this.saveData(fr.result)
                    }
                }

                // Read file
                fr.readAsText(file)
            }
        },
        data () {
            return {
                model: null,
                data: null
            }
        }
    }
</script>

<style>

.dashboard-header-section {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.title-wrapper {
  margin-left: 10px;
  margin-right: 10px;
  align-items: center;
}

.upload-model-wrapper {
  align-items: left;
}

.upload-data-wrapper {
  align-items: right;
}

</style>
