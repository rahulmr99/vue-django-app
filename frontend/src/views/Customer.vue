<template>
  <div class="animated fadeIn">
    <div v-show="!Import" class="container-fluid">
      <UserForm v-on:fetchCustomers="fetchCustomers"></UserForm>

      <div class="row main-route">
        <div class="col-md-8">
          <div class="row">
            <div class="col-sm-12">
              <input class="form-control search-customer" @keyup="searchCustomers" v-model="search_input"
                     placeholder="search" type="text" autocomplete="off">
            </div>
          </div>
          <div class="row">
            <div class="col-sm-8">
              <div class="btn-group search-customer" role="group" aria-label="...">
                <button @click="addCustomerForm" class="btn btn-primary btn-sm" type="button">
                  <i class="fa fa-plus"></i> Add
                </button>
                <button @click="updateCustomerForm($root.bus.customers.choice_item)"
                        v-if="Object.keys($root.bus.customers.choice_item).length !== 0"
                        class="btn btn-warning btn-sm" type="button"><i class="fa fa-pencil"></i> Update
                </button>
                <button @click="deleteCustomers" v-if="Object.keys($root.bus.customers.choice_item).length !== 0"
                        class="btn btn-danger btn-sm" type="button"><i class="fa fa-plus"></i> Delete
                </button>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-lg-12">
              <div class="card">
                <div class="card-header">
                  <i class="fa fa-align-justify" v-b-tooltip.hover title="Import Patients"  @click="importPatients()"></i> Patients count {{ $root.bus.customers.count }}
                </div>
                <div class="card-block">
                  <table class="table table-sm">
                    <thead>
                    <tr>
                      <th>First name</th>
                      <th>Last name</th>
                      <th>Email</th>
                      <th>Phone</th>
                      <!--<th class="appointments_cell">Note</th>-->
                    </tr>
                    </thead>
                    <tbody>
                    <tr @dblclick.stop="updateCustomerForm(item)" v-for="item in $root.bus.customers.customers_list"
                        @click="selectItem(item)"
                        v-bind:class="[{ activew: item.id == $root.bus.customers.choice_id }]">
                      <td>{{ item.name }}</td>
                      <td>{{ item.last_name }}</td>
                      <td>{{ item.email }}</td>
                      <td>{{ item.phone }}</td>
                      <!--<td>{{ item.note }}</td>-->
                    </tr>
                    </tbody>
                  </table>
                  <ul class="pagination">
                    <li @click.prevent="paginatePrevious" v-if="this.$root.bus.customers.previous" class="page-item"><a
                      class="page-link" href="#">Prev</a></li>
                    <li @click.prevent="paginateNext" v-if="this.$root.bus.customers.next" class="page-item"><a
                      class="page-link" href="#">Next</a></li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-lg-4 animated fadeIn">
          <div v-show="$root.bus.customers.appointments_list.length === 0" class="card">
            <div class="card-header">
              <i class="fa fa-align-justify"></i> Past Appointments
            </div>
            <div class="card-block">
              <p>Empty appointment.</p>
            </div>
          </div>
          <div class="card" v-for="item in $root.bus.customers.appointments_list">
            <div class="card-header">
              <i class="fa fa-align-justify"></i> Past Appointments
            </div>
            <div class="card-block">
              <p>
                {{ $moment(item.start_datetime).format('DD/MM/YYYY h:mm') }}
                -
                {{ $moment(item.end_datetime).format('DD/MM/YYYY h:mm') }}</p>
              <p>{{ item.services.name }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-show="Import">
      <div class="row up-wrap mb20">
        <label>Select a CSV with patients to upload</label>
        <input class="form-control csvFile" type="file" accept=".csv" @change="onFileChange">
        <button @click="uploadCSV()" class="btn btn-primary mt10 mb20" :disabled="!lines" >Import</button>
      </div>
      <div class="row m0">
        <csvImport :colNum="columnCount" :lines="data"></csvImport>
      </div>
    </div>
  </div>
</template>

<script>
  import UserForm from '../components/forms/UserForm.vue'
  import csvImport from '../components/class/csvImport.vue'

  export default {
    name: 'customer',
    components: {
      UserForm,
      csvImport,
    },
    mounted: function () {
      this.fetchCustomers()
    },
    data () {
      return {
        search_input: null,
        fileinput: '',
        data: [],
        form: {
          name: '',
          last_name: '',
          email: '',
          phone: '',
          note: '',
          is_customers: true,
          generalsettings_id: this.$root.bus.info.generalsettings_id,
        },
        columnCount: null,
        Import: false,
        lines: null,
      }
    },
    created: function () {
      this.$root.bus.checkLogin()
    },
    watch: {
      fileinput: function () {
        this.lines = this.fileinput.trim().split('\n')
        this.columnCount = this.lines[0].split(',')
        for (var i = 0; i < this.lines.length; i++) {
          this.data.push(this.lines[i].slice(0, -1).split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/))
        }
      },
    },
    methods: {
      importPatients () {
        this.Import = true
      },
      uploadCSV () {
        this.$children[1].parsed_data['num_of_records'] = this.data.length - 1
        this.$api.users.app.add_customers(this.$children[1].parsed_data).then(response => {
          this.Import = false
          this.data = []
          this.columnCount = null
          this.$children[1].colNum = null
          this.$children[1].lines = null
          this.$children[1].parsed_data = {}
          window.$('.csvFile').val(null)
          this.fetchCustomers()
        }, response => {
          this.data = []
          this.columnCount = null
          this.$children[1].colNum = null
          this.$children[1].lines = null
          this.$children[1].parsed_data = {}
          window.$('.csvFile').val(null)
        })
      },
      onFileChange (e) {
        var files = e.target.files || e.dataTransfer.files
        if (!files.length) return
        this.createInput(files[0])
      },
      createInput (file) {
        var reader = new FileReader()
        var vm = this
        reader.onload = (e) => {
          vm.fileinput = reader.result
        }
        reader.readAsText(file)
      },
      fetchCustomers () {
        this.$api.users.getAllCustomers(`&page=${this.$root.bus.customers.page}`).then(response => {
          this.$root.bus.customers.customers_list = response.body.results
          this.$root.bus.customers.next = response.body.next
          this.$root.bus.customers.previous = response.body.previous
          this.$root.bus.customers.count = response.body.count
        }, response => {
        })
      },
      deleteCustomers () {
        this.$api.users.app.deleted_customer(this.$root.bus.customers.choice_id).then(response => {
          this.fetchCustomers()
        }, response => {
        })
      },
      searchCustomers () {
        this.$root.bus.customers.page = 1
        this.$api.users.app.search(this.search_input).then(response => {
          this.$root.bus.customers.customers_list = response.body.results
          this.$root.bus.customers.next = response.body.next
          this.$root.bus.customers.previous = response.body.previous
          this.$root.bus.customers.count = response.body.count
        }, response => {
        })
      },
      feetchAppointments () {
        let sendId = {'id': this.$root.bus.customers.choice_id}
        this.$api.calendar.filterCalendarId(sendId).then(response => {
          this.$root.bus.customers.appointments_list = response.body
        }, response => {
          this.$notify({group: 'app', text: 'Failed to fetch appointments.', type: 'error'})
        })
      },
      selectItem (item) {
        this.$root.bus.customers.choice_id = item.id
        this.$root.bus.customers.choice_item = item
        this.feetchAppointments()
      },
      addCustomerForm () {
        this.$root.bus.setFormUserType(3)
        this.$emit('updateUserInfo')
      },
      updateCustomerForm (info) {
        this.$root.bus.setFormUserType(3)
        this.$emit('updateUserInfo', info)
      },
      paginateNext () {
        this.$root.bus.customers.page = this.$root.bus.customers.page + 1
        this.fetchCustomers()
      },
      paginatePrevious () {
        this.$root.bus.customers.page = this.$root.bus.customers.page - 1
        this.fetchCustomers()
      },
    },
  }
</script>



<style lang="css">
  .search-customer {
    margin-bottom: 20px;
  }

  .appointments_cell {
    width: 30px;
  }

  tr {
    cursor: pointer;
  }

  .activew {
    background-color: #5bc0de;
  }

  .list-inline {
    display: flex;
    justify-content: center;
  }

.up-wrap {
    background: #eaeaea;
    padding: 10px;
    border-radius: 5px;
    margin-top: 2em;}

.mb20 { margin-bottom:20px;}

.btn-primary.disabled, .btn-primary:disabled {
    color: #fff;
    background-color: #3b77e7;
    border-color: #3b77e7;
}
</style>
