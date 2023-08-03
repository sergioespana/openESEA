<template>
    <div @click="goIntoEdit">
        <component
            class="component"
            :is="getComponentType"
            :hidden="this.editing">
            {{ value }}
        </component>
        <input :hidden="!this.editing"
            class="input"
            ref="input"
            :value="value"
            @keyup.enter="updateValue"
            @focusout="exitEditing"
            type="text"/>
    </div>
</template>

<script>
// https://stackoverflow.com/questions/45050119/click-to-edit-text-field-with-vue
export default {
    name: 'EditableText',
    props: {
        componentType: {
            datatype: String,
            default: () => { return 'span' }
        },
        initialValue: {
            datatype: String,
            default: () => { return '' }
        }
    },
    data () {
        return {
            editing: false,
            value: this.initialValue
        }
    },
    computed: {
        getComponentType () {
            return this.componentType
        }
    },
    methods: {
        exitEditing () {
            this.editing = false
        },
        updateValue ($event) {
            const valueLocal = $event.target.value
            this.value = valueLocal
            this.editing = false
            this.$emit('enteredValue', valueLocal)
        },
        goIntoEdit () {
            this.editing = true
            const inputNode = this.$refs.input
            inputNode.focus()
        }
    }
}
</script>

<style>
.input {
    /* font: inherit; */
    font-family: inherit;
    width: calc(min(100%, max(50%, 200px)));
    height: 100%;
}

.component {
    width: 100%;
    height: 100%;
}
</style>
