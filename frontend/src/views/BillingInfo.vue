<template>
   <div class="row row-bill">
       <div class="col-md-6 left-side">
           <div class="form-info text-center left-side-inner" >
             <img src="/static/img/booked-fusion-white-v2.png" alt="Booked Fusion Billing" class="bill-logo">
               <br>
               <br>
               <h1 class="form-title sansationbold">Finalize Your Account</h1>
               <h3 v-if="left" class="form-description sansationbold">Step 1: Account Information</h3>
               <h3 v-if="!left" class="form-description sansationbold">Step 2: Payment Option</h3>
           </div>
       </div>
       <div class="col-md-6 right-content-wrap">
           <div class="right-side-content" v-if="left">
               <div class="my-form" >
                   <div class="row">
                       <h3 class="col-md-12 sansationbold">Create Your Account</h3>
                   </div>
                   <div class="row" v-if="form.form_field_error.non_field_errors">
                       <div class="col-md-12 " id="reason" v-for="error in form.form_field_error.non_field_errors">{{error}}</div>
                   </div>
                   <form id="billing-form" name="billingForm" method="post">
                   <div class="row">
                       <div class="col-md-6">
                           <inp id="first_name" :required="true" class="sansationbold" style="box-shadow: 0 4px 2px -2px #eeedee;" v-model="form.first_name" placeholder="First name"  type="text"/>
                       </div>
                       <div class="col-md-6">
                           <inp id="last_name" :required="true" class="sansationbold" style="box-shadow: 0 4px 2px -2px #eeedee;" v-model="form.last_name" placeholder="Last name"  type="text"/>
                       </div>
                   </div>
                   <div class="row">
                       <div class="col-md-12">
                           <inp id="email" :required="true" class="sansationbold" style="box-shadow: 0 4px 2px -2px #eeedee;" v-model="form.email" placeholder="Email Address"  type="email"/>
                       </div>
                   </div>
                   <div class="row">
                       <div class=" col-md-12">
                           <inp id="work_phone" class="sansationbold" style="box-shadow: 0 4px 2px -2px #eeedee;" v-model="form.phone" :required="true" placeholder="Phone"  type="text"/>
                       </div>
                   </div>
                   <div class="row">
                       <h3 class="col-md-12 sansationbold">Password</h3>
                   </div>
                   <div class="row">
                       <div class=" col-md-12">
                           <inp id="password" class="sansationbold" v-model="form.password" style="box-shadow: 0 4px 2px -2px #eeedee;" :required="true" placeholder="Choose your password"  type="password"/>
                       </div>
                   </div>
                   <div class="row">
                       <h3 class="col-md-12 sansationbold">Billing Address</h3>
                   </div>
                   <div class="row">
                       <div class=" col-md-12">
                           <inp id="address" class="sansationbold" style="box-shadow: 0 4px 2px -2px #eeedee;" v-model="form.address" :required="true" placeholder="Address"  type="text"/>
                       </div>
                   </div>
                   <div class="row">
                       <div class="col-md-6">
                           <inp id="city" class="sansationbold" style="box-shadow: 0 4px 2px -2px #eeedee;" v-model="form.city" :required="true" placeholder="City"  type="text"/>
                       </div>
                       <div class="col-md-6">
                           <inp id="state" class="sansationbold" style="box-shadow: 0 4px 2px -2px #eeedee;" v-model="form.state" :required="true" placeholder="State"  type="text"/>
                       </div>
                   </div>
                   <div class="row">
                       <div class="col-md-6">
                           <inp id="zipCode" class="sansationbold" style="box-shadow: 0 4px 2px -2px #eeedee;" v-model="form.zip_code" :required="true" placeholder="Zip Code"  type="text"/>
                       </div>
                       <div class="col-md-6">
                           <flags-dropdown class="sansationbold" style="width: 100%; font-size: 11px !important;" v-on:change="optionCountrySelected" bill="1" showCountryName="1" ></flags-dropdown>
                       </div>
                   </div>
                   <div class="row" id="tc">
                       <div class="col-md-12">
                           <span class="checkbox">
                               <input type="checkbox" v-model="checked"/>
                               <i class="input-helper"></i>
                           </span>
                           <span class="terms-cond">
                               <label class="sansationbold" style="color: black">I accept the <a style="color: rgb(0, 105, 255) !important;" href="https://www.bookedfusion.com/terms-of-use.html" target="_blank">terms and conditions of use</a></label>
                           </span>
                       </div>
                   </div>
                   <br>
                       <div class="col-md-12" style="padding: 0">
                           <button type="button"  class="btn btn-primary btn-create-account" @click="registerBilling">
                               Create My Account
                           </button>
                       </div>
               </form>
           </div>
           </div>
           <payment-card v-if="!left" :udata="form"></payment-card>
       </div>

   </div>
</template>

<style type="text/css" media="screen">
  @import "https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700&display=swap"
</style>

<script>
    import Inp from '../components/class/Inp.vue'
    import FlagsDropdown from '../components/class/FlagsDropdown'
    import PaymentCard from './PaymentCard'
    export default {
      name: 'BillingInfo',
      components: {
        Inp,
        FlagsDropdown,
        PaymentCard,
      },
      data () {
        return {
          left: true,
          checked: false,
          form: {
            first_name: null,
            last_name: null,
            email: null,
            password: null,
            address: null,
            city: null,
            state: null,
            zip_code: null,
            country: null,
            country_code: null,
            phone: null,
            form_field_error: {
              first_name_error: null,
              last_name_error: null,
              email_error: null,
              password_error: null,
              address_error: null,
              city_error: null,
              state_error: null,
              zip_code_error: null,
              country_error: null,
              country_code_error: null,
              phone_error: null,
              non_field_errors: null,
            },
          },
        }
      },
      methods: {
        optionCountrySelected: function (data) {
          this.form.country = data.code.toUpperCase()
          this.form.country_code = data.phonecode
        },
        failureCallback (response) {
          this.apiErrors = response.body
          this.$emit('apiErrors', response.body)
        },
        registerBilling: function () {
          this.$emit('apiErrors', {})
          this.$emit('validateAll')
          let obj = {
            'first_name': this.form.first_name,
            'last_name': this.form.last_name,
            'email': this.form.email,
            'password': this.form.password,
            'address': this.form.address,
            'city': this.form.city,
            'state': this.form.state,
            'zip_code': this.form.zip_code,
            'country': this.form.country,
            'country_code': this.form.country_code,
            'phone': this.form.phone,
          }
          let _this = this
          this.$api.billing.billingRegister(obj).then(response => {
            _this.left = false
          }, response => {
            _this.form.form_field_error.non_field_errors = response.body.non_field_errors
            this.failureCallback(response)
          })
        },
      },
      created: function () {
      },
    }
</script>

<style scoped>

.btn-create-account{
    font-size: 22px !important;
    font-family: 'Roboto', sans-serif;
    border-color: rgb(247,183,45);
    background: rgb(247,183,45);
    color: rgb(7,11,83);
    font-weight: 500;
    border-radius: 0px;
    text-transform: inherit;
    width: 100%;
  }

#reason{
    display: block;
    width: 100%;
    margin-top: 0.25rem;
    font-size: 99%;
    color: #f86c6b;
}
.right-content-wrap {
    height: 100vh;
    overflow: auto;
}
.row-bill{
    margin: 0px;
    background-color: #fff;
}
@font-face {
    font-family: sansationbold;
  src: url('/static/sansation/Sansation_Bold.ttf');
}
@font-face {
    font-family: sansationregular;
  src: url('/static/sansation/Sansation_Regular.ttf');
}
.left-side{
    background-color:rgb(0, 105, 255);
    height: 100vh;
}
.left-side-inner{
    margin-top: 25%;
}
.bill-logo{
    text-align: center;
    width: 350px;
}
.sansationbold{
    font-family: 'sansationbold';
}
.sansationregular{
    font-family: 'sansationregular';
}
.form-title{
    color: #fff;
    font-size: 40px;
}
.form-description{
    color: #fff;
    font-size: 30px;
}
.right-side-content{
    color: #2a292e;
    padding-top: 2em;
    padding-left: 3em;
    padding-bottom: 2em;
}
.right-side-content .my-form {
    width: 100%;
}
.checkbox {
    position: relative;
    margin-bottom: 20px;
}
.terms-cond{
    margin-left: 7%;
    position: relative;
    top: 5px;
}
/*.btn-create-account{
    background-color: rgb(0, 105, 255);
    font-size: 22px !important;
    border-radius: 0px;
    font-family: 'sansationregular';
    text-transform: inherit;
    width: 100%;
}*/
.checkbox input {
    top: 0;
    left: 0;
    z-index: 1;
    cursor: pointer;
    opacity: 0;
    position: absolute;
}
.checkbox input:checked + .input-helper:before {
    border-color: #90a4ae;
}
.checkbox .input-helper:before,
.checkbox .input-helper:after {
    position: absolute;
    content: "";
    transition: all 200ms;
}
.checkbox .input-helper:before {
    left: 0;
    border: 1px solid #90a4ae;
}
.checkbox input {
    width: 23px;
    height: 23px;
}

.checkbox input:checked + .input-helper:before {
    background-color: rgb(0, 105, 255);
}
.checkbox input:checked + .input-helper:after {
    opacity: 1;
    -webkit-transform: rotate(45deg);
    -ms-transform: rotate(45deg);
    transform: rotate(45deg);
}
.checkbox .input-helper:before {
    top: 0;
    width: 23px;
    height: 23px;
    border-radius: 2px;
    color: #fff;
}
.checkbox .input-helper:after {
    left: 9px;
    top: 5px;
    width: 5px;
    height: 10px;
    border: solid white;
    border-width: 0 3px 3px 0;
    -webkit-transform: rotate(60deg);
    -ms-transform: rotate(60deg);
    transform: rotate(60deg);
}
@media screen and (max-width: 920px){
    .terms-cond{
        margin-left: 9%;
    }
}
@media screen and (max-width: 768px){
    .terms-cond{
        margin-left: 5%;
    }
}
@media screen and (max-width: 580px){
    .terms-cond{
        margin-left: 6%;
    }
}
@media screen and (max-width: 480px){
    .terms-cond{
        margin-left: 8%;
    }
}
@media screen and (max-width: 400px){
    .terms-cond{
        margin-left: 10%;
    }
}
@media screen and (max-width: 768px){
    .left-side{
        height: 425px;
    }
}
@media screen and (max-width: 768px){
    #tc{
        margin-top: 2%;
    }
}
@media screen and (max-width: 768px){
    .left-side-inner{
        margin-top: 20%;
    }
}
</style>

<style>
        .multiselect {
            font-size: 11px !important;
        }
        .multiselect__option--highlight {
            background: rgb(0, 105, 255);
            outline: none;
            color: #fff;
        }

        .multiselect__option--selected.multiselect__option--highlight {
            background: gray;
            color: #fff;
        }
        .multiselect__content-wrapper{
            border-bottom-left-radius: 0;
            border-bottom-right-radius: 0;
        }
</style>
