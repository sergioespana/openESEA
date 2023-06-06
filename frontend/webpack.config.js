//const path = require('path');

module.exports = {
  // ...other configuration options

  module: {
    rules: [
      // ...other rules
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
        },
      },
    ],
  },

  // ...other configuration options
}
