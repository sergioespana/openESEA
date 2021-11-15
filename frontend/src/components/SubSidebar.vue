// used by UserDetails.vue, Network.vue

<template>
    <div class="sidebar p-shadow-5" :style="(true ? 'width: 55px;': 'width: 55px;')" style="height: 100%; background-color: #F5F7F6;">
        <div>
            <h3 v-if="false" class="p-text-bold">Patagonia</h3>
            <Divider />
            <div v-for="item in links" :key="item" @click="goToPage(item.path)"> <!-- a href="#" -->
                <div class="sidebar-element p-d-flex p-ai-center" :style="((item.path === $route.name) ? 'background-color: #E1E7E4;':'')">
                    <a :class="(item.icon)" style="width: 50px" v-tooltip.right="item.name" />
                    <div v-if="false" class="p-d-flex p-ai-center p-jc-between p-px-3" style="width: 100%">
                        <div> {{item.name}}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        links: {
            type: Array,
            default: function () {
                return []
            }
        },
        paramsdata: {
        }
    },
    data () {
        return {
        }
    },
    methods: {
        goToPage (path) {
            if (path) {
                if (path.startsWith('network')) {
                    this.$router.push({ name: path, params: { NetworkId: this.$route.params.NetworkId } })
                } else if (path.startsWith('organisation')) {
                    this.$router.push({ name: path, params: { OrganisationId: this.$route.params.OrganisationId } })
                }
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
        padding-top: 20px;
        margin-top: 1px;
        background-color: rgba($color: #00695C, $alpha: 1);
        // background-image: //// #355e3b // #2f7532 // 486b3e
        //     linear-gradient(
        //     #00695C, #00695C
        //     );
        // box-shadow: 1px 0px 0px 0px rgba(0, 0, 0, 0.3);
        min-height: 100%;

    .sidebar-element {
        width: 100%;
        margin: 0px 0px;
        padding: 0x 0px;
        text-decoration: none;
        font-size: 22px;
        cursor: pointer;
        color: #1C312F;
        border-top: 1px solid rgba($color: lightgrey, $alpha: 0.1);
        border-bottom: 1px solid rgba($color: lightgrey, $alpha: 0.1);
    }

    .subelement {
        background-color: rgba($color: lightgrey, $alpha: 0.05);
        color: #1C312F;
        font-size: 16px;
        padding: 10px 40px;
        text-decoration: none;
        text-transform: uppercase;
        cursor: pointer;
    }
    .subelement:hover {
        background-color: rgba($color: lightgrey, $alpha: 0.1);
    }
    a {
    //     border-right: 1px solid rgba($color: lightgrey, $alpha: 0.1);
    //     // border-bottom: 1px solid rgba($color: lightgrey, $alpha: 0.2);
            // font-size: 18px;
    //     color: black;;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
            // padding: 1em 1em;

    }
    .sidebar-element:hover {
        background-color: rgba($color: #E1E7E4, $alpha: 1);
    }
    a:hover {
        font-size: 20px;
    //     background-color: rgba($color: lightgrey, $alpha: 0.1);
    }
    }
</style>
