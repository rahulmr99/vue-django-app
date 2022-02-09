<template>
  <div>
    <modal class="" :title="title" v-model="showForm"  effect="zoom" ref="modal">
      <b-row>
        <b-col>
          <inp :required="true" id="first-name" label="First Name" v-model="form.name"
               placeholder="Enter your first name"></inp>
        </b-col>
        <b-col>
          <inp id="last_name" label="Last name" :required="true" v-model="form.last_name"
               placeholder="Enter your last name"/>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <inp id="phone" v-model="form.phone" placeholder="Enter your phone" label="Phone Number"/>
        </b-col>
        <b-col>
          <inp id="email" label="Email" v-model="form.email" placeholder="Enter your email"
               type="email"/>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <div class="form-group">
            <label>Note</label>
            <textarea rows="6" class="form-control" name="note" v-model="form.note" placeholder="Enter note"></textarea>
          </div>
        </b-col>
      </b-row>
      <div slot="modal-footer" class="modal-footer">
        <!-- <b-btn v-if="editingUser" @click="showResetPasswordForm = true">Set password</b-btn> -->
        <button type="button" @click="saveUser" class="btn btn-primary">{{ submitButton }}</button>
      </div>
    </modal>
    <div v-show="showResetPasswordForm" class="stub-form">
      <div class="modal-mask">
        <div class="modal-wrapper">
          <div class="modal-container">
            <div class="row">
              <div class="col-sm-12">
                <h2>Update password</h2>
              </div>
              <div class="col-sm-12">
                <div class="form-group">
                  <label for="password1">Password 1</label>
                  <input class="form-control" id="password1" v-model="form.password1" placeholder="Enter new password"
                         type="text">
                </div>
              </div>
              <div class="col-sm-12">
                <div class="form-group">
                  <label for="password2">Password 2</label>
                  <input class="form-control" id="password2" v-model="form.password2" placeholder="Retry password"
                         type="text">
                </div>
              </div>
            </div>
            <div slot="modal-footer">
              <button type="button" @click="savePassword" class="btn btn-danger">Save</button>
              <button type="button" @click="showResetPasswordForm = false" class="btn btn-secondary">Cancel</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import modal from '../class/ModalFormClass.vue'
  import Inp from '../class/Inp'

  export default {
    name: 'customer-form',
    components: {
      modal,
      Inp,
    },
    props: {},
    data () {
      return {
        apiErrors: {},
        editingPatient: false,
        editingAdmin: false,
        editingUser: false,
        form: {
          name: '',
          last_name: '',
          email: '',
          password: '',
          phone: '',
          mobile: '',
          address: '',
          city: '',
          zip_code: '',
          note: '',
        },
        showForm: false,
        showResetPasswordForm: false,
      }
    },
    computed: {
      title () {
        if (this.editingAdmin) {
          this.submitButton = 'Update admin'
          return 'Update Admin'
        } else if (this.editingPatient) {
          this.submitButton = 'Update Patient'
          this.editingUser = true
          return 'Update Patient'
        } else if (!this.editingPatient) {
          this.submitButton = 'Add Patient'
          return 'Add New Patient'
        }
      },

    },
    created: function () {
      this.$parent.$on('updateUserInfo', this.updateUserInfo)
    },
    methods: {
      updateUserInfo (info) {
        this.resetForm()
        if (info === undefined) {
          this.editingPatient = false
        } else if (info.is_admin === undefined || false) {
          this.editingPatient = Boolean(info)
        } else {
          this.editingAdmin = Boolean(info)
        }
        if (info) {
          // update form data from the user information
          for (let key in this.form) {
            if (info.hasOwnProperty(key)) {
              this.form[key] = info[key]
            }
          }
        }
        this.showForm = true
      },
      savePassword () {
        let obj = {
          'email': this.form.email,
          'password1': this.form.password1,
          'password2': this.form.password2,
        }
        this.$api.users.app.update_password(obj).then(response => {
          this.showResetPasswordForm = false
          this.form.password1 = null
          this.form.password2 = null
        }, response => {
        })
      },
      failureCallback (response) {
        this.$notify({group: 'app', text: 'Failed to update user info.', type: 'error'})
        this.apiErrors = response.body
        this.$refs.modal.$emit('apiErrors', response.body)
      },
      successCallback () {
        if (this.$root.bus.getFormUserTypeIsProvider()) {
          this.$emit('fetchProviders')
        } else if (this.$root.bus.getFormUserTypeIsAdmin()) {
          this.$emit('fetchAdmins')
        } else if (this.$root.bus.getFormUserTypeIsCustomer()) {
          this.$emit('fetchCustomers')
        } else {
          this.$emit('fetchSecretaries')
        }

        let msg = this.editingPatient ? 'Updated user info' : 'Created user account successfully'
        this.$notify({group: 'app', text: msg, type: 'success'})
        this.resetForm()
      },
      submitForm () {
        let obj = Object.assign({
          is_provider: this.$root.bus.getFormUserTypeIsProvider(),
          is_admin: this.$root.bus.getFormUserTypeIsAdmin(),
          is_secretarie: this.$root.bus.getFormUserTypeIsSecretarie(),
          is_customers: this.$root.bus.getFormUserTypeIsCustomer(),
          generalsettings: this.$root.bus.info.generalsettings_id,
        }, this.form)

        if (this.editingUser) {
          // update user
          this.$api.users.app.update_customers(this.$root.bus.customers.choice_id, obj)
            .then(this.successCallback).catch(this.failureCallback)
        } else {
          // create user
          this.$api.users.app.add_customers(obj)
            .then(this.successCallback).catch(this.failureCallback)
        }
      },
      saveUser () {
        // remove any previously set errors from api
        this.$refs.modal.$emit('apiErrors', {})
        // when submit button is clicked, trigger call to validate all component validations
        // if all of them are valid, Then only we will submit the form
        this.$refs.modal.$emit('validateAll')
        for (let inpChild of this.$refs.modal.$children) {
          // if any of the input has error, halt form submission
          if (inpChild.hasDanger) return
        }
        this.submitForm()
      },
      resetForm () {
        Object.assign(this.$data, this.$options.data.call(this))
      },
    },
    mounted () {
      this.$on('resetUserForm', this.resetForm())
    },
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .server-header {
    cursor: pointer;
  }

  .edit-header {
    color: #1fa67b;
    font-size: 20px;
    text-align: center;
    font-weight: bold;
    padding-bottom: 20px;
  }

  .modal-mask {
    margin-top: 30px;
    position: absolute;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    /*background-color: rgba(0, 0, 0, .5);*/
    display: table;
    transition: opacity .3s ease;
  }

  .modal-wrapper {
    display: table-cell;
    vertical-align: middle;
  }

  .modal-container {
    width: 550px;
    margin: 0 auto;
    padding: 20px 30px;
    background-color: #fff;
    border-radius: 2px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, .33);
    transition: all .3s ease;
    font-family: Helvetica, Arial, sans-serif;
  }

  .modal-header h3 {
    margin-top: 0;
    color: #42b983;
  }

  .modal-enter .modal-container,
  .modal-leave-active .modal-container {
    -webkit-transform: scale(1.1);
    transform: scale(1.1);
  }

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
