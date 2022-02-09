<template>
  <div class="sidebar">
    <nav class="sidebar-nav">
      <div class="calendar-wrapper">
        <mini-calendar></mini-calendar>
      </div>
      <ul class="nav">
        <li class="nav-item">
          <router-link :to="'/calendar'" class="nav-link">
            <i class="icon-calendar"></i> Calendar
          </router-link>
          <router-link :to="'/messages'" class="nav-link">
            <i class="icon-bubbles"></i> Messenger
          </router-link>
          <router-link :to="'/customers'" class="nav-link">
            <i class="icon-earphones-alt"></i> Patients
          </router-link>
          <!--<router-link v-if="this.$root.bus.is_admin" :to="'/services'" class="nav-link">-->
            <!--<i class="icon-bubble"></i> Services-->
          <!--</router-link>-->
          <router-link :to="'/settings'" class="nav-link">
            <i class="icon-envelope"></i> Email Settings
          </router-link>
          <router-link v-if="this.$root.bus.is_admin" :to="'/accounts'" class="nav-link">
            <i class="icon-user"></i> Account Settings
          </router-link>
          <router-link v-if="this.$root.bus.is_admin" :to="'/ratings'" class="nav-link">
            <i class="icon-star"></i> Email Surveys
          </router-link>
          <router-link v-if="this.$root.bus.is_admin" :to="'/links'" class="nav-link">
            <i class="icon-notebook"></i> Scheduling page
          </router-link>
          <router-link v-if="this.$root.bus.is_admin" :to="'/customer-booked-script'" class="nav-link">
            <i class="icon-bubble"></i>Booked Script
          </router-link>
          <!-- <div class="nav-link" @click='showphone()'>
            <i class="icon-phone"></i>Call
          </div> -->
         <!--  <router-link :to="'/voicemails'" class="nav-link">
            <i class="icon-folder-alt"></i>Voice Mails
            <span class="notify-bubble" style="display: inline-block;" v-show="voicemails > 0">{{voicemails}}</span>
          </router-link> -->
          <router-link :to="'/import'" class="nav-link">
            <i class="icon-plus"></i> Import
          </router-link>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
  import MiniCalendar from './class/MiniCalendar'

  export default {
    components: {
      MiniCalendar,
    },
    name: 'sidebar',
    methods: {
      handleClick (e) {
        e.preventDefault()
        e.target.parentElement.classList.toggle('open')
      },
    },
    data () {
      return {
        voicemails: 0,
      }
    },
    created () {
      var component = this
      var channel = this.$pusher.subscribe('bookedfusion')
      channel.bind('voicemail-created', function (data) {
        if (data.generalsettings_id === component.$root.bus.info.generalsettings_id) {
          component.voicemails++
        }
      })
    },
  }
</script>

<style lang="css">
  .nav-link {
    cursor: pointer;
  }

  .notify-bubble {
    position: relative;
    top: -10px;
    right: 6px;
    padding: 2px 5px 2px 6px;
    background-color: #ef4d40;
    color: white;
    font-size: 0.65em;
    border-radius: 50%;
    -webkit-box-shadow: 1px 1px 1px grey;
    box-shadow: 1px 1px 1px #8080808f;
    display: none;
  }

</style>
