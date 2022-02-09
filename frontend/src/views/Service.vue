<template>
  <div class="animated fadeIn">
    <div class="container-fluid">
      <div class="row main-route">
        <div class="col-md-12">
          <div class="row">
            <div class="col-sm-8">
              <div class="btn-group search-customer" role="group" aria-label="...">
                <button @click="addServiceCategoryForm" class="btn btn-success btn-sm" type="button">
                  <i class="fa fa-plus"></i> Add
                </button>
                <button @click="updateServiceCategoryForm"
                        v-if="Object.keys($root.bus.services.category.choice_item).length !== 0"
                        class="btn btn-warning btn-sm" type="button"><i class="fa fa-pencil"></i> Update
                </button>
                <button @click="deleteCategory"
                        v-if="Object.keys($root.bus.services.category.choice_item).length !== 0"
                        class="btn btn-danger btn-sm" type="button"><i class="fa fa-plus"></i> Delete
                </button>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-lg-12">
              <table class="table">
                <thead>
                <tr>
                  <th>Name</th>
                  <th>Description</th>
                </tr>
                </thead>
                <tbody>
                <tr @dblclick.stop="updateServiceCategoryForm"
                    v-for="item in $root.bus.services.category.category_list"
                    @click="selectItemCategory(item)"
                    v-bind:class="[{ activew: item.id == $root.bus.services.category.choice_id }]">
                  <td>{{ item.name }}</td>
                  <td>{{ item.description }}</td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import ServiceCategoryFormAdd from '../components/forms/ServiceCategoryFormAdd.vue'
  import ServiceCategoryFormUpdate from '../components/forms/ServiceCategoryFormUpdate.vue'

  export default {
    name: 'service',
    components: {
      ServiceCategoryFormAdd,
      ServiceCategoryFormUpdate,
    },
    mounted: function () {
      this.feetchCategory()
    },
    created: function () {
      this.$root.bus.checkLogin()
    },
    methods: {
      feetchCategory () {
        this.$api.category.getAllCategory().then(response => {
          this.$root.bus.services.category.category_list = response.body
        }, response => {
        })
      },
      deleteCategory () {
        this.$api.category.app.deleted(this.$root.bus.services.category.choice_id).then(response => {
          this.feetchCategory()
        }, response => {
        })
      },
      selectItemCategory (item) {
        this.$root.bus.services.category.choice_id = item.id
        this.$root.bus.services.category.choice_item = item
      },
      addServiceCategoryForm () {
        this.$refs.ServiceCategoryFormAdd.closeForm()
        this.$root.bus.services.category.add_form = true
      },
      updateServiceCategoryForm () {
        this.$refs.ServiceCategoryFormUpdate.closeForm()
        this.$root.bus.services.category.form_field_data.name = this.$root.bus.services.category.choice_item.name
        this.$root.bus.services.category.form_field_data.description = this.$root.bus.services.category.choice_item.description
        this.$root.bus.services.category.edit_form = true
      },
    },
    data: function () {
      return {
        activeTab: 0,
      }
    },
  }
</script>

<style lang="css">
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
