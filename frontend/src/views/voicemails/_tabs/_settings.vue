<template>
  <div>
    <b-form @submit="saveSettings" ref="form">
      <b-col sm="12" md="8" lg="6">
        <b-row>
          <b-col>
            <inp v-model="formData.greeting_message" label="Greetings Message 
            (Please note: say press star key once finished after your message)" name="greeting_message"></inp>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <ui-switch type="3d" variant="primary" label="Greet with custom audio"
                       v-model="formData.use_audio"></ui-switch>
          </b-col>
        </b-row>
        <div v-show="formData.use_audio">
          <b-row>
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
                    <a href="javascript:void(0)" class="btn outline-secondary" v-text="file_name"></a>
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
          <!--<b-row>-->
            <!--<b-col>-->
              <!--<label>Record your welcome message</label>-->
              <!--<a :class="['btn', recordingClassName]" @click="toggleRecording">-->
                <!--<i class="fa fa-microphone"></i>-->
                <!--<span v-if="isRecording">Stop</span>-->
                <!--<span v-else>Record</span>-->
              <!--</a>-->
              <!--<a class="btn btn-success">-->
                <!--<i class="fa fa-play"></i> Play-->
              <!--</a>-->
              <!--<a class="btn btn-danger">-->
                <!--<i class="fa fa-times"></i>-->
              <!--</a>-->
              <!--<audio id="audio" preload="auto"></audio>-->
            <!--</b-col>-->
          <!--</b-row>-->
        </div>
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
  import UiSwitch from '../../../components/class/UiSwitch.vue'
  import Inp from '../../../components/class/Inp.vue'
  import AudioFileInput from '../components/audio-file-input'
  import MediaStreamRecorder from 'msr'

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
        isRecording: false,
        audioRecorder: null,
        recordingData: [],
        dataUrl: null,
      }
    },
    computed: {
      recordingClassName () {
        return this.isRecording ? 'btn-danger' : 'btn-success'
      },
    },
    methods: {
      fetchSettings () {
        this.$api.caller.getVoiceConfigs().then(response => {
          this.formData = response.body.results[0] || {}
          this.file = this.formData.greeting_voice
          this.sound.src = this.formData.greeting_voice
          this.file_name = this.formData.greeting_voice_filename
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
        this.$api.caller.saveVoiceConfigs(this.formData.id, formData).then(response => {
          this.$notySuccess()
        }, response => {
          this.$notify({group: 'app', text: 'Failed to save settings', type: 'error'})
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
        this.sound.play()
        this.playing = true
      },
      pauseAudio () {
        if (!this.sound.ended) {
          this.sound.pause()
        }
        this.playing = false
      },
      changeFile (e) {
        let files = e.target.files || e.dataTransfer.files
        if (files.length) {
          this.file = files[0]
        }

        this.sound.src = URL.createObjectURL(files[0])
        this.file_name = this.file.name
      },
      captureUserMedia () {
        navigator.mediaDevices.getUserMedia({
          audio: true,
        }).then(this.onMediaSuccess).catch(this.onMediaError)
      },
      onMediaSuccess (stream) {
        this.audioRecorder = new MediaStreamRecorder(stream)
        this.audioRecorder.stream = stream
        this.audioRecorder.mimeType = 'audio/webm' // audio/webm or audio/ogg or audio/wav
        this.audioRecorder.ondataavailable = this.onDataAvailable
        this.audioRecorder.start(3000)
      },
      onMediaError (err) {
        console.error('media error', err)
      },
      onDataAvailable (event) {
        // when audio record is available as the bytes specified
        this.recordingData.push(event.data)
      },
      toggleRecording: function () {
        // todo: handle playing data
        // https://github.com/streamproc/MediaStreamRecorder
        this.isRecording = !this.isRecording
        if (this.isRecording) {
          //  start recording
          this.captureUserMedia()
        } else {
          //  stop recording
          if (this.audioRecorder) {
            this.audioRecorder.stop()
            this.audioRecorder.stream.stop()
            // this.audioRecorder.save()
            console.log('recording stopped and saving data')
            let blob = new Blob(this.recordingData, {type: 'audio/webm'})
            this.dataUrl = window.URL.createObjectURL(blob)
            console.log('saved data', this.dataUrl)
            console.log(this.dataUrl)
            window.dt = this.dataUrl
          }
        }
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
    margin: 6px 0;
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
