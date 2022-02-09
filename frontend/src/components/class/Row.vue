<template>
  <div class="row">
    <div class="col-sm-12">
      <div class="form-group" :class="[{'required': required }]">
        <label v-if="label">{{label}}</label>
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    required: {
      type: Boolean,
    },
    label: {
      type: String,
    },
  },
  methods: {
    updateValue (val) {
      this.$emit('input', val)
    },
  },
}
</script>
