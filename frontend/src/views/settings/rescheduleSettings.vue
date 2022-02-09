<template>
  <div>
    <div class="row">
      <div class="col-sm-12">
        <h2>Rescheduling E-mail</h2><hr>
        <p>A Rescheduling e-mail is sent to you and your patients immediately after an appointment has been
          rescheduled.</p>
        
      </div>
    </div>
    <div class="row">
      <div class="col-sm-12">
        <div class="form-group">
          <label for="email_subjectsecond">E-mail Subject</label>
          <input class="form-control" v-model="itemData.email_subject"
                 id="email_subjectsecond" required type="text">
        </div>
        <div class="form-group">
          <trumbowyg v-model="itemData.email_body"></trumbowyg>
        </div>
        <button @click="saveSettings" type="button" class="btn btn-primary">Save template</button>
        <button @click="showPreview" class="btn btn-primary">Preview</button>
      </div>
    </div>
  </div>
</template>

<script>
  import previewEmailMixin from './previewEmailMixin'

  export default {
    data () {
      return {
        previewTitle: 'Rescheduling Email',
        saveResourceFunc: this.$api.settings.app.saveReschedulingSettings,
        getResourceFunc: this.$api.settings.getReschedulingSettings,
      }
    },
    mixins: [previewEmailMixin],
    methods: {},
  }
</script>
