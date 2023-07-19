<template>
    <div class="file-upload">
        <div class="file-upload-wrapper">
            <div class="file-upload-area">
                <input type="file" accept="application/JSON, .yaml, .yml" :id="fileInputId" @change="$event=>this.handleFileChange($event)" :hidden="true"/>
                <label :for="fileInputId" class="upload-button">
                    <i :class="iconClass"></i>
                </label>
            </div>
            <div v-if="success === false" class="error-message">
                <i class="pi pi-times"></i>
            </div>
            <div v-else-if="success === true" class="success-message">
                <i class="pi pi-check"></i> File uploaded successfully!
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'UploadFileButton',
    data () {
        return {
            success: null
        }
    },
    props: {
        iconClass: {
            type: String,
            default: () => 'pi pi-upload'
        },
        fileInputId: {
            type: String,
            required: true
        }
    },
    methods: {
        handleFileChange (e) {
            // Check if file is selected
            if (e.target.files && e.target.files[0]) {
                // Get uploaded file
                const file = e.target.files[0]
                // Update status to success
                this.success = true
                // Emit the fileUploaded event with the file data
                this.$emit('fileUploaded', file)
            } else {
                // Else not successful
                this.success = false
            }
            // Reset file such that you can upload it again
            e.target.value = ''
            // Reset success
            setTimeout(() => {
                this.success = null
            }, 2000)
        }
    }
}
</script>

<style scoped>

/* Upload area */
.file-upload {
  height: auto;
  width: 100%;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

/* Wrapper for centering elements */
.file-upload-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Box around button */
.file-upload .file-upload-area {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  padding: 10px;
  border-radius: 8px;
}

/* Change cursor to pointer */
.file-upload .file-upload-area label.upload-button {
  cursor: pointer;
}

/* Upload icon */
.file-upload .file-upload-area label.upload-button i {
  font-size: 24px;
  color: #333;
}

/* Display success */
.file-upload .success-message {
  margin-left: 10px;
  margin-top: 5px;
  color: green;
  font-size: 14px;
}

</style>
