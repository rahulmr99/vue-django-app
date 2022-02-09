<template>
  <modal class="" title="Edit service" v-model="$root.bus.services.category.edit_form" @ok="$root.bus.services.category.edit_form = false" effect="zoom">
    <div class="row">
      <div class="col-sm-12">
        <div class="form-group" v-bind:class="[{'has-danger': $root.bus.services.category.form_field_error.error_name }]">
          <label for="add-serv-name">Name *</label>
          <input class="form-control" id="add-serv-name" required v-model="$root.bus.services.category.form_field_data.name" placeholder="Enter name" type="text">
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-12">
        <div class="form-group">
          <label for="description">Description</label>
          <textarea rows="6" class="form-control" id="description" v-model="$root.bus.services.category.form_field_data.description" placeholder="Enter note"></textarea>
        </div>
      </div>
    </div>
    <div slot="modal-footer" class="modal-footer">
      <button type="button" @click="updateCategory" class="btn btn-primary">Update</button>
    </div>
  </modal>
</template>

<script>
  import modal from '../class/ModalFormClass.vue'

  export default {
    name: 'services-category-update',
    components: {
      modal,
    },
    data () {
      return {
      }
    },
    methods: {
      updateCategory () {
        let obj = {
          name: this.$root.bus.services.category.form_field_data.name,
          description: this.$root.bus.services.category.form_field_data.description,
          generalsettings: this.$root.bus.info.generalsettings_id,
        }
        this.$api.category.app.update(this.$root.bus.services.category.choice_id, obj).then(response => {
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
        this.$root.bus.services.category.edit_form = false
      },
    },
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
