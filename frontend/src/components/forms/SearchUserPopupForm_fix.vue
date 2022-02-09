<template>
  <div v-show="$root.bus.calendar.search_user_popup_form" class="stub-form">
    <div id="myModal" class="modal">

      <!-- Modal content -->
      <div class="modal-content">
        <div class="row">
          <div class="col-sm-12">
            <div class="form-group">
              <input class="form-control" id="search_user" @keyup="searchCustomers" v-model="search_input"
                     placeholder="Enter request" type="text">
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-sm-12">
            <table class="table table-bordered table-sm">
              <thead>
              <tr>
                <th>First name</th>
                <th>Last name</th>
                <th>Email</th>
                <th>city</th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="item in find_list" @click="selectItem(item)"
                  v-bind:class="[{ activew: item.id == choice_item.id }]">
                <td>{{ item.name }}</td>
                <td>{{ item.last_name }}</td>
                <td>{{ item.email }}</td>
                <td> {{ item.city }} </td>
              </tr>
              <tr v-if="Object.keys(find_list).length == 0">
                <td class="text-center" colspan="4"><h2>Empty</h2></td>
              </tr>
              </tbody>
            </table>
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
  export default {
    name: 'search-user-popup-form',
    data () {
      return {
        find_list: [],
        choice_item: {},
        search_input: null,
      }
    },
    methods: {
      searchCustomers () {
        if (this.search_input === '') {
          this.find_list = []
          return
        }
        this.$api.users.app.search(`${this.search_input}&is_customers=true`).then(response => {
          this.find_list = response.body.results
        }, response => {
        })
      },
      selectItem (item) {
        this.choice_item = item
        this.$root.bus.calendar.form_field_data.first_name = item.name
        this.$root.bus.calendar.form_field_data.last_name = item.last_name
        this.$root.bus.calendar.form_field_data.email = item.email
        this.$root.bus.calendar.form_field_data.address = item.address
        this.$root.bus.calendar.form_field_data.city = item.city
        this.$root.bus.calendar.form_field_data.phone = item.phone
        this.$root.bus.calendar.form_field_data.mobile = item.mobile
        this.$root.bus.calendar.form_field_data.zip_code = item.zip_code
        this.$root.bus.calendar.form_field_data.note = item.note
      },
      closeWindow () {
        this.$root.bus.calendar.search_user_popup_form = false
      },
    },
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

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
