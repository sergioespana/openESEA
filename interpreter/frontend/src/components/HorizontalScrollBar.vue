// used by NetworkOverview.vue

<template>
    <div class="p-p-3 p-m-3 p-shadow-2" style="border: 1px solid #e2e2e2;">
        <div class="p-d-flex p-jc-between">
            <h3 class="p-text-left"><router-link v-if="itemslink" :to="{name: itemslink, params: { NetworkId: $route.params.NetworkId } }" style="text-decoration: none; color: blue;">{{name}}</router-link><span v-else>{{name}}</span></h3>
            <h3>Page {{currentPage}} of {{itemPages}}</h3>
        </div>
        <div class="p-d-flex p-jc-between p-ai-center" style="height: 150px; width: 100%;">
            <div style="width: 50px;">
                <div v-if="currentPage !== (0 && 1)" class="scrollIcon p-d-flex" @click="itemsScroll('left')"> <i class="pi pi-angle-left p-as-center" style="font-size: 3rem;" /> </div>
            </div>
            <ProgressSpinner v-if="loading && !failedLoad" class="p-ai-center" style="height: 100%;"/>
            <div v-else-if="loading && failedLoad" class="p-text-italic">{{name}} could not be retrieved!</div>
            <div v-else-if="items.length" ref="itemss" class="p-grid" style="width: 100%;">
                <div v-for="item, index in itemsbar" :key="item" @mouseover="item.hover=true" @mouseleave="item.hover=false" :class="'p-col'">
                    <div class="p-grid" :class="((item.hover && !item.placeholder) ? 'p-shadow-5 p-mx-0 p-text-bold' : 'p-shadow-1 p-mx-2')" style="height: 150px;" :style="[item.placeholder ? 'background-color: lightgrey' : 'background-color: #F3F3F3', (item.hover && !item.placeholder) ? 'background-color: white' : '']" @click.left="goToItem(item)">
                        <p v-if="item.name" class="p-as-center" style="width: 100%;">{{index + 1}}. {{item.name}}</p>
                        <h5 v-if="item.method" class="p-as-center" style="width: 100%;">{{item.method_name}}</h5>
                    </div>
                </div>
            </div>
            <h3 v-else-if="permission" class="p-text-italic p-text-light">
                <slot></slot>
            </h3>
            <h3 v-else>
                None to show
            </h3>
            <div style="width: 50px;">
                <div v-if="currentPage !== itemPages" class="scrollIcon p-d-flex" @click="itemsScroll('right')"> <i class="pi pi-angle-right p-as-center" style="font-size: 3rem;" /> </div>
            </div>
        </div>
    </div>
</template>

<script>
    import ProgressSpinner from 'primevue/progressspinner'

    export default {
        components: {
            ProgressSpinner
        },
        props: {
            items: {
                type: Array
            },
            name: {
                type: String,
                required: true
            },
            permission: {
                type: Boolean,
                required: false
            }
        },
        data () {
            return {
                loading: true,
                failedLoad: false,
                itemsbar: [],
                currentPage: 1,
                itemsPerPage: 4
            }
        },
        computed: {
            itemPages () {
                const page = Math.ceil(this.items.length / this.itemsPerPage)
                return page
            }
        },
        watch: {
            items: function () {
                if (this.items) {
                    this.checkWindowSize()
                }
            }
        },
        created () {
            // Gets window size in order to show correct amount of items
            window.addEventListener('resize', this.checkWindowSize)
            setTimeout(() => { this.failedLoad = true }, 10000)
        },
        methods: {
            checkWindowSize () {
                const itemWidth = this.$refs.itemss?.clientWidth
                if (itemWidth) {
                    this.itemsPerPage = Math.floor(itemWidth / 250)
                }

                if (this.currentPage > this.itemPages) {
                    this.currentPage = this.itemPages
                }
                this.changeDisplayedItems()
            },
            changeDisplayedItems () {
                this.itemsbar = this.items.slice(((this.currentPage - 1) * this.itemsPerPage), (this.currentPage * this.itemsPerPage))

                if (!this.itemsbar.length || (this.itemsbar.length % this.itemsPerPage !== 0)) {
                    const placeholderItems = this.itemsPerPage - (this.itemsbar.length % this.itemsPerPage)
                    for (let i = 0; i < placeholderItems; i++) {
                        this.itemsbar.push({ hover: false, placeholder: true })
                    }
                }
                if (this.items) {
                    this.loading = false
                }
            },
            itemsScroll (direction) {
                if (direction === 'left' && this.currentPage > 1) {
                    this.currentPage--
                }
                if (direction === 'right' && this.currentPage < this.itemPages) {
                    this.currentPage++
                }
                this.changeDisplayedItems()
            },
            goToItem (item) {
                this.$emit('clicked-item', item, this.name.toLowerCase())
            }
        }
    }
</script>

<style lang="scss" scoped>
    .scrollIcon {
        color: grey;
        &:hover {
            background-color: #EFEEEE;
            color: black;
        }
    }
</style>
