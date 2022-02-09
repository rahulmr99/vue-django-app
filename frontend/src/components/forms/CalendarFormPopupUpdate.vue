<template>
  <modal class="calendar-add-form" :title="getFormTitle" large v-model="showForm"
         @ok="showForm = false" effect="zoom" ref="modal">
    <template slot="header-buttons">
      <button class="btn btn-primary ml15 pop-head-b p-relative " v-show="$root.bus.calendar.edit_form" @click="confirmation()">Cancel
      <div class="cancel-div" v-show="cancelBtn">
        <p>Do you Want to Cancel the Appointment? </p>
        <div class="op-btn">
          <button class="btn" @click="cancelAppt()"> YES  </button>
          <button class="btn"> NO  </button>
        </div>
      </div>
      </button>
      <button class="btn btn-primary ml15 pop-head-b " v-show="$root.bus.calendar.edit_form" @click="rescheduleFunc()" >Reschedule</button>
    </template>
    <template slot="modal-footer">
      <div class="modal-footer">
        <button type="button" @click="validateForm" class="btn btn-primary">{{ saveBtnText }}</button>
        <button v-show="$root.bus.calendar.edit_form" type="button" @click="deleteCalendar"
                class="btn btn-danger pull-left">Remove
        </button>
      </div>
    </template>
    <!--Provider and Service-->
    <schedulerForm v-show="reschedule"></schedulerForm>

    <div v-show="!reschedule">
      <div class="row">
        <div class="col-sm-12">
          <div class="form-group required"
              v-bind:class="[{'has-danger': $root.bus.calendar.form_field_error.service_error }]">
            <!--label class="caption">Select Service</label-->
            <select class="form-control" v-model="$root.bus.calendar.form_field_data.service_choice" v-on:change="changeAppointmentType()"
                    v-bind:class="[{'is-invalid': $root.bus.calendar.form_field_error.service_error }]">
              <option disabled :value="null">Choose appoinment type</option>
              <option
                :value="item.id"
                :selected="$root.bus.calendar.form_field_data.service_list.length === 1"
                v-for="item in $root.bus.calendar.form_field_data.service_list">
                {{item.name}}
              </option>
            </select>
            <div class="invalid-feedback" v-if="$root.bus.calendar.form_field_error.service_error">is required</div>
          </div>
        </div>
      </div>
      <!--Date time row-->
      <div class="row">
        <div class="col-sm-3">
          <inp id="start_date" v-model="$root.bus.calendar.form_field_data.start_date"
              :required="true"></inp>
        </div>
        <div class="col-sm-3 tym">
          <inp id="start_time" v-model="$root.bus.calendar.form_field_data.start_time"
              :required="true"></inp>
        </div>
        <div class="col-sm-3">
          <inp id="end_time" v-model="$root.bus.calendar.form_field_data.end_time"
              :required="true"></inp>
        </div>
        <div class="col-sm-3">
          <inp id="end_date" v-model="$root.bus.calendar.form_field_data.end_date"
              :required="true"></inp>
        </div>
        <div class="col-sm-12" v-if="this.$root.bus.calendar.form_non_field_errors">
          <div class="invalid-feedback" style="display: block;">{{this.$root.bus.calendar.form_non_field_errors}}</div>
        </div>
      </div>

      <!--First name Address-->
      <div class="row">
        <div class="col-sm-12">
          <inp id="first_name" v-model="$root.bus.calendar.form_field_data.first_name"
               :required="true" placeholder="Enter first name*"
               type="text" @input="searchCustomers($event)" @click="hideSearchResults" />

            <div class="search-result1">
              <div class="search-section" v-if="find_list" v-on:click="GotoDate(item)" v-for="(item, index) in find_list">
                <div class="search-text" >{{ item.name }} {{ item.last_name }}</div>
              </div>
            </div>
        </div>
      </div>
      <!--Last name -->
      <div class="row">
        <div class="col-sm-12">
            <inp id="last_name" v-model="$root.bus.calendar.form_field_data.last_name"
                    :required="true" placeholder="Enter last name*"  type="text" />

        </div>
      </div>
      <!--Phone Mobile-->
      <div class="row">
        <div class="col-sm-12">
          <inp id="email" v-model="$root.bus.calendar.form_field_data.email" placeholder="Enter email" type="email"
          ></inp>
        </div>
        <!--div class="col-sm-6">
          <inp label="Mobile" id="mobile" v-model="$root.bus.calendar.form_field_data.mobile"
              placeholder="Enter mobile"></inp>
        </div-->
      </div>
      <!--Email Zip code-->
       <div class="row">
        <div class="col-sm-12">
          <div class="input-group mb20">
            <input class="form-control" id="phone" v-model="$root.bus.calendar.form_field_data.phone"
                placeholder="Enter phone" type="text">
           <!--  <span class="input-group-btn" > <button class="btn btn-secondary" @click="makeCall" type="button"><i class="fa fa-phone" aria-hidden="true"></i> </button> -->
            </span>
          </div>
        </div>
        <!--div class="col-sm-6">
          <inp label="Zip code" id="zip" v-model="$root.bus.calendar.form_field_data.zip_code"
              placeholder="Enter zip code"></inp>
        </div-->
      </div> 
      <!--Notes-->
      <div class="row">
        <div class="col-sm-12">
          <div class="form-group">
            <!--label for="note">Note</label-->
            <textarea rows="6" class="form-control" id="note" v-model="$root.bus.calendar.form_field_data.note"
                      placeholder="Enter note"></textarea>
          </div>
        </div>
      </div>
    </div>
  </modal>
</template>

<style>
.required .flatpickr-input {
    background-color: #e6e6e6 ! important;
    border: 0px;
    padding: 10px;
    border-radius: 5px;
    color: black;
    font-weight: 400;
    text-align: center;
    font-size: 14px;
    }

.form-control:focus {
    color: #3e515b;
    background-color: #fff;
    border-color: #3b77e75e;
    outline: 0;
    -webkit-box-shadow: 0 0 0 0.1rem rgba(59, 119, 231, 0.48);
    box-shadow: 0 0 0 0.1rem rgba(59, 119, 231, 0.68);
}

.ml15 { margin-left:15px;}

.pop-head-b {padding: 3px 10px;}

.tym:after {
 content: 'TO';
    position: absolute;
    color: #737373;
    font-size: 14px;
    z-index: 111;
    top: 10px;
    right: -10px;
}

.cancel-div {     position: absolute;
    background: #fff;
    padding: 10px;
    -webkit-box-shadow: 0px 0px 9px 2px #929292;
    box-shadow: 0px 0px 9px 2px #9292928a;
    z-index: 5;
    border-radius: 4px;
    top: 40px;
    overflow-wrap: break-word;
    left: -113px;}

.cancel-div:before {
      content: '';
    width: 0;
    position: absolute;
    height: 0;
    border-style: solid;
    border-width: 0 7.5px 10px 7.5px;
    border-color: transparent transparent #ffffff transparent;
    top: -9px;
    left: 47%;
    z-index: 0;}


.cancel-div:after {
    content: '';
    width: 0;
    position: absolute;
    height: 0;
    border-style: solid;
    border-width: 0 7.5px 10px 7.5px;
    border-color: transparent transparent #7b7a7a transparent;
    top: -9px;
    left: 47%;
    z-index: -1;}

.cancel-div p {    color: #1d1d1d;
    margin-bottom: 0px;
    font-weight: bold;
    font-size:13px;
        }
.op-btn {
    margin: 5px;
}

.pb20 { padding-bottom:20px;}

.search-result1 {
    position: absolute;
    background: white;
    width: 100%;
    -webkit-box-shadow: 0 0 2px rgba(0, 0, 0, 0.12), 0 2px 4px rgba(0, 0, 0, 0.24), inset 0 4px 6px -4px rgba(0, 0, 0, 0.24);
    box-shadow: 0 0 2px rgba(0, 0, 0, 0.12), 0 2px 4px rgba(0, 0, 0, 0.24), inset 0 4px 6px -4px rgba(0, 0, 0, 0.24);
    margin-top: 2px;
    border-radius: 2px;
    z-index: 1;
    top: 34px;
}



</style>



<script>
  import modal from '../class/ModalFormClass.vue'
  import flatpickr from 'flatpickr'
  import Inp from '../class/Inp.vue'
  import schedulerForm from '../class/reschedule.vue'

  export default {
    name: 'calendar-add-popup-form',
    components: {
      modal,
      Inp,
      schedulerForm,
    },
    mounted () {
      this.$nextTick(function () {
        this.initStartDate()
        this.initStartTime()
      })
      this.end_time_component = flatpickr('#end_time', {
        enableTime: true,
        noCalendar: true,
        time_24hr: false,
        dateFormat: 'h:i K',
        defaultHour: 12,
        defaultMinute: 0,
      })
      this.end_date_component = flatpickr('#end_date', {
        dateFormat: 'm.d.Y',
      })
    },
    data () {
      return {
        error: false,
        start_date_component: null,
        start_time_component: null,
        end_date_component: null,
        end_time_component: null,
        cancelBtn: false,
        reschedule: false,
        find_list: [],
      }
    },
    watch: {
      showForm: function () {
        if (!this.showForm) {
          this.reschedule = false
          this.find_list = []
        }
      },
    },
    computed: {
      getFormTitle () {
        if (this.$root.bus.calendar.edit_form) {
          return 'Appointment'
        }
        return 'Appointment'
      },
      saveBtnText () {
        if (this.$root.bus.calendar.edit_form) {
          return 'Update'
        }
        return 'Create Appointment'
      },
      showForm: {
        get: function () {
          this.cleanErrors()
          return this.$root.bus.calendar.edit_form || this.$root.bus.calendar.add_form
        },
        set: function (newValue) {
          if (!newValue) {
            this.$root.bus.calendar.edit_form = newValue
            this.$root.bus.calendar.add_form = newValue
          }
        },
      },
    },
    methods: {
      makeCall () {
        this.cleanErrors()
        this.showForm = false
        this.clearForm()
        this.$root.$children[0].$children[2].$children[0].showPhone = true
        this.$root.$children[0].$children[2].$children[0].$children[0].currentNumber = window.$('input[id="phone"]').val()
      },
      hideSearchResults () {
        this.find_list = []
      },
      GotoDate (event) {
        this.$root.bus.calendar.form_field_data.first_name = event.name
        this.$root.bus.calendar.form_field_data.last_name = event.last_name
        this.$root.bus.calendar.form_field_data.phone = event.phone
        this.$root.bus.calendar.form_field_data.email = event.email
        this.$root.bus.calendar.form_field_data.note = event.note
        this.find_list = []
      },
      searchCustomers (str) {
        if (str === '') {
          this.find_list = []
          return
        }
        this.$api.users.app.search(`${str}&is_customers=true`).then(response => {
          this.find_list = response.body.results
        }, response => {
        })
      },
      cancelAppt () {
        this.$api.calendar.cancel({id: this.$root.bus.calendar.form_field_data.id}).then(response => {
          this.showForm = false
          this.deleteCalendar()
        }, response => {
        })
      },
      rescheduleFunc () {
        this.reschedule = true
      },
      confirmation () {
        if (!this.cancelBtn) {
          this.cancelBtn = true
        } else {
          this.cancelBtn = false
        }
      },
      searchUserForm () {
        this.$root.bus.calendar.search_user_popup_form = true
      },
      fetchProviders () {
        this.$api.calendar.getProviders().then(response => {
          this.error = false
          this.$root.bus.calendar.form_field_data.provider_list = response.body
          if (response.body && response.body.length > 0) {
            this.$root.bus.calendar.form_field_data.provider_choice = response.body[0].id
          }
        }, response => {
        })
      },
      fetchServices () {
        this.$api.services.getAllServices().then(response => {
          this.error = false
          this.$root.bus.calendar.form_field_data.service_list = response.body
        }, response => {
        })
      },
      deleteCalendar () {
        this.$api.calendar.deleteCalendar(this.$root.bus.calendar.form_field_data.id).then(response => {
          this.cleanErrors()
          this.showForm = false
          this.clearForm()
          this.$emit('fetchCalendarEvents')
        }, response => {

        })
      },
      validateForm () {
        this.cleanErrors()
        // remove any previously set errors from api
        this.$refs.modal.$emit('apiErrors', {})
        // when submit button is clicked, trigger call to validate all component validations
        // if all of them are valid, Then only we will submit the form
        this.$refs.modal.$emit('validateAll')
        if (!this.$root.bus.calendar.form_field_data.service_choice) {
          this.$root.bus.calendar.form_field_error.service_error = true
        }
        for (let inpChild of this.$refs.modal.$children) {
          // if any of the input has error, halt form submission
          if (inpChild.hasDanger) return
        }
        this.saveCalendar()
      },

      saveCalendar () {
        let obj = {
          'provider_id': this.$root.bus.calendar.form_field_data.provider_choice,
          'service_id': this.$root.bus.calendar.form_field_data.service_choice,
          'start_date': this.$root.bus.calendar.form_field_data.start_date,
          'start_time': this.$root.bus.calendar.form_field_data.start_time,
          'end_time': this.$root.bus.calendar.form_field_data.end_time,
          'end_date': this.$root.bus.calendar.form_field_data.end_date,
          'first_name': this.$root.bus.calendar.form_field_data.first_name,
          'last_name': this.$root.bus.calendar.form_field_data.last_name,
          'email': this.$root.bus.calendar.form_field_data.email,
          'phone': this.$root.bus.calendar.form_field_data.phone,
          'mobile': this.$root.bus.calendar.form_field_data.mobile,
          'address': this.$root.bus.calendar.form_field_data.address,
          'city': this.$root.bus.calendar.form_field_data.city,
          'zip_code': this.$root.bus.calendar.form_field_data.zip_code,
          'note': this.$root.bus.calendar.form_field_data.note,
        }

        // send id when editing form
        if (this.$root.bus.calendar.edit_form) {
          obj.id = this.$root.bus.calendar.form_field_data.id
        }

        this.$api.calendar.saveCalendar(obj).then(response => {
          this.cleanErrors()
          this.showForm = false
          this.clearForm()
          this.$emit('fetchCalendarEvents')
        }, response => {
          this.cleanErrors()
          this.$root.bus.calendar.form_field_error.service_error = response.body.service_id
          this.$root.bus.calendar.form_field_error.first_name_error = response.body.first_name
          this.$root.bus.calendar.form_field_error.start_date_error = response.body.start_date
          this.$root.bus.calendar.form_field_error.start_time_error = response.body.start_time
          this.$root.bus.calendar.form_field_error.end_time_error = response.body.end_time
          this.$root.bus.calendar.form_field_error.end_date_error = response.body.end_date
          this.$root.bus.calendar.form_field_error.email_error = response.body.email
          this.$root.bus.calendar.form_non_field_errors = response.body.non_field_errors[0]
        })
      },
      cleanErrors () {
        this.$root.bus.calendar.form_field_error.service_error = null
        this.$root.bus.calendar.form_field_error.first_name_error = null
        this.$root.bus.calendar.form_field_error.start_date_error = null
        this.$root.bus.calendar.form_field_error.start_time_error = null
        this.$root.bus.calendar.form_field_error.end_time_error = null
        this.$root.bus.calendar.form_field_error.end_date_error = null
        this.$root.bus.calendar.form_field_error.email_error = null
        this.$root.bus.calendar.form_non_field_errors = null
      },
      clearForm () {
        this.$root.bus.calendar.form_field_data.provider_choice = null
        this.$root.bus.calendar.form_field_data.service_choice = null
        this.$root.bus.calendar.form_field_data.start_date = null
        this.$root.bus.calendar.form_field_data.start_time = null
        this.$root.bus.calendar.form_field_data.end_time = null
        this.$root.bus.calendar.form_field_data.end_date = null
        this.$root.bus.calendar.form_field_data.selected_calendar_data = null
        this.$root.bus.calendar.form_field_data.id = null
        this.$root.bus.calendar.form_field_data.first_name = null
        this.$root.bus.calendar.form_field_data.address = null
        this.$root.bus.calendar.form_field_data.last_name = null
        this.$root.bus.calendar.form_field_data.city = null
        this.$root.bus.calendar.form_field_data.phone = null
        this.$root.bus.calendar.form_field_data.mobile = null
        this.$root.bus.calendar.form_field_data.email = null
        this.$root.bus.calendar.form_field_data.zip_code = null
        this.$root.bus.calendar.form_field_data.note = null
      },
      initStartDate () {
        let _this = this
        this.start_date_component = flatpickr('#start_date',
          {
            dateFormat: 'm.d.Y',
            onChange: function (selectedDates, dateStr, instance) {
              _this.$root.bus.calendar.form_field_data.end_date = dateStr
            },
          }
        )
      },
      parseInputDateTime (stDate, stTime) {
        let date = stDate.split('.')
        let month = parseInt(date[0]) - 1
        let time = stTime.split(':')
        let timePt = time[1].split(' ')
        let year = date[2]
        let day = date[1]
        let hour = time[0]
        let mint = timePt[0]
        if (timePt[1] === 'PM') {
          hour = parseInt(hour) + 12
        }
        return new Date(year, month, day, hour, mint)
      },
      changeAppointmentType () {
        this.updateCalendarEndTime(this.parseInputDateTime(this.$root.bus.calendar.form_field_data.start_date, this.$root.bus.calendar.form_field_data.start_time))
      },
      get_service_duration (serviceId) {
        let calDuration = 0
        this.$root.bus.calendar.form_field_data.service_list.forEach(function (service) {
          if (service.id === serviceId) {
            calDuration = service.duration
          }
        })
        return calDuration
      },
      updateCalendarEndTime (selectedDate) {
        let duration = 30
        if (this.$root.bus.calendar.form_field_data.service_choice !== null) {
          duration = this.get_service_duration(this.$root.bus.calendar.form_field_data.service_choice)
        }
        this.$root.bus.calendar.form_field_data.end_time = this.$moment(selectedDate.setMinutes(selectedDate.getMinutes() + duration)).format('h:mm A')
      },
      initStartTime () {
        let _this = this
        this.start_time_component = flatpickr('#start_time', {
          enableTime: true,
          noCalendar: true,
          time_24hr: false,
          dateFormat: 'h:i K',
          defaultHour: 12,
          defaultMinute: 0,
          onChange: function (selectedDates, dateStr, instance) {
            _this.updateCalendarEndTime(selectedDates[0])
          },
        })
      },
    },
  }
</script>
