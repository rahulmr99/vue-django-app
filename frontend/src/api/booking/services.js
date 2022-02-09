import Vue from '../vue-resorse-custom'

export const getAllServices = () => Vue.http.get(`api/v1/service/?format=json`)

export const app = {
  deleted: (params) => Vue.http.delete(`api/v1/service/${params}/`),
  add: (obj) => Vue.http.post(`api/v1/service/`, obj),
  update: (id, obj) => Vue.http.patch(`api/v1/service/${id}/`, obj),
}
