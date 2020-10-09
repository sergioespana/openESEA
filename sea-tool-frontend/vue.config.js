module.exports = {
	css: {
		loaderOptions: {
			scss: {
				sourceMap: true,
				prependData: '@import "@/assets/sass/default/master";',
			},
		},
	},
	transpileDependencies: [
		'vuetify',
		'vuex-persist',
	],
};
