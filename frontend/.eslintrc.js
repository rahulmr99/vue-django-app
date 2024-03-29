// http://eslint.org/docs/user-guide/configuring

module.exports = {
  root: true,
  parser: 'babel-eslint',
  parserOptions: {
    sourceType: 'module',
    "ecmaVersion": 6,
  },
  env: {
    browser: true,
  },
  // https://github.com/feross/standard/blob/master/RULES.md#javascript-standard-style
  extends: ['standard'],
  // required to lint *.vue files
  plugins: [
    'html',
    'flowtype-errors'
  ],
  // add your custom rules here
  'rules': {
    // allow paren-less arrow functions
    'arrow-parens': 0,
    'comma-dangle': ['error', 'always-multiline'],
    // allow async-await
    'generator-star-spacing': 0,
    'object-curly-spacing': 0,
    // allow debugger during development
    'no-debugger': process.env.NODE_ENV === 'production' ? 2 : 0,
    'flowtype-errors/show-errors': 2
  }
}
