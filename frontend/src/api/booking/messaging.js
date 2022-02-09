import Vue from '../vue-resorse-custom'
export const app = {
  appoinments: (obj) => Vue.http.get(`rasa-bot/sms/user/get-upcoming-appointments/` + obj.phone),
  tokenGeneration: () => Vue.http.get(`rasa-bot/chat/get-token/`),
  onOffAi: (obj) => Vue.http.post(`rasa-bot/on-off-ai/`, obj),
  getOnOffStatus: (obj) => Vue.http.get(`rasa-bot/ai-on-off-status/` + obj.phone),
  providerNumber: (obj) => Vue.http.post(`rasa-bot/get-provider-phone-number/`, obj),
  addMemberToChannel: (obj) => Vue.http.post(`rasa-bot/sms/user/add-member-to-channel/`, obj),
  validateNumber: (obj) => Vue.http.post(`rasa-bot/check-phone-no-is-valid/`, obj),
}
