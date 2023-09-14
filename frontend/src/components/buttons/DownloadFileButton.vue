<template>
    <div class="file-download">
        <div class="file-download-wrapper">
            <div class="file-download-area">
                <button :id="fileInputId" @click="onClick()" :hidden="true"></button>
                <label :for="fileInputId" class="download-button">
                    <i :class="iconClass"></i>
                </label>
            </div>
            <div v-if="clicked" class="download-message">
                <i class="pi pi-spinner"></i> Downloading file...
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'DownloadFileButton',
    props: {
        iconClass: {
            type: String,
            default: () => 'pi pi-download'
        },
        fileInputId: {
            type: String,
            required: true
        }
    },
    data () {
        return {
            clicked: null
        }
    },
    methods: {
        onClick (e) {
            this.clicked = true
            this.$emit('buttonClicked')

            setTimeout(() => {
                this.clicked = null
            }, 2000)
        }
    }
}
</script>

<style scoped>

/* Upload area */
.file-download {
  height: auto;
  width: 100%;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

/* Wrapper for centering elements */
.file-download-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Box around button */
.file-download .file-download-area {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  padding: 10px;
  border-radius: 8px;
}

/* Change cursor to pointer */
.file-download .file-download-area label.download-button {
  cursor: pointer;
}

/* Upload icon */
.file-download .file-download-area label.download-button i {
  font-size: 24px;
  color: #333;
}

/* Display success */
.file-download .download-message {
  margin-left: 10px;
  margin-top: 5px;
  color: blue;
  font-size: 14px;
}

</style>
