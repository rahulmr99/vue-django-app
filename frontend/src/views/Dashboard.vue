<template>
  <div class="animated fadeIn">
    Hello World
  </div>
</template>

<script>
export default {
  name: 'dashboard',
  methods: {
    created: function () {
      this.$root.bus.checkLogin()
    },
  },
}
</script>
