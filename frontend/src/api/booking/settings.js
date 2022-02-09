import Vue from '../vue-resorse-custom'

export const getFeedbackReport = () => Vue.http.get(`api/v1/feedback/reports/?format=json`)
export const getRatingsSettings = () => Vue.http.get(`api/v1/ratings_settings/?format=json`)
export const getInitialSettings = () => Vue.http.get(`api/v1/initial_confirmation/?format=json`)
export const getReminderSettings = () => Vue.http.get(`api/v1/reminder/?format=json`)
export const getCancellationSettings = () => Vue.http.get(`api/v1/cancellation_settings/?format=json`)
export const getReschedulingSettings = () => Vue.http.get(`api/v1/reschedule_settings/?format=json`)

export const app = {
  getGeneralSettings: (id) => Vue.http.get(`api/v1/general_settings/${id}/?format=json`),
  save_general: (id, obj) => Vue.http.patch(`api/v1/general_settings/${id}/`, obj),
  save_ratings: (id, obj) => Vue.http.patch(`api/v1/ratings_settings/${id}/`, obj),
  save_initial: (id, obj) => Vue.http.patch(`api/v1/initial_confirmation/${id}/`, obj),
  save_reminder: (id, obj) => Vue.http.patch(`api/v1/reminder/${id}/`, obj),
  saveCancellationSettings: (id, obj) => Vue.http.patch(`api/v1/cancellation_settings/${id}/`, obj),
  saveReschedulingSettings: (id, obj) => Vue.http.patch(`api/v1/reschedule_settings/${id}/`, obj),
}
