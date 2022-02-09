<template>
  <div v-show="$root.bus.users.provider.set_service_popup_form" class="stub-form">
    <div id="myModal" class="modal">

      <!-- Modal content -->
      <div class="modal-content">
        <div class="row">
          <div class="col-sm-12">
            <div class="form-group">
              <h2>Choose service</h2>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-sm-12">
            <div class="form-group">
              <div class="list-group">
                <a href="#" @click.prevent="selectItem(item)"
                   v-bind:class="[{ active: choice_item.indexOf(item.id) >= 0 }]" v-for="item in service_list"
                   class="list-group-item list-group-item-action flex-column align-items-start item-margin">
                  <div class="d-flex w-100 justify-content-between">
                    <h5 class="mb-1">{{ item.name }}</h5>
                    <small class="text-muted">{{ item.duration }} min.</small>
                  </div>
                  <p class="mb-1"> {{ item.description }}</p>
                  <small class="text-muted">Price {{ item.price }} {{ item.currency }}</small>
                </a>

              </div>
            </div>
          </div>
        </div>
        <div slot="modal-footer">
          <button type="button" @click="closeWindow" class="btn btn-danger">Close</button>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
  /* eslint-disable indent */

  export default {
    name: 'set-service-popup-form',
    data () {
      return {
        service_list: [],
        choice_item: [6],
      }
    },
    methods: {
      fetchService () {
        this.$api.services.getAllServices().then(response => {
          this.service_list = response.body
          this.choice_item = this.$root.bus.users.provider.choice_item.services
          this.$root.bus.users.provider.set_service_popup_form = true
        }, response => {
        })
      },
      saveService () {
        let obj = {
          'services': this.choice_item,
        }
        this.$api.users.app.update(this.$root.bus.users.provider.choice_id, obj).then(response => {
//          this.$emit('fetchProviders')
        }, response => {
        })
      },
      selectItem (item) {
        if (this.choice_item.indexOf(item.id) === -1) {
          this.choice_item.push(item.id)
        } else {
          this.choice_item.splice(this.choice_item.indexOf(item.id), 1)
        }
        this.saveService()
      },
      closeWindow () {
        this.$root.bus.users.provider.set_service_popup_form = false
      },
      activateWindow () {
        this.fetchService()
      },
    },
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .item-margin {
    margin-top: 5px;
  }

  /* The Modal (background) */
  .modal {
    display: block; /* Hidden by default */
    position: fixed; /* Stay in place */
    z-index: 9998; /* Sit on top */
    padding-top: 100px; /* Location of the box */
    left: 0;
    top: 0;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
    overflow: auto; /* Enable scroll if needed */
    background-color: rgb(0, 0, 0); /* Fallback color */
    background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */
  }

  /* Modal Content */
  .modal-content {
    position: relative;
    background-color: #fefefe;
    margin: auto;
    padding: 20px 30px;
    border: 1px solid #888;
    width: 60%;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    -webkit-animation-name: animatetop;
    -webkit-animation-duration: 0.4s;
    animation-name: animatetop;
    animation-duration: 0.4s
  }

  /* Add Animation */
  @-webkit-keyframes animatetop {
    from {
      top: -300px;
      opacity: 0
    }
    to {
      top: 0;
      opacity: 1
    }
  }

  @keyframes animatetop {
    from {
      top: -300px;
      opacity: 0
    }
    to {
      top: 0;
      opacity: 1
    }
  }

  /* The Close Button */
  .close {
    color: white;
    float: right;
    font-size: 28px;
    font-weight: bold;
  }

  .close:hover,
  .close:focus {
    color: #000;
    text-decoration: none;
    cursor: pointer;
  }

  .modal-header {
    padding: 2px 16px;
    background-color: #5cb85c;
    color: white;
  }

  .modal-body {
    padding: 2px 16px;
  }

  .modal-footer {
    padding: 2px 16px;
    background-color: #5cb85c;
    color: white;
  }
</style>
