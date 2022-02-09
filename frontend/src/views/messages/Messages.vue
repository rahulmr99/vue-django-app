<template>
  <div>
    <div v-if="$root.bus.chatClient == null">
      Please wait
    </div>
    <div v-else class="msg-wrap">
      <div class="messaging">
        <div class="inbox_msg">
          <div class="inbox_people">
            <div class="headind_srch" @click="sendNewMessage()">
              <i  class="fa fa-plus plus-color" aria-hidden="true"></i>
                Send new message
            </div>
            <div class="inbox_chat custom-scroll" @click="add_new_number = false">
              <div class="chat_list active_chat" v-if="$root.bus.fetchingChannels">Fetching chats. Please wait....</div>
              <div class="chat_list active_chat" v-else v-for="(channel,index) in filteredContacts" :key="index"  @click="selectedChannel = channel">
                <div class="chat_people">
                  <div class="chat_img">
                    <img src="static/img/avatars/userlogin.png" :alt="channel.friendlyName">
                  </div>
                  <div class="chat_ib">
                    <h5>
                      {{channel.friendlyName}}
                      <span class="unread-count"
                        v-if="channel.lastConsumedMessageIndex == null && typeof channel.lastMessage != 'undefined' && typeof channel.lastMessage != undefined">{{parseInt(channel.lastMessage.index) + 1}}</span>
                      <span class="unread-count"
                        v-if="channel.lastConsumedMessageIndex !== null && parseInt(channel.lastMessage.index - channel.lastConsumedMessageIndex) > 0">{{parseInt(channel.lastMessage.index - channel.lastConsumedMessageIndex)}}</span>
                    </h5>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="mesgs">
            <div class="new-message" v-if="add_new_number" v-on-click-outside="hide_floating_box">
              <div>
                <span>To:</span>
                <input v-model="new_number" placeholder="Enter the phone number" class="new-msg">
                <div class="floating_box" v-if="show_floating_box" @click="create_channel()"><svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fit="" preserveAspectRatio="xMidYMid meet" focusable="false"><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H4V4h16v12z"></path><path d="M6 12h12v2H6zm0-3h12v2H6zm0-3h12v2H6z"></path></svg> {{new_number}}</div>
              </div>
            </div>
            <div v-if="add_new_number == false">
              <div class="msg_history" v-if="selectedChannel != null">
                <div class="chat-name">{{selectedChannel.friendlyName}}</div>
                <div class="chat-height custom-scroll" ref="messageHistory" @scroll="paginateMesages">
                  <div v-if="fetchingMessages" class="message-loader">
                    <img src="static/img/loading.gif" />
                  </div>
                  <div v-else v-for="(item, index) in messages" :key="index">
                    <div v-if="$root.bus.info.username != item.author" class="incoming_msg">
                      <div class="incoming_msg_img">
                        <img src="static/img/avatars/userlogin.png" :alt="item.author">
                      </div>
                      <div class="received_msg">
                        <div class="received_withd_msg">
                          <p>{{item.body}}</p>
                          <span class="time_date">{{$moment(item.timestamp).fromNow()}}</span>
                        </div>
                      </div>
                    </div>

                    <div v-else class="outgoing_msg">
                      <div class="sent_msg">
                        <p>{{item.body}}</p>
                        <span class="time_date">{{$moment(item.timestamp).fromNow()}}</span>
                      </div>
                    </div>
                  </div>

                  <!-- <div class="outgoing_msg">
                    <div class="sent_msg">
                      <p>Test which is a new approach to have all
                        solutions</p>
                      <span class="time_date"> 11:01 AM | June 9</span>
                    </div>
                  </div>-->
                </div>
                <div class="type_msg">
                  <div class="input_msg_write">
                    <textarea type="text" class="write_msg" placeholder="Type a message" v-model.trim="newMessage"
                      @keypress.enter="sendMessage"></textarea>
                    <button class="msg_send_btn" type="button">
                      <img class="send-img" src="static/img/send.png" @click="sendMessage">
                    </button>
                  </div>
                </div>
              </div>
              <div v-else class="msg_history">
                <div class="no_chat">
                  <img :src="'static/img/no-chat.png'" />
                  <p>Please select a conversation</p>
                </div>
              </div>
            </div>
            <div v-else class="msg_history">
              <div class="no_chat">
                <img :src="'static/img/no-chat.png'" />
                <p>Please select a conversation</p>
              </div>
            </div>
          </div>
          <div class="chat-op">
            
            <div class="switch-wrap" v-if="selectedChannel != null && add_new_number == false">
              <div class="material-switch pull-right">
                <span class="switch-span">AI status</span>
                <input id="someSwitchOptionPrimary" name="someSwitchOption001" @change="toogleAi()" type="checkbox" v-model="aiStatus">
                <label for="someSwitchOptionPrimary" class="label-primary"></label>
              </div>

              <div class="material-switch pull-right">
                <span class="switch-span">Mark done</span>
                <input id="someSwitchOptionPrimary1" name="someSwitchOption002" type="checkbox" @change="deleteChannel()">
                <label for="someSwitchOptionPrimary1" class="label-primary"></label>
              </div>
            </div>
            <div v-if="Object.keys(userData).length > 0 && add_new_number == false">
              <h6 class="chat-op-name">
                <img src="static/img/avatars/userlogin.png" width="30px" alt="">
                {{userData.name}}
              </h6>
              <div class="tags">
                <span class="patient_status">{{userData.is_new_patient ? 'New patient' : 'Returning patient' }}</span>
                <label>Appointment</label>
                <div v-if="userData.upcoming_appt_date!= null" class="appoinment-date"><i class="icon-calendar"></i> {{userData.upcoming_appt_date}}</div>
                <div v-else class="appoinment-date">No upcoming appointment</div>
                <hr>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script src="./messages_script.js" />
<style scoped>

.plus-color {    
    color: #3e68ff;
    margin-right: 5px;}

.new-msg{
  width: 90%;
      border: 0px;
    outline: none;
}
.new-message {
  padding: 14px;
  border-bottom: 1px solid #c4c4c4;
  position: relative;
}
.floating_box {
    position: absolute;
    z-index: 1;
    width: 95%;
    padding: 15px;
    background: #fff;
    -webkit-box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 2px 6px 2px rgba(60,64,67,0.15);
    box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 2px 6px 2px rgba(60,64,67,0.15);
    border-radius: 3px;
    top: 44px;
}

.floating_box svg path {
    fill: #3b77e7;
}
.floating_box  svg { width: 20px;}

.send-img {
  width: 15px;
  height: 15px;
  margin: auto;
  margin-top: -4px;
  margin-right: -3px;
}

.material-switch {
  margin-right: 10px;
  margin-top: 5px;
}

.switch-wrap {
  height: 60px;
}

.switch-span {
  margin-right: 10px;
  font-size: 16px;
  font-weight: 600;
  color: #7d7d7d;
  line-height: 19px;
}
.write_msg{
   margin-top: 0px;
    margin-bottom: 0px;
    min-height: 20px;
    width: 100%;
    padding-right: 50px;
    border: 0px;
    outline: none;
}

.material-switch > input[type="checkbox"] {
  display: none;
}

.material-switch > label {
  cursor: pointer;
  height: 0px;
  position: relative;
  width: 40px;
}

.material-switch > label::before {
  background: rgb(0, 0, 0);
  box-shadow: inset 0px 0px 10px rgba(0, 0, 0, 0.5);
  border-radius: 8px;
  content: "";
  height: 16px;
  margin-top: -8px;
  position: absolute;
  opacity: 0.3;
  transition: all 0.4s ease-in-out;
  width: 40px;
}
.material-switch > label::after {
  background: rgb(255, 255, 255);
  border-radius: 16px;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.3);
  content: "";
  height: 24px;
  left: -4px;
  margin-top: -8px;
  position: absolute;
  top: -4px;
  transition: all 0.3s ease-in-out;
  width: 24px;
}
.material-switch > input[type="checkbox"]:checked + label::before {
  background: #3b77e7;
  opacity: 0.5;
}
.material-switch > input[type="checkbox"]:checked + label::after {
  background: #3b77e7;
  left: 20px;
}

.tags label {
  margin-top: 10px;
  font-size: 15px;
  font-weight: 500;
}

.tags p {
  color: #989898;
  margin-bottom: 5px;
}

.tags h6 {
  margin-bottom: 1px;
}

.tags {
  padding: 10px;
  padding-bottom: 20px;
}

.tags hr {
  border-top: 1px solid #e0e0e0;
  margin-bottom: 0px;
}

.chat-op img {
  display: inline-block;
  margin-top: 1px;
  margin-right: 4px;
  width: 20px;
}

.chat-op-name span {
  display: block !important;
  font-size: 12px;
  color: #646464;
}

.chat-op-name {
  display: inline-block;
  font-size: 15px;
  margin-left: 10px;
  width: 100%;
}

.chat-op {
  float: left;
  padding: 20px;
  width: 25%;
}

.custom-scroll::-webkit-scrollbar {
  width: 10px;
}

/* Track */
.custom-scroll::-webkit-scrollbar-track {
  background: #f1f1f1;
}

/* Handle */
.custom-scroll::-webkit-scrollbar-thumb {
  background: #d0cece;
  border-radius: 15px;
}

/* Handle on hover */

.chat-height {
height: 100%;
overflow-y: scroll;
position: relative;
padding-bottom: 20px;
}

.chat-name {
  font-size: 20px;
  padding: 20px;
  border-bottom: 1px solid #c4c4c4;
  margin-bottom: 10px;
  font-weight: 500;
}

.incoming_msg {
  padding-left: 20px;
}
.search-msg {
  width: 100%;
  border: 0px;
  background: #efefef;
  height: 40px;
  border-radius: 3px;
  font-size: 16px;
  padding-left: 45px;
  outline: 0;
  background-image: url(/static/img/s-ic.png);
  background-size: 21px;
  background-repeat: no-repeat;
  background-position: 12px;
  font-weight: 500;
}

.msg-wrap {
  margin: 1em;
  height: 79.2vh;
}
img {
  max-width: 100%;
}
.inbox_people {
background: #fff;
float: left;
overflow: hidden;
width: 25%;
border-right: 1px solid #c4c4c4;
height: 100%;
padding-bottom: 4em;
}
.inbox_msg {
  box-shadow: 0px 0px 4px 0px #c5c5c5;
  clear: both;
  overflow: hidden;
 height: 94%;
}
.top_spac {
  margin: 20px 0 0;
}

.recent_heading {
  float: left;
  width: 40%;
}
.srch_bar {
  display: inline-block;
  text-align: right;
  width: 60%;
}
.headind_srch {
  padding: 15px;
  overflow: hidden;
  border-bottom: 1px solid #c4c4c4;
}

.recent_heading h4 {
  color: #05728f;
  font-size: 21px;
  margin: auto;
}
.srch_bar input {
  border: 1px solid #cdcdcd;
  border-width: 0 0 1px 0;
  width: 80%;
  padding: 2px 0 4px 6px;
  background: none;
}
.srch_bar .input-group-addon button {
  background: rgba(0, 0, 0, 0) none repeat scroll 0 0;
  border: medium none;
  padding: 0;
  color: #707070;
  font-size: 18px;
}
.srch_bar .input-group-addon {
  margin: 0 0 0 -27px;
}

.chat_ib h5 {
  font-size: 15px;
  color: #464646;
  margin: 0 0 8px 0;
  white-space: nowrap;
  width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-right: 20px;
  position: relative;
  cursor: pointer;
}
/* .chat_ib h5 span {
  font-size: 13px;
  float: right;
  color: #a9a9a9;
  font-weight: 400;
} */
.chat_ib p {
  font-size: 14px;
  color: #6d6d6d;
  margin: auto;
  white-space: nowrap;
  width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
}
.chat_img {
  float: left;
  width: 11%;
}
.chat_ib {
  float: left;
  padding: 0 0 0 15px;
  width: 88%;
}

.chat_people {
  overflow: hidden;
  clear: both;
  height: 100%;
}
.chat_list {
  border-bottom: 1px solid #ececec;
  margin: 0;
  padding: 18px 16px 10px;
}
.inbox_chat {
  height: 100%;
  overflow-y: scroll;
}

.active_chat {
  background: #f7f7f7;
}

.incoming_msg_img {
  display: inline-block;
  width: 4%;
}
.received_msg {
  display: inline-block;
  padding: 0 0 0 10px;
  vertical-align: top;
  width: 92%;
}
.received_withd_msg p {
  background: #ebebeb none repeat scroll 0 0;
  border-radius: 3px;
  color: #646464;
  font-size: 14px;
  margin: 0;
  padding: 5px 10px 5px 12px;
  width: 100%;
  word-break: break-word;
}
.time_date {
  color: #747474;
  display: block;
  font-size: 12px;
  margin: 8px 0 0;
}
.received_withd_msg {
  width: 57%;
}
.mesgs {
 float: left;
width: 50%;
height: 100%;
border-right: 1px solid #c4c5c4;
}

.sent_msg p {
  background: #3b77e7 none repeat scroll 0 0;
  border-radius: 3px;
  font-size: 14px;
  margin: 0;
  color: #fff;
  padding: 5px 10px 5px 12px;
  width: 100%;
  word-break: break-word;
}
.outgoing_msg {
  overflow: hidden;
  margin: 26px 0 26px;
}
.sent_msg {
  float: right;
  width: 46%;
}
.input_msg_write input {
  background: rgba(0, 0, 0, 0) none repeat scroll 0 0;
  border: medium none;
  color: #4c4c4c;
  font-size: 15px;
  min-height: 48px;
  width: 100%;
  outline: 0;
}

.type_msg {
  border-top: 1px solid #c4c4c4;
  position: absolute;
  bottom: 0;
  width: 100%;
  padding-left: 15px;
  background: #fff;
}
.msg_send_btn {
  background: #3b77e7 none repeat scroll 0 0;
  border: medium none;
  border-radius: 50%;
  color: #fff;
  cursor: pointer;
  font-size: 17px;
  height: 33px;
  position: absolute;
  right: 8px;
  top: 8px;
  width: 33px;
  outline: none;
}
.messaging {
  height: 100%;
}
.msg_history {
height: 75vh;
border-right: 1px solid #c4c4c4;
position: relative;
width: 100%;
float: left;
padding-bottom: 96px;
}
.unread-count {
  min-width: 15px;
  height: 15px;
  background: #f90505 !important;
  text-align: center;
  border-radius: 31px;
  line-height: 16px;
  color: #fff !important;
  font-size: 9px !important;
  position: absolute;
  right: 0px;
}
.no_chat{
  text-align: center;
}
.no_chat img {
  width: 30%;
  padding-top: 25%;
  opacity: 0.8;
}
.no_chat p {
  font-size: 17px;
  color: #8d8f90;
  margin-top: 10px;
}
.message-loader{
  text-align: center
}
.message-loader img{
  position: absolute;
  left: 46%;
  top: 33%;
  width: 46px;
}
.appoinment-date{
  padding: 5px;
  background-color: #cae0f3;
  text-align: center;
}
.patient_status{
  padding: 10px;
}
</style>
