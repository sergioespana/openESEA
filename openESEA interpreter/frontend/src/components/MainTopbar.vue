// Used by App.vue

<template>
    <div class="menubar p-shadow-2" id="menubar">
        <i class="bars pi pi-bars p-p-5" @click="expandedSidebar = !expandedSidebar" />
        <span class="p-input-icon-left">
                <i class="pi pi-search" /><InputText v-model="search" placeholder="Search the ESEA App..." />
            </span>
        <div class="p-d-flex p-ai-center">
            <div class="notification pi pi-bell"><span class="badge">42</span></div>
            <div class="profile p-d-flex p-ai-center p-pr-5" @click="goToProfile()">
            <i class="pi pi-user p-p-1 p-mx-4" style="border: 1px solid lightgrey; border-radius: 50%; font-size: 25px; color: lightgrey;"/>
            <h3 class="p-text-light" style="color: white;">{{ currentuser }}</h3>
            </div>
        </div>
    </div>
</template>

<script>
    import { mapState } from 'vuex'

    export default {
        data () {
            return {
                expandedSidebar: false,
                search: ''
            }
        },
        computed: {
            ...mapState('authentication', ['currentuser'])
        },
        watch: {
            expandedSidebar (val) {
                this.$emit('sidebar', val)
            }
        },
        methods: {
            goToProfile () {
                this.$router.push({ name: 'userprofile' })
            }
        }
    }
</script>

<style lang="scss" scoped>
    .menubar {
        display: flex;
        z-index: 100;
        position: absolute;
        width: 100%;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        height: 70px;
        margin: 0px;
        background-color: #00695C;
        // background-image:
        //     linear-gradient(
        //         to right,
        //     #486b3e, #355e3b
        //     );
        // border-bottom: 1px solid lightgrey;
    }
    .notification {
    color: white;
    text-decoration: none;
    padding-top: 10px;
    font-size: 20px;
    }
    .bars {
        font-size: 40px;
        color: lightgrey;
    }
    .bars:hover {
        color: rgba($color: white, $alpha: 1);
    }
    .profile:hover {
        background-color: rgba($color: lightgrey, $alpha: 0.1);
    }
    .notification .badge {
        position: relative;
        top: -15px;
        right: 5px;
        padding: 3px;
        border-radius: 50%;
        font-size: 15px;
        font-weight: bold;
        background-color: rgba($color: yellow, $alpha: 0.5);
        color: #323232;
    }
    .notification:hover {
        color: rgba($color: orange, $alpha: 1);
        font-weight: bold;
    }
</style>
