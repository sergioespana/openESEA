// http://localhost:8081/methods/3/indicator-creation

<template>
    <div class="p-d-flex" style="height: calc(100vh - 145px);">
        <method-tree-sidebar style="height: 100%; flex: 0 0 400px;" />
        <div class="p-px-5" style="width: 100%; overflow-y: auto;">
            <div v-for="indicator in items" :key="indicator.key">
                <component :is="`${indicator.objType}-edit-form`" :errors="errors[indicator.objType] && errors[indicator.objType][indicator.id]" :check-saving-status="checkSavingStatus" @savingstatus="savingStatus(indicator, $event)"
                :direct-indicator="indicator" :indirect-indicator="indicator" :active="activeItem.objType === indicator.objType && activeItem.id === indicator.id"
                @input="saveActive(indicator.objType, $event)" @click="toggleActive(indicator)" @delete="deleteActive(indicator.objType, $event)" />
            </div>
        </div>
    </div>
    <div class="p-d-flex p-ai-center p-shadow-2" style="position: fixed; top: 45%; right: 0px; width: 100px; background-color: #fcfcfc; border: 1px solid grey;">
        <div>
            <div v-for="option in addBar" :key="option.choice" class="p-d-flex p-jc-center p-ai-center" style="height: 100px; width: 100px; border: 1px solid lightgrey" :style="(option.hover ? 'background-color: lightgrey;' : '')" @mouseover="option.hover=true" @mouseleave="option.hover=false" @click="addBarMethod(option.choice)">
                <div>
                    <i :class="option.icon? option.icon : 'pi pi-plus'" />
                    <p class="p-text-italic p-m-2">{{option.choice}}</p>
                </div>
            </div>
        </div>
    </div>
    <Dialog v-model:visible="unsavedChangesDialog" style="width: 600px;" header="Unsaved Changes" :modal="true" :dismissableMask="true">
        <div class="confirmation-content">
            This page contains unsaved changes, leaving the page now will destroy these. Do you still wish to leave the page?
        </div>
        <template #footer>
            <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="unsavedChangesChoice(true)" />
            <Button label="No" icon="pi pi-times" class="p-button-text" @click="unsavedChangesChoice(false)"/>
        </template>
    </Dialog>
</template>

<script>
    import { mapState, mapActions } from 'vuex'
    import MethodTreeSidebar from '@/components/MethodTreeSideBar'
    import IndirectIndicatorEditForm from '@/components/forms/IndirectIndicatorEditForm'
    import DirectIndicatorEditForm from '@/components/forms/DirectIndicatorEditForm'

    export default {
        components: {
            MethodTreeSidebar,
            IndirectIndicatorEditForm,
            DirectIndicatorEditForm
        },
        data () {
            return {
                checkSavingStatus: false,
                indicatorsSavingStatus: {},
                to: null,
                allowRouting: false,
                unsavedChangesDialog: false,
                discardUnsavedChanges: false,
                addBar: [
                    { choice: 'indicator' },
                    { choice: 'calculation' }
                ]
            }
        },
        computed: {
            ...mapState('method', ['method', 'error']),
            ...mapState('directIndicator', { activeDirectIndicator: 'directIndicator', directIndicators: 'directIndicators', directIndicatorErrors: 'errors' }),
            ...mapState('indirectIndicator', { activeIndirectIndicator: 'indirectIndicator', indirectIndicators: 'indirectIndicators', indirectIndicatorErrors: 'errors' }),
            items () {
                this.directIndicators.forEach(direct => { direct.objType = 'direct-indicator' })
                this.indirectIndicators.forEach(indirect => { indirect.objType = 'indirect-indicator' })
                return this.directIndicators.concat(this.indirectIndicators)
            },
            // activeItem.objType decides which EditForm will be shown
            activeItem () {
                let objType = null
                let id = null
                if (this.activeDirectIndicator.id) {
                    objType = 'direct-indicator'
                    id = this.activeDirectIndicator.id
                }
                if (this.activeIndirectIndicator.id) {
                    objType = 'indirect-indicator'
                    id = this.activeIndirectIndicator.id
                }
                return { objType, id }
            },
            errors () {
                return {
                    'direct-indicator': this.directIndicatorErrors,
                    'indirect-indicator': this.indirectIndicatorErrors
                }
            }
        },
        watch: {
            indicatorsSavingStatus: {
                handler (val) {
                    console.log(this.indicatorsSavingStatus)
                    if ((Object.keys(val).length === this.items.length) & (!Object.keys(this.directIndicatorErrors).length) & (!Object.keys(this.indirectIndicatorErrors).length)) {
                        for (const key in val) {
                            if (val[key]) {
                                this.indicatorsSavingStatus = {}
                                this.unsavedChangesDialog = true
                                return
                            }
                        }
                        this.allowRouting = true
                        this.$router.push(this.to)
                    }
                },
                deep: true
            }
        },
        beforeRouteLeave (to, from, next) {
            if (!this.items.length) { this.allowRouting = true }
            if (this.allowRouting || this.discardUnsavedChanges) { //  & !this.discardUnsavedChanges
                next(true)
            } else {
                this.to = to
                this.allowRouting = false
                this.checkSavingStatus = !this.checkSavingStatus
                next(false)
            }
        },
        created () {
            this.initialize()
        },
        methods: {
            ...mapActions('method', ['fetchMethod']),
            ...mapActions('directIndicator', ['fetchDirectIndicators', 'setDirectIndicator', 'addNewDirectIndicator', 'updateDirectIndicator', 'deleteDirectIndicator']),
            ...mapActions('indirectIndicator', ['fetchIndirectIndicators', 'setIndirectIndicator', 'addNewIndirectIndicator', 'updateIndirectIndicator', 'deleteIndirectIndicator']),
            async initialize () {
                const methodId = parseInt(this.$route.params.id, 10)
                // Checks whether the url method's id corresponds to the id of the method in the local storage
                if (this.method.id !== methodId) {
                    await this.fetchMethod({ id: methodId })
                    if (this.error) {
                        this.$router.push({ name: 'methods' })
                    }
                }
                await this.fetchDirectIndicators({ mId: this.method.id })
                await this.fetchIndirectIndicators({ mId: this.method.id })
            },
            // Add either a direct or indirect indicator
            addBarMethod (choice) {
                if (choice === 'indicator') { this.addDirectIndicator() }
                if (choice === 'calculation') { this.addIndirectIndicator() }
            },
            addDirectIndicator () {
                this.addNewDirectIndicator({ mId: this.method.id })
                this.setIndirectIndicator()
            },
            addIndirectIndicator () {
                this.addNewIndirectIndicator({ mId: this.method.id })
                this.setDirectIndicator()
            },
            // Activates (=Expands) indicator once it's clicked
            toggleActive (item) {
                const { objType } = item
                if (objType === 'direct-indicator' && item.id !== this.activeDirectIndicator.id) {
                    this.setDirectIndicator(item)
                    this.setIndirectIndicator()
                } else if (objType === 'indirect-indicator' && item.id !== this.activeIndirectIndicator.id) {
                    this.setIndirectIndicator(item)
                    this.setDirectIndicator()
                }
            },
            saveActive (type, object) {
                if (object.target) { return } // Checks whether the $event contains an object or only an inputEvent
                if (type === 'direct-indicator') { this.updateDirectIndicator({ mId: this.method.id, directIndicator: object }) }
                if (type === 'indirect-indicator') { this.updateIndirectIndicator({ mId: this.method.id, indirectIndicator: object }) }
            },
            deleteActive (objType, object) {
                if (objType === 'direct-indicator') { this.deleteDirectIndicator({ mId: this.method.id, SuId: 0, SeId: 0, id: object.id }) }
                if (objType === 'indirect-indicator') { this.deleteIndirectIndicator({ mId: this.method.id, SuID: 0, SeId: 0, id: object.id }) }
            },
            savingStatus (indicator, status) {
                const key = indicator.objType + indicator.id
                this.indicatorsSavingStatus[key] = status
            },
            unsavedChangesChoice (choice) {
                this.unsavedChangesDialog = false
                this.discardUnsavedChanges = choice
                if (choice) {
                    this.$router.push(this.to)
                }
            }
        }
    }
</script>
