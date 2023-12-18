http://localhost:8080/

<template>
    <div class="p-m-5">
        <h1>Dashboard</h1>
    </div>
    <div class="p-grid nested-grid p-m-5 p-jc-center">
        <div class="p-col-12 p-py-5">
            <div v-if="tasks">
                <h4>All Done!</h4>
                <p>
                    None of your organisations or networks require your attention right now.
                </p>
            </div>
            <div v-else>
                <h4>The following tasks require your attention.</h4>
                <div class="p-shadow-2 p-m-3 p-p-3 p-text-left"><span class="p-text-bold">Task 1:</span> Fill in the survey of network 1.</div>
                <div class="p-shadow-2 p-m-3 p-p-3 p-text-left"><span class="p-text-bold">Task 2:</span> Reply to network participation request on network 2.</div>
            </div>
            <img alt="logo" src="../../assets/tasklist.png" class="p-m-5" style="height: 400px;">
        </div>
    </div>
</template>

<script>
    export default {
            data () {
                return {
                    tasks: []
                }
            }
        }
</script>
