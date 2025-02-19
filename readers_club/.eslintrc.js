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
    'no-undef': 'off',
    "space-before-blocks": ["warn", "always"],
    "eqeqeq": ["warn", "always"],
    "space-in-parens": ["warn", "never"],
    "space-before-blocks": "off", // Disable the rule
    "eqeqeq": "off", // Disable the rule
    "space-in-parens": "off", // Disable the rule,
    "object-curly-newline": "off",
    "key-spacing": "off",
    "quotes": "off",
    "prefer-promise-reject-errors": "off",
    "quotes": "off",
    "object-curly-spacing": "off",
    "no-multi-spaces": "off",
    "camelcase": "off",
    "padded-blocks": "off",
    "quote-props": "off",
    "vue/multi-word-component-names": "off",
    "vue/no-textarea-mustache": "off",
    "prefer-const": "off",
    "no-unused-expressions" : "off",
    "no-unreachable" : "off",
    "no-unused-vars" : "off",
    "vue/no-unused-components" : "off",
    "comma-spacing": "off"
  },
}
