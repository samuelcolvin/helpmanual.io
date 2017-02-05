var webpack = require('webpack')

module.exports = {
  entry: './js-src/main.js',
  // remove output to supply it from command line
  // output: {path: __dirname + '/site/static/js', filename: 'main.js'},
  output: {path: __dirname + '/static/js', filename: 'main.js'},
  externals: {
    jquery: 'jQuery'
  },
  module: {
    loaders: [
      {
        test: /.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      }
    ]
  },
  plugins: [
    new webpack.optimize.UglifyJsPlugin({compress: {warnings: false}}),
    new webpack.optimize.DedupePlugin(),
    new webpack.optimize.OccurrenceOrderPlugin()
  ]
}
