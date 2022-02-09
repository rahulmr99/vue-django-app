import Vue from '../vue-resorse-custom'

export const getAllCategory = () => Vue.http.get(`api/v1/service_category/?format=json`)

export const app = {
  deleted: (params) => Vue.http.delete(`api/v1/service_category/${params}/`),
  add: (obj) => Vue.http.post(`api/v1/service_category/`, obj),
  update: (id, obj) => Vue.http.patch(`api/v1/service_category/${id}/`, obj),
}
