import Vue from '../vue-resorse-custom'

export const app = {
  token_check: (obj) => Vue.http.post(`token_check/`, obj),
  login: (obj) => Vue.http.post(`login/`, obj),
  sendResetLink: (obj) => Vue.http.post(`send-reset-link/`, obj),
  resetPassword: (obj) => Vue.http.put(`send-reset-link/`, obj),
}
