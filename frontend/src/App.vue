<template>
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
    <!-- <div v-if="accessToken === null" style="position: absolute; height: 100%; width: 100%;background-color: #00695C;"> calc(100vh - 70px)
            <div class="centered">
                <h3 style="color: white; font-size: 60px;">Open ESEA</h3> style="position: fixed; height: 100%; z-index: 1;"
                <router-view name="loginview" />
            </div>
            <div class="p-d-flex p-text-center" style="position: absolute; bottom: 0px; left: 0; right: 0; margin-left: auto; margin-right: auto; width: 580px; color: lightgrey;">
                <div>
                    <router-link to="/login" class="link">Terms of Service</router-link>
                    <span> | </span>
                    <router-link to="/login" class="link">Privacy Policy</router-link>
                    <span> | </span>
                    <span style="color: lightgrey; font-size: 14px;">Copyright 2021 ESEA Team. All rights reserved.</span>
                </div>
            </div>
    </div> -->
</template>
<script>
import { mapState } from 'vuex'
// import MyBreadCrumb from './components/MyBreadCrumb' v-if="accesToken === null"
import MainSidebar from './components/MainSidebar'
import MainTopbar from './components/MainTopbar.vue'
// import SubSidebar from './components/SubSidebar'

export default {
  components: {
   //  MyBreadCrumb,
    MainSidebar,
    MainTopbar
    // SubSidebar
  },
  data () {
    return {
        expandedSidebar: false
    }
  },
  methods: {
   toggle (event) {
            this.$refs.menu.toggle(event)
        },
    changeSidebar (value) {
        this.expandedSidebar = value
    }
  },
  computed: {
    ...mapState('authentication', ['accessToken', 'currentuser'])
  }
}
</script>

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

    // isIdle () {
    //   return this.$store.state.idleVue.isIdle
    // },
    // onIdle () {
    //   console.log('user idled')
    //   return this.$store.state.idleVue
    // }
    <!-- <Menubar :model="items" v-if="accessToken!=null" class="p-shadow-5" style="background-color: #EFEEEE; z-index: 1000;">
        <template #start>
            <i class="pi pi-bars" />
            <img alt="logo" src="./assets/logo.png" height="40" class="p-mr-5">
        </template>
        <template #end>
          <Button type="button" :label="'account ('+ currentuser + ')'" @click="toggle" aria-haspopup="true" aria-controls="profile_menu" class="p-button-raised p-button-text p-button-plain"/>
          <Menu id="profile_menu" ref="menu" :model="profile" :popup="true" />
        </template>
    </Menubar>
   <my-bread-crumb />
    <h1>Breadcrumb with Chosen Network>Chosen Organisation>Chosen Method</h1> -->
