<template>
    <div class="app-wrapper">
      <UserResponse v-if="responseClass.includes('displayed')" :class="['response-message', responseClass]" :dbResponse="dbResponse" @close="closeResponse" />
      <div class="home-wrapper col-100">
        <div class="col-100 title-bar col-flex">
            <div class="col-100">
                <p class="title-text"><i class="fa-solid fa-envelope"> </i>Messages</p>
            </div>
        </div>
        <div class="chat-body">
            <!-- chat list -->
            <div class="chat-list" v-if="chat_list">
            <div class="no_message col-90 text-center" v-if="empty_chat">
                <img src="../assets/logos/empty_folder.png"> 
                <p>Start a new chat</p>
            </div>
            <div class="col-100">
                <input type="text" class="universal-input form-input" style="width:93% !important;" placeholder="Search user" v-model="password">
            </div>
            <div class="chat-box col-flex" @click="openChat">
                <div class="col-20">
                    <img src="../assets/860.jpg" class="read-pic"> 
                </div>
                <div class="col-67">
                    Lorem ipsum dolor...
                </div>
                <div class="col-10 text-center">
                    <p class="sm-time">12:10</p>
                    <div class="not-dot">
                        <div class="not-dot-inner">
                            2
                        </div>
                    </div>
                </div>
            </div>
            <div class="chat-box col-flex">
                <div class="col-20">
                    <img src="../assets/g10.png" class="read-pic"> 
                </div>
                <div class="col-67">
                    Lorem ipsum dolor...
                </div>
                <div class="col-10">
                    <p class="sm-font">12:10</p>
                </div>
            </div>
            <!-- new chat button -->
             <div class="col-90 new-chat-holder text-right">
               <div class="new-chat-btn" @click="showUsers">
                   <span>New Chat <i class="fa-solid fa-plus"></i></span>
               </div>
             </div>
        </div>
        <!-- chat page -->
        <div class="chat-page" v-if="shown_chat">
            <div class="col-100 col-flex chat-top">
                <div class="col-40 col-flex" @click="hideChat" style="width:fit-content;">
                    <div class="col-10">
                        <i class="fa-solid fa-angle-left"></i>
                    </div>
                    <div class="col-90">
                        <img :src="user_image" class="chat-pic">
                    </div>
                </div>
                <div class="col-60">
                    <p>{{ f_name }} {{l_name }}</p>
                </div>
            </div>
            <!-- chat body -->
             <div class="chat-page-body col-flex">
                <!-- start of chat -->
                <div class="full-chat-box col-100" v-for="(message, index) in chat_messages" :key="index">
                    <div class="chat-body-box col-flex" 
                         :class="{ 
                           'sent-to-me': message.sender_id !== userStore.user,
                           'i-sent': message.sender_id === userStore.user
                         }">
                      <div class="col-100">
                        <p>{{ message.message }}</p>
                      </div>
                      <div class="col-100 text-right">
                        <span>{{ formatDateTime(message.time) }}</span>
                      </div>
                    </div>
                  </div>
                <!-- end of chat -->
             </div>
             <!-- input field -->
            <div class="send-msg-box col-100 col-flex">
                <div class="col-80">
                    <textarea
                      class="universal-input form-input message-box"
                      v-model="message"
                      ref="textarea"
                      @input="adjustHeight"
                      rows="1"
                      placeholder="Type a message..."
                    ></textarea>
                </div>
                <div class="col-20 text-center">
                    <i class="fa-solid fa-paper-plane" @click="sendMessage"></i>
                </div>
            </div>
        </div>
        <!-- end of chat list -->
         <div class="view-users" v-if="show_users">
            <div class="col-100 col-flex chat-top">
                <div class="col-40 col-flex" @click="hideChat" style="width:fit-content;">
                    <div class="col-10">
                        <i class="fa-solid fa-angle-left"></i>
                    </div>
                    <div class="col-90">
                        <span style="margin-left:10px;">Contacts</span>
                    </div>
                </div>
            </div>
            <div class="col-100">
                <input type="text" class="universal-input form-input" style="width:93% !important;" placeholder="Search user" v-model="password">
            </div>
            <!-- user panel -->
             <div class="user-panel">
                <div class="chat-box col-flex" v-for="(user, index) in users" :key="index" @click="openChat(user.id)">
                    <div class="col-20">
                        <img :src="user.profile" class="read-pic"> 
                    </div>
                    <div class="col-80">
                        <p>{{ user.f_name }} {{ user.l_name }}</p>
                    </div>
                </div>
             </div>
         </div>
    </div>
      </div>
      <!-- end of message -->
       <UserNavigation/>
    </div>
  </template>
  
  <script>
  import { io } from "socket.io-client";
  import axios from 'axios';
  import UserResponse from '@/components/UserResponse.vue';
  import UserNavigation from '@/components/UserNavigation.vue';
  import { useUserStore } from '@/assets/js/userStore.js'
  
  export default {
    name: 'UserReads',
    components: { UserResponse, UserNavigation },
    setup() {
        const userStore = useUserStore();
        return { userStore };
    },
    data() {
        return {
          responseClass: '',
          dbResponse: '',
          email: '',
          password: '',
          shown_chat: false,
          chat_list: true,
          messages: [],
          empty_chat: false,
          show_users:false,
          users:[],
          message:'',
          recepient_id: '',
          user_image:'',
          f_name:'',
          l_name:'',
          chat_messages: [],
          socket: null, // WebSocket connection
        }
      },
      methods: {
        adjustHeight() {
            const textarea = this.$refs.textarea;
            textarea.style.height = "auto"; // Reset height
            textarea.style.height = Math.min(textarea.scrollHeight, 100) + "px";
        },
        formatDateTime(dbTime) {
            if (!dbTime) return '';
            const date = new Date(dbTime);
            return date.toLocaleString('en-GB', { 
                year: 'numeric', 
                month: '2-digit', 
                day: '2-digit', 
                hour: '2-digit', 
                minute: '2-digit', 
                hour12: false 
            }).replace(',', '');
        },
        closeResponse() {
          this.responseClass = '';
          this.dbResponse = '';
        },
        openChat(id){
            this.shown_chat = true
            this.show_users = false
            this.chat_list = false
            this.recepient_id = id
            this.getChatUser()
        },
        hideChat(){
            this.shown_chat = false
            this.show_users = false
            this.chat_list = true
        },
        showUsers(){
            this.show_users = true
            this.chat_list = false
            this.empty_chat = false
            this.getUsers()
        },
        async getMessages(){
            
            try {
                const response = await axios.post('http://192.168.1.125:5000/get-messages', {
                    id: this.userStore.user
                });
                const data = response.data;
                if (data.length > 0) {
                    this.messages = data;
                } else {
                    this.empty_chat = true
                }
            } catch (error) {
                this.responseClass = 'my-red displayed';
                this.dbResponse = 'Failed. Server Offline. Please try again later.';
            }
        },
        async getChatMessage(){
            this.chat_messages = ''
            try {
                const response = await axios.post('http://192.168.1.125:5000/get-chat-message', {
                    id: this.userStore.user,
                    receiver: this.recepient_id
                });
                const data = response.data;
                if (data.length > 0) {
                    this.chat_messages = data;
                } else {
                    this.empty_chat = true
                }
            } catch (error) {
                this.responseClass = 'my-red displayed';
                this.dbResponse = 'Failed. Server Offline. Please try again later.';
            }
        },
        async getUsers(){
            try {
                const response = await axios.post('http://192.168.1.125:5000/get-client-users', {
                    id: this.userStore.user
                });
                const data = response.data;
                if (data.length > 0) {
                    this.users = data;
                } else {
                    this.responseClass = 'my-success displayed';
                this.dbResponse = 'No active users';
                }
            } catch (error) {
                this.responseClass = 'my-red displayed';
                this.dbResponse = 'Failed. Server Offline. Please try again later.';
            }
        },
        async sendMessage(){
            if(this.message == ''){
                return
            }
            //send message
            try {
                const response = await axios.post('http://192.168.1.125:5000/send-message', {
                    id: this.userStore.user,
                    receiver: this.recepient_id,
                    message: this.message
                });
                const data = response.data;
                const gotten_response = data.message
                if(gotten_response == '1'){
                    this.message = ''
                    this.getChatMessage()
                }else if(gotten_response == '2'){
                    this.responseClass = 'my-red displayed';
                    this.dbResponse =  "Error sending message";
                }else{
                    this.responseClass = 'my-red displayed';
                    this.dbResponse =  "Failed";
                }
            } catch (error) {
                this.responseClass = 'my-red displayed';
                this.dbResponse = 'Failed. Server Offline. Please try again later.';
            }
        },
        async getChatUser(){
            //send message
            try {
                const response = await axios.post('http://192.168.1.125:5000/get-chat-user', {
                    receiver: this.recepient_id,
                });
                const data = response.data;
                const gotten_response = data[0]
                this.user_image = gotten_response.pic
                this.f_name = gotten_response.f_name
                this.l_name = gotten_response.l_name
                this.getChatMessage()
                
            } catch (error) {
                this.responseClass = 'my-red displayed';
                this.dbResponse = 'Failed. Server Offline. Please try again later.';
            }
        },
        //setup socket
        setupSocketListeners() {
            this.socket = io('http://192.168.1.125:5000');

            this.socket.on(`new_message_${this.userStore.user}`, (data) => {
                console.log("New message received:", data);
                this.chat_messages.push({
                    sender_id: data.sender_id,
                    message: data.message,
                    time: new Date().toISOString(),
                });
            });
        }
      },
      mounted(){
        this.getMessages();
        this.setupSocketListeners();
        this.chat_messages = ''
      },
      beforeUnmount() {
        if (this.socket) {
            this.socket.disconnect();
        }
    }
  }
  </script>
  