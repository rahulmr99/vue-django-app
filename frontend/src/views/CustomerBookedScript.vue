<template>
  <div class="animated fadeIn">
    <br>
    <div class="row">
      <div class="col-sm-12">
        <h2>Boost Your Appointments With Social Proof</h2>
        <hr>
        <p>
          Adds notifications to the bottom of your website page showing recent bookings. When visitors see that others are coming to your practice… they are statistically more likely to book as well. Simply paste the small BookedFusion Generated snippet of HTML tracking code onto your website.
        </p>
        <br>
      </div>
    </div>
      <p class="card-text">
        Paste the following script in your <code>body</code> section
      </p>
      <b-card sub-title="Embeddable Script">
      <textarea rows="4" cols="80" readonly>
        {{embedLink}}
      </textarea>
      </b-card>
    </b-card>
  </div>
</template>
<script>
  export default {
    name: 'customerBookedScript',
    data () {
      return {
        embedLink:
          `<script>!function(){function b(){var a=(new Date).getTime(),b=document.createElement('script');b.type='text/javascript',b.async=!0,b.src='https://secure.bookedfusion.com/embedded/script/popup/${this.$root.bus.info.generalsettings_id}';var c=document.getElementsByTagName('script')[0];c.parentNode.insertBefore(b,c);}
var a=window;a.attachEvent?a.attachEvent('onload',b):a.addEventListener('load',b,!1)}()<\/script>`, // eslint-disable-line no-useless-escape
      }
    },
    computed: {
    },
  }
</script>

<style scoped="true">
  .card {
    padding: 2vh
  }
</style>
