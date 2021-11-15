// Used by MethodSidebarComponent.vue

<template>
    <div class="p-text-left">
        <div class="p-m-2" style="height: 50px;">
                <div class="p-d-flex p-mt-2">
                <div v-for="item in ComponentOptions" :key="item" class="p-col-4" style="font-size: 14px;" :style="(item === filterOption) ? 'border-bottom: 1px solid #00695C; font-size;':'border-bottom: 1px solid lightgrey;'" @click="filterOption = item">
                    {{item}}
                </div>
            </div>
            <span class="p-input-icon-left" style="width: 100%">
                <i class="pi pi-search" /><InputText ref="searchbarQuestions" v-model="searchbar" placeholder="Search Components..." style="width: 100%;" />
            </span>
        </div>
        <div class="p-mt-5" style="height: calc(100vh - 280px); overflow-y: scroll;">
            <div v-for="item in filteredItems" :key="item" class="directIndicators p-m-1" style="font-size: 16px; padding: 10px; overflow: hidden; border: 1px solid lightgrey; cursor: grab;" :style="(item.id === activeItem?.id) ? 'background-color: #EEEEEE;':''"  @dragstart="startDrag($event, item)" @dragover.prevent @dragenter.prevent :draggable="true">
                <span v-if="itemType === 'topic'">{{item.name}}</span><span v-else>{{item.key}}</span>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        props: {
            items: {
                type: Array,
                default: function () {
                    return []
                }
            },
            activeItem: {
                type: Object
            },
            itemType: {
                type: String
            }
        },
        data () {
            return {
                ComponentOptions: ['Unused', 'Used', 'All'],
                filterOption: 'Unused',
                searchbar: ''
            }
        },
        computed: {
            filteredItems () {
                if (this.itemType !== 'topic') {
                    if (this.filterOption === 'Unused') {
                        return this.items.filter(item => !(item.topic > 0))
                    } else if (this.filterOption === 'Used') {
                        return this.items.filter(item => item.topic > 0)
                    }
                }
                return this.items
            }
        },
        watch: {
            filterOption (val) {
                this.$emit('filteroption', val)
            },
            searchbar () {
                this.$emit('update:searchbar', this.searchbar)
            }
        },
        methods: {
            startDrag (evt, item) {
                console.log(item)
                evt.dataTransfer.dropEffect = 'move'
                evt.dataTransfer.effectAllowed = 'move'
                if (typeof item === 'object') {
                    item = JSON.stringify(item)
                }
                evt.dataTransfer.setData('draggedItem', item)
            }
        }
    }
</script>

<style lang="scss" scoped>
    .directIndicators:hover {
        background-color: #EEEEEE;
    }
</style>
