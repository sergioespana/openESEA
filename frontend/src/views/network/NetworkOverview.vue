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
        }
    }
</script>
