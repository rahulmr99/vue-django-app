<template>
  <row>
    <h3>Patient Experience Report</h3>
    <b-table hover :fields="lFields" :items="$root.bus.settings.ratings_settings.report">
      <template slot="name" slot-scope="data">
        <b-img :src="emojicon(data.value)" alt="rating" fluid width="35"></b-img>
      </template>
    </b-table>
  </row>
</template>

<script>
  import Row from '../../../components/class/Row'
  import getSmileyImgPath from './get_smiley'

  export default {
    components: {
      Row,
    },
    mounted: function () {
      this.loadFeedbackReport()
    },
    methods: {
      emojicon (val) {
        return getSmileyImgPath(val)
      },
      // fetch feedback statistics
      loadFeedbackReport () {
        this.$api.settings.getFeedbackReport().then(response => {
          this.$root.bus.settings.ratings_settings.report = response.body
          // removing first element
          this.$root.bus.settings.ratings_settings.report.shift()
        }, response => {
          this.$notify({group: 'app', text: 'Failed to fetch Feedback report', type: 'error'})
        })
      },
    },
    data: function () {
      return {
        lFields: [
          {
            key: 'name',
            label: 'Rating',
          },
          {
            key: 'count',
            label: 'Clicks',
          },
          {
            key: 'percent',
          },
        ],
      }
    },
  }
</script>
