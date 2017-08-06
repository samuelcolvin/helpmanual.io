const webpack = require('webpack')
const path = require('path')

module.exports = {
  entry: {
    main: path.resolve(__dirname, 'js-src/main.js')
  },
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, 'static/js'),
    publicPath: '/static/js/',
  },
  devtool: 'source-map',
  externals: {
    jquery: 'jQuery'
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: [{
          loader: 'babel-loader',
          options: {
            presets: [['env', {
              loose: true,
              targets: {browsers: ['last 2 versions']}
            }]]
          }
        }]
      }
    ]
  }
}
