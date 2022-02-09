<template>
    <table class="table table-csv">
        <tr>
            <td v-for="(key,index) in colNum">
                <select class="form-control" @change="getData(index,$event)">
                    <option value=''></option>
                    <option value='service_id' v-if="importAppoinment()">Service</option>
                    <option value='start_date_time' v-if="importAppoinment()">Start Date and Time</option>
                    <option value='end_date_time' v-if="importAppoinment()">End Date and Time</option>
                    <option value='name'>First Name</option>
                    <option value='last_name'>Last Name</option>
                    <option value='email'>Email</option>
                    <option value='phone'>Phone</option>
                    <option value='note'>Note</option>
                </select>
            </td>
        </tr>
        <tr v-for="row in lines">
            <td v-for="col in row">
            {{col}}
            </td>
        </tr>
    </table>
</template>
<script>
  export default {
    props: ['colNum', 'lines'],
    // A data object containing all data for this component.
    data: function () {
      return {
        parsed_data: {},
      }
    },
    created () {
    },
    // Methods, we will bind these later on.
    methods: {
      getData (columnIndex, e) {
        var fieldName = e.target.value
        var arr = []
        for (var i = 1; i < this.lines.length; i++) {
          for (var j = 0; j < this.lines[i].length; j++) {
            if (j === columnIndex) {
              arr.push(this.lines[i][j])
            }
          }
        }
        this.parsed_data[fieldName] = arr
      },
      importAppoinment () {
        if (this.$parent.importAppoinment === true) return true; else return false
      },
    },
  }
</script>

<style>
.table-csv  td {
    padding: 0.75rem;
    vertical-align: top;
    background: #eaeaea;
    font-size:12px;
}

.table-csv select {    border-radius: 5px !important;
    border: 0px !important;
    box-shadow: 0px 0px 2px 1px #6767676b !important;}

</style>