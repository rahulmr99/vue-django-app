<template>
  <div>
    <row>
      <b-table show-empty hover :fields="lFields" :items="dataProvider" :current-page="currentPage" :per-page="perPage">
        <template slot="rating_given" slot-scope="data">
          <b-img :src="emojicon(data.value)" alt="rating" fluid width="35"></b-img>
        </template>
      </b-table>
    </row>
    <row>
      <b-pagination :total-rows="totalRows" :per-page="perPage" v-model="currentPage"></b-pagination>
    </row>
  </div>
</template>

<script>
  import Row from '../../../components/class/Row'
  import getSmileyImgPath from './get_smiley'

  export default {
    components: {
      Row,
    },

    methods: {
      emojicon (val) {
        return getSmileyImgPath(val)
      },
      // fetch feedback statistics
      dataProvider (ctx) {
        // this.isBusy = true
        // try fetching only if the data is not cached locally
        if (!(this.pages[ctx.currentPage])) {
          return this.$http.get(`api/v1/feedback/?format=json&content=true&page=${ctx.currentPage}`)
            .then((response) => {
              this.totalRows = response.body.count
              this.pages[ctx.currentPage] = response.body.results
              return response.body.results
            }).catch(() => {
              this.$notify({group: 'app', text: 'Failed to fetch feedback', type: 'error'})
              // request failed
              return []
            })
        } else {
          return this.pages[ctx.currentPage]
        }
        // this.isBusy = false
      },
    },

    data: function () {
      return {
        lFields: [
          {key: 'rating_given'},
          'content',
        ],
        currentPage: 1,
        perPage: 10,
        totalRows: 0,
        pages: {},
        isBusy: false,
      }
    },
  }
</script>
