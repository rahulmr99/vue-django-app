/* eslint-disable import/first,camelcase */
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import api from './api/booking/index'
import VueProgressBar from 'vue-progressbar'
import FullCalendar from 'vue-full-calendar'
import Notifications from 'vue-notification'
import BootstrapVue from 'bootstrap-vue'
import VueTrumbowyg from 'vue-trumbowyg'
import moment from 'moment'
import VueTheMask from 'vue-the-mask'
import VueResourceProgressBarInterceptor from 'vue-resource-progressbar-interceptor'

// a quick-fix to solve icons not loading issue easy_appointments_backend#65 point-30.
// The correct way to set up vue-loader or webpack 4
window.$.trumbowyg.svgPath = 'https://cdn.jsdelivr.net/npm/trumbowyg/dist/ui/icons.svg'

// directives
Vue.use(VueTheMask)

Vue.config.productionTip = false

// global components
Vue.use(BootstrapVue)
Vue.use(FullCalendar)
Vue.use(VueTrumbowyg)
// notification and helper methods
Vue.use(Notifications)
Vue.prototype.$notySuccess = function (msg, title) {
  msg = msg || 'Saved Successfully'
  this.$notify({
    group: 'success',
    text: msg,
    title: title,
  })
}

Vue.filter('currency', function (value) {
  if (value === 1) {
    return ' USD'
  } else {
    return 'EUR'
  }
})

Vue.filter('two_digits', function (value) {
  if (value.toString().length <= 1) {
    return '0' + value.toString()
  }
  return value.toString()
})

Vue.filter('dayweek', function (value) {
  if (value === 1) {
    return ' Monday'
  } else if (value === 2) {
    return 'Tuesday'
  } else if (value === 3) {
    return 'Wednesday'
  } else if (value === 4) {
    return 'Thursday'
  } else if (value === 5) {
    return 'Friday'
  } else if (value === 6) {
    return 'Saturday'
  } else if (value === 7) {
    return 'Sunday'
  }
})

Vue.use(VueProgressBar, {
  color: '#104cba',
  failedColor: 'red',
  thickness: '5px',
  transition: {
    speed: '0.1s',
    opacity: '0.6s',
    termination: 2000,
  },
})

Vue.use(require('vue-pusher'), {
  api_key: '4010826535e9b939f154',
  options: {
    cluster: 'ap2',
    encrypted: true,
  },
})

Vue.use(VueResourceProgressBarInterceptor, {
  latencyThreshold: 10,
})

// instance properties/helpers
Vue.prototype.$api = api
Vue.prototype.$moment = moment
Vue.prototype.$eventBus = new Vue()
const Twilio = require('twilio-common')
const TwilioChat = require('twilio-chat')

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  data: {
    bus: new Vue({
      data: {
        router: router,
        info: {},
        user_login: false,
        loading: false,
        is_admin: false,
        is_provider: false,
        is_secretarie: false,
        calendar: {
          add_form: false,
          edit_form: false,
          search_user_popup_form: false,
          current_date: null,
          form_field_error: {
            service_error: null,
            first_name_error: null,
            start_date_error: null,
            start_time_error: null,
            end_time_error: null,
            end_date_error: null,
            email_error: null,
          },
          form_field_data: {
            id: null,
            selected_calendar_data: null,
            provider_list: null,
            provider_choice: 1,
            service_list: null,
            service_choice: 1,
            start_date: null,
            start_time: null,
            end_time: null,
            end_date: null,
            first_name: null,
            last_name: null,
            email: null,
            address: null,
            city: null,
            phone: null,
            mobile: null,
            zip_code: null,
            note: null,
            non_field_errors: null,
            error_first_name: null,
            error_last_name: null,
            error_email: null,
          },
        },
        customers: {
          customers_list: null,
          appointments_list: [],
          page: 1,
          next: null,
          previous: null,
          count: 0,
          choice: null,
          choice_id: null,
          choice_item: {},
          search: null,
        },
        services: {
          category: {
            add_form: false,
            edit_form: false,
            category_list: null,
            page: 1,
            next: null,
            previous: null,
            count: 0,
            choice: null,
            choice_id: null,
            choice_item: {},
            search: null,
            form_field_data: {
              name: null,
              description: null,
            },
            form_field_error: {
              non_field_errors: null,
              error_name: null,
            },
          },
          add_form: false,
          edit_form: false,
          pane1: true,
          pane2: false,
          services_list: null,
          page: 1,
          next: null,
          previous: null,
          count: 0,
          choice: null,
          choice_id: null,
          choice_item: {},
          search: null,
          form_field_data: {
            name: null,
            duration: null,
            price: null,
            // currency: null,
            category: null,
            availabilities_type: null,
            attendants: null,
            description: null,
          },
          form_field_error: {
            non_field_errors: null,
            error_name: null,
            error_duration: null,
            error_price: null,
            error_attendants: null,
          },
        },
        users: {
          form_data: {
            userType: '',
            userTypes: {
              0: 'admin',
              1: 'provider',
              2: 'secretarie',
              3: 'customer',
            },
          },
          admin: {
            admin_list: null,
            page: 1,
            next: null,
            previous: null,
            count: 0,
            choice: null,
            choice_id: null,
            choice_item: {},
            search: '',
          },
          provider: {
            provider_list: null,
            set_service_popup_form: false,
            page: 1,
            next: null,
            previous: null,
            count: 0,
            choice: null,
            choice_id: null,
            choice_item: {},
            search: '',
          },
          secretarie: {
            secretarie_list: null,
            page: 1,
            next: null,
            previous: null,
            count: 0,
            choice: null,
            choice_id: null,
            choice_item: {},
            search: '',
          },
          working_plan: {
            item: null,
            edit_form: false,
            working_plan_list: [],
            breaks_list: [],
            choice_id: null,
            choice_item: {},
            choice_id_break: null,
            choice_item_break: {},
            form_select_day: '7',
            form_select_start: '06:00',
            form_select_end: '06:10',
            edit_break: false,
          },
          pane1: true,
          pane2: false,
          pane3: false,
        },
        settings: {
          general_settings: {
            error_email: null,
            error_link: null,
            item: {},
          },
          initial_settings: {
            item: {},
          },
          reminder_settings: {
            item: {},
          },
          ratings_settings: {
            item: {},
            report: [],
          },
          credentials_settings: {
            password1: null,
            password2: null,
          },
          working_plan: {
            item: null,
            edit_form: false,
            working_plan_list: [],
            breaks_list: [],
            choice_id: null,
            choice_item: {},
            choice_id_break: null,
            choice_item_break: {},
            form_select_day: '7',
            form_select_start: '06:00',
            form_select_end: '06:10',
            edit_break: false,
          },
          pane1: false,
          pane2: false,
          pane3: false,
          pane4: true,
          pane5: false,
        },
        booked_fusion_number: null,
        chatClient: null,
        channels: [],
        fetchingChannels: false,
      },
      created: function () {
        this.check_token()
      },
      methods: {
        getFormUserTypeIsAdmin () {
          return this.users.form_data.userType === 'admin'
        },
        getFormUserTypeIsProvider () {
          return this.users.form_data.userType === 'provider'
        },
        getFormUserTypeIsCustomer () {
          return this.users.form_data.userType === 'customer'
        },
        getFormUserTypeIsSecretarie () {
          return this.users.form_data.userType === 'secretarie'
        },
        setFormUserType (index) {
          this.users.form_data.userType = this.users.form_data.userTypes[index]
        },
        loginFailedCallback (errors) {
          console.log(errors)
          this.loading = true
          localStorage.removeItem('key')
          this.user_login = false
          this.checkLogin()
        },
        check_token () {
          let jwt = localStorage.getItem('key')
          if (jwt) {
            api.login.app.token_check({
              'token': jwt,
            }).then(response => {
              this.user_login = true
              this.info = response.body.info
              this.is_admin = response.body.info.is_admin
              this.is_provider = response.body.info.is_provider
              this.is_secretarie = response.body.info.is_secretarie
              this.loading = true
              this.requestChatToken()
            }, this.loginFailedCallback)
          } else {
            this.loginFailedCallback()
          }
        },
        checkLogin () {
          if (window.location.hash.indexOf('signup') > -1) {
            router.push({
              path: '/signup',
            })
          } else if (!this.user_login) {
            router.push({
              path: '/login',
            })
          }
        },
        checkLogout () {
          this.user_login = false
          localStorage.removeItem('key')
          this.check_token()
          router.push({
            path: '/login',
          })
          this.chatClient.shutdown()
        },
        requestChatToken () {
          api.messaging.app.tokenGeneration().then(response => {
            let token = response.body.token

            TwilioChat.Client.create(token).then(client => {
              this.chatClient = client
              var subscribedChannels = []
              this.fetchingChannels = true
              var instance = this

              const accessManager = Twilio.AccessManager(token)
              accessManager.on('tokenUpdated', am => client.updateToken(am.token))

              accessManager.on('tokenExpired', () => {
                api.messaging.app.tokenGeneration().then(resp => {
                  accessManager.updateToken(resp.body.token)
                })
              })

              this.chatClient.getSubscribedChannels().then(function (paginator) {
                subscribedChannels = paginator.items
                instance.channels = subscribedChannels.sort(function (a, b) {
                  if (typeof a.lastMessage !== 'undefined' && typeof b.lastMessage !== 'undefined') {
                    if (Date.parse(a.lastMessage.timestamp) > Date.parse(b.lastMessage.timestamp)) {
                      return -1
                    }
                    if (Date.parse(a.lastMessage.timestamp) < Date.parse(b.lastMessage.timestamp)) {
                      return 1
                    }
                    return 0
                  } else {
                    if (typeof a.lastMessage !== 'undefined') {
                      return -1
                    }
                    if (typeof b.lastMessage !== 'undefined') {
                      return 1
                    }
                    return 0
                  }
                })
                instance.fetchingChannels = false
              })
              this.chatClient.on('messageAdded', function (message) {
                instance.$eventBus.$emit('newMessage', message)
              })
              this.chatClient.on('channelJoined', function (channel) {
                instance.channels.push(channel)
              })
              this.chatClient.on('channelUpdated', function (updateDetails) {
                if (updateDetails.updateReasons.includes('friendlyName')) {
                  for (var key in instance.channels) {
                    if (instance.channels[key].uniqueName === updateDetails.channel.uniqueName) {
                      instance.$set(instance.channels, key, updateDetails.channel)
                      break
                    }
                  }
                }
              })
            }, error => {
              console.log(error)
            })
          }, this.loginFailedCallback)
        },
      },
    }),
  },
  components: {
    App,
  },
  watch: {
    '$route': function (value) {
      if (value.name === 'login' || value.name === 'BillingInfo') {} else {
        this.$api.billing.status().then(response => {
          if (response.body.cancelled === true) {
            this.$router.push({
              path: '/calendar',
            })
          }
        }, response => {})
      }
    },
  },
})
