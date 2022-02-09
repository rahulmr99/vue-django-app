<template>
  <div>
    <div class="row">
      <div class="col-sm-12">
        <b-alert :show="good_save !== null" dismissible variant="success">
          {{ good_save }}
        </b-alert>
        <b-alert :show="errorsMsg" dismissible variant="error">{{ errorsMsg }}</b-alert>
      </div>
    </div>
    <div class="row">
      <div class="col-md-6 col-xs-12">
        <h2>Working plan</h2>
        <table class="table table-bordered table-sm">
          <thead>
          <tr>
            <th class="action-plan">###</th>
            <th class="day">Day</th>
            <th>Start</th>
            <th>End</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="item in working_plan_list">
            <td>
              <a v-if="!item.show" @click.prevent="item.show = true" href="#">edit</a>
              <a v-if="item.show" @click.prevent="saveWorkingPlan(item)" href="#">save</a>
            </td>
            <td>
              <div class="checkbox">
                <label class="labelcheck">
                  <input v-if="item.show" class="inputcheck"
                         v-model="item.enable" type="checkbox">
                  <span v-bind:class="[{ strike: !item.enable }]">{{ item.day | dayweek }}</span>
                </label>
              </div>
            </td>
            <td><span v-show="!item.show">{{ item.start }}</span>
              <input class="form-control" v-show="item.show" v-model="item.start" v-mask="'##:## AA'">
            </td>
            <td><span v-show="!item.show">{{ item.end }}</span>
              <input class="form-control" v-show="item.show" v-model="item.end" v-mask="'##:## AA'">
            </td>
          </tr>
          <tr v-show="Object.keys(working_plan_list).length == 0">
            <td class="text-center" colspan="4"><h2>Empty</h2></td>
          </tr>
          </tbody>
        </table>
      </div>
      <div v-show="!edit_break" class="col-md-6 col-xs-12">
        <h2>Breaks
          <button class="btn btn-primary btn-sm" @click="edit_break = true" type="button">
          Add Break
          </button>
        </h2>
        <table class="table table-bordered table-sm">
          <thead>
          <tr>
            <th class="action-plan">###</th>
            <th class="day">Day</th>
            <th>Start</th>
            <th>End</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="item in breaks_list">
            <td>
              <a v-show="!item.show" @click.prevent="item.show = true" href="#">edit</a>
              <a v-show="item.show" @click.prevent="updateProviderBreaks(item)" href="#">save</a>
              <a v-show="item.show" @click.prevent="deleteProviderBreaks(item)" href="#">delete</a>
            </td>
            <td>{{ item.day | dayweek }}</td>
            <td><span v-if="!item.show">{{ item.start }}</span>
              <input class="form-control" v-if="item.show" v-model="item.start" v-mask="'##:## AA'">
            </td>
            <td><span v-if="!item.show">{{ item.end }}</span>
              <input class="form-control" v-if="item.show" v-model="item.end" v-mask="'##:## AA'">
            </td>
          </tr>
          <tr v-if="Object.keys(breaks_list).length == 0">
            <td class="text-center" colspan="4"><h2>Empty</h2></td>
          </tr>
          </tbody>
        </table>
      </div>
      <div v-show="edit_break" class="col-sm-6">
        <h2>Add new break
          <button class="btn btn-secondary btn-sm" @click="closeAddForm" type="button">back</button>
        </h2>
        <div class="row">
          <div class="col">
            <div class="form-group">
              <label class="caption">Day</label>
              <select class="form-control" v-model="form.day">
                <option value="7" selected>Sunday</option>
                <option value="6">Saturday</option>
                <option value="5">Friday</option>
                <option value="4">Thursday</option>
                <option value="3">Wednesday</option>
                <option value="2">Tuesday</option>
                <option value="1">Monday</option>
              </select>
            </div>
          </div>
          <div class="col">
            <div class="form-group">
              <label class="caption">Start time</label>
              <input class="form-control" v-model="form.start" v-mask="'##:## AA'">
            </div>
          </div>
          <div class="col">
            <div class="form-group">
              <label class="caption">End time</label>
              <input class="form-control" v-model="form.end" v-mask="'##:## AA'">
            </div>
          </div>
        </div>
        <button type="button" @click="saveProviderBreaks" class="btn btn-primary">Save break</button>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'user-workingplan-admin-form',
    data () {
      return {
        form: {
          users: null,
          day: '7',
          start: '10:00 AM',
          end: '10:30 AM',
        },
        edit_break: false,
        good_save: null,
        error_start: null,
        error_end: null,
        working_plan_list: [],
        breaks_list: [],
      }
    },
    computed: {
      errorsMsg () {
        if (this.error_start) {
          return this.error_start[0]
        } else if (this.error_end) {
          return this.error_end[0]
        }
      },
    },
    methods: {
      closeAddForm () {
        this.edit_break = false
      },
      initForm (userId) {
        this.cleareErrorCaption()
        this.resetData()
        this.form.users = userId
        this.searchProviderWorkingPlan()
        this.searchProviderBreaks()
      },
      searchProviderWorkingPlan () {
        this.$api.users.getAllWorkingPlans(`&users=${this.form.users}`)
          .then(response => {
            this.working_plan_list = response.body.results
          }, response => {
          })
      },
      saveWorkingPlan (item) {
        this.$api.users.setWorkingPlans(item.id, item).then(response => {
          item.show = false
          this.good_save = 'Time save.'
          this.error_start = null
          this.error_end = null
        }, response => {
          this.error_start = response.body.start
          this.error_end = response.body.end
        })
      },
      searchProviderBreaks () {
        this.$api.users.getAllBreaks(`&users=${this.form.users}`).then(response => {
          this.breaks_list = response.body.results
        }, response => {
        })
      },
      saveProviderBreaks () {
        this.$api.users.createBreaks(this.form).then(response => {
          this.searchProviderBreaks()
          this.closeAddForm()
        }, response => {
        })
      },
      updateProviderBreaks (item) {
        this.$api.users.setBreaks(item.id, item)
          .then(response => {
            item.show = false
            this.good_save = 'Time break save.'
            this.error_start = null
            this.error_end = null
          }, response => {
            this.error_start = response.body.start
            this.error_end = response.body.end
          })
      },
      deleteProviderBreaks (item) {
        this.$api.users.deleteBreaks(item.id)
          .then(response => {
            this.searchProviderBreaks()
            item.show = false
            this.good_save = 'Break delete save.'
          }, response => {
          })
      },
      cleareErrorCaption () {
        this.good_save = null
        this.error_start = null
        this.error_end = null
      },
      resetData () {
        Object.assign(this.$data, this.$options.data.call(this))
      },
    },
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .activew {
    background-color: #5bc0de;
  }

  tr {
    cursor: pointer;
  }

  .inputcheck {
    left: 200px;
    vertical-align: middle;
  }

  .labelcheck {
    left: -20px;
    display: inline-block;
    vertical-align: middle;
  }

  .day {
    width: 110px;
  }

  .action-plan {
    width: 50px;
  }

  .strike {
    text-decoration: line-through;
  }
</style>
