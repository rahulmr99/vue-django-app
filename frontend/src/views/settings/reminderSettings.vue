<template>
  <div>
    <div class="row">
      <div class="col-sm-12">
        <h2>E-mail Reminder</h2>
        <hr>
        <p>
          An email and text reminder is sent to patients (prior to their appointment) based on the time specified below to minimize no shows and late shows. The text in email subject field is what will be included in text reminder.
        </p>
        <br>
      </div>
    </div>
    <b-row>
      <b-col sm="12">
        <input v-model="$root.bus.settings.reminder_settings.item.send_time" class="form-control" id="hour"
               required type="number">
        <label for="hour">Hours before their appointment</label>
      </b-col>
    </b-row>
    <br>
    <div class="row">
      <div class="col-sm-12">
        <div class="form-group">
          <label for="email_subjectsecond">E-mail Subject</label>
          <input class="form-control" v-model="$root.bus.settings.reminder_settings.item.email_subject"
                 id="email_subjectsecond" required type="text">
        </div>
        <div class="form-group">
          <trumbowyg v-model="$root.bus.settings.reminder_settings.item.email_body"></trumbowyg>
        </div>
        <button @click="reminder_settings_save" type="button" class="btn btn-primary">Save template</button>
        <button @click="showPreview" class="btn btn-primary">Preview</button>
      </div>
    </div>
  </div>
</template>

<style>
  #hour{
    display: inline;
    width: 65px;
    margin-right: 10px;
  }
</style>
<script>
  /* eslint-disable camelcase */

  import UiSwitch from '../../components/class/UiSwitch.vue'

  export default {
    components: {
      UiSwitch,
    },
    mounted () {
      this.reminder_settings_load()
    },
    methods:
      {
        reminder_settings_load () {
          this.$api.settings.getReminderSettings().then(response => {
            this.$root.bus.settings.reminder_settings.item = response.body[0]
          }, response => {
          })
        },
        reminder_settings_save () {
          this.$api.settings.app.save_reminder(
            this.$root.bus.settings.reminder_settings.item.id,
            this.$root.bus.settings.reminder_settings.item
          ).then(response => {
            this.$notySuccess()
          }, response => {
            this.$notify({group: 'app', text: 'Failed to save settings', type: 'error'})
          })
        },
        showPreview () {
          this.$emit('preview', 'E-mail Reminder', this.$root.bus.settings.reminder_settings.item.email_body)
        },
      },
  }
</script>
