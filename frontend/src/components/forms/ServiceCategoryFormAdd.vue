<template>
  <modal class="" title="Add new category" v-model="$root.bus.services.category.add_form" @ok="$root.bus.services.category.add_form = false" effect="zoom">
    <div class="row">
      <div class="col-sm-12">
        <div class="form-group" v-bind:class="[{'has-danger': $root.bus.services.category.form_field_error.error_name }]">
          <label for="name">Name *</label>
          <input class="form-control" id="name" required v-model="$root.bus.services.category.form_field_data.name" placeholder="Enter name" type="text">
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-12">
        <div class="form-group">
          <label for="description">Description</label>
          <textarea rows="6" class="form-control" id="description" v-model="$root.bus.services.category.form_field_data.description" placeholder="Enter description"></textarea>
        </div>
      </div>
    </div>
    <div slot="modal-footer" class="modal-footer">
      <button type="button" @click="saveCategory" class="btn btn-primary">Save changes</button>
    </div>
  </modal>
</template>

<script>
  import modal from '../class/ModalFormClass.vue'

  export default {
    name: 'services-category-add',
    components: {
      modal,
    },
    data () {
      return {
      }
    },
    methods: {
      saveCategory () {
        let obj = {
          name: this.$root.bus.services.category.form_field_data.name,
          description: this.$root.bus.services.category.form_field_data.description,
          generalsettings: this.$root.bus.info.generalsettings_id,
        }
        this.$api.category.app.add(obj).then(response => {
          this.$emit('feetchCategory')
          this.closeForm()
        }, response => {
          this.$root.bus.services.category.form_field_error.non_field_errors = response.body.non_field_errors
          this.$root.bus.services.category.form_field_error.error_name = response.body.name
        })
      },
      closeForm () {
        this.$root.bus.services.category.form_field_data.name = null
        this.$root.bus.services.category.form_field_data.description = null
        this.$root.bus.services.category.form_field_error.non_field_errors = null
        this.$root.bus.services.category.form_field_error.error_name = null
        this.$root.bus.services.category.add_form = false
      },
    },
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
