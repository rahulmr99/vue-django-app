<template>
  <div class="animated fadeIn">
    <!--<b-card title="Schedule Page Link">-->
      <!--<p class="card-text">-->
        <!--Here is the link to your personal booking page.-->
      <!--</p>-->
      <!--<a target="_blank" :href="schedulePageLink" class="card-link">Booking Page</a>-->
    <!--</b-card>-->
    <b-card title="24/7 Online Self-Scheduling Anytime, Anywhere">
      <p class="card-text">
        Paste in the snippet of code on your webpage to drive more patients from your site
      </p>
      <b-card sub-title="Insert the script below wherever you want the booking button to appear on your webpage">
        <v-code>{{styleLink}}
          {{altBtnLink}}
          {{embedLink}}
        </v-code>
      </b-card>
      <b-card title="Booking Links"
              sub-title="Now your patients can book directly from an article or anywhere on your site by a link without going to another page">
        <v-code>{{styleLink}}
          {{anchorLink}}
          {{embedLink}}
        </v-code>
      </b-card>
    </b-card>
    <!--<b-card title="Twilio call responder webhook">-->
      <!--<p class="card-text">-->
        <!--Copy the below link and configure it as the webhook for your twilio number.-->
      <!--</p>-->
      <!--<v-code>{{twilioWebhook}}</v-code>-->
    <!--</b-card>-->
    <!--<b-card title="Book by Text Messaging">-->
      <!--<p class="card-text">-->
        <!--Copy the below link and configure it as the SMS webhook for your twilio number.-->
      <!--</p>-->
      <!--<v-code>{{lexbotSMSWebhook}}</v-code>-->
    <!--</b-card>-->
    <!--<b-card title="Book by Phone">-->
      <!--<p class="card-text">-->
        <!--Copy the below link and configure it as the Voice webhook for your twilio number.-->
      <!--</p>-->
      <!--<v-code>{{lexbotVoiceWebhook}}</v-code>-->
    <!--</b-card>-->
  </div>
</template>
<script>
  import VCode from '../components/class/VCode'

  const API_BASE_URL = 'https://secure.bookedfusion.com'
  export default {
    components: {VCode},
    name: 'scheduleLinksPage',
    data () {
      return {
        lexbotSMSWebhook: `${API_BASE_URL}/bot/sms/${this.$root.bus.info.generalsettings_id}/`,
        lexbotVoiceWebhook: `${API_BASE_URL}/bot/voice/${this.$root.bus.info.generalsettings_id}/`,
        twilioWebhook: `${API_BASE_URL}/ivrs/caller-vr/${this.$root.bus.info.generalsettings_id}/`,
        anchorLink: `<a href="${API_BASE_URL}/embedded/">Schedule Appointment</a>`,
        styleLink: `<link rel="stylesheet" href="${API_BASE_URL}/static/embed/css/main.css">`,
        btnLink: '<button id="easy-booking-btn-styled">Schedule Appointment</button>',
        altBtnLink: `<a href="${API_BASE_URL}/embedded/"
                  style="background: #5fb8b9;color: #fff; padding: 8px 12px; border: 0px;\
-webkit-box-shadow: 0 -2px 0 rgba(0,0,0,0.15) inset;-moz-box-shadow: 0 -2px 0 rgba(0,0,0,0.15) inset;\
box-shadow: 0 -2px 0 rgba(0,0,0,0.15) inset;border-radius: 4px; text-decoration: none; display: inline-block;">
            Schedule Appointment
          </a>`,
        embedLink: `<script src="${API_BASE_URL}/embedded/script/${this.$root.bus.info.generalsettings_id}"><\/script>`, // eslint-disable-line no-useless-escape
      }
    },
    computed: {
      schedulePageLink () {
        return `https://schedule.bookedfusion.com/#/comp/${this.$root.bus.info.generalsettings_id}`
      },
    },
  }
</script>
