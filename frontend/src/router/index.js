import Vue from 'vue'
import Router from 'vue-router'
// Containers
import Full from '@/containers/Full'
// account related pages
import Login from '@/components/page/Login'
import Register from '@/components/page/Register'
import ForgotPassword from '@/components/page/ForgotPassword'
import ResetPassword from '@/components/page/ResetPassword'
//  Billing
import BillingInfo from '@/views/BillingInfo'
// Views
import Calendar from '@/views/Calendar'
import Customer from '@/views/Customer'
// import Service from '@/views/Service'
// import User from '@/views/User'
import Ratings from '../views/ratings/Ratings'
import Settings from '../views/settings/Settings'
import Links from '../views/ScheduleLinksPage.vue'
import CustomerBookedScript from '../views/CustomerBookedScript.vue'
import Caller from '../views/Caller'
// import VoiceMails from '../views/voicemails/VoiceMails'
import AccountSettings from '../views/accounts/Accounts'
import ImportPatients from '../views/ImportPatients'
import Messages from '../views/messages/Messages.vue'

Vue.use(Router)

export default new Router({
  mode: 'hash',
  linkActiveClass: 'open active',
  scrollBehavior: () => ({y: 0}),
  routes: [
    {
      path: '/',
      redirect: '/calendar',
      name: 'Home',
      component: Full,
      children: [
        {path: 'calendar', name: 'Calendar', component: Calendar},
        {path: 'customers', name: 'Customers', component: Customer},
        {path: 'import', name: 'ImportPatients', component: ImportPatients},
        // {path: 'services', name: 'Services', component: Service},
        // {path: 'users', name: 'Users', component: User}, # this will be removed in future
        {path: 'accounts', name: 'AccountSettings', component: AccountSettings},
        {path: 'settings', name: 'Settings', component: Settings},
        {path: 'ratings', name: 'Ratings', component: Ratings},
        {path: 'links', name: 'Links', component: Links},
        {path: 'customer-booked-script', name: 'Customer Booked Script', component: CustomerBookedScript},
        {path: 'caller', name: 'IVRS Calls', component: Caller},
        // {path: 'voicemails', name: 'VoiceMails', component: VoiceMails},
        {path: '/messages', name: 'Messages', component: Messages},
      ],
    },
    // authentication related views
    {path: '/login', name: 'login', component: Login},
    {path: '/register', name: 'signup', component: Register},
    {path: '/forgot-password', name: 'forgotpassword', component: ForgotPassword},
    {path: '/reset-password', name: 'resetpassword', component: ResetPassword},
    {path: '/signup', name: 'BillingInfo', component: BillingInfo},
  ],
  meta: {
    progress: {
      func: [
        {call: 'color', modifier: 'temp', argument: '#ffb000'},
        {call: 'fail', modifier: 'temp', argument: '#6e0000'},
        {call: 'location', modifier: 'temp', argument: 'top'},
        {call: 'transition', modifier: 'temp', argument: {speed: '1.5s', opacity: '0.6s', termination: 400}},
      ],
    },
  },
})
