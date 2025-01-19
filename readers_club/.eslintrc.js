module.exports = {
  root: true,
  env: {
    node: true
  },
  extends: [
    'plugin:vue/vue3-essential',
    '@vue/standard'
  ],
  parserOptions: {
    parser: '@babel/eslint-parser'
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-trailing-spaces': 'off', // Disable trailing spaces rule
    'no-multiple-empty-lines': ['off'], // Disable multiple empty lines rule
    'eol-last': 'off', // Disable end-of-line rule,
    'indent': 'off',
    'comma-dangle': 'off',
    'semi': 'off',
    'spaced-comment': 'off',
    'space-before-function-paren': 'off',
    'keyword-spacing': 'off',
  },
}
