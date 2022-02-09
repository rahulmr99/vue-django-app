<template>
  <header class="app-header navbar">
    <Caller v-show="showPhone" v-on:got-twilio-token="enableCallerBtn"></Caller>
    <button class="navbar-toggler mobile-sidebar-toggler d-lg-none" type="button" @click="mobileSidebarToggle">&#9776;
    </button>
    <b-link class="navbar-brand" to="#"></b-link>

    <button class="navbar-toggler sidebar-toggler d-md-down-none" type="button" @click="sidebarToggle">&#9776;</button>
    <span class="ml-auto p-relative">
     <input type="text" class="custom-search ml-auto" placeholder="Search" @keyup="searchCustomers" v-model="search_input"/>
      <div class="search-result" v-on-click-outside="hideSearchResults">
        <div class="search-section" v-if="find_list" v-on:click="GotoDate(item)" v-for="(item, index) in find_list">
          <div class="search-text">{{ item.name }} {{ item.last_name }}</div>
          <div v-if="item.next_appoinment" class="search-text1">Next appointment : <span v-model="date">{{ item.next_appoinment }}</span> </div>
          <div v-else class="search-text1">No upcoming appointments </div>
        </div>
      </div>
     </span>

    <b-navbar-nav class="ml-auto">
      <!-- <button
        class="caller-ph"
        @click='showphone()' :disabled="!gotTwilioToken">
        <i :class="['fa', fetchingToken ? 'fa-circle-o-notch fa-spin' : 'fa-phone call']"></i>
      </button> -->
      <b-nav-item-dropdown right>

        <template slot="button-content">
          <img src="static/img/avatars/userlogin.png" class="img-avatar" :alt="$root.bus.info.email">
          <!-- <span class="d-md-down-none">{{ $root.bus.info.email }}</span> -->
        </template>
        <b-dropdown-header tag="div" class="text-center"><strong>Action</strong></b-dropdown-header>
        <b-dropdown-item-button @click="$root.bus.checkLogout">
          <i class="fa fa-lock"></i> Sign out
        </b-dropdown-item-button>
      </b-nav-item-dropdown>
    </b-navbar-nav>
  </header>
</template>

<script>
  // import moment from 'moment'
  import Caller from '../views/Caller'
  import { mixin as onClickOutside } from 'vue-on-click-outside'
  import moment from 'moment'

  export default {
    name: 'header',
    mixins: [onClickOutside],
    components: {
      Caller,
    },
    data () {
      return {
        find_list: [],
        choice_item: {},
        search_input: null,
        date: '',
        showPhone: false,
        fetchingToken: true,
        gotTwilioToken: false,
      }
    },
    methods: {
      showphone () {
        this.showPhone = true
      },
      hideSearchResults () {
        this.find_list = []
      },
      sidebarToggle (e) {
        e.preventDefault()
        document.body.classList.toggle('sidebar-hidden')
      },
      enableCallerBtn () {
        this.fetchingToken = false
        this.gotTwilioToken = true
      },
      GotoDate (event) {
        var eventObj = null
        if (event.next_appoinment) {
          var nextAppt = event.next_appoinment
          let sendId = {
            'date': nextAppt,
            'end_date': null,
          }
          this.$api.calendar.filterCalendarEvents(sendId).then(response => {
            var events = response.body
            var _this = this
            for (var i = 0; i < events.length; i++) {
              if (events[i].users_customer && events[i].users_customer.id === event.id) {
                eventObj = events[i]
                if (_this.$root.$children[0].$children[2].$children[2]._uid === 33) {
                  _this.$emit('resetCalendarForm')
                } else {
                  _this.$emit('resetUserForm')
                }
                _this.$root.bus.calendar.form_field_data.start_date = moment(eventObj.start.split('T')[0]).format('MM.DD.YYYY')
                _this.$root.bus.calendar.form_field_data.start_time = moment(eventObj.start).format('h:mm A')
                _this.$root.bus.calendar.form_field_data.end_time = moment(eventObj.end).format('h:mm A')
                _this.$root.bus.calendar.form_field_data.end_date = moment(eventObj.end.split('T')[0]).format('MM.DD.YYYY')
                _this.$root.bus.calendar.form_field_data.selected_calendar_data = eventObj
                _this.$root.bus.calendar.form_field_data.id = eventObj.id
                _this.$root.bus.calendar.form_field_data.first_name = eventObj.users_customer.name
                _this.$root.bus.calendar.form_field_data.address = eventObj.users_customer.address
                _this.$root.bus.calendar.form_field_data.last_name = eventObj.users_customer.last_name
                _this.$root.bus.calendar.form_field_data.city = eventObj.users_customer.city
                _this.$root.bus.calendar.form_field_data.phone = eventObj.users_customer.phone
                _this.$root.bus.calendar.form_field_data.mobile = eventObj.users_customer.mobile
                _this.$root.bus.calendar.form_field_data.email = eventObj.users_customer.email
                _this.$root.bus.calendar.form_field_data.zip_code = eventObj.users_customer.zip_code
                _this.$root.bus.calendar.form_field_data.note = eventObj.users_customer.note
                _this.$root.bus.calendar.form_field_data.provider_choice = eventObj.users_provider
                _this.$root.bus.calendar.form_field_data.service_choice = eventObj.services
                _this.$root.bus.calendar.edit_form = !!(eventObj && eventObj.id)
              }
            }
          }, response => {
          })
        } else {
          this.$root.$children[0].$children[2].$children[2].addCalendarForm(eventObj)
          this.$root.bus.calendar.form_field_data.first_name = event.name
          this.$root.bus.calendar.form_field_data.last_name = event.last_name
          this.$root.bus.calendar.form_field_data.phone = event.phone
          this.$root.bus.calendar.form_field_data.email = event.email
          this.$root.bus.calendar.form_field_data.note = event.note
        }
      },
      sidebarMinimize (e) {
        e.preventDefault()
        document.body.classList.toggle('sidebar-minimized')
      },
      mobileSidebarToggle (e) {
        e.preventDefault()
        document.body.classList.toggle('sidebar-mobile-show')
      },
      searchCustomers () {
        if (this.search_input === '') {
          this.find_list = []
          return
        }
        this.$api.users.app.search(`${this.search_input}&is_customers=true`).then(response => {
          this.find_list = response.body.results
        }, response => {
        })
      },
    },
  }
</script>
