<template>
  <multiselect class="dail-text" v-model="value" track-by="code" label="nicename" :options="countries" :show-labels="false"
               @input="onFlagChange" placeholder="----" style="width: 88px;" >
    <template slot="option" slot-scope="props">
      <span class="props__code">
        <i v-if="!bill" :class="'flag flag-'+props.option.code"></i>
        <!-- <span style="text-transform: uppercase;">{{ props.option.nicename }}</span> -->
        <span v-if="bill"> {{props.option.nicename}}</span>
        <span v-else>(+{{ props.option.phonecode }})</span>
      </span>
    </template>
    <template slot="singleLabel" slot-scope="lab">
      <span class="lab__code">
        <i v-if="!bill" :class="'flag flag-'+lab.option.code"></i>
        <span v-if="showCountryName">&nbsp;{{ lab.option.nicename }}</span>
      </span>
    </template>
  </multiselect>
</template>
<style>

.multiselect{
  font-size:12px !important;
}
.multiselect__select{
  height:32px !important;
}
.multiselect__single{
  font-size:12px !important;
}
.multiselect__tags{
  border: 0px !important;
}
.multiselect__content-wrapper{
  width: 100% !important;
}
.multiselect input{
  width : 40px !important;
}
</style>
<script>
  import Multiselect from 'vue-multiselect'
  import 'vue-multiselect/dist/vue-multiselect.min.css'
  import * as countriesList from './countriesList'

  export default {
    components: {Multiselect},
    props: ['showCountryName', 'bill'],
    // A data object containing all data for this component.
    data: function () {
      return {
        value: null,
        countries: countriesList.countriesList,
        currentlySelectedIndex: 225,
      }
    },
    created () {
      let currentlySelectedIndex = parseInt(localStorage.getItem('currentlySelectedIndex')) || this.currentlySelectedIndex
      this.value = this.countries[currentlySelectedIndex]
      this.$emit('change', this.value)
    },
    // Methods, we will bind these later on.
    methods: {
      onFlagChange: function (value) {
        if (value) {
          this.value = value
          this.currentlySelectedIndex = value.id
          localStorage.setItem('currentlySelectedIndex', value.id)
          this.$emit('change', value)
        }
      },
    },
  }
</script>
