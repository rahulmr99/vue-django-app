<template>
  <div>
    <app-noty></app-noty>
    <p v-if="!this.$root.bus.loading">Loading...</p>
    <router-view v-if="this.$root.bus.loading"></router-view>
    <vue-progress-bar></vue-progress-bar>
  </div>
</template>

<script>
  import appNoty from './components/appNotifications.vue'

  export default {
    name: 'app',
    components: {
      appNoty,
    },
  }
</script>
<style lang="scss">

@import url('https://fonts.googleapis.com/css?family=Roboto:300,300i,400,400i,500,500i,700,900');

body {font-family: 'Roboto', sans-serif;}


  // Import Main styles for this application
  @import '../scss/style';

   .app-header.navbar, .app-header.navbar .navbar-brand {
    height: 55px;
    background-color: #3b77e7;
    border-bottom: 1px solid #a4b7c1;
    box-shadow: 1px 3px 1px -1px #c1c1c1;
}

.caller-ph {    
    background: none;
    border: 0px;
    outline: none !important;
    }


.app-header.navbar .navbar-toggler {
    min-width: 50px;
    padding: .25rem 0;
    color: #fff;
    font-size: 20px;
    outline: none;
}

.app-header.navbar .navbar-toggler {
    min-width: 50px;
    padding: .25rem 0;
    color: #fff;
    font-size: 20px;
    outline: none;
}

.app-header.navbar .navbar-brand {
    display: inline-block;
    width: 220px;
    padding: .5rem 1rem;
    margin-right: 0;
    background-image: url(/static/img/logo.png) !important;
    background-repeat: no-repeat;
    background-position: 50%;
    background-size: 70px auto;
    background-color: #fff;
}

.flatpickr-day.today {
    border-color: #3b77e7;
    background: #3b77e7;
    color: #fff;
}

.sidebar .sidebar-nav {
    position: relative;
    -webkit-box-flex: 1;
    -ms-flex: 1;
    flex: 1;
    overflow-x: hidden;
    overflow-y: auto;
    -ms-overflow-style: -ms-autohiding-scrollbar;
    width: 220px;
    box-shadow: 1px 1px 1px 1px #c1c1c1;
    z-index: 2;
}


.sidebar {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-orient: vertical;
    -webkit-box-direction: normal;
    -ms-flex-direction: column;
    flex-direction: column;
    padding: 0;
    color: #fff;
    background: #ffffff;
}


.navbar .sidebar .dropdown-toggle, .sidebar .nav-link, .sidebar .navbar .dropdown-toggle {
    display: block;
    padding: .75rem 1rem;
    color: #767676;
    text-decoration: none;
    background: transparent;
    font-size: 16px;
    font-weight: 500;
}

.header-fixed .app-header {
    position: fixed;
    z-index: 100;
    width: 100%;
}

.sidebar .nav-link:hover, .sidebar .navbar .dropdown-toggle:hover, .navbar .sidebar .dropdown-toggle:hover, .sidebar .navbar .dropdown-toggle:hover, .navbar .sidebar .dropdown-toggle:hover {
    background: #f1f1f1;
    color: #8d8d8d;
}

.sidebar .nav-link:hover i, .sidebar .navbar .dropdown-toggle:hover i, .navbar .sidebar .dropdown-toggle:hover i {
    color: #8d8d8d;
}

.sidebar .nav-link.active, .sidebar .navbar .active.dropdown-toggle, .navbar .sidebar .active.dropdown-toggle {
    color: #3b77e7;
    background: #f1f1f1;
}

.sidebar .nav-link.active i, .sidebar .navbar .active.dropdown-toggle i, .navbar .sidebar .active.dropdown-toggle i {
    color: #3b77e7;
}

.sidebar .sidebar-nav::-webkit-scrollbar-thumb {
    height: 50px;
       background-color: #e3e3e3;
    background-clip: content-box;
    border-color: transparent;
    border-style: solid;
    border-width: 1px 2px;
}



.sidebar .sidebar-nav::-webkit-scrollbar-track {
    background-color: #ffffff;
    border-right: 1px solid #ffffff;
    border-left: 1px solid #ffffff;
}

.navbar-nav .nav-link, .navbar-nav .navbar .dropdown-toggle, .navbar .navbar-nav .dropdown-toggle {
    color: #ffffff !important;
}

.card {
    position: relative;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-orient: vertical;
    -webkit-box-direction: normal;
    -ms-flex-direction: column;
    flex-direction: column;
    min-width: 0;
    word-wrap: break-word;
    background-color: #fff;
    background-clip: border-box;
   webkit-box-shadow: -1px 0 2px rgba(0,0,0,0.15), 1px 0 2px rgba(0,0,0,0.15), 0 4px 8px rgba(0,0,0,0.15);
    box-shadow: -1px 0 2px rgba(0,0,0,0.15), 1px 0 2px rgba(0,0,0,0.15), 0 4px 8px rgba(0,0,0,0.15);
    border:0px;
}

.app-body .main {
    -webkit-box-flex: 1;
    -ms-flex: 1;
    flex: 1;
    min-width: 0;
   
}


.tabs { webkit-box-shadow: -1px 0 2px rgba(0,0,0,0.15), 1px 0 2px rgba(0,0,0,0.15), 0 4px 8px rgba(0,0,0,0.15);
    box-shadow: -1px 0 2px rgba(0,0,0,0.15), 1px 0 2px rgba(0,0,0,0.15), 0 4px 8px rgba(0,0,0,0.15);}


.fc-view-container {
    background-color: white !important;
}

.custom-search {
    background: #71a3f7;
    background-image: url(/static/img/search.png) !important;
    background-position-y: -29px;
    background-position-x: 6px;
    border: 0px;
    height: 34px;
    border-radius: 2px;
    outline: none;
    width: 350px;
    padding-left: 50px;
    -webkit-box-shadow: 0 2px 6px 0 rgba(0, 0, 0, 0.16), 0 0 0 1px rgba(0, 0, 0, 0.04);
    box-shadow: 0 2px 6px 0 rgba(0, 0, 0, 0.16), 0 0 0 1px rgba(0, 0, 0, 0.04);
    background-repeat: no-repeat;
}

.custom-search:focus { background:#fff; background-repeat: no-repeat;    background-position-x: 6px;
    background-position-y: -1px;}

.custom-search::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
    color: #fff;
    font-weight:500;
}

:focus::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
    color: #767676;
    font-weight:500;
}

.custom-search { color:#fff;}

.custom-search:focus { color :black;}


.card-header {
    padding: 0.75rem 1.25rem;
    margin-bottom: 0;
    background-color: #fdfdfd;
    border-bottom: 0px;
    background: #f2f2f2;
}

.card-header .nav.nav-tabs .nav-link.active, .card-header .nav.nav-tabs .navbar .active.dropdown-toggle, .navbar .card-header .nav.nav-tabs .active.dropdown-toggle {
    color: #3b77e7;
    background: none;
    border: 0px;
    border-bottom: 3px solid #3b77e7;
}

.card-header .nav.nav-tabs .nav-link, .card-header .nav.nav-tabs .navbar .dropdown-toggle, .navbar .card-header .nav.nav-tabs .dropdown-toggle {
    padding: 0.75rem 0.625rem;
    color: #536c79;
    border-top: 0;
    border: 0px;
    text-transform:uppercase;
}

.nav-tabs .nav-link:hover, .nav-tabs .navbar .dropdown-toggle:hover, .navbar .nav-tabs .dropdown-toggle:hover, .nav-tabs .nav-link:focus, .nav-tabs .navbar .dropdown-toggle:focus, .navbar .nav-tabs .dropdown-toggle:focus {
    border-color: #c2cfd6 #c2cfd6 #a4b7c1;
    background: #e6e6e6;
}

.card-header .nav.nav-tabs {
    margin-top: -0.75rem;
    margin-bottom: -0.75rem;
    border-bottom: 0;
    outline: none;
}
.call {font-size: 23px;
    color: #fff;
    padding-right: 10px;
    padding-top: 3px;}

.voice-call {      
    background: #4ab41c !important;
    border-radius: 4px;
    color: #ffffff !important;
    font-size: 15px;
    margin-left: 10px;
    border: 0px;
        -webkit-box-shadow: 0 6px 10px 0 rgba(0, 0, 0, 0.14), 0 1px 18px 0 rgba(0, 0, 0, 0.12), 0 3px 5px -1px rgba(0, 0, 0, 0.2);
    box-shadow: 0 6px 10px 0 rgba(0, 0, 0, 0.14), 0 1px 18px 0 rgba(0, 0, 0, 0.12), 0 3px 5px -1px rgba(0, 0, 0, 0.2);}

.play-stop {color: #ffffff !important;
    background-color: #3b77e7 !important;
    border-color: #3b77e7 !important;
    -webkit-box-shadow: 0 6px 10px 0 rgba(0, 0, 0, 0.14), 0 1px 18px 0 rgba(0, 0, 0, 0.12), 0 3px 5px -1px rgba(0, 0, 0, 0.2);
    box-shadow: 0 6px 10px 0 rgba(0, 0, 0, 0.14), 0 1px 18px 0 rgba(0, 0, 0, 0.12), 0 3px 5px -1px rgba(0, 0, 0, 0.2);}


.mt10 {    margin-top: 10px;} 

.play-stop {    border-radius: 50%;
    width: 35px;
    height: 35px;
    font-size: 12px;
    text-align: center;
    padding-left: 12px;}   
.form-control:disabled, .form-control[readonly] {
       background-color: #f8f8f8;
    opacity: 1;
}    

.switch-primary > .switch-input:checked ~ .switch-label {
    background: #3b77e7 !important;
    border-color: #3b77e7;
}

.btn-primary {
    color: #fff;
    background-color: #3b77e7;
    border-color: #3b77e7;
    border-radius: 3px;
    text-transform: uppercase;
    padding: 5px 20px;
   box-shadow: 0px 0px 5px 1px #828282;
}

.btn-primary:hover {
    color: #fff;
    background-color: #3b77e7;
    border-color: #3b77e7;
}

.page-item.active .page-link, .pagination-datatables li.active .page-link, .pagination li.active .page-link, .page-item.active .pagination-datatables li a, .pagination-datatables li .page-item.active a, .pagination-datatables li.active a, .page-item.active .pagination li a, .pagination li .page-item.active a, .pagination li.active a {
    z-index: 1;
    color: #fff;
    background-color: #3b77e7;
    border-color: #3b77e7;
}

.btn-primary:not(:disabled):not(.disabled):active, .btn-primary:not(:disabled):not(.disabled).active, .show > .btn-primary.dropdown-toggle {
    color: #fff;
    background-color: #3b77e7;
    border-color: #3b77e7;
}

.app-body .main {
    -webkit-box-flex: 1;
    -ms-flex: 1;
    flex: 1;
    min-width: 0;
    background: #fafafa;
}

.tab-content {    border: 1px solid #d6d9da;
    border-left: 0px;
    border-right: 0px;
    border-bottom: 0px;}

.fc-event, .fc-event-dot {
    background: #3b77e7 !important;
    color: #fff !important;
        border: 0px;
}

.add-calendar {    position: fixed;
    right: 59px;
    bottom: 19px;
    z-index: 11;
    padding: 15px;
    border-radius: 35px;
    box-shadow: 0 6px 10px 0 rgba(0,0,0,0.14), 0 1px 18px 0 rgba(0,0,0,0.12), 0 3px 5px -1px rgba(0,0,0,0.2);
    background-color: #db4437;}

.dropdown-header {
    padding: 8px 20px;
    background: #ffffff;
    border-bottom: 1px solid #c2cfd6;
}

.dropdown-item:hover, .dropdown-item:focus {
    color: #0b0e0f;
    text-decoration: none;
    background-color: #f0f3f5;
    outline: none;
}

.app-header.navbar .dropdown-menu {
    padding-bottom: 0;
    line-height: 1.5;
    border-radius: 4px;
    margin-top: 8px;
        -webkit-box-shadow: 0 6px 10px 0 rgba(0, 0, 0, 0.14), 0 1px 18px 0 rgba(0, 0, 0, 0.12), 0 3px 5px -1px rgba(0, 0, 0, 0.2);
    box-shadow: 0 6px 10px 0 rgba(0, 0, 0, 0.14), 0 1px 18px 0 rgba(0, 0, 0, 0.12), 0 3px 5px -1px rgba(0, 0, 0, 0.2);
}

.app-header.navbar .dropdown-menu:before {     width: 0px;
    height: 0px;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-bottom: 5px solid #ffffff;
    content: '';
    position: absolute;
    right: 22px;
    margin-top: -5px;}

.dropdown-toggle::after {
    display: inline-block;
    width: 0;
    height: 0;
    margin-left: 0.255em;
    vertical-align: 0.255em;
    content:none;
    border-top: 0.3em solid;
    border-right: 0.3em solid transparent;
    border-bottom: 0;
    border-left: 0.3em solid transparent;
}

.dropdown-item {
    position: relative;
    padding: 10px 20px;
    border-bottom: 1px solid #c2cfd6;
    background: #efefef;
}

.p-relative { position:relative;}

.search-result {    position: absolute;
    background: white;
    width: 100%;
    box-shadow: 0 0 2px rgba(0,0,0,.12), 0 2px 4px rgba(0,0,0,.24), inset 0 4px 6px -4px rgba(0,0,0,.24);
    margin-top: 2px;
    border-radius: 2px;}

.search-text {    color: #212121;
    display: block;
    outline: 0;
        padding: 3px 10px;
    -webkit-transition: background .2s;
    transition: background .2s;
    font-size: 15px;
    }

.search-text1 {padding-left: 10px;
    font-style: italic;
    color: #9f9f9f;}

.search-text1 span {color: #3b77e7;}

.search-section:hover {    background: #f5f5f5;}

.app-header.navbar .navbar-brand {
    display: inline-block;
    width: 220px;
    padding: .5rem 1rem;
    margin-right: 0;
    background-image: url(/static/img/logo-new.png) !important;
    background-repeat: no-repeat;
    background-position: 50%;
    background-size: 185px auto;
    background-color: #fff;
    -webkit-transition: margin-left 0.25s, margin-right 0.25s, width 0.25s, -webkit-box-flex 0.25s;
    transition: margin-left 0.25s, margin-right 0.25s, width 0.25s, -webkit-box-flex 0.25s;
    transition: margin-left 0.25s, margin-right 0.25s, width 0.25s, flex 0.25s;
    transition: margin-left 0.25s, margin-right 0.25s, width 0.25s, flex 0.25s, -webkit-box-flex 0.25s, -ms-flex 0.25s;}

@media screen and (max-width: 990px) {
 
 .navbar-brand { display:none !important;}

}

@media screen and (min-width: 768px){
  #hour { width: 45%; }
}



</style>
