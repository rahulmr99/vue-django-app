<template>
  <div class="app flex-row align-items-center">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card mx-4">
            <div class="card-body p-4">
              <b-row>
                <b-col cols="8">
                  <h1>Reset Password</h1>
                </b-col>
                <b-col>
                  <router-link :to="'/login'" class="nav-link text-right">Login</router-link>
                </b-col>
              </b-row>
              <p class="text-muted">Check your inbox for confirmation code. It will expire in 5 mins.</p>
              <inp id="email" :required="true" type="email" icon="envelope" placeholder="Email" v-model="form.email"/>
              <inp id="password" :required="true" type="password" icon="lock" placeholder="Enter new password"
                   v-model="form.password"/>
              <inp id="code" :required="true" icon="shield" placeholder="Enter confirmation code" v-model="form.code"/>
              <br/>
              <button type="button" class="btn btn-block btn-primary" @click="onFormSubmit()">
                <i class="icon-arrow-up"></i>
                Update password
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
    name: 'ResetPassword',
    components: {
      Inp,
    },
    data () {
      return {
        form: {
          email: '',
          password: '',
          code: '',
        },
      }
    },
    mixins: [FormMixin],
    methods: {
      onFormValidationSuccess () {
        // call api to check email is present in database
        this.$api.login.app.resetPassword(this.form).then(response => {
          this.clearData()
          this.$notySuccess('Your password is updated successfully')
          this.$router.push({name: 'login'})
        }, this.onFormApiSaveFailed)
      },
    },
  }
</script>
