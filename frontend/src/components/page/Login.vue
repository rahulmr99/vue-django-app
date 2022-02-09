<template>

  <div class="outer">
  <div class="middle">
    <div class="container">
    <div class="col-md-5 offset-md-4">
    <div class="inner">
    <div class="login-wrap">
      <div class="text-center">
        <img src="static/img/logo-new.png" width="60%">
      </div>
      
      <div v-if="error" class="alert alert-danger" role="alert">
        <!-- <strong>Oh snap!</strong> login error. -->
        Your password or email you enter is incorrect
        <a href="#" @click.prevent="error = null" class="close" data-dismiss="alert" aria-label="close">×</a>
      </div>
      <form v-on:submit.prevent="loginUser">

      <div class="login-inner">
        
        <div class="form-group">
          <label>Email</label>
          <input type="text" class="form-control" v-model="login" placeholder="Email address">
        </div>
        
        <div class="form-group">
          <label>Password</label>
          <input type="password" class="form-control" v-model="password" placeholder="password">
        </div>

        <button class="btn btn-block btn-lb" type="submit">Log In</button>

        <div class="text-right">
          <router-link :to="'/forgot-password'" class="nav-link">Forgot password?</router-link>
        </div>

      </div>
      </form>
    </div>
    </div>
  </div>
  </div>
  </div>
</div>
</template>


<style>
.outer {
  display: table;
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
}

.middle {
  display: table-cell;
  vertical-align: middle;
}

.inner {

}

.login-inner {
  -webkit-box-shadow: 0 1px 2px 0 rgba(34,36,38,.15);
    box-shadow: 0 1px 2px 0 rgba(34,36,38,.15);
    margin: 1rem 0;
    padding: 1em 1em;
    border-radius: .28571429rem;
    border: 1px solid rgba(34,36,38,.15);
    background: #fff;
 }

.login-inner label {    font-weight: 700;}

.login-inner .form-control {    border-radius: 3px;
    border-color: #d2d2d2;}

/* The container */
.cus-check {
  display: block;
  position: relative;
  padding-left: 28px;
  margin-bottom: 12px;
  cursor: pointer;
  font-size: 14px;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  font-weight: 500 !important;
}

/* Hide the browser's default checkbox */
.cus-check input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

/* Create a custom checkbox */
.checkmark {
    position: absolute;
    top: 2px;
    left: 0;
    height: 20px;
    width: 20px;
    background-color: #fff;
    border: 1px solid #d2d2d2;
    border-radius: 3px;
}



/* When the checkbox is checked, add a blue background */

/* Create the checkmark/indicator (hidden when not checked) */
.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

/* Show the checkmark when checked */
.cus-check input:checked ~ .checkmark:after {
  display: block;
}

/* Style the checkmark/indicator */
.cus-check .checkmark:after {
    left: 7px;
    top: 2px;
    width: 6px;
    height: 11px;
    border: solid #3a3a3a;
    border-width: 0 2px 2px 0;
    -webkit-transform: rotate(45deg);
    transform: rotate(45deg);
}


.btn-lb {    margin-top: 20px;
    margin-bottom: 15px;
    background: #0069ff;
    padding: 7px;
    color: #fff;
    font-weight: 600;
    border-radius: 4px;
     font-size: 18px !important;
    font-family: 'Roboto', sans-serif;
    border-color: rgb(247,183,45);
    background: rgb(247,183,45);
    color: rgb(7,11,83);
    font-weight: 500;
  }

</style>




</template>

<script>
  import Vue from '../../api/vue-resorse-custom'

  export default {
    name: 'Login',
    data () {
      return {
        error: false,
        login: null,
        password: null,
      }
    },
    mounted () {
      this.goHome()
    },
    methods: {
      goHome () {
        // if user is logged in then redirect to home page
        if (this.$root.bus.user_login) {
          this.$router.push({path: '/calendar'})
        }
      },
      loginUser () {
        this.$api.login.app.login({email: this.login, password: this.password}).then(response => {
          localStorage.setItem('key', response.body.token)
          this.error = false
          this.$root.bus.user_login = true
          Vue.updateAuthHeader()
          this.$root.bus.check_token()
          this.$root.bus.requestChatToken()
          this.goHome()
        }).catch(() => {
          this.error = true
        })
      },
    },
  }
</script>
