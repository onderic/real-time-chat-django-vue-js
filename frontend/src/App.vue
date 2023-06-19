
<template>
  <div class="tracking-wider  bg-gray-700  flex flex-col min-h-screen">
    <div class="relative flex min-h-screen"  v-if="userStore.user.isAuthenticated">
    
      <div class="fixed top-0 h-screen bg-gray-700 dark:text-white w-1/3 space-x-6 shadow-lg border border-gray-300 inset-y-0 left-0 md:relative md:-translate-x-0 transform -translate-x-full transition duration-200 ease-in-out overflow-y-auto">
      <!-- Sidebar content -->
      <div   class="bg-gray-800 shadow-md  py-2 mt-0 px-4 flex items-center justify-between" style="position: sticky; top: 0;">
        <div class="flex items-center">
          <div class="hs-dropdown relative inline-flex">
            <img id="hs-dropdown-default" :src="userStore.user.user_avatar" 
        
          alt="" 
          class="mr-2 h-12 w-12 rounded-full border-2 border-green-400">

          <div class="hs-dropdown-menu transition-[opacity,margin] duration-[0.1ms] hs-dropdown-open:opacity-100 opacity-0 w-72 hidden z-10 mt-2 min-w-[15rem] bg-gray-900 shadow-md rounded-lg p-2 dark:bg-gray-800 dark:border dark:border-gray-700 dark:divide-gray-700" aria-labelledby="hs-dropdown-default">
            <a class="flex items-center gap-x-3.5 py-2 px-3 rounded-md text-sm text-white  dark:text-gray-400">
              Welcome,<b>{{ userStore.user.username }}</b>
            </a>
            <a class="flex items-center gap-x-3.5 py-2 px-3 rounded-md text-sm text-white hover:bg-white hover:text-gray-600 focus:ring-2 focus:ring-blue-500 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-300" href="#">
              Profile
            </a>
            <a class="flex items-center gap-x-3.5 py-2 px-3 rounded-md text-sm text-white hover:bg-white hover:text-gray-600 focus:ring-2 focus:ring-blue-500 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-300" @click="logout">
             logout
            </a>
          </div>
        </div>
        
        </div>
        
        <div class="px-2  ml-2 rounded-md">
        <div >
          <input
          type="text"
          v-model="searchTerm"
          @input="filterItems"
          placeholder="Search..."
          class="border border-gray-300 bg-white rounded-md px-4 py-2 w-full"
        />
        </div>

  </div>
  </div>
  
  <div class="mt-5">
    <div class="mr-4">
     
      <ul v-if="filteredItems.length > 0" class="mt-4">
        <li v-for="(item, index) in filteredItems" :key="index" class="bg-gray-800 text-white w-full shadow-md rounded-md mr-2  mb-3 px-4 py-2">
          <div
            class="flex items-center space-x-1 px-4 py-2 rounded-md cursor-pointer"
            :class="{ 'bg-gray-700 w-full': selectedUser === item.username }"
            @click="selectUser(item.username)"
          >
            <img
              :src="item.user_user_avatar"
              @error="handleImageError"
              alt=""
              class="mr-2 h-8 w-8 bg-gray-200  rounded-full"
            />
            <span class="mb-2" :class="{ 'font-bold': selectedUser === item.username }">{{ item.username }}</span>
          </div>
        </li>
      </ul>
      <p v-else-if="searchTerm" class="mt-2 text-white text-2xl">No results found!</p>
      <!-- <p v-else class="mt-2">Type to search.</p> -->
    </div>
  </div>
    </div>
      <!-- Main content -->
          <div class="h-screen w-full overflow-y-auto">
            <div  v-if="selectedUser" class="mb-18">
              <nav  class="bg-gray-800 text-white py-2 px-4 overflow-y-auto flex items-center justify-between fixed top-0 lg:left-1/4 lg:w-3/4 w-full border-b border-gray-300">
                <!-- Navigation content -->
                <div class="flex items-center">
                <img :src="getUserImage(selectedUser)" 
                @error="handleImageError"
                alt="" 
                class="h-12 w-12 rounded-full  border-r-2 border-gray-300 mr-2">
                <span v-if="selectedUser" class=" text-xl">{{ selectedUser }}</span>
              </div>
              <div class="ml-auto">
              <button class="bg-sky-500 hover:bg-sky-700 text-white font-bold py-1 px-2 rounded-md" @click="logout()">logout</button>
          
             </div>
              </nav>


            <div :class="{ 'bg-gray-500': selectedUser, 'bg-slate-800': !selectedUser }">
            <div class="h-screen  bg-gray-700 flex flex-col">
            <div v-if="chatItems.length > 0" class="px-4 mt-10 py-8  h-screen  ">
            <div class="overflow-y-auto max-h-[630px]">
              <div v-for="(item, index) in chatItems" :key="index">
                <div v-if="item.sender === userStore.user.username" class="bg-gray-100 ml-2 mb-4 border border-gray-200 rounded-md shadow-md px-4 py-2 w-1/2">
                  <span>Me :</span>
                  <span class="ml-3">{{ item.message }}</span>
                </div>
                <div v-else class="flex justify-end">
                  <div class="bg-green-300 rounded-md w-1/2 shadow-md px-16 py-2 mb-4 mr-4">
                    <!-- <span>{{ item.sender }} :</span> -->
                    <span class="ml-3">{{ item.message }}</span>
                  </div>
                </div>
              </div>
              </div>
            </div>
          
            <div v-else class="flex-grow"></div>
            <div v-if="selectedUser" class="bg-gray-800 p-4 w-full " style="position: sticky; bottom: 0;">
              <div class="flex items-center rounded-md px-10">
                <input v-model="message" @keydown.enter="sendMessage" type="text" class="w-1/2 rounded-md py-3  px-4" placeholder="Type here..." required>
                <button @click="sendMessage" class="ml-3 focus:outline-none bg-white p-3 rounded-md">
                  <i class="fas fa-paper-plane text-gray-600 hover:text-gray-700"></i>
                </button>
              </div>
            </div>
          </div>
            </div>
            </div>
            <div v-else class="bg-gray-700 h-screen flex justify-center  items-center">
            <div class="bg-white px-8 py-8 rounded-lg" >
              <h1 class="text-4xl font-bold mb-4 ml-4">Welcome to Gigs Chat</h1>
                <p class="text-xl">Time to connect to friends and family you love.</p>
              <div class="flex justify-center items-center mt-4" >
                <img src="./assets/home.jpg" class="h-64 rounded-md " alt="">
              </div>
            </div>
            </div>
        <toast></toast>
      </div>
    </div>
    <router-view v-else></router-view>
  </div>
</template>

<script>
import axios from 'axios';
import { useUserStore } from '@/stores/user'

export default {
  setup() {
    const userStore = useUserStore();
    return {
      userStore
    };
  },
  data() {
    return {
      searchTerm: '',
      users: [],
      recipient: '',
      message: '',
      chatItems: [],
      items: [],
      filteredItems: [],
      selectedUser: null,
      selectedUserImage: null,
    };
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    handleImageError(event){

      event.target.src = "data:image/png;base64,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"
    },
    selectUser(username) {
      this.selectedUser = username;
      const user = this.items.find(item => item.username === username);
      if (user) {
        this.selectedUserImage = user.user_user_avatar;
        this.recipient = user.username; // Store the recipient's name
        this.fetchChatMessages(this.recipient); // Fetch chat messages for the selected user
      }
    },

    getUserImage(username) {
      if (this.selectedUser === username) {
        return this.selectedUserImage;
      }
      const user = this.items.find(item => item.username === username);
      if (user) {
        return user.user_user_avatar;
      }
      // Return a default image URL if the user is not found
      return 'default-avatar.jpg';
    },
    logout() {
      this.userStore.removeToken();
      this.$router.push({ name: 'login' }); // Redirect to the login page
    },
    filterItems() {
      this.filteredItems = this.items.filter(item => {
        const lowercaseItem = item.username.toLowerCase();
        return lowercaseItem.includes(this.searchTerm.toLowerCase());
      });
    },
    initializeFilteredItems() {
      this.filterItems();
    },
    
    fetchUsers() {
      axios
        .get('api/v1/users/')
        .then(response => {
          console.log(response.data); // Log the response data
          const responseData = response.data.users; // Assuming users array is inside a "users" property
          this.items = responseData.map(user => ({
            username: user.username,
            user_user_avatar: `http://127.0.0.1:8000${user.user_avatar}`
          }));
          this.filterItems(); // Initialize filteredItems with the complete list of users
        })
        .catch(error => {
          console.error('Error fetching users:', error);
        });
    },
    
    async sendMessage() {
        const username = this.userStore.user.username;
        const recipient = this.recipient;
        const message = this.message;

        if (!message.trim()) {
          return; // Don't send empty messages
        }

        try {
          const connection = new WebSocket("ws://localhost:8000//chat/");

          connection.onopen = () => {
            console.log("WebSocket connection opened.");

            const payload = JSON.stringify({
              message: message,
              username: username,
              recipient: recipient,
            });

            connection.send(payload);
          };

          this.message = ''; // Clear the input field after sending the message

          connection.onmessage = async (event) => {
            console.log('Received message:', event);

            const data = JSON.parse(event.data);
            await this.saveMessage(data.username, data.recipient, data.message);
            await this.fetchChatMessages(recipient); // Update chat messages immediately after saving the new message
          };

          connection.onclose = () => {
            console.log("WebSocket connection closed.");
          };

          connection.onerror = (error) => {
            console.error('WebSocket error:', error);
          };
        } catch (error) {
          console.error('Error sending message:', error);
        }
      },
    saveMessage(senderUsername, recipientUsername, message) {
      console.log('Saving message:', senderUsername, recipientUsername, message);

      const existingMessage = this.chatItems.find(item => item.message === message);

      if ( !existingMessage ){
        this.chatItems.push({
        username: senderUsername,
        message:message
      })
      }
      
    },
    async fetchChatMessages(recipientUsername) {
        try {
          const senderUsername = this.userStore.user.username;
          // clear the chatitem
          this.chatItems = [];

          const response = await axios.get(`/chat/api/v1/fetch-chat-messages/${senderUsername}/${recipientUsername}/`);
          console.log('Response:', response);
          this.chatItems = response.data;
          console.log('Chat Messages:', this.chatItems);
        } catch (error) {
          console.error('Error fetching chat messages:', error);
        }
    },
    scrollToBottom(){
      this.$nextTick(() =>{
        const container = this.$refs.chatContainer;
        container.scrollTop = container.scrollHeight;
      })
    },


  },
  
  created() {
    this.userStore.initStore();

    const token = this.userStore.user.access;

    if (token) {
      axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;

      // Check if the user is authenticated
      if (this.userStore.user.isAuthenticated) {
        // User is authenticated, proceed to the home page
        this.$router.push({ name: 'home' });
      } else {
        // User is not authenticated, redirect to the login page
        this.$router.push({ name: 'login' });
      }
    } else {
      axios.defaults.headers.common['Authorization'] = '';

      // User is not authenticated, redirect to the login page
      this.$router.push({ name: 'login' });
    }

    this.fetchUsers();
    this.initializeFilteredItems();
  }
};
</script>