module.exports = {
	root: true,
	env: {
		node: true,
	},
	extends: [
		'plugin:vue/recommended',
		'@vue/airbnb',
	],
	rules: {
		'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
		'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
		'max-len': ['error', { code: 80, tabWidth: 2 }],
		indent: ['error', 'tab'],
		'no-tabs': ['error', { allowIndentationTabs: true }],
		'linebreak-style': 0,
		'vue/html-indent': ['error', 'tab'],
		'vue/max-attributes-per-line': ['error', {
			singleline: 5,
			multiline: { max: 3 },
		}],
		'import/no-extraneous-dependencies': 0,
		'import/no-unresolved': 0,
		'no-return-assign': 0,
		'vue/no-template-shadow': 0,
		'import/extensions': ['error', 'always', {
			js: 'never',
			vue: 'never',
		}],
		'arrow-parens': ['error', 'as-needed', { requireForBlockBody: true }],
		'object-curly-newline': ['error', {
			ObjectPattern: { multiline: true, minProperties: 5 },
		}],
	},
	parserOptions: {
		parser: 'babel-eslint',
		sourceType: 'module',
	},
};
