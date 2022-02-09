<script>
  /**
   * to use this mixin,
   * 1. in the mixins: array add this
   * 2. in b-tabs there should be `$refs=tabs` and the `v-model=activeTabIndex`
   * @returns {{activeIndex: number}}
   */
  export default {
    data () {
      return {
        activeIndex: 0,
      }
    },
    computed: {
      keyForStoringTabIndex () {
        return `${this.$refs.tabs.$el.id}-tab-index`
      },
      activeTabIndex: {
        get () {
          return this.activeIndex
        },
        set (val) {
          this.activeIndex = val
          localStorage.setItem(this.keyForStoringTabIndex, val)
        },
      },
    },
    mounted () {
      this.activeTabIndex = parseInt(localStorage.getItem(this.keyForStoringTabIndex) || 0)
    },
  }
</script>

