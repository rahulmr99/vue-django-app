<template>
  <div>
    <notifications group="success"
                   :width="500"
                   animation-name="v-fade-left"
                   position="top right">
      <template slot="body" slot-scope="props">
        <div class="noty-success">
          <div class="noty-success-icon">
            <i class="fa fa-check-circle"></i>
          </div>
          <div class="noty-success-content">
            <div class="noty-success-title">
              {{props.item.title}}
            </div>
            <div class="noty-success-text"
                 v-html="props.item.text"></div>
          </div>
          <div class="noty-success-close"
               @click="props.close">
            <i class="icon ion-android-close"></i>
          </div>
        </div>
      </template>
    </notifications>
    <notifications group="app" position="top right" classes="vue-notification vue-app-notification"/>
  </div>
</template>

<style lang="scss">
  .noty-success {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    text-align: left;
    font-size: 13px;
    margin: 5px;
    margin-bottom: 0;
    align-items: center;
    justify-content: center;
    &, & > div {
      box-sizing: border-box;
    }
    background: #E8F9F0;
    border: 2px solid #D0F2E1;
    .noty-success-icon {
      flex: 0 1 auto;
      color: #15C371;
      font-size: 32px;
      padding: 0 10px;
    }
    .noty-success-close {
      flex: 0 1 auto;
      padding: 0 20px;
      font-size: 16px;
      opacity: 0.2;
      cursor: pointer;
      &:hover {
        opacity: 0.8;
      }
    }
    .noty-success-content {
      padding: 10px;
      flex: 1 0 auto;
      .noty-success-title {
        letter-spacing: 1px;
        text-transform: uppercase;
        font-size: 10px;
        font-weight: 600;
      }
    }
  }

  .v-fade-left-enter-active,
  .v-fade-left-leave-active,
  .v-fade-left-move {
    transition: all .5s;
  }

  .v-fade-left-enter,
  .v-fade-left-leave-to {
    opacity: 0;
    transform: translateX(-500px) scale(0.2);
  }

  // vue notification default style
  .vue-app-notification {
    margin: 50px 5px 5px;
  }
</style>
