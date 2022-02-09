<script>
  /**
   * To use this mixin,
   * 0. there must be a `form` in component's data
   * 1. call onFormSubmit from the component usually when save clicked
   * 2. implement onFormValidationSuccess to call API
   * 3. use onFormApiSaveFailed as the error handler in API call
   */
  const notImplementedError = new Error('Not implemented.')
  export default {
    name: 'formsMixin',
    data () {
      return {
        apiErrors: {},
        form: {}, // must add the fields and use them in templates
      }
    },
    methods: {
      // utility function to empty the form data
      clearData () {
        Object.keys(this.form).forEach(key => {
          this.form[key] = ''
        })
      },

      /**
       * recursively check any child component for error and scroll to it
       * @param component
       * @returns {boolean}
       */
      focusFirstStatus (component = this) {
        if (component.validateAll) { // this is Inp component
          component.validateAll() // trigger validation
          if (component.hasDanger) {
            component.$el.focus()
            return true
          }
        }

        let focused = false

        component.$children.some((childComponent) => {
          focused = this.focusFirstStatus(childComponent)
          return focused
        })

        return focused
      },

      /**
       * implement this to call save form to backend
       */
      onFormValidationSuccess () {
        throw notImplementedError
      },

      /**
       * catch form validation
       */
      onFormValidationFailed () {},

      /**
       * must be called when form is submitted. Triggers validation in all the child inputs
       */
      onFormSubmit () {
        this.$emit('apiErrors', {})

        if (this.focusFirstStatus()) {
          // for failed validation
          this.onFormValidationFailed()
        } else {
          // form is valid
          this.onFormValidationSuccess()
        }
      },

      /**
       * could be called when form is failed to be saved in the backend API
       */
      onFormApiSaveFailed (response) {
        this.apiErrors = response.body
        this.$notify({
          group: 'app',
          text: (this.apiErrors.non_field_errors && this.apiErrors.non_field_errors[0]) || 'Failed to save form.',
          type: 'error',
        })
        this.$emit('apiErrors', response.body)
      },
    },
  }
</script>
