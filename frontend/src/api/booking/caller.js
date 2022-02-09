import Vue from '../vue-resorse-custom'

export const getCallerToken = (companyId) => Vue.http.get(`ivrs/token/${companyId}`)
export const getVoiceMails = () => Vue.http.get(`api/v1/voicemail.json`)
export const deleteVoiceMail = (id, obj) => Vue.http.delete(`api/v1/voicemail/${id}/`, obj)

export const voiceConfigsUrl = 'api/v1/voicemail_config'
export const getVoiceConfigs = () => Vue.http.get(`${voiceConfigsUrl}.json`)
export const saveVoiceConfigs = (id, obj) => Vue.http.put(`${voiceConfigsUrl}/${id}/`, obj)

export const voiceBotConfigsUrl = 'api/v1/voicebot_config'
export const getVoiceBotConfigs = () => Vue.http.get(`${voiceBotConfigsUrl}.json`)
export const saveVoiceBotConfigs = (id, obj) => Vue.http.put(`${voiceBotConfigsUrl}/${id}/`, obj)

export const getTwilioNumber = (id) => Vue.http.get(`ivrs/get_twilio_number/?id=${id}`)
export const getNumbers = (areacode, countrycode) => Vue.http.get(`ivrs/get_numbers/?areacode=${areacode}&countrycode=${countrycode}`)
export const purchaseNumberpurchaseNumber = (number) => Vue.http.post(`ivrs/get_numbers/`, number)
