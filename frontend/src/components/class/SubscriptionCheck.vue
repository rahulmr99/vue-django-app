<template>
    <div id="managesubscription">
        <p id="subscriptionMsg">You can cancel, upgrade or downgrade your subscription, and update your billing details here</p>
        <p id="subtn">
            <b-button @click="modalShow = !modalShow" class="btn btn-primary" id="manageBtn">
                Manage your subscription
            </b-button>
        </p>
        <b-modal v-model="modalShow" class="subscribeModal">
            <iframe  src="https://bookedfusion.chargebee.com/portal/v2/login?forward=portal_main"
                scrolling="no"  frameborder="0" style="height: 500px; width: 100%;">
            </iframe>
        </b-modal>
    </div>
</template>

<script>
    export default {
      name: 'SubscriptionCheck',
      components: {
      },
      data () {
        return {
          modalShow: false,
        }
      },
    }
</script>

<style scoped>
    #manageBtn{
        text-align: center;
    }
    #subscriptionMsg{
        text-align: center;
    }
    #managesubscription{
        padding-top: 100px;
        padding-bottom: 100px;
        margin: auto;
    }
    #subtn{
        text-align: center;
    }
</style>
<style>

    .mngsub-modal-content{
        height:300px;
        width: 403px;
    }
    .mngsub-modal-content footer{
        display: none;
    }
    .mngsub-modal-content .modal-dialog {
        width: 400px;
        background-color: #00aced;
    }
    div.subscribeModal header,
    div.subscribeModal footer
    {
        display: none !important;
    }
    div.subscribeModal div.modal_body{
        padding: 10px;
    }
</style>