// template is html of the page
<template>
  <div>
      <div class="myapp" v-if="accessToken !== null" style="position: relative; height: 100%; min-width: 1400px; overflow: auto;"> <!--F5F7F6 -style="min-height: 800px; height: auto; min-width: 1100px; background-color: #F8F9FA;" position: fixed; width: 100%;-->
          <main-topbar @sidebar="changeSidebar" style="position: fixed;" />
          <div class="p-d-flex" style="height: 100%; width: 100%; padding-top: 70px;">
              <main-sidebar :sidebar="expandedSidebar" />
              <!-- <div style="height: 100%; position: relative; background-color: blue;" :style="(expandedSidebar) ? 'width: 350px;': 'width: 55px;'"></div> -->
              <!-- <sub-sidebar /> -->
              <div :style="(expandedSidebar) ? 'margin-left: 350px': 'margin-left: 55px;'" style="width: 100%;">
                  <router-view />
                  <router-view name="surveyview" style="width: 100%;"/>
              </div>
          </div>
      </div>
      <router-view v-if="accessToken === null" name="surveyview"/>
      <router-view name="anonymousview"/>
    </div>
</template>

// script is javascript code that is executed on the page
<script>
  // Import of Store states(mapState)/functions(mapState) and Custom components
  import { mapState } from 'vuex'
  import MainSidebar from './components/MainSidebar'
  import MainTopbar from './components/MainTopbar.vue'

  export default {
    components: {
      MainSidebar,
      MainTopbar
    },
    // local data
    data () {
      return {
          expandedSidebar: false
      }
    },
    computed: {
      ...mapState('authentication', ['accessToken', 'currentuser'])
    },
    // functions
    methods: {
      /*
      toggle (event) {
        this.$refs.menu.toggle(event)
      },
      */
      changeSidebar (value) {
          this.expandedSidebar = value
      }
    }
  }
</script>

// style is the css of the page
<style lang="scss">
  html, body, #app {
      overflow: auto;
      // background-color:; //white; // #F7F7F7; // #F8F9FA;
      margin: 0 0;
      padding: 0 0;
      height: 100%;
    }

  #app {
    font-family: 'Raleway'; // Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    background-color: #F7F7F7;
  }

  #nav {
    a {
      font-weight: bold;
      color: #2c3e50;

      &.router-link-exact-active {
        color: #42b983;
      }
    }
  }
  .link {
      text-decoration: None;
      color: lightgrey;
      font-size: 14px;
  }
  .link:hover {
      text-decoration: underline;
  }

  .centered {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 400px;
  }

  @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@300&display=swap');
</style>

--> Might be required to log out idle users!

// isIdle () {
//   return this.$store.state.idleVue.isIdle
// },
// onIdle () {
//   console.log('user idled')
//   return this.$store.state.idleVue
// }
