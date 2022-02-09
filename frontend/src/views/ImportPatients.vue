<template>
    <div>
      <div class="row up-wrap mb20">
        <label>Select a CSV with patients to upload</label>
        <input class="form-control csvFile" type="file" accept=".csv" @change="onFileChangeP">
        <button @click="uploadCSV()" class="btn btn-primary mt10 mb20" :disabled="!lines || importAppoinment" >Import</button>
      </div>
      <div class="row m0" v-if="importPatient">
        <csvImport :colNum="columnCount" :lines="data"></csvImport>
      </div>
      <div class="row up-wrap mb20">
        <label>Import Appointments here</label>
        <input class="form-control csvFile" type="file" accept=".csv" @change="onFileChangeA">
        <button @click="uploadAppoinments()" class="btn btn-primary mt10 mb20" :disabled="!lines || importPatient" >Import Appointments</button>
      </div>
      <div class="row m0" v-if="importAppoinment">
        <csvImport :colNum="columnCount" :lines="data"></csvImport>
      </div>      
    </div>
</template>
<style>
  .search-customer {
    margin-bottom: 20px;
  }

  .appointments_cell {
    width: 30px;
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

<script>
  import csvImport from '../components/class/csvImport.vue'
  export default {
    name: 'customer',
    components: {
      csvImport,
    },
    data () {
      return {
        fileinput: '',
        data: [],
        columnCount: null,
        lines: null,
        importPatient: null,
        importAppoinment: null,
        provider_id: null,
      }
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
    created () {
      this.fetchProviders()
    },
    methods: {
      uploadCSV () {
        this.$children[0].parsed_data['num_of_records'] = this.data.length - 1
        this.$api.users.app.add_customers(this.$children[0].parsed_data).then(response => {
          this.data = []
          this.columnCount = null
          this.$children[0].colNum = null
          this.$children[0].lines = null
          this.$children[0].parsed_data = {}
          this.fileinput = null
          window.$('.csvFile').val(null)
        }, response => {
          this.data = []
          this.columnCount = null
          this.$children[0].colNum = null
          this.$children[0].lines = null
          this.$children[0].parsed_data = {}
          window.$('.csvFile').val(null)
          this.fileinput = null
        })
      },
      uploadAppoinments () {
        this.$children[0].parsed_data['provider_id'] = this.provider_id
        this.$children[0].parsed_data['num_of_records'] = this.data.length - 1
        this.$api.calendar.importAppointments(this.$children[0].parsed_data).then(response => {
          this.fileinput = null
          this.data = []
          this.columnCount = null
          this.$children[0].colNum = null
          this.$children[0].lines = null
          this.$children[0].parsed_data = {}
          this.lines = null
          window.$('.csvFile').val(null)
        }, response => {
          if (response.body.status === 'service not found') {
            alert('Before uploading you must add those services from the cvs file in account settings')
          } else if (response.body.status === 'email error') {
            alert('E-Mail ID is already registered with us')
          }
          this.fileinput = null
          this.data = []
          this.columnCount = null
          this.$children[0].colNum = null
          this.$children[0].lines = null
          this.$children[0].parsed_data = {}
          this.lines = null
          window.$('.csvFile').val(null)
        })
      },
      fetchProviders () {
        this.$api.calendar.getProviders().then(response => {
          if (response.body && response.body.length > 0) {
            this.provider_id = response.body[0].id
          }
        }, response => {
        })
      },
      onFileChangeP (e) {
        this.importPatient = true
        this.importAppoinment = false
        var files = e.target.files || e.dataTransfer.files
        if (!files.length) return
        this.createInput(files[0])
      },
      onFileChangeA (e) {
        this.importAppoinment = true
        this.importPatient = false
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
    },
  }
</script>