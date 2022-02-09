<template>
  <div class="animated fadeIn">
    <div class="container-fluid">
      <b-card no-body>
        <b-tabs ref="tabs" card>
          <b-tab title="1-Click Email Surveys" v-if="this.$root.bus.is_admin" active>
            <rating-settings @preview="showPreview"></rating-settings>
          </b-tab>
          <b-tab title="Patient Experience Report">
            <ratings-results></ratings-results>
          </b-tab>
          <b-tab title="Real-Time Feedback">
            <div class="row">
              <div class="col-sm-12">
                <h2>Real-Time Feedback</h2>
                <hr>
                <p>
                  Real-time patient feedback enables you to understand the patient experience to reduce patient discharge and improve the patient experience.
                </p>
                <br>
              </div>
            </div>
            <feedbacks-table></feedbacks-table>
          </b-tab>
        </b-tabs>
      </b-card>
    </div>
    <!-- modal dialogues -->
    <b-modal v-model="showTemplatePreview" :title="templatePreviewTitle" size="lg" :hide-footer="true">
      <b-container fluid>
        <b-row>
          <div v-html="templatePreviewContent"></div>
        </b-row>
      </b-container>
    </b-modal>
  </div>
</template>

<script>
  import RatingsResults from './ratings/RatingsResults'
  import RatingSettings from './ratings/ratingSettings'
  import FeedbacksTable from './ratings/FeedbacksTable'

  export default {
    name: 'ratings',
    components: {
      RatingsResults,
      FeedbacksTable,
      RatingSettings,
    },
    data: function () {
      return {
        showTemplatePreview: false,
        templatePreviewTitle: '',
        templatePreviewContent: '',
      }
    },
    methods: {
      showPreview (title, html) {
        this.showTemplatePreview = true
        this.templatePreviewTitle = title
        this.templatePreviewContent = html
      },
    },
  }
</script>

<style>
  .modal-content {
    margin-top: 50px;
  }
</style>
