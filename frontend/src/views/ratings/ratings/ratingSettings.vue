<template>
  <div>
      <div class="row">
      <div class="col-sm-12">
        <h2>1-Click Email Surveys</h2>
        <hr>
        <p>
          An email is sent to patients (after their appointment) based on the time specified below to drive more 5 star reviews while intercepting negative reviews.
        </p>
        <br>
      </div>
    </div>

    <row>
      <label class="switch switch-text switch-primary">
        <input v-model="form.send" checked="" class="switch-input"
               type="checkbox">
        <span class="switch-label" data-off="Off" data-on="On"></span>
        <span class="switch-handle"></span>
      </label>
      <label>Enable Ratings Feature</label>
    </row>
    
  

    <inp type="number"
         id="send_time"
         label="Hours after their appointment"
         :required="true"
         v-model="form.send_time"
         placeholder="Enter in hours"
    ></inp>

    <!-- review links -->
    <inp type="url"
         label="Link to Google Review"
         id="google_rateus_link"
         :required="true"
         placeholder="http://bookedfusion.com"
         v-model="form.google_rateus_link"
    ></inp>
    <inp type="url"
         label="Link to Yelp Review"
         :required="true"
         id="'yelp_rateus_link"
         v-model="form.yelp_rateus_link"
         placeholder="http://yelp.com"
    ></inp>
    <inp
      type="text"
      label="Email Subject "
      :required="true"
      id="email_subject"
      v-model="form.email_subject"
      placeholder="Enter Email subject"
    >
    </inp>
    <row>
      <trumbowyg v-model="form.email_body"></trumbowyg>
    </row>

    <!-- save button -->
    <row>
      <button @click="onFormSubmit()" type="button" class="btn btn-primary">Save changes</button>
      
    </row>
  </div>
</template>

<script>
  import Row from '../../../components/class/Row'
  import Inp from '../../../components/class/Inp'
  import FormMixin from '../../../components/mixins/formsMixin'

  export default {
    name: 'rating_settings',
    components: {
      Row,
      Inp,
    },
    mixins: [FormMixin],
    data () {
      return {
        form: {
          send: '',
          send_time: '',
          google_rateus_link: '',
          yelp_rateus_link: '',
          email_subject: '',
          email_body: '',
        },
      }
    },
    mounted: function () {
      this.loadRatingSettings()
    },
    methods: {
      // fetch settings and assign to variables
      loadRatingSettings () {
        this.$api.settings.getRatingsSettings().then(response => {
          this.form = response.body[0]
        }, response => {
        })
      },
      // save settings
      onFormValidationSuccess () {
        this.$api.settings.app.save_ratings(
          this.form.id, this.form
        ).then(
          //  success callback
          response => {
            this.$notySuccess()
          },
          this.onFormApiSaveFailed // error callback
        )
      },
    },
  }
</script>
