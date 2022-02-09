<template>
  <div>
    <b-form @submit="saveSettings" ref="form">
      <b-col sm="12" md="10" lg="8">
        <b-row>
          <b-col>
            <inp v-model="formData.greeting_message" label="Greetings Message 
            (Please note: say press 1 to book, 2 to reschedule, 3 to cancel, and 4 for all other questions)" name="greeting_message"></inp>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <ui-switch type="3d" variant="primary" label="Greet with custom audio"
                       v-model="formData.use_audio"></ui-switch>
          </b-col>
        </b-row>
        <b-row v-show="formData.use_audio">
          <b-col>
            <inp label="Greetings Voice">
              <div slot="formControl">
                <b-input-group id="exampleGroup4">
                  <div class="clearFileInputBtn">
                    <b-button @click="clearFiles"><i class="fa fa-times"></i></b-button>
                  </div>
                  <audio ref="sound" controls hidden></audio>
                  <b-form-file accept="audio/*" v-model="formData.greeting_voice" ref="fileInput"
                               name="greeting_voice" @change='changeFile'>
                  </b-form-file>
                </b-input-group>
                <div class="uploaded-file" v-if="file&&!playing">
                  <a href="javascript:void(0)" class="btn outline-secondary" v-text="file_name">

                  </a>
                  <b-btn @click="playAudio"><i class="fa fa-play">Play</i></b-btn>
                </div>
                <div class="uploaded-file" v-if="file&&playing">
                  <a href="javascript:void(0)" class="btn outline-secondary" v-text="file_name">
                    Uploaded audio
                  </a>
                  <b-btn @click="pauseAudio"><i class="fa fa-stop"> stop</i></b-btn>
                </div>
              </div>
            </inp>
          </b-col>
        </b-row>
        <b-row v-show="!formData.redirect_to_browser">
          <b-col>
            <inp v-model="formData.redirect_telephone_number" label="Redirect Number (should include country code)"
                 name="redirect_telephone_number"></inp>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <ui-switch type="3d" variant="primary" label="Redirect customer support call to browser"
                       v-model="formData.redirect_to_browser"></ui-switch>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <b-button type="submit" variant="primary">Save</b-button>
          </b-col>
        </b-row>
      </b-col>
    </b-form>
  </div>
</template>

<script>
  import UiSwitch from '../../components/class/UiSwitch.vue'
  import Inp from '../../components/class/Inp.vue'
  import AudioFileInput from '../voicemails/components/audio-file-input'

  export default {
    name: 'voiceMailSettings',
    components: {
      UiSwitch,
      Inp,
      AudioFileInput,
    },
    data () {
      return {
        formData: {},
        file: '',
        sound: '',
        playing: false,
        file_name: '',
      }
    },
    methods: {
      fetchSettings () {
        this.$api.caller.getVoiceBotConfigs().then(response => {
          let resp = response.body.results[0] || {}
          this.formData = resp
          this.file = resp.greeting_voice
          this.sound.src = resp.greeting_voice
          this.file_name = resp.greeting_voice_filename
        }, response => {
          this.$notify({group: 'app', text: 'Failed to fetch settings', type: 'error'})
        })
      },
      saveSettings (evt) {
        evt.preventDefault()
        let formData = new FormData(evt.target)
        for (let key in this.formData) {
          if (this.formData.hasOwnProperty(key)) {
            let val = this.formData[key]
            if (val) {
              if ((key === 'greeting_voice') && typeof val === 'string') {
                // upload only if it is a valid file object
                formData.delete(key)
              } else {
                formData.append(key, val)
              }
            }
          }
        }
        this.$api.caller.saveVoiceBotConfigs(this.formData.id, formData).then(response => {
          this.$notySuccess()
        }, response => {
          this.$notify({group: 'app', text: 'Failed to save Voice-bot settings', type: 'error'})
        })
      },
      clearFiles () {
        this.sound.src = ''
        this.playing = false
        this.file = ''
        this.file_name = ''
        if (this.formData.greeting_voice) {
          this.formData.greeting_voice = null
          this.formData.greeting_voice_filename = null
          this.$refs.fileInput.reset()
        } else {
          this.$refs.fileInput.reset()
        }
      },
      playAudio () {
        console.log('play audio')
        this.sound.play()
        this.playing = true
      },
      pauseAudio () {
        this.sound.pause()
        this.playing = false
      },
      changeFile (e) {
        var files = e.target.files || e.dataTransfer.files
        if (files.length) {
          this.file = files[0]
        }

        this.sound.src = URL.createObjectURL(files[0])
        this.file_name = this.file.name
      },
    },
    mounted () {
      this.sound = this.$refs.sound
      this.sound.onended = this.pauseAudio
      this.fetchSettings()
    },
  }
</script>

<style scoped>
  .uploaded-file {
    overflow: hidden;
    text-align: right;
    margin: 6px 0px;
    border: 1px solid #d2cece;
    border-radius: 2px;
  }

  .uploaded-file button {
    background: #45a8d8;
    color: #fff
  }

  [type=reset], [type=submit], button, html [type=button] {
    -webkit-appearance: button;
  }

  [role=button], a, area, button, input:not([type=range]), label, select, summary, textarea {
    -ms-touch-action: manipulation;
    touch-action: manipulation;
  }
</style>
