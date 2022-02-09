<template>
    <multiselect class="dail-text"  v-model="value" lable="tzname" :options="ustz" :show-labels="false"
                 @input="onTZChange" placeholder="----">

        <template slot="option" slot-scope="props">
            <span class="props">
                <span> ( {{ props.option.offset }} ) </span>
                <span> {{ props.option.timezone }} </span>
            </span>
        </template>

        <template slot="singleLabel" slot-scope="lab">
            <span class="lab">
                <span> ( {{ lab.option.offset }} ) </span>
                <span> {{ lab.option.timezone }} </span>
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
    import * as ustimezonesList from './ustimezonesList'

    export default {
      name: 'UsTimeZonesDropDown',
      components: { Multiselect },
      data () {
        return {
          value: null,
          ustz: ustimezonesList.ustimezonesList,
          currentlyselectedTzIndex: 5,
        }
      },
      created () {
        let selectedTzInfo = parseInt(localStorage.getItem('currentlyselectedTzIndex')) || this.currentlyselectedTzIndex
        this.value = this.ustz[selectedTzInfo]
        this.$emit('change', this.value)
      },
      methods: {
        onTZChange: function (value) {
          if (value) {
            this.value = value
            this.currentlyselectedTzIndex = value.id
            localStorage.setItem('currentlyselectedTzIndex', value.id)
            this.$emit('change', value)
          }
        },
      },
    }
</script>