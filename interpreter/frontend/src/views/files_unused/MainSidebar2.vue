<template>
    <div :style="(sidebar ? 'width: 350px':'width: 50px')" style="min-height: 100%" class="sidebar">
        <div>
            <div v-for="(item, index) in navElements" :key="item" > <!-- a href="#" -->
                <div class="sidebar-element p-d-flex p-ai-center" :style="((item.path === $route.name) ? 'background-color: #b2b2b2;':'')">
                    <a :class="(item.icon)" style="width: 50px" @click="goToPage(item.path)" />
                    <div v-if="sidebar" class="p-d-flex p-ai-center p-jc-between p-px-3" style="width: 100%"  @click="goToPage(index)">
                        <div> {{item.name}}</div>
                        <i v-if="item.subElements" :class="(item.open ? 'pi pi-chevron-down':'pi pi-chevron-left')" />
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
                    path: 'networks',
                    subElements:
                        [
                            { name: 'Networks List', icon: 'pi pi-list', path: 'networks' },
                            { name: 'Add Network', icon: 'pi pi-plus', path: 'network-create' }
                        ]
                },
                {
                    name: 'Organisations',
                    icon: 'pi pi-globe',
                    path: 'organisations',
                    subElements:
                        [
                            { name: 'Organisations List', icon: 'pi pi-list', path: 'organisations' },
                            { name: 'Add Organisation', icon: 'pi pi-plus', path: 'organisation-create' }
                        ]
                },
                {
                    name: 'Methods',
                    icon: 'pi pi-briefcase',
                    path: 'methods',
                    subElements:
                        [
                            { name: 'Methods List', icon: 'pi pi-list', path: 'methods' },
                            { name: 'Add Method', icon: 'pi pi-plus', path: 'methodcreation' }
                        ]
                },
                {
                    name: 'Users',
                    icon: 'pi pi-users',
                    path: 'users'
                },
                {
                    name: 'Account',
                    icon: 'pi pi-user',
                    path: 'userdetails',
                    subElements:
                        [
                            { name: 'Profile', path: 'userdetails' },
                            { name: 'Messages', path: '' },
                            { name: 'Settings', path: '' }
                        ]
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
        position: relative;
        flex-direction: column;
        padding-top: 50px;
        margin-top: 1px;
        background-color: rgba($color: #00695C, $alpha: 1);
        // background-image: //// #355e3b // #2f7532 // 486b3e
        //     linear-gradient(
        //     #00695C, #00695C
        //     );
        box-shadow: 3px 0px 0px 0px rgba(0, 0, 0, 0.3);
        min-height: 100%;

    .sidebar-element {
        width: 100%;
        margin: 0px 0px;
        padding: 0x 0px;
        text-decoration: none;
        font-size: 22px;
        cursor: pointer;
        color: #fefefe;
        border-top: 1px solid rgba($color: lightgrey, $alpha: 0.2);
        border-bottom: 1px solid rgba($color: lightgrey, $alpha: 0.2);
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
        border-right: 1px solid rgba($color: lightgrey, $alpha: 0.2);
        // border-bottom: 1px solid rgba($color: lightgrey, $alpha: 0.2);
        color: white;
        padding: 1em 1em;
        text-decoration: none;
        text-transform: uppercase;
    }
    .sidebar-element:hover {
        background-color: rgba($color: lightgrey, $alpha: 0.2);
    }
    a:hover {
        background-color: rgba($color: lightgrey, $alpha: 0.1);
    }
    }
</style>
