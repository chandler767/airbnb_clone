// webpack bundles js files into one file for react front-end
// module.exports represents configs for webpack
module.exports = {
    entry: "./js/app.js", //Entry
    output: {
	   filename: "./static/bundle.js", // oOutput filename
	   path: __dirname // out path
    },
    module: {
    	loaders: [
  	    {
      		test: /\.js$/,
      		loader: 'babel-loader',
      		exclude: /node_modules/,
      		query: {
      		    presets: ['es2015', 'react']
          }
        }
	   ]
    }
}
