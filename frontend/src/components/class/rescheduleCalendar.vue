 <template>
  <div id="mini-control-calendar">
  </div>
</template>

<script>
  // todo: select week when week selection is enabled on fullcalendar
  // todo: respond to the date set on fullcalendar
  import Flatpickr from 'flatpickr'
  import Moment from 'moment'

  export default {
    name: 'reschedule-calendar',
    data () {
      return {
        fp: null, // flatpickr instance
        events: null,
        day_date: new Moment(),
        page: 0,

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
      toIsoString (date) {
        var pad = function (num) {
          var norm = Math.floor(Math.abs(num))
          return (norm < 10 ? '0' : '') + norm
        }
        return date.getFullYear() +
          '-' + pad(date.getMonth() + 1) +
          '-' + pad(date.getDate()) +
          'T' + pad(date.getHours()) +
          ':' + pad(date.getMinutes()) +
          ':' + pad(date.getSeconds())
      },
      onChangeHandler (date) {
        var dayDate = new Date(date[0])
        dayDate = this.toIsoString(dayDate)
        this.day_date = dayDate
        this.$root.bus.calendar.form_field_data.start_date = Moment(date[0]).format('MM.DD.YYYY')
        this.fetchCalendarTime()
      },
      fetchCalendarTime () {
        this.$api.calendar.getCalendar(`&page=${this.page}&daydate=${this.day_date}&service_id=${this.$root.bus.calendar.form_field_data.service_choice}&provider_id=${this.$root.bus.calendar.form_field_data.provider_choice}`)
          .then(response => {
            this.$parent.options = response.body.days
          }, response => {
            this.$parent.options = null
          })
          .catch(function (error) {
            console.log(error)
          })
      },
    },
  }
</script>

<style>
</style>
