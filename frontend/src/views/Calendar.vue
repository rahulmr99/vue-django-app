<template>
  <div class="animated fadeIn">

    <b-modal ref="cancel" no-close-on-esc no-close-on-backdrop hide-footer title="Your account has been cancelled" class="canceled-subscription-alert">
      <p id="cancel-modal-body">Click the button below to reactivate it.</p>
      <button @click="reactivate" id="cancel-modal-button" class="btn btn-primary">Reactivate Your Account</button>
    </b-modal>

    <b-modal no-close-on-esc no-close-on-backdrop ref="reactive" class="subscribeModal">
      <iframe  src="https://bookedfusion.chargebee.com/portal/v2/login?forward=portal_main"
               scrolling="no"  frameborder="0" style="height: 500px; width: 100%;">
      </iframe>
    </b-modal>
    <searchPhone v-if="show_booked_fusion_number_form" ></searchPhone>

    <SearchUserPopupForm></SearchUserPopupForm>
    <CalendarFormPopupUpdate ref="CalendarFormPopupUpdate"
                             v-on:fetchCalendarEvents="fetchCalendarEvents"></CalendarFormPopupUpdate>
    <div class="row color-calendar">
      <div class="col-md-12">
        <button class="btn btn-danger btn-sm add-calendar" @click="addCalendarForm()" type="button">
          <img src="/static/img/add.png" width="20px" >
        </button>
      </div>
    </div>
    <br/>
    <div class="row">
      <div class="col">
        <full-calendar id="event-calendar" ref="fullCalendar" :events="events" @event-selected="addCalendarForm"
                       @event-created="addCalendarForm"
                       :config="configs.fc_config"
                       :header="configs.header">


                       </full-calendar>
      </div>
    </div>
  </div>
</template>

<script>
  import CalendarFormPopupUpdate from '../components/forms/CalendarFormPopupUpdate.vue'
  import SearchUserPopupForm from '../components/forms/SearchUserPopupForm_fix.vue'
  import searchPhone from '../components/PhoneSearch.vue'
  import SubscriptionCheck from '../components/class/SubscriptionCheck.vue'
  export default {
    name: 'calendar',
    components: {
      CalendarFormPopupUpdate,
      SearchUserPopupForm,
      searchPhone,
      SubscriptionCheck,
    },
    created () {
      this.$root.bus.checkLogin()
    },

    mounted () {
      // set business hours
      this.$on('resetCalendarForm', this.resetForm())
      this.setBusinessHours()
      if (!localStorage.getItem('shownAddAppointmentInfo')) {
        this.$notySuccess('Click and drag anywhere on the calendar to add new appointment')
        localStorage.setItem('shownAddAppointmentInfo', true)
      }
      this.$root.bus.$on('go-to-date', this.selectFullCalendarDate)
      this.$api.billing.status().then(response => {
        if (response.body.cancelled === true) {
          this.$refs.cancel.show()
          this.show_booked_fusion_number_form = false
        } else {
          this.show_booked_fusion_number_form = !response.body.is_booked_fusion_number
        }
      }, response => {
      })
    },
    methods: {
      CheckSubscriptionStatus () {
        this.$api.billing.status().then(response => {
          if (response.body.cancelled === false) {
            this.$refs.reactive.hide()
          } else {
            setTimeout(this.CheckSubscriptionStatus, 5000)
          }
        }, response => {
        })
      },
      reactivate () {
        this.$refs.cancel.hide()
        this.$refs.reactive.show()
        setTimeout(this.CheckSubscriptionStatus(), 5000)
      },
      selectFullCalendarDate (e, o) {
        this.$refs.fullCalendar.fireMethod('gotoDate', o)
        this.$refs.fullCalendar.fireMethod('changeView', 'agendaDay')
        this.fetchCalendarEvents()
      },
      resetForm () {
        this.$refs.CalendarFormPopupUpdate.fetchProviders()
        this.$refs.CalendarFormPopupUpdate.fetchServices()
        this.$refs.CalendarFormPopupUpdate.cleanErrors()
        this.$refs.CalendarFormPopupUpdate.clearForm()
      },
      addCalendarForm (event) {
        this.resetForm()
        if (event) {
          this.$root.bus.calendar.form_field_data.start_date = event.start.format('MM.DD.YYYY')
          this.$root.bus.calendar.form_field_data.start_time = event.start.format('h:mm A')
          this.$root.bus.calendar.form_field_data.end_time = event.end.format('h:mm A')
          this.$root.bus.calendar.form_field_data.end_date = event.end.format('MM.DD.YYYY')
          this.$root.bus.calendar.form_field_data.selected_calendar_data = event

          // the below will get filled only in case of update
          if (event.id) {
            this.$root.bus.calendar.form_field_data.id = event.id
            this.$root.bus.calendar.form_field_data.first_name = event.users_customer.name
            this.$root.bus.calendar.form_field_data.address = event.users_customer.address
            this.$root.bus.calendar.form_field_data.last_name = event.users_customer.last_name
            this.$root.bus.calendar.form_field_data.city = event.users_customer.city
            this.$root.bus.calendar.form_field_data.phone = event.users_customer.phone
            this.$root.bus.calendar.form_field_data.mobile = event.users_customer.mobile
            this.$root.bus.calendar.form_field_data.email = event.users_customer.email
            this.$root.bus.calendar.form_field_data.zip_code = event.users_customer.zip_code
            this.$root.bus.calendar.form_field_data.note = event.users_customer.note

            this.$nextTick(function () {
              this.$root.bus.calendar.form_field_data.provider_choice = event.users_provider ? event.users_provider : -1
              this.$root.bus.calendar.form_field_data.service_choice = event.services ? event.services : -1
            })
          }
        }

        this.$root.bus.calendar.add_form = !(event && event.id)
        this.$root.bus.calendar.edit_form = !!(event && event.id)
      },
      setBusinessHours () {
        this.$api.users.app.getBusinessHours().then(response => {
          this.configs.fc_config.businessHours = response.body
          window.$('#event-calendar').fullCalendar('option', 'businessHours', response.body)

          // calculate min/max time range
          let minStart, maxEnd
          response.body.forEach(function (elem) {
            if (!minStart) {
              minStart = elem.start
            }
            if (!maxEnd) {
              maxEnd = elem.end
            }

            if (elem.start < minStart) {
              minStart = elem.start
            }
            if (elem.end > maxEnd) {
              maxEnd = elem.end
            }
          })

          // update full-calendar using jquery.
          // todo: find a reactive library to do this
          window.$('#event-calendar').fullCalendar('option', 'businessHours', response.body)
          window.$('#event-calendar').fullCalendar('option', 'minTime', minStart)
          window.$('#event-calendar').fullCalendar('option', 'maxTime', maxEnd)
          window.$('#event-calendar').fullCalendar('option', 'slotDuration', '00:10:00')
        }, response => {
        })
      },
      fetchCalendarEvents () {
        let dateFormat = 'YYYY-MM-DD'
        let sendId = {
          'date': this.start_date.format(dateFormat),
          'end_date': this.end_date.format(dateFormat),
        }

        this.$api.calendar.filterCalendarEvents(sendId).then(response => {
          this.events = response.body
        }, response => {
        })
      },
      handleFCViewRender (fullCalendarView, element) {
        if (!(this.start_date.isSame(fullCalendarView.start)) || !(this.end_date.isSame(fullCalendarView.end))) {
          this.start_date = fullCalendarView.start
          this.end_date = fullCalendarView.end
          this.fetchCalendarEvents()
        }
      },
      handleFCViewWeekHeaderRender (mom) {
        if (window.$('.fc-month-button.fc-state-active').length > 0) {
          return '<div class="day">' + mom.format('ddd') + '</div>' + '<div class="date"></div>'
        } else {
          return '<div class="day">' + mom.format('ddd') + '</div>' + '<div class="date">' + mom.format('D') + '</div>'
        }
      },
    },
    data: function () {
      return {
        modalShow: false,
        start_date: this.$moment(),
        end_date: null,
        show_booked_fusion_number_form: false,
        configs: {
          header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay,listWeek',
          },
          fc_config: {
            aspectRatio: 1,
            gotoDate: this.start_date,
            eventOverlap: false,
            selectOverlap: false,
            firstDay: 1,
            timeFormat: 'hh:mm a',
            columnHeaderHtml: this.handleFCViewWeekHeaderRender,
            viewRender: this.handleFCViewRender,
            navLinks: true,
          },
        },
        events: [],
      }
    },
    beforeDestroy () {
      this.$root.bus.$off('go-to-date', this.selectFullCalendarDate)
    },
  }
 </script>

<style>
  #cancel-modal-body{
    text-align: center;
  }
  #cancel-modal-button{
    margin-left: 120px;
  }
  .color-calendar {
    padding: 10px;
  }

  .fc-view-container {
    background-color: floralwhite;
  }

.date {    font-size: 40px;
    text-align: left;
    font-weight: 200;
    padding-left: 10px;}


.day {text-align: left;
    padding-left: 10px;
    font-size: 12px;
    padding-top: 10px;}

    .fc-ltr .fc-axis {
    text-align: left;
    font-size: 10px;
}

.fc-view-container {
    background-color: white !important;
   webkit-box-shadow: -1px 0 2px rgba(0, 0, 0, 0.15), 1px 0 2px rgba(0, 0, 0, 0.15), 0 4px 8px rgba(0, 0, 0, 0.15);
    -webkit-box-shadow: -1px 0 2px rgba(0, 0, 0, 0.15), 1px 0 2px rgba(0, 0, 0, 0.15), 0 4px 8px rgba(0, 0, 0, 0.15);
    box-shadow: -1px 0 2px rgba(0, 0, 0, 0.15), 1px 0 2px rgba(0, 0, 0, 0.15), 0 4px 8px rgba(0, 0, 0, 0.15);
}

.fc-today { color:#3b77e7;}

.date:hover { text-decoration:underline;}

div.subscribeModal header,
div.subscribeModal footer
{
  display: none !important;
}

div.subscribeModal div.modal_body{
  padding: 10px;
}
.canceled-subscription-alert .close{
  display: none;
}
</style>


