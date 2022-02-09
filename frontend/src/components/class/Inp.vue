<template>
  <div class="form-group" :class="[{'has-danger': hasDanger, 'required':required}]">
    <div :class="[{'input-group':hasIcon}]">
      <label v-if="label" :for="id">{{label}} </label>
      <span v-if="hasIcon" class="input-group-addon">
        <i :class="iconClass"></i>
      </span>
      <slot name="formControl">
        <input :class="['form-control', hasDanger ? 'is-invalid':'']" :type="type" ref="input" :value="value"
               @input="emitValue()" :id="id" :placeholder="placeholder"
               v-bind="$attrs" :len="len" :maxLen="maxLen" @focusout="focusoutCallback" :name="getName">
      </slot>
      <div class="invalid-feedback">
        {{ invalidFeedback }}
      </div>
    </div>
  </div>
</template>

<script>
  /* eslint-disable no-useless-escape */
  import RegexPatterns from './regex_patterns'

  export default {
    props: {
      value: {},
      id: {},
      name: {},
      label: {
        default: '',
        type: String,
      },
      placeholder: {
        default: '',
        type: String,
      },
      len: {
        type: Number,
      },
      maxLen: {
        type: Number,
      },
      minLen: {
        type: Number,
      },
      required: {
        default: false,
        type: Boolean,
      },
      type: {
        default: 'text',
      },
      faicon: { // font-awesome icon
        type: String,
      },
      icon: { // line icon
        type: String,
      },
    },
    data: function () {
      return {
        focused: false,
        apiErrors: {},
      }
    },
    created: function () {
      this.$parent.$on('apiErrors', this.checkApiErrorFeedback)
      this.$parent.$on('validateAll', this.validateAll)
    },
    computed: {
      hasDanger () {
        return this.invalidFeedback !== ''
      },
      hasIcon () {
        return this.icon || this.faicon
      },
      getName () {
        return this.name || this.id
      },
      iconClass () {
        if (this.icon) {
          return `icon-${this.icon}`
        } else {
          return `fa fa-${this.faicon}`
        }
      },
      invalidFeedback () {
        if (!this.focused) {
          return ''
        }
        if (this.required && !(this.value)) {
          // check for required field
          return this.label + ' is required'
        } else if (this.maxLen && this.value.length > this.maxLen) {
          // check for length in case of string else check the actual value in case of number
          return this.label + ' should contain less than ' + this.maxLen + ' characters'
        } else if (this.minLen && this.value < this.minLen) {
          // check for minimum length
          return this.label + ' should contain more than ' + this.maxLen + ' characters'
        } else if (this.type === 'email' && this.value && !(this.value === '') && !this.validatePattern(RegexPatterns.emailPattern, this.value)) {
          // regex check for mail id
          return this.label + ' should be a valid e-mail ID'
        } else if (this.type === 'url' && !this.validatePattern(RegexPatterns.urlPattern, this.value)) {
          if (this.label === 'Link to Google Review') {
            return this.label + ' should be a valid URL ex.) http://google.com'
          } else {
            return this.label + ' should be a valid URL ex.) ex.) http://yelp.com'
          }
        } else if (this.apiErrors && this.id && this.apiErrors[this.id]) {
          // check for errors sent from api
          return this.apiErrors[this.id][0]
        }
        return ''
      },
    },
    methods: {
      // event handler
      checkApiErrorFeedback (errors) {
        this.focused = true
        this.apiErrors = errors
      },
      // event handler
      validateAll () {
        // since the error checks are all computed properties, they will get triggered automatically
        this.focused = true
      },
      // this propagates changes to parents
      emitValue () {
        this.apiErrors = {}
        this.$emit('input', this.$refs.input.value)
      },
      // on focusout event vaidate input
      focusoutCallback () {
        this.focused = true
      },
      // utility method can be moved anywhere.
      validatePattern (pattern, val) {
        return pattern.test(val)
      },
    },
  }
</script>
