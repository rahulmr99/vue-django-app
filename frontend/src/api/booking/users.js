import Vue from '../vue-resorse-custom'

export const getAllAdmins = (params) => Vue.http.get(`api/v1/users/?format=json&is_admin=true${params}`)
export const getAllSecretaries = (params) => Vue.http.get(`api/v1/users/?format=json&is_secretarie=true${params}`)
export const getAllPrividers = (params) => Vue.http.get(`api/v1/users/?format=json&is_provider=true${params}`)
export const getAllCustomers = (params) => Vue.http.get(`api/v1/customers/?format=json${params}`)

export const getAllWorkingPlans = (params) => Vue.http.get(`api/v1/working_plan/?format=json${params}`)
export const setWorkingPlans = (id, obj) => Vue.http.patch(`api/v1/working_plan/${id}/`, obj)

export const getAllBreaks = (params) => Vue.http.get(`api/v1/breaks/?format=json${params}`)
export const createBreaks = (obj) => Vue.http.post(`api/v1/breaks/`, obj)
export const setBreaks = (id, obj) => Vue.http.patch(`api/v1/breaks/${id}/`, obj)
export const deleteBreaks = (id) => Vue.http.delete(`api/v1/breaks/${id}/`)

export const app = {
  deleted: (params) => Vue.http.delete(`api/v1/users/${params}/`),
  search: (obj) => Vue.http.get(`api/v1/users/?search=${obj}`),
  update: (id, obj) => Vue.http.patch(`api/v1/users/${id}/`, obj),
  add: (obj) => Vue.http.post(`api/v1/users/`, obj),
  update_password: (obj) => Vue.http.post(`api/v1/users/update_password/`, obj),
  getGAuthUrl: () => Vue.http.get(`api/v1/users/get_gauth_link/`),
  revokeGoogleCredentials: () => Vue.http.delete(`api/v1/users/revoke_google_credentials/`),
  getCaller: (params) => Vue.http.post(`api/v1/users/getCaller/${params}`),

  deleted_customer: (params) => Vue.http.delete(`api/v1/customers/${params}/`),
  add_customers: (obj) => Vue.http.post(`api/v1/customers/`, obj),
  update_customers: (id, obj) => Vue.http.patch(`api/v1/customers/${id}/`, obj),

  getBusinessHours: () => Vue.http.get(`api/v1/working_plan/get_business_hours/?format=json`),
}
