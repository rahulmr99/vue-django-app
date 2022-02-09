<template>
  <div>
    <div class="row">
      <div class="col-sm-12">
        <h3>My Account</h3>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-6">
        <!--<div class="form-group required">-->
        <!--<label for="username_admin">Username</label>-->
        <!--<input class="form-control" id="username_admin"-->
        <!--placeholder="Enter email"-->
        <!--v-model="$root.bus.info.email"-->
        <!--type="text">-->
        <!--</div>-->
        <div class="form-group required">
          <label for="first_name_admin">First name</label>
          <input class="form-control" id="first_name_admin"
                 placeholder="First Name"
                 v-model="$root.bus.info.name"
                 type="text">
        </div>
        <div class="form-group required">
          <label for="last_name_admin">Last name</label>
          <input class="form-control" id="last_name_admin"
                 placeholder="Last Name"
                 v-model="$root.bus.info.last_name"
                 type="text">
        </div>
        <div class="form-group required">
          <label for="phone_number_admin">Mobile Phone</label>
          <input class="form-control" id="phone_number_admin"
                 placeholder="Enter Mobile number"
                 v-model="$root.bus.info.phone"
                 type="text">
        </div>
	     <div class="form-group required">
          <label for="timezone_admin">Timezone</label>
          <select class="form-control" v-model="$root.bus.info.timezone">
                <option disabled value="">Please select one</option>
                <option value="US/Alaska" >Alaska</option>
                <option value="US/Arizona" >Arizona</option>
                <option value="US/Central" >Central</option>
                <option value="EST" >Eastern</option>
                <option value="US/Hawaii" >Hawaii</option>
                <option value="US/Mountain" >Mountain</option>
                <option value="US/Pacific" >Pacific</option>
                
            </select>
        </div>
      </div>
      <div class="col-sm-6">
        <div class="form-group required">
          <label for="first_name">Company Name</label>
          <input class="form-control" id="company_name" required
                 placeholder="Enter company name"
                 v-model="$root.bus.settings.general_settings.item.company_name"
                 type="text">
        </div>
        <div class="form-group required"
             v-bind:class="[{'has-danger': $root.bus.settings.general_settings.error_email }]">
          <label for="first_name">Company Email</label>
          <input class="form-control" id="company_email" required
                 placeholder="Enter email"
                 v-model="$root.bus.settings.general_settings.item.company_email"
                 type="text">
        </div>
        <div class="form-group">
          <label for="first_name">Booked Fusion Number</label>
          <input class="form-control" id="booked_fusion_number"
                 placeholder="Booked Fusion Number"
                 v-model="$root.bus.settings.general_settings.item.booked_fusion_number"
                 type="text">
        </div>


      </div>
    </div>
    <div class="row">
      <div class="col-sm-12">
        <!-- <div class="form-group">
          <label for="description">If anyone else needs to get notifications when appointment is booked, rescheduled, and canceled, just put their email in field below. Just remember to put a comma ( , ) between each one.</label>
          <input type="text" v-model="$root.bus.info.additionalemails" class="form-control" id="description"
                    placeholder="ex. bookedfusion@example.com,bookedfusion1@example1.com" maxlength="255"/>
        </div> -->
        <ui-switch type="3d" variant="primary" :value="true" label="Receive notification"/>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-12">
        <button @click="personal_info_save" type="button" class="btn btn-primary">

          Save
        </button>
        <button @click="openPasswordForm" type="button" class="btn btn-outline-warning">
          <i class="fa fa-lock" aria-hidden="true"></i>
          Update Password
        </button>
      </div>
    </div>
    <modal title="Change Password" v-model="showPasswordForm" @ok="new_password_save" effect="zoom" ref="modal">
      <div class="form-group required">
        <label for="password1_admin">Password</label>
        <input class="form-control" id="password1_admin"
               placeholder="Enter a new password"
               v-model="$root.bus.settings.credentials_settings.password1"
               type="password">
      </div>
      <div class="form-group required">
        <label for="password2_admin">Retype Password</label>
        <input class="form-control" id="password2_admin"
               placeholder="Retype the new password"
               v-model="$root.bus.settings.credentials_settings.password2"
               type="password">
      </div>
      <!--<button @click="new_password_save" type="button" class="btn btn-primary">Update</button>-->
    </modal>
  </div>
</template>

<script>
  import UiSwitch from '../../components/class/UiSwitch.vue'
  import Inp from '../../components/class/Inp.vue'
  import modal from '../../components/class/ModalFormClass.vue'

  export default {
    components: {
      UiSwitch,
      Inp,
      modal,
    },
    data () {
      return {
        showPasswordForm: false,
      }
    },
    mounted: function () {
      this.genral_settings_load()
    },
    methods: {
      genral_settings_load () {
        this.$api.settings.app.getGeneralSettings(this.$root.bus.info.generalsettings_id).then(response => {
          this.$root.bus.settings.general_settings.item = response.body
        }, response => {
        })
      },
      genral_settings_save () {
        this.$api.settings.app.save_general(this.$root.bus.settings.general_settings.item.id, this.$root.bus.settings.general_settings.item).then(response => {
          this.$root.bus.settings.general_settings.error_link = null
          this.$root.bus.settings.general_settings.error_email = null
          this.$notySuccess()
        }, response => {
          this.$root.bus.settings.general_settings.error_link = response.body.company_link
          this.$root.bus.settings.general_settings.error_email = response.body.company_email
          this.$notify({group: 'app', text: 'Failed to update settings', type: 'error'})
        })
      },
      openPasswordForm () {
        this.showPasswordForm = true
      },
      personal_info_save () {
        this.$emit('savePersonalInfo')
        this.genral_settings_save()
      },
      new_password_save () {
        const obj = {
          'email': this.$root.bus.info.email,
          'password1': this.$root.bus.settings.credentials_settings.password1,
          'password2': this.$root.bus.settings.credentials_settings.password2,
        }
        this.$api.users.app.update_password(obj).then(response => {
          this.$root.bus.settings.credentials_settings.password1 = null
          this.$root.bus.settings.credentials_settings.password2 = null
        }, response => {
        })
        this.showPasswordForm = false
      },
    },
  }
</script>
