<template>
  <div class="app">
    <AppHeader/>
    <div class="app-body">
      <Sidebar/>
      <main class="main">
        <!--<breadcrumb :list="list"/>-->
        <div class="container-fluid">
          <router-view></router-view>
        </div>
      </main>
    </div>
    <AppFooter/>
  </div>
</template>

<script>
import AppHeader from '../components/Header'
import Sidebar from '../components/Sidebar'
import AppFooter from '../components/Footer'
import Breadcrumb from '../components/Breadcrumb'

export default {
  name: 'full',
  components: {
    AppHeader,
    Sidebar,
    AppFooter,
    Breadcrumb,
  },
  created: function () {
    this.$root.bus.checkLogin()
  },
  computed: {
    name () {
      return this.$route.name
    },

    list () {
      return this.$route.matched
    },
  },
}
</script>

<style lang="css">
  .main-route {
    margin-top: 50px;
  }

</style>
