<template>
  <div class="app flex-row align-items-center">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card mx-4">
            <div class="card-body p-4">
              <b-row>
                <b-col cols="8">
                  <h1>Forgot Password</h1>
                </b-col>
                <b-col>
                  <router-link :to="'/login'" class="nav-link text-right">Login</router-link>
                </b-col>
              </b-row>
              <p class="text-muted">Input your email ID to get password reset link</p>
              <inp id="email" :required="true" type="email" icon="envelope" placeholder="Email" v-model="form.email"/>
              <br/>
              <button type="button" class="btn btn-block btn-primary" @click="onFormSubmit()">
                Send Link
                <i class="icon-arrow-right"></i>
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
    name: 'ForgotPassword',
    components: {
      Inp,
      FormMixin,
    },
    mixins: [FormMixin],
    data () {
      return {
        apiErrors: {},
        form: {
          email: '',
        },
      }
    },
    methods: {
      onFormValidationSuccess () {
        // call api to check email is present in database
        this.$api.login.app.sendResetLink(this.form).then(response => {
          let email = this.form.email
          this.clearData()
          this.$notySuccess('An Email with confirmation code is sent to your Email ID')

          // redirect to next page
          this.$router.push({
            name: 'resetpassword',
            props: {
              form: {email: email},
            },
          })
        }, this.onFormApiSaveFailed)
      },
    },
  }
</script>
