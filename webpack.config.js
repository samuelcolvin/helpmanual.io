module.exports = {
  entry: './js-src/main.js',
  // remove output to supply it from command line
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
  }
}
