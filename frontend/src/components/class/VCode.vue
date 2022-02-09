<template>
  <div>
    <div class="code-toolbar">
      <button id="copyToClipboardBtn" class="btn" @click="copyElemCodeText"><i class="fa fa-clipboard"></i></button>
    </div>
    <pre>
      <code data-language="html" ref="code">
        <slot></slot>
      </code></pre>
  </div>
</template>

<script>
  export default {
    name: 'code',
    methods: {
      copyElemCodeText () {
        // select text in browser
        let textarea = document.createElement('textarea')
        textarea.style.height = 0
        document.body.appendChild(textarea)
        textarea.value = this.$refs.code.innerText
        textarea.select()

        // run copy command
        document.execCommand('Copy')
        this.$notySuccess('Text copied to clipboard')

        // cleanup element
        document.body.removeChild(textarea)
      },
    },
  }
</script>

<style scoped>
  pre {
    background: #fafafa;
  }

  .code-toolbar {
    position: absolute;
    right: 20px;
  }
</style>
