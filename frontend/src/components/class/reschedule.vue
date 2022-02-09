<template>
    <div class="row mt20">
    <div class="col-sm-2"></div>

        <div class="col-sm-5 ccc pb20">
            <reschedule-calendar></reschedule-calendar>
            <button class="btn btn-default mr10 " @click="goBack()" >Back</button>
            <button type="button" class="btn btn-primary mt20 mb20" @click="reschedule()" >Reschedule</button>
            
        </div>
        <div class="col-sm-5 pb20">
            <div class="avb-tym">
                <div v-for="item in options">
                        <div>
                            <span v-for="time in item.date">
                                <input type="radio" name="time[]" :id="time.key" v-model="dateTime" :value="time.datetime">
                                <label :id="`lbl_${time.key}`" :for="time.key">{{ time.time }}</label><br>
                            </span>
                        </div>
                </div>
            </div>
        </div>
    
    </div>
</template>

<style>
.mr10 {margin-right:10px;}
.ml20 { margin-left:20px;}
.mt20 { margin-top:20px;}
.mb20 { margin-bottom:20px;}

 .ccc .flatpickr-calendar {    box-shadow: none;}

.avb-tym {    text-align: center;
    border: 1px solid #cecece;
    padding: 10px;
    height: 238px;
    overflow-y: scroll;
    width: 200px;}
</style>
<script>

import rescheduleCalendar from './rescheduleCalendar'
import Moment from 'moment'

export default {
  name: 'schedulerForm',
  components: {
    rescheduleCalendar,
  },
  data: function () {
    return {
      dateTime: null,
      options: null,
    }
  },
  methods: {
    goBack () {
      this.$parent.$parent.reschedule = false
    },
    reschedule () {
      this.$root.bus.calendar.form_field_data.start_time = Moment((this.dateTime).split('.')[0]).format('hh:mm A')
      let obj = {
        'id': this.$root.bus.calendar.form_field_data.id,
        'provider_id': this.$root.bus.calendar.form_field_data.provider_choice,
        'service_id': this.$root.bus.calendar.form_field_data.service_choice,
        'start_date': this.$root.bus.calendar.form_field_data.start_date,
        'start_time': this.$root.bus.calendar.form_field_data.start_time,
        // 'end_time': this.$root.bus.calendar.form_field_data.end_time,
        // 'end_date': this.$root.bus.calendar.form_field_data.end_date,
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
      this.$api.calendar.update(obj).then(response => {
        this.dateTime = null
        this.options = null
        this.showForm = false
        this.$parent.$parent.showForm = false
        this.$parent.$parent.reschedule = false
        this.$parent.$parent.$parent.fetchCalendarEvents()
      }, response => {
        console.log(response)
      })
    },
  },
}
</script>