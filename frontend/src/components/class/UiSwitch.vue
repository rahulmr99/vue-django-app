<template>
  <div class="form-group">
    <label :class="classList">
      <input type="checkbox"
             class="switch-input"
             :value="value"
             :checked="isChecked"
             @change="handleChange">
      <span class="switch-label" :data-on="on" :data-off="off"></span>
      <span class="switch-handle"></span>
    </label>
    <label>{{label}}</label>
  </div>
</template>

<script>
  export default {
    props: {
      label: String,
      value: Boolean,
      uncheckedValue: {
        default: false,
      },
      type: {
        type: String,
        default: 'default',
      },
      variant: {
        type: String,
        default: '',
      },
      pill: {
        type: Boolean,
        default: false,
      },
      on: {
        type: String,
        default: null,
      },
      off: {
        type: String,
        default: null,
      },
      size: {
        type: String,
        default: null,
      },
    },
    computed: {
      classList () {
        return [
          'switch',
          this.switchType,
          this.switchVariant,
          this.switchPill,
          this.switchSize,
        ]
      },
      switchType () {
        return this.type ? `switch-${this.type}` : `switch-default`
      },
      switchVariant () {
        return this.variant ? `switch-${this.variant}` : `switch-secondary`
      },
      switchPill () {
        return !this.pill ? null : `switch-pill`
      },
      switchSize () {
        return this.size ? `switch-${this.size}` : ''
      },
      isChecked () {
        return this.value
      },
      isOn () {
        return !this.on ? null : true
      },
    },
    methods: {
      handleChange ({target: {checked}}) {
        this.$emit('input', !this.value)
        this.$emit('change', !this.value)
      },
    },
  }
</script>
