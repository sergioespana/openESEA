module.exports = {
    devServer: {
      proxy: process.env.VUE_APP_ROOT_API // 'https://esea-api.herokuapp.com/' // 'http://localhost:8000' // http://127.0.0.1:8000/
    }
}
