<template>
  <div class="main-route">
    <b-tabs ref="tabs" card v-model="activeTabIndex">
      <b-tab title="Inbox">
        <inbox></inbox>
      </b-tab>
      <b-tab title="Settings">
        <settings></settings>
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
  import inbox from './_tabs/_inbox'
  import settings from './_tabs/_settings'
  import rememberTabMixin from '../../components/mixins/rememberTabMixin'

  export default {
    components: {
      inbox,
      settings,
    },
    data () {
      return {}
    },
    mixins: [rememberTabMixin],
  }
</script>
<style scoped>
</style>
