<template>
     <div class="p-d-flex p-jc-between p-ai-center p-m-5">
            <div class="p-d-flex p-ai-center">
                <!-- <Button :label="(allNetworks ? 'All Networks' : 'My Networks')" class="p-button-sm p-mr-2" @click="allNetworks = !allNetworks"/> -->
                <div  v-if="includecheckbox" class="p-ml-2">
                    <Checkbox id="includeItems" v-model="allItems" :binary="true" class="p-mr-2" @change="changeShownItems()" />
                    <label for="includeItems">Include Public {{name}}</label>
                 </div>
                <div v-else>
                    <slot>
                    </slot>
                </div>
            </div>
            <div class="p-d-flex p-ai-center">
                                <div class="p-d-flex p-ai-center">
                <i class="pi pi-list" :style="(tabledisplay ? 'color: lightgrey;': '')" style="font-size: 30px;" @click="changeDisplay()" />
                <i class="pi pi-microsoft p-mx-3" :style="(tabledisplay ? '' : 'color: lightgrey;')" style="font-size: 23px;" @click="changeDisplay()" />
                </div>
                <span class="p-input-icon-left">
                    <i class="pi pi-search" /><InputText v-model="search" placeholder="Search through items..." />
                </span>
            </div>
     </div>
     <Divider />
</template>

<script>
export default {
    props: {
        name: {
            type: String,
            default: 'items'
        },
        tabledisplay: {
            type: Boolean,
            default: false
        },
        includecheckbox: {
            type: Boolean,
            default: false
        },
        showpublicitems: {
            type: Boolean,
            default: false
        }
    },
    data () {
        return {
            allItems: false,
            search: ''
        }
    },
    watch: {
        search () {
             this.$emit('update:search', this.search)
        }
    },
    methods: {
        changeDisplay () {
            console.log('check')
            const tabledisplay = !this.tabledisplay
            this.$emit('update:tabledisplay', tabledisplay)
        },
        changeShownItems () {
            this.$emit('update:allitems', this.allItems)
        }
    }
}
//   <!-- <Button label="Join Network" />
//   <Button label="Remove Network" /> -->
//   !-- <Button v-if="true" :label="joinButton? 'Show own Networks' : 'Join Network'" :icon="joinButton? '' : 'pi pi-plus'" :class="joinButton? 'p-button-warning' : 'p-button-success'" class="p-mx-2 p-button-sm" @click="joinableNetworks" />
//   <Button v-if="true" :label="removeMode ? 'Select the networks to remove': 'Enable Remove Mode'" icon="pi pi-trash" class="p-button-sm" :class="removeMode ? 'p-button-danger' : 'p-button-warning'" :disabled="!networks.length" @click="removeMode = !removeMode" /> -->
</script>
