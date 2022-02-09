import Vue from '../vue-resorse-custom'

export const billingRegister = (obj) => Vue.http.post(`billing/register/?format=json`, obj)
export const subscribe = (obj) => Vue.http.post(`billing/subscribe/?format=json`, obj)
export const status = (obj) => Vue.http.get(`billing/status-subscription/?format=json`, obj)
