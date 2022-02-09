<template>
  <div>
    <div v-for="mail in items" class="list-group-item">
      <list-item :mail="mail"></list-item>
    </div>
  </div>
</template>

<script>
  import listItem from '../components/_listItem'

  export default {
    components: {listItem},
    name: 'voiceMailInbox',
    data () {
      return {
        items: [],
      }
    },
    methods: {
      loadVoiceMails () {
        this.$api.caller.getVoiceMails().then(response => {
          this.items = response.body.results
          var sidebar = this.$parent.$parent.$parent.$parent.$children[1]
          sidebar.voicemails = 0
        }, response => {
          this.$notify({
            group: 'app',
            text: 'Failed to fetch voice mails.',
            type: 'error',
          })
        })
      },
    },
    mounted () {
      this.loadVoiceMails()
    },
  }
</script>
