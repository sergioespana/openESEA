<template>
<div class="p-grid nested-grid">
    <div class="p-col-12 p-m-0 p-p-0">
        <div class="p-p-3 p-shadow-2" style="border: 1px solid lightgray; background-color: white;">
            <div class="p-text-justify"><p class="p-text-bold">Network Manager</p>
                <router-link :to="{name: 'userdetails', params: { id: network.owner_id } }" style="text-decoration: none; color: blue;">{{network.owner}}</router-link>
            </div>
            <div class="p-text-justify"><p class="p-text-bold">Description</p>
                    {{network.description}}
                    <!-- Lorem ipsum dolor sit amet, consectetur adipiscing elit. In convallis mi sit amet faucibus malesuada. Vestibulum fringilla sed dui bibendum laoreet. Donec suscipit sit amet leo et mattis. Aenean mattis tempus turpis a vulputate. Nunc bibendum pulvinar neque, nec mattis nisl tincidunt ut. Nam a quam id justo dictum pulvinar. Sed luctus dictum ligula, id sagittis tellus aliquam id. Vestibulum auctor vestibulum turpis. -->
            </div>
        </div>
        <!-- <div class="p-col-12 p-p-5 p-my-5" style="border: 1px solid lightgray; background-color: white; border-radius: 5px;">
            <div v-if="Tasks">
                <h4>No tasks!</h4>
                <p class="p-text-italic">
                    {{network.name}} does not require your attention right now.
                </p>
            </div>
            <div v-else>
                <h4 class="p-mb-0">The following tasks require your attention.</h4>
                <div v-for="survey, index in surveys" :key="survey.id" class="p-p-5">
                    <Button :label="`Survey ${index+1}: As ${survey.stakeholders} of ${network.name} you are asked to fill in the following survey deployed by network 1: '${survey.name}'.`" class="p-button-text p-shadow-3 p-p-4" @click="goToSurvey(survey.method.id, survey.id)"/>
                    <br><br>
                    <Button label="Task 2: As manager of organisation 2 you are asked to fill in the survey of network 1." class="p-button-text p-shadow-1" />
                </div>
                <br>
                <Button label="Task 1: Organisation is requesting network membership." class="p-button-secondary p-shadow-1" />
                <br><br>
                <Button label="Task 2: Survey responserate threshold has been achieved for method BIA." class="p-button-secondary p-shadow-1" />
            </div>
        </div> -->
        <div class="p-m-5">
            <horizontal-scroll-bar :items="methods" name="Methods" :permission="permission" @clicked-item="goToItem">
                <slot>
                    There are no Methods, <router-link :to="{name: 'networkmethods', params: { NetworkId: $route.params.NetworkId } }" style="text-decoration: none; color: blue;">create or import Methods!</router-link>
                </slot>
            </horizontal-scroll-bar>
            <horizontal-scroll-bar :items="organisations" name="Organisations" :permission="permission"  @clicked-item="goToItem">
                <slot>
                    There are no connected organisations, <router-link :to="{name: 'networkorganisations', params: { NetworkId: $route.params.NetworkId } }" style="text-decoration: none; color: blue;">invite organisations!</router-link>
                </slot>
            </horizontal-scroll-bar>
            <horizontal-scroll-bar :items="campaigns" name="Campaigns" :permission="permission"  @clicked-item="goToItem">
                <slot>
                    <slot>There are no campaigns, <router-link :to="{name: 'networkcampaigns', params: { NetworkId: $route.params.NetworkId } }" style="text-decoration: none; color: blue;">create a new campaign!</router-link></slot>
                </slot>
            </horizontal-scroll-bar>
        </div>
    </div>

</div>
</template>
<script>
import { mapActions, mapState } from 'vuex'
import HorizontalScrollBar from '../../components/HorizontalScrollBar'

export default {
    components: {
        HorizontalScrollBar
    },
    data () {
        return {

        }
    },
    computed: {
        ...mapState('network', ['network']),
        ...mapState('organisation', ['organisations']),
        ...mapState('method', ['methods']),
        ...mapState('campaign', ['campaigns']),
        ...mapState('survey', ['surveys']),
        methodPages () {
            const page = Math.ceil(this.methods.length / this.numberOfItems)
            return page
        },
        organisationPages () {
            const page = Math.ceil(this.organisations.length / this.numberOfItems)
            return page
        },
        permission () {
            if (this.network.accesLevel) {
                const accesLevel = this.network.accesLevel
                if (accesLevel === 'admin' || accesLevel === 'network admin') {
                    return true
                }
            }
            return false
        }

    },
    // watch: {
    //     numberOfItems: function () {
    //         console.log('changed')
    //         this.changeList()
    //     }
    // },
    created () {
        window.addEventListener('resize', this.checkWindowSize)
        this.initialize()
    },
    methods: {
        ...mapActions('organisation', ['fetchOrganisations', 'setOrganisation']),
        ...mapActions('method', ['fetchMethods', 'setMethod']),
        ...mapActions('campaign', ['fetchCampaigns', 'setCampaign']),
        ...mapActions('survey', ['fetchSurveys']),
        async initialize () {
            // this.checkWindowSize()
            await this.fetchMethods({ query: `?network=${this.$route.params.NetworkId}` })
            await this.fetchOrganisations({ query: `?network=${this.$route.params.NetworkId}` })
            await this.fetchCampaigns({ nId: this.$route.params.NetworkId })

            for (const method of this.methods) {
                await this.fetchSurveys({ mId: method.id, query: `?organisation=${this.$route.params.OrganisationId}` })
            }
        },
        async goToItem (item, name) {
            if (!item.id) { return }
            if (name === 'organisations') {
                await this.setOrganisation({ id: item.id })
                this.$router.push({ name: 'organisationoverview', params: { OrganisationId: item.id } })
            }
            if (name === 'methods') {
                await this.setMethod({ id: item.id })
                this.$router.push({ name: 'newmethoddetails', params: { id: item.id } })
            }
            if (name === 'campaigns') {
                await this.setCampaign({ id: item.id })
                this.$router.push({ name: 'networkcampaign', params: { NetworkId: this.$route.params.NetworkId, CampaignId: item.id } })
            }
            console.log(name, item)
        }
        // checkWindowSize () {
        //     if (window.innerWidth <= 1200) {
        //         this.numberOfItems = 4
        //     }
        //     if (window.innerWidth > 1200) {
        //         this.numberOfItems = 6
        //     }
        // },
        // methodsScroll (direction) {
        //     if (direction === 'left' && this.methodPage > 1) {
        //         this.methodPage--
        //         this.methodbar = this.methods.slice((this.methodPage - 1) * 4, (this.methodPage) * 4)
        //         }

        //     if (direction === 'right' && this.methodPage < this.methodPages) {
        //         this.methodPage++
        //         this.methodbar = this.methods.slice((this.methodPage - 1) * 4, (this.methodPage) * 4)
        //         }
        //     console.log(direction)
        //     // Show other Methods
        // },
        // organisationsScroll (direction) {
        //     // if (direction === 'left' && this.organisationPage > 1) {
        //     //     this.organisationPage--
        //     //     this.organisationbar = this.organisations.slice((this.organisationPage - 1) * 4, (this.organisationPage) * 4)
        //     //     }
        //     // if (direction === 'right' && this.organisationPage < this.organisationPages) {
        //     //     this.organisationPage++
        //     //     this.organisationbar = this.organisations.slice((this.organisationPage - 1) * 4, (this.organisationPage) * 4)
        //     //     }
        //     if (direction === 'left') {
        //         if (this.organisationPage < 2) {
        //         return
        //         }
        //         this.organisationPage--
        //     }
        //     if (direction === 'right') {
        //         if (this.organisationPage >= this.organisationPages) {
        //         return
        //         }
        //         this.organisationPage++
        //     }
        //     this.organisationbar = this.organisations.slice((this.organisationPage - 1) * this.numberOfItems, (this.organisationPage) * this.numberOfItems)

        //     if (this.organisationbar.length < this.numberOfItems) {
        //         console.log(this.organisationbar.length)
        //         const j = this.numberOfItems - this.organisationbar.length
        //         for (let i = 0; i < j; i++) {
        //             console.log('c')
        //             this.organisationbar.push({ hover: false, color: true })
        //         }
        //         console.log('length:', this.organisationbar.length)
        //     }
        // },
        // changeList () {
        //     this.methodbar = this.methods.slice(0, this.numberOfItems)
        //     const methodPlaceholderItems = this.numberOfItems - this.methodbar.length
        //     if (this.methodbar.length < this.numberOfItems) {
        //         for (let i = 0; i < methodPlaceholderItems; i++) {
        //             this.methodbar.push({ hover: false, color: true })
        //             console.log(this.methodbar.length)
        //         }
        //     }

        //     this.organisationbar = this.organisations.slice(0, this.numberOfItems)
        //     const organisationPlaceholderItems = this.numberOfItems - this.organisationbar.length
        //     if (organisationPlaceholderItems > 0) {
        //         for (let i = 0; i < organisationPlaceholderItems; i++) {
        //             this.organisationbar.push({ hover: false, color: true })
        //             console.log(this.organisationbar.length)
        //         }
        //     }
        // }
    }
}
        // methodbar () {
        //     this.changeList()
        //     // const methodbar = this.methods.slice(0, this.numberOfItems)
        //     // console.log(this.numberOfItems)
        //     // if (this.methodbar.length < this.numberOfItems) {
        //     //     for (let i = 0; i <= (this.numberOfItems - this.methodbar.length); i++) {
        //     //         this.methodbar.push({ hover: false, color: true })
        //     //     }
        //     // }
        //     // return methodbar
        //     return []
        // }
        // methodbar () {
        //     const m = [...this.methods]
        //     if (m.length < 5) {
        //         for (let i = 0; i <= (5 - m.length); i++) {
        //             m.push({ hover: false, color: 'lightgrey' })
        //         }
        //     }
        //     return m
        // }
        // bar () {
        //     const m = this.localmethods
        //     if (this.localmethods.length < 5) {
        //         for (let i = 0; i <= (5 - m.length); i++) {
        //             m.push({ hover: false })
        //         }
        //     }
        //     return m
        // }
    // <!-- <div class="p-col-1">
    //     <Divider layout="vertical" />
    // </div>
    // <div class="p-col-2">
    //     <div class="p-grid">
    //         Content here
    //          <div class="p-col-12">
    //             <h3 class="p-mb-2 p-text-left">Available Surveys</h3>
    //             <Divider class="p-m-0" />
    //             <div class="p-m-3">
    //                 <div v-if="surveys.length">
    //                     <div v-for="survey, num in surveys" :key="survey.name">
    //                         {{num+1}}. <router-link :to="{name: 'survey-fill', params: { id: survey.method.id, surveyId: survey.id }}" style="text-decoration: none; color: blue;">survey {{num+1}}</router-link>
    //                         <Divider class="p-m-1" />
    //                     </div>
    //                 </div>
    //                 <div v-else>
    //                     <div class="p-py-5 p-text-italic">No surveys</div>
    //                 </div>
    //             </div>
    //             <router-link :to="{name: 'organisationsurveys', params: { OrganisationId: this.$route.params.OrganisationId }}" style="text-decoration: none; color: blue;">Show all Organisation Surveys</router-link>
    //         </div>
    //         <div class="p-col-12">
    //             <h3 class="p-mb-2 p-text-left">Reports</h3>
    //             <Divider class="p-m-0" />
    //             <div class="p-m-3">
    //                 <div v-if="organisations">
    //                     <div v-for="organisation, num in organisations" :key="organisation.name">
    //                         {{num+1}}. <router-link :to="{name: 'organisationreports', params: { OrganisationId: this.$route.params.OrganisationId }}" style="text-decoration: none; color: blue;">report {{num+1}}</router-link>
    //                         <Divider class="p-m-1" />
    //                     </div>
    //                 </div>
    //                 <div v-else>
    //                     <div class="p-py-5 p-text-italic">No reports yet</div>
    //                 </div>
    //             </div>
    //             <router-link :to="{name: 'organisationreports', params: { OrganisationId: this.$route.params.OrganisationId } }" style="text-decoration: none; color: blue;">Show all Organisation Reports</router-link>
    //         </div>
    //     </div>
    // </div> -->
        //     <!-- <div class="p-d-flex p-jc-between">
        //     <h3 class="p-text-left"><router-link :to="{name: 'networkmethods', params: { NetworkId: network.id } }" style="text-decoration: none; color: blue;">Methods</router-link></h3> {{numberOfItems}}
        //     <h3>Page {{methodPage}} of {{methodPages}}</h3>
        // </div>
        // <div class="p-d-flex" style="height: 150px;">
        //     <div class="scrollIcon p-d-flex"  style="height: 150px;" @click="methodsScroll('left')"> <i class="pi pi-angle-left p-as-center" style="font-size: 3rem;" /> </div>
        //     <div v-for="method, index in methodbar.slice(0,1)" :key="method" @mouseover="method.hover=true" @mouseleave="method.hover=false">
        //         <div class="p-d-flex" :class="((method.hover && !method.color) ? 'p-shadow-2 p-m-1 p-text-bold' : 'p-shadow-1 p-mx-1')" style="background-color: white; width: 200px; height: 150px;" :style="(method.hover ? 'background-color: #EFEEEE' : '', method.color ? 'background-color: #F3F3F3' : '' )" >
        //             <p v-if="method.name" class="p-as-center" style="width: 100%">{{index + 1}}. Method</p>
        //         </div>
        //     </div>
        //    <div class="scrollIcon p-d-flex" style="height: 150px;" @click="methodsScroll('right')"> <i class="pi pi-angle-right p-as-center" style="font-size: 3rem;" /> </div>
        // </div>
        // <Divider />
        // <div class="p-d-flex p-jc-between">
        //     <h3 class="p-text-left"><router-link :to="{name: 'networkorganisations', params: { NetworkId: network.id } }" style="text-decoration: none; color: blue;">Organisations</router-link></h3>
        //     <h3>Page {{organisationPage}} of {{organisationPages}}</h3>
        // </div>
        // <div class="p-d-flex" style="height: 150px;">
        //     <div class="scrollIcon p-d-flex"  style="height: 150px;" @click="organisationsScroll('left')"> <i class="pi pi-angle-left p-as-center" style="font-size: 3rem;" /> </div>
        //     <div v-for="organisation, index in organisationbar.slice(0,1)" :key="organisation" @mouseover="organisation.hover=true" @mouseleave="organisation.hover=false">
        //         <div class="p-d-flex" :class="((organisation.hover && !organisation.color) ? 'p-shadow-2 p-m-1 p-text-bold' : 'p-shadow-1 p-mx-1')" style="background-color: white; width: 200px; height: 150px;" :style="(organisation.hover ? 'background-color: #EFEEEE' : '', organisation.color ? 'opacity: 0.35;' : '' )" >  background-color: #F3F3F3;
        //             <p v-if="organisation.name" class="p-as-center" style="width: 100%">{{index + 1}}. {{organisation.name}}</p>
        //         </div>
        //     </div>
        //    <div class="scrollIcon p-d-flex" style="height: 150px;" @click="organisationsScroll('right')"> <i class="pi pi-angle-right p-as-center" style="font-size: 3rem;" /> </div>
        // </div>
        // <Divider /> -->
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
