<template>
    <div class='credit-card-inputs'>
        <div class="row">
            <div class="col-md-12">
               <span>
                   <i class="fa fa-question-circle" style="margin-left: 67%; color: rgba(22, 122, 198, 0.63);"></i>
               </span>
                <span>
                    <a href="#" class="why-cc" v-on:mouseover="mouseOver" v-on:mouseleave="mouseOver" >Why do we ask for your cc?
                        <span v-show="cc_tooltip_active">We ask for your credit card to prevent interruption of your BookedFusion account should you decide to keep your account active once your trial expires. Your credit card will not be charged during your 21-day trial. If you decide that BookedFusion isn’t for you, you can cancel anytime.</span>
                    </a>
                </span>
            </div>
        </div>
        <div class="row">
            <div class="col-md-3 col-sm-3 col-3">
                <label class="sansationbold control-label">Card Number:</label>
            </div>
            <div class="col-md-9 col-sm-9 col-sansationbold user-card-number" :class='{ complete }'>
                <card-number class='stripe-element card-number form-control input-lg stripe-input'
                             ref='cardNumber'
                             v-bind:id='{here:ended}'
                             stripe='pk_live_wVuUyG2V97AC1V3G1YVnQgDJ'
                             :options='options'
                             @change='expiry = $event.complete'
                />
            </div>
        </div>
        <div class="row">
            <div class="col-md-3 col-sm-3 col-3">
                <label class="row sansationbold control-label exp-label">Expiration </label>
                <label class="row sansationbold control-label exp-label">Date:</label>
            </div>
            <div class="col-md-3 col-sm-3 col-3 sansationbold user-card-expiry" :class='{ complete }'>
                <card-expiry class='stripe-element card-expiry form-control input-lg stripe-input'
                             ref='cardExpiry'
                             stripe='pk_live_wVuUyG2V97AC1V3G1YVnQgDJ'
                             :options='options'
                             @change='expiry = $event.complete'
                />
            </div>
            <label class="col-md-3 col-sm-3 col-3 sansationbold control-label cvc-label">CVC:</label>
            <div class="col-md-3 col-sm-3 col-3 sansationbold user-card-cvc" :class='{ complete }'>
                <card-cvc class='stripe-element card-cvc form-control input-lg stripe-input'
                          ref='cardCvc'
                          stripe='pk_live_wVuUyG2V97AC1V3G1YVnQgDJ'
                          :options='options'
                          @change='cvc = $event.complete'
                />
            </div>
        </div>
        <div class="row">
            <div class="col-md-12 col-sm-12 col-12 " id="reason" v-if="reason">{{reason}}</div>
        </div>
        
            <div class="col-md-12 col-sm-12 col-12">
                <button type="button"  @click="pay" class="btn btn-primary btn-order-complete">Start My Free 21 Day Trial Now!</button>
            </div>
 
        <div class="row" style="margin-top: 15px;">
            <div class="payment-image" style="background-size: contain;background-repeat: no-repeat;"></div>
          <!-- <img src="/static/img/right.png" class="col-md-3 col-sm-3 col-3" style="padding: 5px 30px 5px 30px; height: 40px;"/> -->
          <!-- <img src="/static/img/stripe.png" class="col-md-6 col-sm-6 col-6" style="padding: 10px 90px 10px 90px; height: 40px;"/> -->
          <!-- <img src="/static/img/left.png" class="col-md-3 col-sm-3 col-3" style="padding: 5px 55px 5px 55px; height: 35px;"/> -->
        </div>
    </div>
</template>

<script>
    import { CardNumber, CardExpiry, CardCvc, createToken } from 'vue-stripe-elements-plus'
    export default {
      name: 'PaymentCardForm',
      props: ['stripe', 'options', 'myProp', 'data'],
      data () {
        return {
          complete: false,
          number: false,
          expiry: false,
          cvc: false,
          plan_id: null,
          reason: null,
          ended: false,
          cc_tooltip_active: false,
        }
      },
      components: {CardNumber, CardExpiry, CardCvc},
      methods: {
        callback (e) {
          console.log(e)
        },
        mouseOver: function () {
          this.cc_tooltip_active = !this.cc_tooltip_active
        },
        update () {
          this.complete = this.number && this.expiry && this.cvc
          // field completed, find field to focus next
          if (this.number) {
            if (!this.expiry) {
              this.$refs.cardExpiry.focus()
            } else if (!this.cvc) {
              this.$refs.cardCvc.focus()
            }
          } else if (this.expiry) {
            if (!this.cvc) {
              this.$refs.cardCvc.focus()
            } else if (!this.number) {
              this.$refs.cardNumber.focus()
            }
          }
        },
        pay () {
          this.planid(this.myProp)
          let _this = this
          createToken().then(function (result) {
            _this.submitSubscribe(result.token.id)
          })
        },
        planid (price) {
          if (price === 97) {
            this.plan_id = 'starter'
          } else if (price === 147) {
            this.plan_id = 'silver'
          } else if (price === 197) {
            this.plan_id = 'gold'
          }
        },
        submitSubscribe (token) {
          let obj = {
            'first_name': this.data.first_name,
            'last_name': this.data.last_name,
            'email': this.data.email,
            'password': this.data.password,
            'address': this.data.address,
            'city': this.data.city,
            'state': this.data.state,
            'zip_code': this.data.zip_code,
            'country': this.data.country,
            'country_code': this.data.country_code,
            'phone': this.data.phone,
            'stripe_token': token,
            'plan_id': this.plan_id,
          }
          let fusion = this
          this.$api.billing.subscribe(obj).then(response => {
            window.location.href = 'https://bookedfusion.com/welcome.html'
          }, response => {
            fusion.reason = response.body.reason
          })
        },
      },
      beforeMount () {
      },
      created: function () {
      },
      watch: {
        number () {
          this.update()
        },
        expiry () {
          this.update()
        },
        cvc () {
          this.update()
        },
      },
    }
</script>

<style type="text/css" media="screen">
  @import "https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700&display=swap"
</style>

<style scoped>


    .payment-image{
    width: 75%;
    height: 140px;
    margin: auto;
    background: url(/static/img/payment.webp);
    margin-top: 10px;
    }


    @font-face {
        font-family: sansationbold;
      src: url('/static/sansation/Sansation_Bold.ttf');
    }
    @font-face {
        font-family: sansationregular;
      src: url('/static/sansation/Sansation_Regular.ttf');
    }
    #reason{
        display: block;
        width: 100%;
        margin-top: 0.25rem;
        font-size: 99%;
        color: #f86c6b;
    }
    .why-cc{
        color: rgba(22, 122, 198, 0.63);
        font-size: 12px;
        font-weight: bold;
        position: relative;
    }

    .why-cc span{
        position: absolute;
        z-index: 999;
        width: 270px;
        left: 100%;
        margin-left: -270px;
        color: #fff;
        top: -163px;
        background: #000;
        padding: 7px;
    }
    .sansationregular{
        font-family: 'sansationregular';
    }
    .sansationbold{
        font-family: 'sansationbold';
    }
    a:hover {
        text-decoration: none;
    }
    .user-card-number{
        margin-bottom: 3%;
        max-width: 70%;
    }
     .user-card-number#here{
        border: 1px solid red !important;
    }
    .user-card-expiry{
        float: left;
        max-width: 35%;
    }
    .user-card-cvc{
        margin-left: -12%;
        max-width: 20%;
    }
    .stripe-input{
        border: 1px solid rgb(204, 204, 204);
        box-shadow: rgb(238, 237, 238) 0px 4px 2px -2px;
        height: 30px;
        padding-bottom: 2px;
        padding-top: 2px;
    }
    .control-label{
        font-size: 15px;
        color: #525151;
        padding-left: 0px;
        padding-top: 8px;
    }
    .cvc-label{
        margin-left: 15%;
        margin-right: -3%
    }
    .btn-order-complete{
        font-family: 'Roboto', sans-serif;
        border-color: rgb(247,183,45);
        background: rgb(247,183,45);
        color: rgb(7,11,83);
        margin-top: 4%;
        font-size: 22px !important;
        font-weight: 500;
        border-radius: 0px;
        width: 104%;
        margin-left: -3%;
        text-transform: inherit;
    }
    .exp-label{
        margin-left: 1%;
        line-height: 0.5px;
    }
    .form-control.complete {
        border: 1px solid green;
    }
</style>
