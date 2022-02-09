<template>
  <div class="animated fadeIn">
    <UserForm v-on:fetchAdmins="fetchAdmins"
              v-on:fetchProviders="fetchProviders"
              v-on:fetchSecretaries="fetchSecretaries"></UserForm>
    <UserFormPSetServices ref="UserFormPSetServices" v-on:fetchProviders="fetchProviders"></UserFormPSetServices>
    <b-modal hide-footer hide-header v-model="$root.bus.users.working_plan.edit_form" size="lg" no-close-on-esc>
      <b-container>
        <UserWorkingPlanForm ref="UserWorkingPlanForm"></UserWorkingPlanForm>
        <div slot="modal-footer">
          <button type="button" @click="$root.bus.users.working_plan.edit_form = false"
                  class="btn btn-danger">
            Close
          </button>
        </div>
      </b-container>
    </b-modal>
    <div class="container-fluid">
      <div class="row main-route">
        <div class="col-md-12">
          <b-card no-body>
            <b-tabs ref="tabs" card @input="setTabProperties">
              <b-tab title="Admins" active>
                <div class="row">
                  <div class="col-sm-8">
                    <div class="btn-group search-customer" role="group" aria-label="...">
                      <button @click="addUserForm" class="btn btn-success btn-sm" type="button">
                        <i class="fa fa-plus"></i> Add
                      </button>
                      <button @click="updateUserForm($root.bus.users.admin.choice_item)"
                              v-if="Object.keys($root.bus.users.admin.choice_item).length !== 0"
                              class="btn btn-warning btn-sm" type="button">
                        <i class="fa fa-pencil"></i> Update
                      </button>
                      <button @click="deleteUser($root.bus.users.admin.choice_id)"
                              v-if="Object.keys($root.bus.users.admin.choice_item).length !== 0"
                              class="btn btn-danger btn-sm" type="button">
                        <i class="fa fa-plus"></i> Delete
                      </button>
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-sm-12">
                    <!--Search admin-->
                    <div class="form-group">
                      <input class="form-control" id="search" @keyup="searchAdmins"
                             v-model="$root.bus.users.admin.search" placeholder="Search user" type="text">
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-lg-12">
                    <table class="table table-sm">
                      <thead>
                      <tr>
                        <th>First name</th>
                        <th>Last name</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>Note</th>
                      </tr>
                      </thead>
                      <tbody>
                      <tr @dblclick.stop="updateUserForm(item)" :key="item.id"
                          v-for="item in $root.bus.users.admin.admin_list" @click="selectAdminItem(item)"
                          v-bind:class="[{ activew: item.id == $root.bus.users.admin.choice_id }]">
                        <td>{{ item.name }}</td>
                        <td>{{ item.last_name }}</td>
                        <td>{{ item.email }}</td>
                        <td>{{ item.phone }}</td>
                        <td>{{ item.note }}</td>
                      </tr>
                      </tbody>
                    </table>
                    <ul class="pagination">
                      <li @click.prevent="paginatePreviousAdmin" v-if="this.$root.bus.users.admin.previous"
                          class="page-item">
                        <a class="page-link" href="#">Prev</a>
                      </li>
                      <li @click.prevent="paginateNextAdmin" v-if="this.$root.bus.users.admin.next" class="page-item">
                        <a class="page-link" href="#">Next</a>
                      </li>
                    </ul>
                  </div>
                </div>
              </b-tab>
              <b-tab title="Providers">
                <div class="row">
                  <div class="col-sm-8">
                    <div class="btn-group search-customer" role="group" aria-label="...">
                      <button @click="addUserForm" class="btn btn-success btn-sm" type="button">
                        <i class="fa fa-plus"></i> Add

                      </button>
                      <button @click="updateUserForm($root.bus.users.provider.choice_item)"
                              v-if="Object.keys($root.bus.users.provider.choice_item).length !== 0"
                              class="btn btn-warning btn-sm" type="button">
                        <i class="fa fa-pencil"></i> Update

                      </button>
                      <button @click="deleteUser($root.bus.users.provider.choice_id)"
                              v-if="Object.keys($root.bus.users.provider.choice_item).length !== 0"
                              class="btn btn-danger btn-sm" type="button">
                        <i class="fa fa-plus"></i> Delete

                      </button>
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-sm-12">
                    <!--Search admin-->
                    <div class="form-group">
                      <input class="form-control" id="searchp" @keyup="searchProviders"
                             v-model="$root.bus.users.provider.search" placeholder="Search user" type="text">
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-lg-12">
                    <table class="table table-sm">
                      <thead>
                      <tr>
                        <th>First name</th>
                        <th>Last name</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th class="appointments_cell">Services</th>
                        <th class="appointments_cell">Working Plan</th>
                      </tr>
                      </thead>
                      <tbody>
                      <tr @dblclick.stop="updateUserForm(item)" :key="item.id"
                          v-for="item in $root.bus.users.provider.provider_list" @click="selectProviderItem(item)"
                          :class="[{ activew: item.id == $root.bus.users.provider.choice_id }]">
                        <td>{{ item.name }}</td>
                        <td>{{ item.last_name }}</td>
                        <td>{{ item.email }}</td>
                        <td>{{ item.phone }}</td>
                        <td>
                          <a class="btn btn-secondary btn-sm btn-block" @click="setServiceShow()">
                            <i class="fa fa-lightbulb-o"></i>&nbsp; Show</a>
                        </td>
                        <td>
                          <a class="btn btn-secondary btn-sm btn-block" @click="showWorkingPlanForm(item)">
                            <i class="fa fa-lightbulb-o"></i>&nbsp; Show</a>
                        </td>
                      </tr>
                      </tbody>
                    </table>
                    <ul class="pagination">
                      <li @click.prevent="paginatePreviousPAdmin" v-if="this.$root.bus.users.provider.previous"
                          class="page-item">
                        <a class="page-link" href="#">Prev</a>
                      </li>
                      <li @click.prevent="paginateNextPAdmin" v-if="this.$root.bus.users.provider.next"
                          class="page-item">
                        <a class="page-link" href="#">Next</a>
                      </li>
                    </ul>
                  </div>
                </div>
              </b-tab>
              <b-tab title="Secretaries">
                <div class="row">
                  <div class="col-sm-8">
                    <div class="btn-group search-customer" role="group" aria-label="...">
                      <button @click="addUserForm" class="btn btn-success btn-sm" type="button">
                        <i class="fa fa-plus"></i> Add
                      </button>
                      <button @click="updateUserForm($root.bus.users.secretarie.choice_item)"
                              v-if="Object.keys($root.bus.users.secretarie.choice_item).length !== 0"
                              class="btn btn-warning btn-sm" type="button">
                        <i class="fa fa-pencil"></i> Update
                      </button>
                      <button @click="deleteUser($root.bus.users.provider.choice_id)"
                              v-if="Object.keys($root.bus.users.secretarie.choice_item).length !== 0"
                              class="btn btn-danger btn-sm" type="button">
                        <i class="fa fa-plus"></i> Delete
                      </button>
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-sm-12">
                    <!--Search admin-->
                    <div class="form-group">
                      <input class="form-control" id="searchs" @keyup="searchSecretaries"
                             v-model="$root.bus.users.secretarie.search" placeholder="Search user" type="text">
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-lg-12">
                    <table class="table table-sm">
                      <thead>
                      <tr>
                        <th>First name</th>
                        <th>Last name</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>Note</th>
                      </tr>
                      </thead>
                      <tbody>
                      <tr @dblclick.stop="updateUserForm(item)" :key="item.id"
                          v-for="item in $root.bus.users.secretarie.secretarie_list" @click="selectSecretarieItem(item)"
                          v-bind:class="[{ activew: item.id == $root.bus.users.secretarie.choice_id }]">
                        <td>{{ item.name }}</td>
                        <td>{{ item.last_name }}</td>
                        <td>{{ item.email }}</td>
                        <td>{{ item.phone }}</td>
                        <td>{{ item.note }}</td>
                      </tr>
                      </tbody>
                    </table>
                    <ul class="pagination">
                      <li @click.prevent="paginatePreviousSAdmin" v-if="this.$root.bus.users.secretarie.previous"
                          class="page-item">
                        <a class="page-link" href="#">Prev</a>
                      </li>
                      <li @click.prevent="paginateNextSAdmin" v-if="this.$root.bus.users.secretarie.next"
                          class="page-item">
                        <a class="page-link" href="#">Next</a>
                      </li>
                    </ul>
                  </div>
                </div>
              </b-tab>
            </b-tabs>
          </b-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  /* eslint-disable camelcase */

  import UserForm from '../components/forms/UserForm.vue'
  import UserFormPSetServices from '../components/forms/UserFormPSetServices.vue'
  import UserWorkingPlanForm from '../components/forms/UserWorkingPlanForm.vue'

  export default {
    name: 'users',
    components: {
      UserForm,
      UserWorkingPlanForm,
      UserFormPSetServices,
    },
    mounted: function () {
      this.fetchAdmins()
      this.fetchProviders()
      this.fetchSecretaries()
    },
    created: function () {
      this.$root.bus.checkLogin()
    },
    methods: {
      fetchAdmins () {
        if (this.$root.bus.users.admin.search === '') {
          this.$api.users.getAllAdmins(`&page=${this.$root.bus.users.admin.page}`).then(response => {
            this.$root.bus.users.admin.admin_list = response.body.results
            this.$root.bus.users.admin.next = response.body.next
            this.$root.bus.users.admin.previous = response.body.previous
            this.$root.bus.users.admin.count = response.body.count
          }, response => {
          })
        } else {
          this.searchAdmins()
        }
      },
      searchAdmins () {
        this.$api.users.app.search(`${this.$root.bus.users.admin.search}&is_admin=true&page=${this.$root.bus.users.admin.page}`).then(response => {
          this.$root.bus.users.admin.admin_list = response.body.results
          this.$root.bus.users.admin.next = response.body.next
          this.$root.bus.users.admin.previous = response.body.previous
          this.$root.bus.users.admin.count = response.body.count
        }, response => {
        })
      },
      fetchProviders () {
        if (this.$root.bus.users.provider.search === '') {
          this.$api.users.getAllPrividers(`&page=${this.$root.bus.users.provider.page}`).then(response => {
            this.$root.bus.users.provider.provider_list = response.body.results
            this.$root.bus.users.provider.next = response.body.next
            this.$root.bus.users.provider.previous = response.body.previous
            this.$root.bus.users.provider.count = response.body.count
          }, response => {
          })
        } else {
          this.searchProviders()
        }
      },
      searchProviders () {
        this.$api.users.app.search(`${this.$root.bus.users.provider.search}&is_provider=true&page=${this.$root.bus.users.provider.page}`).then(response => {
          this.$root.bus.users.provider.provider_list = response.body.results
          this.$root.bus.users.provider.next = response.body.next
          this.$root.bus.users.provider.previous = response.body.previous
          this.$root.bus.users.provider.count = response.body.count
        }, response => {
        })
      },
      fetchSecretaries () {
        if (this.$root.bus.users.secretarie.search === '') {
          this.$api.users.getAllSecretaries(`&page=${this.$root.bus.users.secretarie.page}`).then(response => {
            this.$root.bus.users.secretarie.secretarie_list = response.body.results
            this.$root.bus.users.secretarie.next = response.body.next
            this.$root.bus.users.secretarie.previous = response.body.previous
            this.$root.bus.users.secretarie.count = response.body.count
          }, response => {
          })
        } else {
          this.searchSecretaries()
        }
      },
      searchSecretaries () {
        this.$api.users.app.search(`${this.$root.bus.users.secretarie.search}&is_secretarie=true&page=${this.$root.bus.users.secretarie.page}`).then(response => {
          this.$root.bus.users.secretarie.secretarie_list = response.body.results
          this.$root.bus.users.secretarie.next = response.body.next
          this.$root.bus.users.secretarie.previous = response.body.previous
          this.$root.bus.users.secretarie.count = response.body.count
        }, response => {
        })
      },
      selectAdminItem (item) {
        this.$root.bus.users.admin.choice_id = item.id
        this.$root.bus.users.admin.choice_item = item
        this.fetchAdmins()
      },
      selectProviderItem (item) {
        this.$root.bus.users.provider.choice_id = item.id
        this.$root.bus.users.provider.choice_item = item
        this.fetchProviders()
      },
      selectSecretarieItem (item) {
        this.$root.bus.users.secretarie.choice_id = item.id
        this.$root.bus.users.secretarie.choice_item = item
        this.fetchSecretaries()
      },
      addUserForm () {
        this.$emit('updateUserInfo')
      },
      updateUserForm (info) {
        this.$emit('updateUserInfo', info)
      },
      deleteUser (id) {
        // todo: confirm with user before delete
        this.$api.users.app.deleted(id).then(response => {
          this.fetchAdmins()
          this.fetchProviders()
          this.fetchSecretaries()
        }, response => {
        })
      },
      paginateNextAdmin () {
        this.$root.bus.users.admin.page = this.$root.bus.users.admin.page + 1
        this.fetchAdmins()
      },
      paginatePreviousAdmin () {
        this.$root.bus.users.admin.page = this.$root.bus.users.admin.page - 1
        this.fetchAdmins()
      },
      paginateNextPAdmin () {
        this.$root.bus.users.provider.page = this.$root.bus.users.provider.page + 1
        this.fetchProviders()
      },
      paginatePreviousPAdmin () {
        this.$root.bus.users.provider.page = this.$root.bus.users.provider.page - 1
        this.fetchProviders()
      },
      paginateNextSAdmin () {
        this.$root.bus.users.secretarie.page = this.$root.bus.users.secretarie.page + 1
        this.fetchSecretaries()
      },
      paginatePreviousSAdmin () {
        this.$root.bus.users.secretarie.page = this.$root.bus.users.secretarie.page - 1
        this.fetchSecretaries()
      },
      showWorkingPlanForm (item) {
        this.$refs.UserWorkingPlanForm.initForm(item.id)
        this.$root.bus.users.working_plan.edit_form = true
      },
      setServiceShow () {
        this.$refs.UserFormPSetServices.activateWindow()
      },
      setTabProperties (index) {
        this.$root.bus.setFormUserType(index)
      },
    },

    data: function () {
      return {}
    },
  }
</script>

<style lang="css" scoped="true">
  .search-customer {
    margin-bottom: 20px;
  }

  .appointments_cell {
    width: 100px;
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
</style>
