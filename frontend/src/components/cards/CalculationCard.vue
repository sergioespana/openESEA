<template>
    <div class="p-m-3 p-px-5 p-py-3 p-shadow-1 p-text-left" :style="[(valid) ? 'border: 1px solid lightgrey;': 'border: 2px solid rgba(255, 0, 0, 0.3);', (hover) ? 'background-color: white;':'background-color: #F2F2F2;']" style="border-radius: 5px;"> <!-- #dcdcdc"> -->
        <h3 class="p-col p-text-center p-m-0">Indirect Indicator - [{{keyy || 'No Key'}}]</h3>
        <div class=" p-mx-5">
             <div class="attribute-name">Name: <span class="value">{{ name || 'None' }}</span></div>
            <div class="attribute-name">Formula: <span class="value">{{ formula || 'None' }}</span></div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        keyy: {
            type: String,
            required: undefined
        },
        formula: {
            type: String,
            default: undefined
        },
        name: {
            type: String,
            default: undefined
        },
        valid: {
            type: Boolean,
            default: undefined
        },
        hover: {
            type: Boolean,
            default: false
        }
    }
}
</script>

<style lang="scss" scoped>
.attribute-name {
    font-size: 20px;
    font-weight: bold;
}
.value {
    font-weight: normal;
}
</style>
