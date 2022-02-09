<template>
  <div class="row">
    <div class="col-sm-12">
      <h2>Initial Confirmation Email</h2>
        <hr>
        <p>
          An Initial Confirmation email is sent to you and your patients immediately after an appointment is scheduled.
        </p>
        <br>
      <div class="form-group">
        <label for="email_subject">E-mail Subject</label>
        <input class="form-control" v-model="$root.bus.settings.initial_settings.item.email_subject"
               id="email_subject" required type="text">
      </div>
      <div class="form-group">
        <trumbowyg v-model="$root.bus.settings.initial_settings.item.email_body"></trumbowyg>
      </div>
      <button @click="initial_settings_save" type="button" class="btn btn-primary">Save template</button>
      <button type="button" class="btn btn-primary"
              @click="showPreview">
        Preview
      </button>
    </div>
  </div>
</template>
<script>
  export default {
    mounted () {
      this.initial_settings_load()
    },
    methods: {
      initial_settings_load () {
        this.$api.settings.getInitialSettings().then(response => {
          this.$root.bus.settings.initial_settings.item = response.body[0]
        }, response => {
        })
      },
      initial_settings_save () {
        this.$api.settings.app.save_initial(
          this.$root.bus.settings.initial_settings.item.id, this.$root.bus.settings.initial_settings.item
        ).then(response => {
          this.$notySuccess()
        }, response => {
          this.$notify({group: 'app', text: 'Failed to save settings', type: 'error'})
        })
      },
      showPreview () {
        this.$emit('preview', 'E-mail Confirmation', this.$root.bus.settings.reminder_settings.item.email_body)
      },
    },
  }
</script>
