<template>
  <div id="mini-control-calendar">
  </div>
</template>

<script>
  // todo: select week when week selection is enabled on fullcalendar
  // todo: respond to the date set on fullcalendar
  import Flatpickr from 'flatpickr'

  export default {
    name: 'mini-calendar',
    data () {
      return {
        fp: null, // flatpickr instance
      }
    },
    mounted () {
      if (this.fp) return

      let config = {
        inline: true,
        onDayCreate: function (dObj, dStr, fp, dayElem) {
          dayElem.className += ' small-flatpickr-day'
          window.fp = fp
        },
      }
      config.onChange = this.onChangeHandler

      this.fp = new Flatpickr(this.$el, config)
      this.fp.calendarContainer.className += ' small-flatpickr-calendar'
      this.fp.daysContainer.className += ' small-flatpickr-days'
    },
    beforeDestroy () {
      if (this.fp) {
        this.fp.destroy()
        this.fp = null
      }
    },
    methods: {
      /**
       * Emit on-change event
       */
      onChangeHandler (...args) {
        if (this.$route.path !== '/calendar') {
          this.$router.push({path: '/calendar'})
        }
        this.$root.bus.$emit('go-to-date', ...args)
      },
    },
  }
</script>

<style>
</style>
