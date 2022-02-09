<template>
  <modal class="" title="Add new service" v-model="$root.bus.services.add_form"
         @ok="$root.bus.services.add_form = false" effect="zoom">
    <div class="row">
      <div class="col-sm-6">
        <div class="form-group" v-bind:class="[{'has-danger': $root.bus.services.form_field_error.error_name }]">
          <label for="add-name">Name *</label>
          <input class="form-control" id="add-name" required v-model="$root.bus.services.form_field_data.name"
                 placeholder="Enter name" type="text">
        </div>
      </div>
      <div class="col-sm-6">
        <div class="form-group" v-bind:class="[{'has-danger': $root.bus.services.form_field_error.error_duration }]">
          <label for="add-duration">Duration *</label>
          <input class="form-control" id="add-duration" required v-model="$root.bus.services.form_field_data.duration"
                 placeholder="Enter duration" type="text">
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-6">
        <div class="form-group" v-bind:class="[{'has-danger': $root.bus.services.form_field_error.error_price }]">
          <label for="add-price">Price *</label>
          <input class="form-control" id="add-price" v-model="$root.bus.services.form_field_data.price"
                 placeholder="Enter price" type="text">
        </div>
      </div>
      <div class="col-sm-6">
        <div class="form-group has-error">
          <label class="caption">Currency</label>
          <select class="form-control" v-model="select">
            <option value="1">USD</option>
            <option value="2">EUR</option>
          </select>
        </div>
      </div>
    </div>
    <!--<div class="row">-->
    <!--<div class="col-sm-6">-->
    <!--<div class="form-group">-->
    <!--<label class="caption">Select Category</label>-->
    <!--<select class="form-control" v-bind="$root.bus.services.form_field_data.category">-->
    <!--<option value="-1" selected hidden>Select Category</option>-->
    <!--<option :value="item.id" v-for="item in $root.bus.services.category.category_list">-->
    <!--{{item.name}}-->
    <!--</option>-->
    <!--</select>-->
    <!--</div>-->
    <!--</div>-->
    <!--</div>-->
    <div class="row">
      <div class="col-sm-12">
        <div class="form-group">
          <label for="add-description">Description</label>
          <textarea rows="6" class="form-control" id="add-description"
                    v-model="$root.bus.services.form_field_data.description" placeholder="Enter note"></textarea>
        </div>
      </div>
    </div>
    <div slot="modal-footer" class="modal-footer">
      <button type="button" @click="saveService" class="btn btn-primary">Save changes</button>
    </div>
  </modal>
</template>

<script>
  import modal from '../class/ModalFormClass.vue'

  export default {
    name: 'customer-form',
    components: {
      modal,
    },
    data () {
      return {
        select: '1',
      }
    },
    methods: {
      saveService () {
        let obj = {
          name: this.$root.bus.services.form_field_data.name,
          duration: this.$root.bus.services.form_field_data.duration,
          price: this.$root.bus.services.form_field_data.price,
          currency: this.select,
          category: this.$root.bus.services.form_field_data.category,
          description: this.$root.bus.services.form_field_data.description,
          generalsettings: this.$root.bus.info.generalsettings_id,
        }
        this.$api.services.app.add(obj).then(response => {
          this.$emit('feetchServices')
          this.closeForm()
        }, response => {
          this.$root.bus.services.form_field_error.non_field_errors = response.body.non_field_errors
          this.$root.bus.services.form_field_error.error_name = response.body.name
          this.$root.bus.services.form_field_error.error_duration = response.body.duration
          this.$root.bus.services.form_field_error.error_price = response.body.price
          this.$root.bus.services.form_field_error.error_attendants = response.body.attendants
        })
      },
      closeForm () {
        this.$root.bus.services.form_field_data.name = null
        this.$root.bus.services.form_field_data.duration = null
        this.$root.bus.services.form_field_data.price = null
        this.$root.bus.services.form_field_data.currency = null
        this.$root.bus.services.form_field_data.category = null
        this.$root.bus.services.form_field_data.availabilities_type = null
        this.$root.bus.services.form_field_data.attendants = null
        this.$root.bus.services.form_field_data.description = null
        this.$root.bus.services.form_field_error.non_field_errors = null
        this.$root.bus.services.form_field_error.error_name = null
        this.$root.bus.services.form_field_error.error_duration = null
        this.$root.bus.services.form_field_error.error_price = null
        this.$root.bus.services.form_field_error.error_attendants = null
        this.$root.bus.services.add_form = false
      },
    },
  }
</script>
