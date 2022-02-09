import { mixin as onClickOutside } from 'vue-on-click-outside'
export default {
    name: 'Messages',
    mixins: [onClickOutside],
    data () {
      return {
        search: '',
        newMessage: '',
        messages: [],
        fetchingMessages: false,
        selectedChannel: null,
        messagePaginator : null,
        fetchingHistory: false,
        userData : {},
        aiStatus : true,
        new_number: null,
        add_new_number:false,
        show_floating_box: false,
      }
    },
    computed: {
      filteredContacts: function () {
        return this.$root.bus.channels.filter(contact => {
          return contact.friendlyName.toLowerCase().includes(this.search.toLowerCase())
        })
      },
    },
    watch : {
      new_number : function() {
        this.new_number = this.new_number.trim();
        var valid_num_regx = /^(\+1\s?)?((\([0-9]{3}\))|[0-9]{3})[\s\-]?[\0-9]{3}[\s\-]?[0-9]{4}$/;
        if(this.new_number.match(valid_num_regx)){
          this.show_floating_box = true;
        }
        else{
          this.hide_floating_box();
        }
      },
      selectedChannel : function(){
        this.messages = []
        this.messagePaginator = null
        this.userData = {}
        this.getLatestMessages()
        this.getAppoinmentDetails()
        this.getAiStatus()
      }
    },
    methods: {
      create_unique_name(provider_number,new_number){
        new_number = new_number.split(' ').join('');
        new_number = new_number.split('(').join('');
        new_number = new_number.split(')').join('');
        new_number = new_number.split('-').join('');
        return provider_number + ' - ' + new_number;
      },
      hide_floating_box() {
        this.show_floating_box = false;
      },
      add_country_code(num){
        if(num.indexOf('+1') < 0) {
          num = '+1' + num;
        }
        return num;
      },
      create_channel(){
        var provider_number = '';
        var new_number = this.new_number;
        var vue_instance = this;
        //validating new mobile number
        this.$api.messaging.app.validateNumber({"phone_number":new_number}).then(() =>{
          //fetching provider's phone number
          this.$api.messaging.app.providerNumber({generalsettings_id:this.$root.bus.info.generalsettings_id}).then(response => {
            provider_number = response.body.provider_number;
            new_number = this.add_country_code(new_number);
            var uniqueName = this.create_unique_name(provider_number,new_number);
            if (provider_number.length > 0){
              var client = this.$root.bus.chatClient
              //creating new channel
              client.createChannel({
                uniqueName: uniqueName,
                friendlyName: new_number,
              })
              .then(function(channel) {
                console.log('Created general channel:');
                console.log(channel);
                // adding member to channel
                vue_instance.$api.messaging.app.addMemberToChannel({'new_number':new_number,'channel_id':channel.sid}).then(response => {
                  console.log('Joined channel ' + channel.friendlyName);
                }).catch((response) => {
                  console.log(response)
                });
                channel.join().catch(function(err) {
                  console.error(
                    "Couldn't join channel " + channel.friendlyName + ' because ' + err
                  );
                });
              }).catch(err => {
                alert('Number already in use');
              });
            }
          });
        }).catch(() => {
          alert('Invalid phone number');
        });
        this.new_number = '';
        this.show_floating_box = false; //hide the box
      },
      sendNewMessage(){
        this.add_new_number = true;
      },
      getLatestMessages () {
        if(this.selectedChannel == null){
          return;
        }
        var vm = this
        vm.fetchingMessages = true
        this.selectedChannel.getMessages(10).then(function (paginator) {
          vm.messagePaginator = paginator
          vm.messages = paginator.items
          vm.fetchingMessages = false
          vm.$nextTick(() => {
            vm.$refs.messageHistory.scrollTop = vm.$refs.messageHistory.scrollHeight
            if(paginator.items.length > 0){
              vm.updateLastConsumedMessage(vm.selectedChannel, paginator.items[paginator.items.length - 1].index)
            }
          })
        })
      },
      getAppoinmentDetails () {
        if(this.selectedChannel == null){
          return;
        }
        let phoneNumber = (this.selectedChannel.uniqueName.split('-')[1].trim()).split('+')[1]
        this.$api.messaging.app.appoinments({phone: phoneNumber}).then(response => {
          this.userData = response.data
        }).catch(() => {
          this.error = true
        })
      },

      toogleAi () {
        let phoneNumber = (this.selectedChannel.uniqueName.split('-')[1].trim()).split('+')[1];
        this.$api.messaging.app.onOffAi({user:phoneNumber, generalsettings_id:this.$root.bus.info.generalsettings_id, toggle: this.aiStatus}).then(response => {
          // pass
        }).catch(() => {
            console.log("error toggle api call")
        })
      },

      getAiStatus () {
        let phoneNumber = (this.selectedChannel.uniqueName.split('-')[1].trim()).split('+')[1];
        this.$api.messaging.app.getOnOffStatus({phone: phoneNumber}).then(response => {
          this.aiStatus = response.data
          if(this.aiStatus.response_message === true || this.aiStatus.response_message === 'true'){
            this.aiStatus = true;
          } else if(this.aiStatus.response_message === 'info is not correct.') {
            this.aiStatus = false;
          } else if(this.aiStatus.response_message === 'Failed'){
              this.aiStatus = false;
          }
          else{
              this.aiStatus = false;
          }
        }).catch(() => {
          console.log("Error occured while fetching the status");
        })
      },

      deleteChannel () {
        var vm = this;
        this.selectedChannel.delete().then(function(channel) {
          var index = vm.$root.bus.channels.findIndex(x => x.uniqueName === vm.selectedChannel.uniqueName);
          if(index >= 0){
            vm.$root.bus.channels.splice(index, 1)
          }
          vm.selectedChannel = null;
        });
      },
      paginateMesages(){
        if(this.$refs.messageHistory.scrollTop == 0 && !this.fetchingHistory && !this.fetchingMessages && this.messagePaginator.hasPrevPage){
          var vm = this;
          var initialHeight = vm.$refs.messageHistory.scrollHeight
          vm.fetchingHistory = true
          this.messagePaginator.prevPage().then(paginator => {
            vm.messagePaginator = paginator
            vm.messages.unshift(...paginator.items.reverse())
            vm.$nextTick(() => {
              vm.$refs.messageHistory.scrollTop = vm.$refs.messageHistory.scrollHeight - initialHeight
            })
            vm.fetchingHistory = false
          });
        }
      },
      updateLastConsumedMessage(channel, index){
        channel.updateLastConsumedMessageIndex(index)
      },
      sendMessage () {
        if (this.newMessage === '') {
          return
        }
        var vm = this
        this.selectedChannel.sendMessage(this.newMessage).then(function (msg) {
          vm.newMessage = ''
        })
      },
      handleNewMessage (message) {
        var index = this.$root.bus.channels.findIndex(x => x.uniqueName === message.channel.uniqueName);
        var vm = this
        var uniquename = message.channel.uniqueName;
        var channels = this.$root.bus.channels;
        this.$root.bus.chatClient.getChannelByUniqueName(uniquename).then(function(channel) {
          for(let i=1;i<=channels.length;i++){
            if(typeof(channels[i]) != 'undefined' && channels[i].uniqueName == uniquename){
              channels.splice(i,1);
              channels.unshift(channel);
              break
            }
          }
        });
        
        if(this.selectedChannel !== null){
          if(message.channel.uniqueName == this.selectedChannel.uniqueName){
            this.messages.push(message)
            this.updateLastConsumedMessage(message.channel, message.index)
            this.$nextTick(() => {
              this.$refs.messageHistory.scrollTop = this.$refs.messageHistory.scrollHeight
            })
          }
        }
      },
    },
    created () {
      this.$eventBus.$on('newMessage', this.handleNewMessage)
    },
}