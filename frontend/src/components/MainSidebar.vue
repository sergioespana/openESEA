// Used by MainSidebar.vue

<template>
    <div :style="(sidebar ? 'width: 350px':'width: 55px')" class="sidebar">
        <div style="height: 100%;">
            <div v-for="(item, index) in navElements" :key="item" > <!-- a href="#" -->
                <div class="sidebar-element p-d-flex p-ai-center" :style="(($route.name?.startsWith(item.path.slice(0, -1))) ? 'background-color: #00453D;':'')">
                    <a class="sidebar-icon" :class="(item.icon)" style="width: 50px" @click="goToPage(item.path)" v-tooltip.right="item.name" />
                    <div v-if="sidebar" class="p-d-flex p-ai-center p-jc-between p-px-3" style="width: 100%"  @click="goToPage(index)">
                        <div> {{item.name}}</div>
                    </div>
                </div>
                <div v-if="sidebar && item.open">
                <div v-for="(subelement) in item.subElements" :key="subelement" class="subelement p-d-flex p-ai-center" @click="goToPage(subelement.path)">
                    <i :class="subelement.icon" class="p-mr-3" />
                    {{subelement.name}}
                </div>
                </div>
            </div>
        </div>
        <div  v-if="sidebar" class="p-py-5" >
            <div style="color: white;">Website <i class="pi pi-external-link" /></div>
        </div>

    </div>
</template>

<script>
    export default {
        props: {
            sidebar: {
                type: Boolean,
                default: false
            }
        },
        data () {
            return {
                fullwidth: true,
                navElements: [
                    {
                        name: 'Dashboard',
                        icon: 'pi pi-home',
                        path: 'home'
                    },
                    {
                        name: 'Networks',
                        icon: 'pi pi-cloud',
                        path: 'networks'
                    },
                    {
                        name: 'Organisations',
                        icon: 'pi pi-globe',
                        path: 'organisations'
                    },
                    {
                        name: 'Methods',
                        icon: 'pi pi-briefcase',
                        path: 'methods'
                    },
                    {
                        name: 'Users',
                        icon: 'pi pi-users',
                        path: 'users'
                    },
                    {
                        name: 'Log out',
                        icon: 'pi pi-sign-out',
                        path: 'logout'
                    }
                ]
            }
        },
        methods: {
            goToPage (path) {
                if (!isNaN(path)) {
                    if (this.navElements[path].subElements) {
                        this.navElements[path].open = !this.navElements[path].open
                        return
                    }
                    path = this.navElements[path].path
                }
                if (path) {
                    console.log(path)
                    this.$router.push({ name: path })
                }
            }
        }
    }
</script>

<style lang="scss" scoped>
    .sidebar {
        display: flex;
        justify-content: space-between;
        align-items: stretch;
        position: fixed;
        height: calc(100vh - 70px);
        flex-direction: column;
        padding-top: 50px;
        margin-top: 1px;
        background-color: rgba($color: #00695C, $alpha: 1);
        // background-image: //// #355e3b // #2f7532 // 486b3e
        //     linear-gradient(
        //     #00695C, #00695C
        //     );
        box-shadow: 0px 0px 0px 0px rgba(0, 0, 0, 0.3);

    .sidebar-element {
        width: 100%;
        margin: 0px 0px;
        padding: 0x 0px;
        text-decoration: none;
        font-size: 20px;
        cursor: pointer;
        color: #fefefe;
        border-top: 1px solid rgba($color: lightgrey, $alpha: 0.1);
        border-bottom: 1px solid rgba($color: lightgrey, $alpha: 0.1);
    }

    .subelement {
        background-color: rgba($color: lightgrey, $alpha: 0.05);
        color: #e2e2e2;
        font-size: 16px;
        padding: 10px 40px;
        cursor: pointer;
    }
    .subelement:hover {
        background-color: rgba($color: lightgrey, $alpha: 0.1);
    }
    a {
        border-right: 1px solid rgba($color: lightgrey, $alpha: 0.1);
        // border-bottom: 1px solid rgba($color: lightgrey, $alpha: 0.2);
        color: white;
        padding: 1em 1em;
        text-decoration: none;
        text-transform: uppercase;
         height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .sidebar-element:hover {
        background-color: rgba($color: lightgrey, $alpha: 0.2);
        font-size: 24px;
    }
    .sidebar-element:hover .sidebar-icon {
        font-size: 20px;
    }
    }
</style>
