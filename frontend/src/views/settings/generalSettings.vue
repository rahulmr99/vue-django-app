<template>
  <div>
    <div class="row">
      <div class="col-sm-12">
        <div class="form-group">
          <label for="first_name">Company Name *</label>
          <input class="form-control" id="company_name" required
                 placeholder="Enter company name"
                 v-model="$root.bus.settings.general_settings.item.company_name"
                 type="text">
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-6">
        <div class="form-group"
             v-bind:class="[{'has-danger': $root.bus.settings.general_settings.error_email }]">
          <label for="first_name">Company Email *</label>
          <input class="form-control" id="company_email" required
                 placeholder="Enter email"
                 v-model="$root.bus.settings.general_settings.item.company_email"
                 type="text">
        </div>
      </div>
      <div class="col-sm-6">
        <div class="form-group"
             v-bind:class="[{'has-danger': $root.bus.settings.general_settings.error_link }]">
          <label for="last_name">Company Link *</label>
          <input class="form-control" id="company_link" required
                 placeholder="Enter url"
                 v-model="$root.bus.settings.general_settings.item.company_link"
                 type="text">
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-6">
        <div class="form-group">
          <label for="first_name">Google Analytics ID</label>
          <input class="form-control" id="first_name" required
                 placeholder="Enter id"
                 v-model="$root.bus.settings.general_settings.item.google_analytics_id"
                 type="text">
        </div>
      </div>
      <div class="col-sm-6">
        <div class="form-group">
          <label for="last_name">Date Format</label>
          <input class="form-control" id="last_name" required
                 placeholder="Enter date format"
                 v-model="$root.bus.settings.general_settings.item.date_format"
                 type="text">
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-12">
        <ui-switch type="3d" variant="primary" label="Enable CAPTCHA"
                   v-model="$root.bus.settings.general_settings.item.captcha"></ui-switch>
      </div>
      <div class="col-sm-12">
        <ui-switch type="3d" variant="primary" label="Enable Customer Notifications"
                   v-model="$root.bus.settings.general_settings.item.send_notification"></ui-switch>
      </div>
      <div class="col-sm-12">
        <div class="form-group">
          <button @click="genral_settings_save" type="button" class="btn btn-primary">Save changes</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import UiSwitch from '../../components/class/UiSwitch.vue'

  export default {
    name: 'generalSettingsForm',
    components: {
      UiSwitch,
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
    },
  }
</script>
