<template>
aa
     <Dialog v-model:visible="dialog" style="{width: '450px'}" header="Unsaved Changes" :modal="true">
        <div class="confirmation-content">
            This page contains unsaved changes, leaving the page now will destroy these. Do you still wish to leave the page?
        </div>
        <template #footer>
            <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="decision(true)" />
            <Button label="No" icon="pi pi-times" class="p-button-text" @click="decision(false)"/>
      </template>
    </Dialog>
</template>

<script>
    export default {
        props: {
            visible: {
                type: Boolean,
                default: true
            }
        },
        data () {
            return {
                dialog: this.visible
            }
        },
        methods: {
            decision (choice) {
                this.$emit('decision', choice)
            }
        }
    }
</script>
