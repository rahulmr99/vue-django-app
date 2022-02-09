<template>
  <div class="animated fadeIn">
    <div class="container-fluid">
      <div class="row main-route">
        <div class="col-md-12">
          <b-tabs ref="tabs" card v-model="activeTabIndex">
            <!--company settings-->
            <!-- <b-tab title="General" v-if="this.$root.bus.is_admin">
              <general-settings></general-settings>
            </b-tab> -->
            <b-tab title="Initial Confirmation" v-if="this.$root.bus.is_admin">
              <init-settings @preview="showPreview"></init-settings>
            </b-tab>
            <b-tab title="Reminder" v-if="this.$root.bus.is_admin">
              <reminder-settings @preview="showPreview"></reminder-settings>
            </b-tab>
            <b-tab title="Cancellation" v-if="this.$root.bus.is_admin">
              <cancellation-settings @preview="showPreview"></cancellation-settings>
            </b-tab>
            <b-tab title="Rescheduling" v-if="this.$root.bus.is_admin">
              <reschedule-settings @preview="showPreview"></reschedule-settings>
            </b-tab>
            <!-- <b-tab title="Business Logic" v-if="this.$root.bus.is_admin">
              <user-working-plan ref="userWorkingPlan"></user-working-plan>
            </b-tab> -->
          </b-tabs>
        </div>
      </div>
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
  import generalSettings from './generalSettings.vue'
  import initSettings from './initSettings.vue'
  import reminderSettings from './reminderSettings.vue'
  import cancellationSettings from './cancellationSettings.vue'
  import rescheduleSettings from './rescheduleSettings.vue'
  import userWorkingPlan from '../../components/forms/UserWorkingPlanForm.vue'
  import rememberTabMixin from '../../components/mixins/rememberTabMixin'

  export default {
    name: 'settings',
    mixins: [rememberTabMixin],
    components: {
      generalSettings,
      initSettings,
      reminderSettings,
      userWorkingPlan,
      cancellationSettings,
      rescheduleSettings,
    },
    mounted: function () {
      if (this.$refs.userWorkingPlan) {
        this.$refs.userWorkingPlan.initForm(this.$root.bus.info.id)
      }
    },
    created: function () {
      this.$root.bus.checkLogin()
    },
    methods: {
      showPreview (title, html) {
        this.showTemplatePreview = true
        this.templatePreviewTitle = title
        this.templatePreviewContent = html
      },
    },
    data: function () {
      return {
        showTemplatePreview: false,
        templatePreviewTitle: '',
        templatePreviewContent: '',
      }
    },
  }
</script>
