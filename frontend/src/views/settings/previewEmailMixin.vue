<script>
  export default {
    name: 'previewEmailMixin',
    data () {
      return {
        itemData: {},
        resource_url_func: null,
      }
    },
    mounted () {
      this.loadSettings()
    },
    methods: {
      showPreview () {
        this.$emit('preview', this.previewTitle, this.itemData.email_body)
      },
      loadSettings () {
        this.getResourceFunc().then(response => {
          this.itemData = response.body[0]
        }, response => {
          this.$notify({group: 'app', text: 'Failed to get email settings.', type: 'error'})
        })
      },
      saveSettings () {
        this.saveResourceFunc(
          this.itemData.id,
          this.itemData
        ).then(response => {
          this.$notySuccess()
        }, response => {
          this.$notify({group: 'app', text: 'Failed to save settings', type: 'error'})
        })
      },
    },

  }
</script>

