module.exports = {
  devServer: {
    disableHostCheck: true,
  },
  chainWebpack: config => {
    config.module
      .rule('vue')
      .use('vue-loader')
        .tap(options => {
          console.log('hello world')
          isCustomElement: (tag) => {
            return tag.startsWith('stripe')
          }
          return options
        })
  }
}
