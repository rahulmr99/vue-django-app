var path = require('path')
var utils = require('./utils')
var config = require('../config')
var vueLoaderConfig = require('./vue-loader.conf')
var webpack = require('webpack')
var WebpackCdnPlugin = require('webpack-cdn-plugin')

function resolve (dir) {
  return path.join(__dirname, '..', dir)
}

module.exports = {
  entry: {
    app: './src/main.js'
  },
  output: {
    path: config.build.assetsRoot,
    filename: '[name].js',
    publicPath: process.env.NODE_ENV === 'production'
      ? config.build.assetsPublicPath
      : config.dev.assetsPublicPath
  },
  resolve: {
    extensions: ['.js', '.vue', '.json'],
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
      '@': resolve('src')
    }
  },
  plugins: [
    new webpack.ProvidePlugin({
      Vue: ['vue/dist/vue.esm.js', 'default'],
      jQuery: 'jquery',
      $: 'jquery',
      'window.jQuery': 'jquery',
    }),
    new WebpackCdnPlugin({
      // prod: (process.env.NODE_ENV === 'production'),
      modules: [
        {
          name: 'jquery',
          var: 'jQuery',
        },
        {
          name: 'moment'
        },
        {
          name: 'lodash.defaultsdeep',
          var: 'defaultsDeep'
        },
        // {
        //   name: 'vue',
        //   var: 'Vue',
        //   path: 'dist/vue.js'
        // },
        {
          name: 'vue-router',
          path: 'dist/vue-router.js',
          var: 'VueRouter'
        },
        {
          name: 'vue-resource',
          path: 'dist/vue-resource.js',
          var: 'VueResource'
        },
        {
          name: 'flatpickr',
          style: 'dist/flatpickr.min.css'
        },
        {
          name: 'trumbowyg',
          var: 'jQuery.trumbowyg',
          style: 'dist/ui/trumbowyg.min.css'
        },
        {
          name: 'fullcalendar',
          var: '$.fullCalendar',
          style: 'dist/fullcalendar.css'
        },
        {
          name: 'vue-trumbowyg',
          var: 'VueTrumbowyg'
        },
        // {
        //   name: 'vue-notification',
        //   var: 'Notifications'
        // },
        // {
        //   name: 'bootstrap-vue',
        //   var: 'window[\'bootstrap-vue\']',
        //   style: 'dist/bootstrap-vue.css',
        //   path: 'dist/bootstrap-vue.js'
        // },
      ],
      publicPath: '/node_modules',
      prodUrl: '//cdn.jsdelivr.net/npm/:name@:version/:path'
    }),
  ],
  module: {
    rules: [
      {
        test: /\.(js|vue)$/,
        loader: 'eslint-loader',
        enforce: 'pre',
        include: [resolve('src'), resolve('test')],
        options: {
          formatter: require('eslint-friendly-formatter')
        }
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: vueLoaderConfig
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        include: [resolve('src'), resolve('test')]
      },
      {
        test: /\.(png|jpe?g|gif|svg)(\?.*)?$/,
        use: {
          loader: 'file-loader',
          options: {
            name: '[name].[hash:7].[ext]',
            // publicPath: '../../',
            outputPath: utils.assetsPath('img/')
          }
        }
      },
      {
        test: /\.(woff2?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
        use: {
          loader: 'file-loader',
          options: {
            name: '[name].[hash:7].[ext]',
            // publicPath: '../../',
            outputPath: utils.assetsPath('fonts/')
          }
        }
      }
    ]
  }
}
