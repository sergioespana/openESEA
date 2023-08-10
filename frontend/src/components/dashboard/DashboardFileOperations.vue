<template>
    <div class="wrapper-dropdown">
        <div class="dropdown-trigger" v-on:click="toggleDropdown">
            <i class="pi pi-ellipsis-v"></i>
        </div>
        <div v-show="showDropdown">
            <UploadFileButton :fileInputId="'modelUpload'" @fileUploaded="handleModelUpload" :iconClass="'pi pi-chart-line'"/>
            <DownloadFileButton :fileInputId="'modelDownload'" @buttonClicked="handleModelDownload"/>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

import UploadFileButton from '../../components/buttons/UploadFileButton.vue'
import DownloadFileButton from '../../components/buttons/DownloadFileButton.vue'

export default {
    name: 'Dashboards',
    components: {
        UploadFileButton,
        DownloadFileButton
    },
    data () {
        return {
            showDropdown: true
        }
    },
    methods: {
        ...mapGetters('dashboardModel', ['getDashboardModel']),
        toggleDropdown () { this.showDropdown = !this.showDropdown },
        // Handle file uploads or downloads
        handleDataUpload (file) {
            const fr = new FileReader()
            fr.onload = () => { this.$emit('dataIsUploaded', fr.result, file) }
            fr.readAsText(file)
        },
        handleModelUpload (file) {
            const fr = new FileReader()
            fr.onload = () => { this.$emit('modelIsUploaded', fr.result, file) }
            fr.readAsText(file)
        },
        handleModelDownload () {
            const dashboardModel = this.getDashboardModel()()
            const jsonDataStr = JSON.stringify(dashboardModel, null, '\t')
            const blob = new Blob([jsonDataStr], { type: 'application/json' })
            const url = URL.createObjectURL(blob)
            const link = document.createElement('a')
            link.href = url
            link.download = 'dashboard.json'
            link.click()
            URL.revokeObjectURL(url)
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
</style>
