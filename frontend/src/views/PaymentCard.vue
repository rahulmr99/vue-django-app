<template>
    <div class="col-md-12">
        <div class=" right-side-content">
            <div class="my-form">
                <div class="row">
                    <h3 class="col-md-12 sansationbold main-title">Payment Information</h3>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <div class="plan-info-content">
                            <h5 class="col-md-12 sansationbold plan-title">Starter Plan</h5>
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group" style="padding: inherit;">
                                        <div class="checkbox">
                                            <input type="radio" name="plan" style="box-shadow: 0 4px 2px -2px #eeedee;" v-model="payment" v-bind:value='97' checked/>
                                            <i class="input-helper"></i>
                                        </div>
                                        <span class="sansationregular plan">Monthly - 21 days Free then $97 per month</span>
                                    </div>
                                </div>
                            </div>
                            <!-- <h5 class="col-md-12 sansationbold plan-title">Silver Plan</h5>
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group" style="padding: inherit;">
                                        <div class="checkbox">
                                            <input type="radio" name="plan" style="box-shadow: 0 4px 2px -2px #eeedee;" v-model="payment" v-bind:value='147'/>
                                            <i class="input-helper"></i>
                                        </div>
                                        <span class="sansationregular plan">Monthly - 14 days Free then $147 per month</span>
                                    </div>
                                </div>
                            </div> -->
                            <h5 class="col-md-12 sansationbold plan-title">Gold Plan</h5>
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group" style="padding: inherit;">
                                        <div class="checkbox">
                                            <input type="radio" name="plan" style="box-shadow: 0 4px 2px -2px #eeedee;" v-model="payment" v-bind:value='197' />
                                            <i class="input-helper"></i>
                                        </div>
                                        <span class="sansationregular plan">Monthly - 21 days Free then $197 per month</span>
                                    </div>
                                </div>
                            </div>
                            <div class="price-content">
                                <div class="price-heading-trial sansationregular">Amount Due Today</div>
                                <div class="sansationregular">$0</div>
                                <div class="price-heading-trial sansationregular">First Bill Amount</div>
                                <div class="sansationregular">${{ payment }}</div>
                                <p class="trial-note sansationregular">
                                    <span class="sansationbold">Note:</span>
                                    You will be billed this amount on <span id="trail-date">{{ trail_end_date }}</span>
                                    if you decide to keep your account active.
                                    No contracts, no setup fees, downgrade or cancel your account anytime with
                                    a single click from your dashboard…
                                </p>
                            </div>
                        </div>
                        <div class="clr">

                        </div>
                        <div class="form-content">
                            <h3 class="col-md-12 sansationbold p-t-3">Credit Card Information</h3>
                            <payment-card-form :myProp="payment" :data="data"></payment-card-form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Inp from '../components/class/Inp.vue'
    import FlagsDropdown from '../components/class/FlagsDropdown'
    import PaymentCardForm from '../components/forms/PaymentCardForm'
    export default {
      name: 'PaymentCard',
      props: ['udata'],
      components: {
        Inp,
        FlagsDropdown,
        PaymentCardForm,
      },
      data () {
        return {
          payment: 97,
          data: this.udata,
          trail_end_date: this.$moment().add(21, 'days').format('MMM D, YYYY'),
        }
      },
      mounted () {
        let cdnScript = document.createElement('script')
        cdnScript.setAttribute('src', 'https://cdn.ywxi.net/js/1.js')
        document.head.appendChild(cdnScript)
      },
    }
</script>


<style scoped>
    @font-face {
        font-family: sansationbold;
      src: url('/static/sansation/Sansation_Bold.ttf');
    }
    @font-face {
        font-family: sansationregular;
      src: url('/static/sansation/Sansation_Regular.ttf');
    }
    .sansationregular{
        font-family: 'sansationregular';
    }
    .sansationbold{
        font-family: 'sansationbold';
    }
    .right-side-content{
        color: #2a292e;
        padding-top: 2em;
        padding-left: 1em;
        padding-bottom: 2em;
    }
    .right-side-content .my-form {
        width: 100%;
    }
    .right-side-content .my-form .main-title{
        font-size: 30px;
        margin-bottom: 15px;
    }
    .right-side-content .my-form .plan-title{
        font-size: 22px;
        margin-bottom: -10px;
    }
    .plan-info-content{
        border: 1px solid #c9d7df;
        padding: 5px;
    }
    .right-side-content .my-form .plan-info-content .form-group span {
        font-size: 15px;
        color: #525151;
    }
    .price-content{
        border-top: 1px solid #c9d7df;
        padding-top: 10px;
        width: 95%;
        margin: 0 auto;
        font-size: 20px;
        color: #525151;
    }
    .price-heading-trial{
        width: 50%;
        float: left;
    }
    .price-content .trial-note {
        margin-top: 10px;
        font-size: 17px;
    }
    .plan{
        margin-left: 30px;
    }
    .clr{
        clear: both;
    }
    .p-t-3{
        padding-top: 4rem !important;
        font-size: 30px;
        margin-bottom: 15px;
        margin-left: -3.5%;
    }
    .checkbox {
        position: relative;
        margin-bottom: 20px;
    }
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
        border-radius:20px;
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
        border-radius:20px;
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
</style>
