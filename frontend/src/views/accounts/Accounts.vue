<template>
  <div class="animated fadeIn">
    <div class="container-fluid">
      <div class="row main-route">
        <div class="col-md-12">
          <b-card no-body>
            <b-tabs ref="tabs" card v-model="activeTabIndex">
              <b-tab title="Account" active>
                <account-settings ref="accountSettingsTab" @savePersonalInfo="savePersonalInfo"/>
              </b-tab>
              <b-tab title="Appointment Settings">
                <appointment-settings @savePersonalInfo="savePersonalInfo"/>
              </b-tab>
              <!-- <b-tab title="Voice-Bot Settings">
                <voicebot-settings/>
              </b-tab> -->
              <b-tab title="Services">
                <services/>
              </b-tab>
              <b-tab title="Business Logic" v-if="this.$root.bus.is_admin">
                <user-working-plan ref="userWorkingPlan"></user-working-plan>
              </b-tab>
              <b-tab title="Manage Your Subscription">
                <subscription-check></subscription-check>
              </b-tab>
            </b-tabs>
          </b-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import accountSettings from './accountSettings.vue'
  import appointmentSettings from './appointmentSettings'
  import services from './services'
  // import voicebotSettings from './voicebotSettings'
  import rememberTabMixin from '../../components/mixins/rememberTabMixin'
  import userWorkingPlan from '../../components/forms/UserWorkingPlanForm.vue'
  import SubscriptionCheck from '../../components/class/SubscriptionCheck.vue'

  export default {
    components: {
      accountSettings,
      appointmentSettings,
      services,
      // voicebotSettings,
      userWorkingPlan,
      SubscriptionCheck,
    },
    mixins: [rememberTabMixin],
    name: 'accounts',
    created: function () {
      this.$root.bus.checkLogin()
    },
    data () {
      return {
        hasAdmin: false,
        userDetail: {},
      }
    },
    mounted: function () {
      this.$refs.userWorkingPlan.initForm(this.$root.bus.info.id)
    },
    methods: {
      savePersonalInfo () {
        let emails = this.$root.bus.info.additionalemails
        if ((/[\w.+-]+@[\w.+-]+\.[a-zA-Z0-9]{2,4}(,\s*)*/ig.test(emails))) {
          emails = emails.split(',')
          this.$root.bus.info.email1 = emails[0]
          this.$root.bus.info.email2 = emails[1]
        }
        delete this.$root.bus.info.additionalemails
        this.$api.users.app.update(this.$root.bus.info.id, this.$root.bus.info).then(response => {
          this.$notySuccess('Account updated successfully.')
        }, response => {
          this.$notify({
            group: 'app',
            text: 'Failed to update account.',
            type: 'error',
          })
        })
      },
    },
  }
</script>

<style scoped>

</style>
