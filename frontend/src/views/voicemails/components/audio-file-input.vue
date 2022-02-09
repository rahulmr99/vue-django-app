<template>
  <div class="audio-file-input">
    <b-input-group id="exampleGroup4">
      <div class="clearFileInputBtn">
        <b-button @click="clearFiles"><i class="fa fa-times"></i></b-button>
      </div>
      <b-form-file accept="audio/*" v-model="value" ref="fileInput" name="greeting_voice"></b-form-file>
    </b-input-group>
  </div>
</template>

<script>
  export default {
    name: 'audio-file-input',
    properties: {
      value: {},
    },
    data () {
      return {
        // file: null,
      }
    },
    computed: {},
    methods: {
      clearFiles () {
        this.$refs.fileInput.reset()
      },
    },
  }
</script>
