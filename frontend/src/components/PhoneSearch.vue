<template>
  <modal class="calendar-add-form m-modal" :title="getFormTitle" large v-model="showForm"
         @ok="showForm = false" effect="zoom">
    <div>
      <label>Choose a country</label>
      <span><flags-dropdown style="width: 100%" class="form-control" v-on:change="optionCountrySelected" showCountryName="1"></flags-dropdown></span>
    </div>
    <div>
      <label class="mt10">Narrow your search by area code by typing in your area code in box</label>
      <span>
        <input class="form-control" @input="searchNumbers()" v-model="areacode">
      </span>
    </div>
    <div v-if="numbers ? numbers.length > 0 : false">
      <b-table class="n-table" :per-page="5" :current-page="currentPage" :items="numbers">
        <template slot="phone numbers" slot-scope="data">
          <span>{{data.value}}</span>
          <span class="pull-right">
            <input type="radio" name="selectedNumber" v-model="selectedNumber" :value="data.value">
          </span>
        </template>
      </b-table>
      <b-pagination size="sm" :total-rows="numbers.length" :per-page="5" v-model="currentPage" >
      </b-pagination>
    </div>
    <template slot="modal-footer">
      <div class="modal-footer">
        <button type="button" class="btn btn-primary" @click="getFreeNumber()">Get Free Phone Number</button>
      </div>
    </template>
  </modal>
</template>

<script>
import modal from './class/ModalFormClass.vue'
import FlagsDropdown from './class/FlagsDropdown'

export default {
  name: 'searchPhone',
  components: {
    modal,
    FlagsDropdown,
  },
  computed: {
    getFormTitle () {
      return 'Claim Your FREE Phone Number'
    },
  },
  data: function () {
    return {
      showForm: true,
      areacode: '',
      numbers: null,
      countrycode: '',
      currentPage: 1,
      selectedNumber: null,
    }
  },
  watch: {
    selectedNumber: function () {
      console.log(this.selectedNumber)
    },
  },
  methods: {
    optionCountrySelected (data) {
      this.countrycode = data.code
      this.searchNumbers()
    },
    searchNumbers () {
      let areacode = this.areacode
      let countrycode = this.countrycode
      this.$api.caller.getNumbers(areacode, countrycode).then(response => {
        this.numbers = response.body.number_list
      })
    },
    getFreeNumber () {
      this.$api.caller.purchaseNumber({'number': this.selectedNumber}).then(response => {
        alert('Congratulations! Your number is ' + this.selectedNumber + ". You'll be able to see this number in your account settings")
        this.showForm = !(response.body.status === 'ok')
      })
    },
  },
}
</script>

<style>
.m-modal .multiselect__content-wrapper {width: 100% !important;}

.m-modal .multiselect { padding: 0px;}

.m-modal .multiselect input {
    width: 100% !important;
}



.n-table  { margin-top: 20px;     border: 1px solid #cec6c6;}

.n-table th {
    vertical-align: bottom;
    border-bottom: 2px solid #a4b7c1;
    background: rgb(0, 105, 255);
    color: white;
}

.n-table td {     padding-left: 45px; position: relative;}

.n-table td:before {
     content: "\F095";
    position: absolute;
    color: #4CAF50;
    font-family: fontawesome;
    left: 15px;
    font-size: 18px;
    top: 9px;
}

</style>

