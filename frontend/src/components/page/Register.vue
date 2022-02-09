<template>
  <div class="app flex-row align-items-center">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card mx-4">
            <div class="card-body p-4">
              <b-row>
                <b-col cols="8">
                  <h1>Register</h1>
                </b-col>
                <b-col>
                  <router-link :to="'/login'" class="nav-link text-right">Login</router-link>
                </b-col>
              </b-row>
              <p class="text-muted">Create your account</p>
              <b-row>
                <b-col cols="7">
                  <inp id="name" :required="true" icon="user" placeholder="First name" v-model="form.name"/>
                </b-col>
                <b-col>
                  <inp id="last_name" placeholder="Last name" v-model="form.last_name"/>
                </b-col>
              </b-row>
              <inp id="email" :required="true" type="email" icon="envelope" placeholder="Email" v-model="form.email"/>
              <inp id="phone" :required="true" icon="phone" placeholder="Phone number" v-model="form.phone"/>
              <inp id="password" :required="true" icon="lock" placeholder="Password" v-model="form.password"
                   type="password"/>

              <button type="button" class="btn btn-block btn-primary" @click="onFormSubmit()">
                <i class="icon-arrow-up"></i>
                Create Account
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
  import Inp from '../class/Inp'
  import FormMixin from '../mixins/formsMixin'

  export default {
    name: 'Register',
    components: {
      Inp,
      FormMixin,
    },
    mixins: [FormMixin],
    data () {
      return {
        form: {
          name: '',
          last_name: '',
          email: '',
          phone: '',
          password: '',
          is_admin: true,
          is_root_user: true,
        },
      }
    },
    methods: {
      onRegisterSuccess (response) {
        this.clearData()
        this.$notySuccess('Account created successfully')
        this.$notySuccess('Login to your account')
        this.$router.push({path: '/login'})
      },
      onRegisterFailed (response) {
        this.$notify({group: 'app', text: 'Failed to create user account.', type: 'error'})
        this.onFormApiSaveFailed(response)
      },
      onFormValidationSuccess () {
        this.$emit('apiErrors', {})
        this.$emit('validateAll')

        for (let inpChild of this.$children) {
          // if any of the input has error, halt form submission
          if (inpChild.hasDanger) return
        }

        // remove any auth token set locally
        localStorage.removeItem('key')
        // call api to create account
        this.$api.users.app.add(this.form).then(this.onRegisterSuccess, this.onRegisterFailed)
      },
    },
  }
</script>
