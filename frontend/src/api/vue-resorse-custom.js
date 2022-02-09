import Vue from 'vue'
import VueResource from 'vue-resource'

Vue.use(VueResource)

const debug = (process.env.NODE_ENV === 'development')

// run the django server in port 8001 - ./manage.py runserver 0.0.0.0:8001
// const localBackendServerUrl = 'http://192.168.1.122:8001'
const localBackendServerUrl = 'http://127.0.0.1:8000/'
const urlMap = {
  localhost: localBackendServerUrl,
  'app.bookedfusion.com': 'https://secure.bookedfusion.com/',
  's-app.bookedfusion.com': 'https://s-secure.bookedfusion.com/',
}
Vue.http.options.root = debug ? localBackendServerUrl : urlMap[document.location.hostname]

Vue.updateAuthHeader = function () {
  let token = localStorage.getItem('key')
  if (token) {
    Vue.http.headers.common.Authorization = 'JWT ' + token
  }
}
Vue.updateAuthHeader()
export default Vue
