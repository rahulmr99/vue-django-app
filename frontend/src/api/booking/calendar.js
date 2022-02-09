import Vue from '../vue-resorse-custom'

export const filterCalendarId = (obj) => Vue.http.post(`api/v1/calendar/filter_appointment/?format=json`, obj)
export const filterCalendarEvents = (obj) => Vue.http.post(`api/v1/calendar/get_main_calendar_from_date/?format=json`, obj)
export const getProviders = () => Vue.http.get(`api/v1/users/get_providers_private/?format=json`)

export const saveCalendar = (obj) => Vue.http.post(`api/v1/calendar/save_calendar_appointment/?format=json`, obj)
export const importAppointments = (obj) => Vue.http.post(`api/v1/calendar/import_appointments/?format=json`, obj)
export const deleteCalendar = (params) => Vue.http.delete(`api/v1/calendar/${params}/`)

export const cancel = (obj) => Vue.http.post(`api/v1/calendar/booking_cancel/?format=json`, obj)
export const getCalendar = (params) => Vue.http.get(`api/v1/calendar/checkin_booking_date/?format=json${params}`)
export const update = (obj) => Vue.http.post(`api/v1/calendar/save_calendar_appointment/?format=json`, obj)
