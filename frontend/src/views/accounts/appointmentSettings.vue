<template>
  <div>
    <user-form v-on:fetchAdmins="fetchAdmins"/>
    <h4>Appointment settings</h4>
    <inp id="appointment_interval" v-model="$root.bus.info.appointment_interval"
         label="Time interval between appointments in minutes"></inp>
    <!--<label>Select US TimeZone</label>-->
    <!--<us-time-zone-drop-down v-on:change="onTZChange" class="tzinfo" style=""></us-time-zone-drop-down>-->
    <!--<ui-switch type="3d" variant="primary" label="Switch to provider account"-->
    <!--v-model="$root.bus.info.is_provider"/>-->
    <button @click="$emit('savePersonalInfo')" type="button" class="btn btn-primary">
      Save
    </button>
    <b-btn variant="outline-success" v-if="this.$root.bus.is_provider" @click="openUserAccount">
      <span v-if="!hasAdmin"><i class="fa fa-file-o" aria-hidden="true"></i> Create </span>
      <span v-else><i class="fa fa-wrench" aria-hidden="true"></i> Update </span>
      Admin Account
    </b-btn>
    <button v-if="enabledGoogleApi" class="btn btn-danger float-right" @click="revokeGoogleAuth">
      <i class="fa fa-google-plus" aria-hidden="true"></i>
      Revoke Google Calendar Integration
    </button>
    <button v-else @click="getGoogleAuth" class="btn btn-success float-right">
      <i class="fa fa-google-plus" aria-hidden="true"></i>
      Enable Google Calendar Integration
    </button>
  </div>
</template>

<script>
  import Inp from '../../components/class/Inp.vue'
  import UserForm from '../../components/forms/UserForm.vue'
  // import UsTimeZoneDropDown from '../../components/class/UsTimeZonesDropDown.vue'

  export default {
    name: 'appointment-settings',
    components: {
      Inp,
      UserForm,
      // UsTimeZoneDropDown,
    },
    mounted: function () {
      this.fetchAdmins()
    },
    created: function () {
      this.$root.bus.checkLogin()
    },
    data () {
      return {
        hasAdmin: false,
        adminFormData: null,
      }
    },
    computed: {
      enabledGoogleApi () {
        return this.$root.bus.info.enabled_google_api
      },
    },
    methods: {
      // onTZChange (data) {
      //   console.log(data)
      //   this.$root.bus.info.timezone = data.timezone
      // },
      openUserAccount () {
        this.$emit('updateUserInfo', this.adminFormData)
      },
      fetchAdmins () {
        this.$api.users.getAllAdmins('').then(response => {
          this.$root.bus.users.admin.admin_list = response.body.results
          this.$root.bus.users.admin.next = response.body.next
          this.$root.bus.users.admin.previous = response.body.previous
          this.$root.bus.users.admin.count = response.body.count
          if (response.body.count > 0) {
            this.hasAdmin = true
            this.adminFormData = response.body.results[0]
          }
        }, response => {
          this.$notify({
            group: 'app',
            text: 'Failed to get Admin Account detail',
            type: 'error',
          })
        })
      },
      revokeGoogleAuth () {
        this.$api.users.app.revokeGoogleCredentials().then(
          () => {
            this.$root.bus.info.enabled_google_api = false
            this.$notySuccess('Google Account Integration removed.')
          },
          () => {
            this.$notify({
              group: 'app',
              text: 'Failed to revoke Google API integration',
              type: 'error',
            })
          }
        )
      },
      getGoogleAuth () {
        let authWindow = window.open(
          'about:blank', 'Google Auth',
          'toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes'
        )
        let self = this
        // to track success call
        window.addEventListener('message', function (event) {
          if (event.data === 'authSuccess') {
            self.$root.bus.info.enabled_google_api = true
            self.$notySuccess('Google Account integrated successfully')
          }
        }, true)
        this.$api.users.app.getGAuthUrl()
          .then((response) => {
            authWindow.location.href = response.body.url
          }, () => {
            authWindow.close()
            // things to do when sign-in fails
            this.$notify({group: 'app', text: 'Failed to enable Google API Integration', type: 'error'})
          })
      },
    },
  }
</script>
<style scoped>
  .tzinfo{
    margin-left: 0.5px;
    border: 1px solid #c2cfd6;
    margin-bottom: 17px;
  }
</style>
<style>
  .multiselect__option--highlight {
    background: rgb(0, 105, 255);
    outline: none;
    color: #fff;
  }
  .multiselect__option--selected.multiselect__option--highlight {
    background: gray;
    color: #fff;
  }
  .multiselect__content-wrapper{
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
  }
</style>