<template>
  <div>
    <ServiceFormAdd ref="ServiceFormAdd" v-on:feetchServices="feetchServices"/>
    <ServiceFormUpdate ref="ServiceFormUpdate" v-on:feetchServices="feetchServices"/>
    <div class="row">
      <div class="col-sm-8">
        <div class="btn-group search-customer" role="group" aria-label="...">
          <button @click="addServiceForm" class="btn btn-success btn-sm" type="button"><i
            class="fa fa-plus"></i> Add
          </button>
          <button @click="updateServiceForm"
                  v-if="$root.bus.services.choice_id"
                  class="btn btn-warning btn-sm" type="button"><i class="fa fa-pencil"></i> Update
          </button>
          <button @click="deleteServices" v-if="$root.bus.services.choice_id && !($root.bus.services.choice_item.is_default)"
                  class="btn btn-danger btn-sm" type="button"><i class="fa fa-trash"></i> Delete
          </button>
        </div>
      </div>
    </div>
    <table class="table">
      <thead>
      <tr>
        <th>Name</th>
        <th>Duration</th>
        <th>Price</th>
        <th>Currency</th>
        <th>Description</th>
      </tr>
      </thead>
      <tbody>
      <tr @dblclick.stop="updateServiceForm" v-for="item in $root.bus.services.services_list"
          @click="selectItem(item)"
          v-bind:class="[{ activew: item.id == $root.bus.services.choice_id }]">
        <td>{{ item.name }}</td>
        <td>{{ item.duration }}</td>
        <td>{{ item.price }}</td>
        <td>{{ item.currency| currency }}</td>
        <td>{{ item.description }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  import ServiceFormAdd from '../../components/forms/ServiceFormAdd.vue'
  import ServiceFormUpdate from '../../components/forms/ServiceFormUpdate.vue'

  export default {
    name: 'services',
    components: {
      ServiceFormAdd,
      ServiceFormUpdate,
    },
    mounted: function () {
      this.feetchServices()
    },
    created: function () {
      this.$root.bus.checkLogin()
    },
    methods: {
      feetchServices () {
        this.$api.services.getAllServices().then(response => {
          this.$root.bus.services.services_list = response.body
        }, response => {
        })
      },
      selectItem (item) {
        this.$root.bus.services.choice_id = item.id
        this.$root.bus.services.choice_item = item
      },
      updateServiceForm () {
        this.$refs.ServiceFormUpdate.closeForm()
        this.$root.bus.services.form_field_data.name = this.$root.bus.services.choice_item.name
        this.$root.bus.services.form_field_data.description = this.$root.bus.services.choice_item.description
        this.$root.bus.services.edit_form = true
      },
      deleteServices () {
        this.$api.services.app.deleted(this.$root.bus.services.choice_id).then(response => {
          this.feetchServices()
        }, response => {
        })
      },
      addServiceForm () {
        this.$refs.ServiceFormAdd.closeForm()
        this.$root.bus.services.add_form = true
      },
    },
  }
</script>

<style scoped>
  tr {
    cursor: pointer;
  }

  .search-customer {
    margin-bottom: 20px;
  }

  .appointments_cell {
    width: 30px;
  }

  tr {
    cursor: pointer;
  }

  .activew {
    background-color: #5bc0de;
  }

  .list-inline {
    display: flex;
    justify-content: center;
  }
</style>
