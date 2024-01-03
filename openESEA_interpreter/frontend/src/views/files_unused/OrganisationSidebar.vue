<template>
    <Button icon="pi pi-angle-right" class="p-button-text" @click="visibleleft=true" style="background-color: #486b3e; min-height: 100%; border-radius: 0%;"/>
    <Sidebar v-model:visible="visibleleft" style="width:250px;">
        <div class="p-py-5">
            <h3>{{name}}</h3>
            <Divider />
            <div class="p-d-flex p-flex-column p-px-5 p-text-left">
                <div v-for="link in links" :key="link.label">
                    <Button :label="link.label" :icon="`pi pi-${link.icon}`" class="p-button-secondary p-button-text" @click="goToPage(link.label)" />
                </div>
            </div>
        </div>
    </Sidebar>
</template>

<script>
// import { mapState } from 'vuex'
export default {
    props: {
        links: {
            type: Array,
            default: function () {
                return []
            }
        },
        name: {
            type: String,
            default: 'Name'
        }
    },
    data () {
        return {
            visibleleft: false
        }
    },
    methods: {
        goToPage (name) {
            this.$emit('reroute', name)
        }
    }

}
</script>
