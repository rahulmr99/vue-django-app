<template>
  <b-row>
    <b-col cols="4">
      <b-row>
        <b-col cols="1">
          <label class="mt10">
            <input type="checkbox" v-model="checked">
           
          </label>
        </b-col>
        <b-col cols="8">
          {{formattedPhoneNumber}}
          <b-button class="voice-call" @click="makeCall"><i class="fa fa-phone"></i></b-button>
        </b-col>
        <b-col cols="2">
          <b-button @click="playVoiceMail" class="play-stop ">
            <i class="fa fa-play" aria-hidden="true" v-show="!isPlayingVoiceMail"></i>
            <i class="fa fa-stop" aria-hidden="true" v-show="isPlayingVoiceMail"></i>
          </b-button>
          <small><span class="badge">{{mail.duration}}</span></small>
        </b-col>
      </b-row>
    </b-col>
    <b-col cols="8">
      <b-row>
        <b-col cols="9">
          {{mail.transcription_text}}
        </b-col>
        <b-col cols="3">
          <span class="badge">{{formattedTime}}</span>
          <button class="btn btn-call-del" v-if="checked" @click="deleteVMail()"> <i class="fa fa-trash" aria-hidden="true"></i> </button>
        </b-col>
      </b-row>
    </b-col>
  </b-row>
</template>
<style>
  .btn-call-del {  
    color: #3b77e7;
    border-radius: 4px;}
  
  </style>
<script>
  export default {
    name: 'list-item',
    props: {
      mail: {},
    },
    data () {
      return {
        checked: false,
        currentAudio: null,
        isPlayingVoiceMail: false,
      }
    },
    computed: {
      formattedTime () {
        if (this.mail.created) {
          return this.$moment(this.mail.created).format('MMM Do YY')
        }
        return ''
      },
      formattedPhoneNumber () {
        // hide + sign
        console.log(this.mail.from_caller_id, 'ss')
        if (this.mail && this.mail.from_caller_id) {
          return this.mail.from_caller_id.replace('+', '')
        }
        return ''
      },
    },
    methods: {
      deleteVMail () {
        this.$api.caller.deleteVoiceMail(this.mail.id, this.mail).then(response => {
          this.$api.caller.getVoiceMails().then(response => {
            this.$parent.items = response.body.results
          })
        }, response => {
        })
      },
      makeCall () {
        this.$parent.$parent.$parent.$parent.$parent.$children[0].$children[0].currentNumber = this.mail.from_caller_id.replace('+', '')
        this.$parent.$parent.$parent.$parent.$parent.$children[0].showPhone = true
      },
      playVoiceMail () {
        if (this.isPlayingVoiceMail) {
          this.stopPlaying()
        } else {
          this.startPlaying()
        }
      },
      startPlaying () {
        this.isPlayingVoiceMail = true
        this.currentAudio = new Audio(this.mail.recording_url)
        this.currentAudio.onended = this.onEndedCallback
        this.currentAudio.play()
      },
      stopPlaying () {
        this.currentAudio.pause()
        this.currentAudio.currentTime = 0
        this.onEndedCallback()
      },
      onEndedCallback () {
        this.isPlayingVoiceMail = false
        this.currentAudio.currentTime = null
      },
    },
  }
</script>
