<template>
  <div class="dail-wrap">
    <div class="top-d">
      <button class="minimize" @click="mini()" v-show="!minimize"></button>
      <button class="maximize" @click="max()" v-show="minimize"></button>
      <button class="close-t" @click="close()"></button>

    </div>
    <div v-show="!incomingCall && !onPhone && !minimize" class="m0">
      <div>
        <h4>
          Dial number
        </h4>
        <div class="row m0">
          <div class="col-xs-4">
            <flags-dropdown v-on:change="optionCountrySelected"></flags-dropdown>
          </div>
          <div class="col-xs-8 p-relative">
            <input type="tel" class="dail-text form-control" v-model="currentNumber" placeholder="Enter a number">
            <button class="btn dail-button " @click="toggleCall()" :disabled="!validPhone">Dial</button>
          </div>
          <div class="clearfix"></div>
          <div class="colsm8 colsmoffset2 mt15">
            <div class="row dailcont">
              <div class="col-xs-4">
                <button class="btn-pad" @click="dial(1)">
                  1
                </button>
              </div>
              <div class="col-xs-4">
                <button class="btn-pad" @click="dial(2)">
                  2
                  <span>ABC</span>
                </button>
              </div>
              <div class="col-xs-4">
                <button class="btn-pad" @click="dial(3)">
                  3
                  <span>DEF</span>
                </button>
              </div>
              <div class="col-xs-4">
                <button class="btn-pad" @click="dial(4)">
                  4
                  <span>GHI</span>
                </button>
              </div>
              <div class="col-xs-4">
                <button class="btn-pad" @click="dial(5)">
                  5
                  <span>JKL</span>
                </button>
              </div>
              <div class="col-xs-4">
                <button class="btn-pad" @click="dial(6)">
                  6
                  <span>MNO</span>
                </button>
              </div>
              <div class="col-xs-4">
                <button class="btn-pad" @click="dial(7)">
                  7
                  <span>PQRS</span>
                </button>
              </div>
              <div class="col-xs-4">
                <button class="btn-pad" @click="dial(8)">
                  8
                  <span>TUV</span>
                </button>
              </div>
              <div class="col-xs-4">
                <button class="btn-pad" @click="dial(9)">
                  9
                  <span>WXYZ</span>
                </button>
              </div>
              <div class="col-xs-4">
                <button class="btn-pad">
                  *
                </button>
              </div>
              <div class="col-xs-4">
                <button class="btn-pad" @click="dial(0)">
                  0
                  <span>+</span>
                </button>
              </div>
              <div class="col-xs-4">
                <button class="btn-pad">
                  #
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- <b-row>
        <b-col>
          <button class="btn btn-circle btn-default" @click="toggleMute"  :disabled="!incomingCall && !onPhone">
            <i class="fa fa-fw" :class="[ muted ? 'fa-microphone-slash': 'fa-microphone' ]"></i>
            <span v-if="muted">Unmute</span><span v-else>Mute</span>
          </button>
        </b-col>
        <b-col v-show="incomingCall">
          <button class="btn btn-circle btn-danger" @click="rejectCall">
            <i class="icon-call-end"></i> Reject
          </button>
        </b-col>
        <b-col v-show="!incomingCall && !onPhone">
          <button class="btn btn-circle btn-large" @click="toggleCall()"
                  :class="[ onPhone ? 'btn-danger': 'btn-success' ]"
                  :disabled="!validPhone">
            <i class="fa fa-fw fa-phone" :class="[ onPhone ? 'fa-close': 'fa-phone' ]"></i>
            <span v-show="incomingCall">Accept</span>
            <span v-show="!incomingCall && !onPhone">Call</span>
            <span v-show="onPhone">End</span>
          </button>
        </b-col>
        <b-col v-show="incomingCall || onPhone">
          <button class="btn btn-circle btn-large" @click="toggleCall()"
                  :class="[ onPhone ? 'btn-danger': 'btn-success' ]"
                  >
            <i class="fa fa-fw fa-phone" :class="[ onPhone ? 'fa-close': 'fa-phone' ]"></i>
            <span v-show="incomingCall">Accept</span>
            <span v-show="!incomingCall && !onPhone">Call</span>
            <span v-show="onPhone">End</span>
          </button>
        </b-col>
      </b-row> -->
    </div>
    <div v-show="(incomingCall || onPhone) && !minimize">
      <div class="bottom-box">
        <div class="call-wrap">
          <h2 v-show="incomingCall && !onPhone">Inbound call</h2>
          <h2 v-show="onPhone">Connected</h2>
          <div class="pull-left call-info">
            <h5><b>From</b></h5>
            <h5 v-if="caller">{{caller}}</h5>
            <h5 v-if="!caller">{{currentNumber}}</h5>
          </div>
          <div align="right" class="pull-right call-info">
            <h5><b>Time elapsed</b></h5>
            <h5 v-show="!onPhone">00:00:00</h5>
            <h5 v-show="onPhone">{{ hours | two_digits }}:{{ minutes | two_digits }}:{{ seconds | two_digits }}</h5>
          </div>

          <div class="income-info">
            <button class="call-accept" v-show="incomingCall && !onPhone" @click="toggleCall">
              <img src="/static/img/call-accept.png">Accept Call
            </button>
            <button class="call-reject" v-show="incomingCall && !onPhone" @click="rejectCall()">
              <img src="/static/img/call-reject.png">Reject Call
            </button>
            <button class="call-end btn-block" v-show="onPhone" @click="toggleCall">
              <img src="/static/img/call-reject.png">End Call
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
  .bottom-box {
    width: 100%;
    height: 464px;
  }

  .close-t {
    background: no-repeat url(/static/img/icons.png) 0 -144px;
    width: 24px;
    height: 24px;
    border: 0px;
    margin-top: 4px;
  }

  .minimize {
    background: no-repeat url(/static/img/icons.png) 0 -212px;
    width: 24px;
    height: 24px;
    border: 0px;
    margin-top: 4px;
  }

  .maximize {
    background: no-repeat url(/static/img/icons.png) 0 -219px;
    width: 24px;
    height: 24px;
    border: 0px;
    margin-top: 4px;
  }


  .m0 {
    margin: 0px;
  }

  #dialer {
    margin: 10px;
  }

  .btn-circle {
    width: 100%;
    padding: 10px 0;
    margin: 10px 0;
  }

  div#log {
    border: 1px solid #686865;
    width: 80%;
    height: 15.5em;
    margin-top: 1.75em;
    text-align: left;
    padding: 1.5em;
    float: right;
    overflow-y: scroll;
  }

  div#log p {
    color: #686865;
    font-family: 'Share Tech Mono', 'Courier New', Courier, fixed-width;
    font-size: 1.25em;
    line-height: 1.25em;
    margin-left: 1em;
    text-indent: -1.25em;
    width: 90%;
  }

  .dail-wrap {
    width: 320px;
    max-height: 464px;
    box-shadow: 0px 0px 15px -2px #848484;
    background: #fff;
    position: fixed;
    right: 20px;
    bottom: 0px;
    display: block;
  }

  .dail-wrap h4 {
    margin-top: 20px;
    color: #000;
    margin-bottom: 24px;
    padding-left: 15px;
  }

  .m0 {
    margin: 0px;
  }

  .dail-text {
    height: 40px;
    border: 0px;
    box-shadow: none;
    border-bottom: 1px solid #000;
    border-radius: 0px;
    position: relative;
  }

  .dail-text::placeholder {
    font-size: 15px;
    color: #606060;
  }

  .dail-button {
    background: #a3acb5;
    height: 30px;
    line-height: 0px;
    color: #fff !important;
    position: absolute;
    right: 0;
    top: 4px;
  }

  .p-relative {
    position: relative;
  }


  .btn-pad {
    width: 100%;
    background: #47596f;
    border-radius: 2px;
    border: 0px;
    color: #fff;
    font-size: 30px;
    height: 50px;
    margin-bottom: 15px;
  }

  .mt15 {
    margin-top: 15px;
  }


  .dail-wrap .col-xs-4 {
    padding-left: 10px;
    padding-right: 10px;
  }

  .btn-pad span {
    font-size: 11px;
    display: block;
    margin-top: -9px;
  }

  .top-d {
    height: 32px;
    background: #404040;
    width: 100%;
    position: relative;
    text-align: right;
  }

  .top-d span {
    width: 18px;
    height: 3px;
    background: rgba(255, 255, 255, 0.56);
    margin: 5px;
    display: inline-block;
    right: 31px;
    position: absolute;
  }

  span.minimize {
    top: 55%
  }

  span.maximize {
    top: 25%
  }

  span.closee {
    background: none;
    right: 21px;
    top: -8px;
  }

  span.closee:after {
    content: '';
    position: absolute;
    width: 18px;
    height: 2px;
    background: rgba(255, 255, 255, 0.56);
    transform: rotate(47deg);
    top: 20px;
  }

  span.closee:before {
    content: '';
    position: absolute;
    width: 18px;
    height: 2px;
    background: rgba(255, 255, 255, 0.56);
    transform: rotate(132deg);
    top: 20px;
  }


  .colsmoffset2 {
    margin-left: 16.66666667%;
  }

  .colsm8 {
    width: 66.66666667%;
  }

  .dailcont .col-xs-4 {
    width: 33.33333333%;
  }

  .call-wrap {
    background: #4392ca;
    padding: 15px;
    min-height: 168px;
  }

  .call-wrap h2 {
    font-size: 28px;
    color: #fff
  }

  .call-info h5 {
    color: #fff;
  }


  .income-info {
    position: absolute;
    bottom: 0px;
    width: 100%;
    left: 0px;
    padding: 15px;
    text-align: center;
  }

  .call-accept {
    background: #538105;
    border: 0px;
    color: #fff;
    padding: 10px 10px;
  }

  .income-info img {
    margin-right: 5px;
    margin-top: -4px;
  }

  .income-info button {
    width: 44%;
    margin: 5px;
  }

  .call-reject {
    background: #d0011b;
    border: 0px;
    color: #fff;
    padding: 10px 10px;
  }

  .call-end {
    width: 100% !important;
    margin: 0px !important;
    background: #d0011b;
    border: 0px;
    color: #fff;
    padding: 10px 10px;
  }
</style>
<script>
  import FlagsDropdown from '../components/class/FlagsDropdown'
  import { Device } from 'twilio-client'

  /// adapted from https://github.com/TwilioDevEd/client-quickstart-js/blob/master/public/quickstart.js
  export default {
    name: 'caller-view',
    components: {
      FlagsDropdown,
    },
    data: function () {
      return {
        // Outgoing call country code
        countryCode: '',
        country_iso: '',
        currentNumber: '',
        muted: false,
        onPhone: false,
        connection: null,
        incomingCall: false,
        now: Math.trunc((new Date()).getTime() / 1000),
        callstartTime: null,
        minimize: false,
        caller: null,
      }
    },
    mounted: function () {
      // load any previously stored number
      this.currentNumber = localStorage.getItem('currentNumber') || ''

      if (this.$root.bus.info.generalsettings_id) {
        // Fetch Twilio capability token from our backend server
        this.$api.caller.getCallerToken(this.$root.bus.info.generalsettings_id).then(response => {
          Device.setup(response.body.token)
          this.$emit('got-twilio-token')
        }, errorResponse => {
          this.log('Failed to fetch Twilio token. You will not be able to make/receive any calls.', 'error')
          console.log(errorResponse)
        })
      }

      /// Configure event handlers for Twilio Device
      /// refer: https://www.twilio.com/docs/voice/client/javascript/device#events
      Device.on('cancel', this.incomingCallCancelHandler)
      // Device.on('connect', () => {
      //   this.log('Successfully established call!')
      // })
      Device.on('disconnect', this.twilioDisconnectionHandler)
      Device.on('error', (error) => {
        this.log('Twilio.Device Error: ' + error.message, 'error')
      })
      Device.on('ready', () => {
        // this.log('Twilio Device Connected')
      })
      Device.on('offline', () => {
        this.log('Twilio Token expired. Please refresh the page to generate new token.', 'error')
      })
      Device.on('incoming', this.twilioIncomingHandler)
    },
    computed: {
      validPhone: function () {
        return /^([0-9]|#|\*)+$/.test(this.currentNumber.replace(/[-()\s]/g, ''))
      },
      seconds: function () {
        return (this.now - this.callstartTime) % 60
      },
      minutes: function () {
        return Math.trunc((this.now - this.callstartTime) / 60) % 60
      },
      hours: function () {
        return Math.trunc((this.now - this.callstartTime) / 60 / 60) % 24
      },
    },
    watch: {
      onPhone: function () {
        if (this.onPhone === true) {
          this.callstartTime = Math.trunc((new Date()).getTime() / 1000)
          this.startTime()
        }
      },
    },
    methods: {
      mini () {
        this.minimize = true
      },
      max () {
        this.minimize = false
      },
      dial (val) {
        this.currentNumber = this.currentNumber + val
      },
      startTime () {
        window.setInterval(() => {
          this.now = Math.trunc((new Date()).getTime() / 1000)
        }, 1)
      },
      close () {
        if (this.incomingCall) {
          this.rejectCall()
        } else if (this.onPhone) {
          this.toggleCall()
        }
        this.$parent.showPhone = false
      },
      twilioDisconnectionHandler () {
        this.onPhone = false
        this.connection = null
        this.incomingCall = false
        this.log('Call ended.')
      },
      incomingCallCancelHandler () {
        this.onPhone = false
        this.connection = null
        this.incomingCall = false
        this.log('Call canceled by the user')
      },
      twilioIncomingHandler (conn) {
        this.log('Incoming connection from ' + conn.parameters.From)
        this.log('Click accept button to answer')
        this.connection = conn
        this.incomingCall = true
        this.$parent.showPhone = true

        this.caller = conn.parameters.From
        this.$api.users.app.getCaller('?number=' + this.caller).then(response => {
          console.log('response == ', response)
          if (response.body.name) {
            this.caller = response.body.name
          }
        }, response => {
          console.log('No user returned')
        })
      },
      log (msg, type = 'info') {
        // this.$notify({group: 'app', text: msg, type: type, title: 'Caller Interface'})
      },
      optionCountrySelected: function (data) {
        this.country_iso = data.code
        this.countryCode = data.phonecode
      },
      // Handle muting
      toggleMute: function () {
        this.muted = !this.muted
        Device.activeConnection().mute(this.muted)
      },
      // Make an outbound call with the current number,
      // or hang up the current call
      toggleCall: function () {
        if (this.incomingCall) {
          this.connection.accept()
          // start timer
          this.callstartTime = Math.trunc((new Date()).getTime() / 1000)
          this.startTime()

          this.incomingCall = false
          this.onPhone = true
        } else if (!this.onPhone) {
          localStorage.setItem('currentNumber', this.currentNumber)
          this.muted = false
          this.onPhone = true
          // make outbound call with current number
          let n = '+' + this.countryCode + this.currentNumber.replace(/\D/g, '')
          this.connection = Device.connect({To: n, CompanyId: this.$root.bus.info.generalsettings_id})
          // this.log('Calling ' + n)
        } else {
          // hang up call in progress
          Device.disconnectAll()
          // get back to dial pad
          this.incomingCall = false
        }
      },
      rejectCall () {
        if (this.incomingCall) {
          this.connection.reject()
          this.log('It\'s your nemesis. Rejected call.')
          // get back to dial pad
          this.incomingCall = false
          this.onPhone = false
        }
      },
    },
  }
</script>
