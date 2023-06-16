
<template>
  <div class="tracking-wider  flex flex-col min-h-screen">
    <div class="relative flex min-h-screen" v-if="userStore.user.isAuthenticated">
      <!-- Sidebar content -->
      <div class="fixed top-0 h-screen bg-slate-300 dark:text-white w-1/3 space-x-6 shadow-lg border border-gray-300 px-0 py-4 inset-y-0 left-0 md:relative md:-translate-x-0 transform -translate-x-full transition duration-200 ease-in-out overflow-y-auto">
  <!-- Sidebar content -->
  <div class="bg-slate-400 py-2 top-0 px-4 flex items-center justify-between">
    <div class="flex items-center">
      <img :src="userStore.user.user_avatar" alt="logo" class="mr-2 h-12 w-12 rounded-full border-2 border-green-400">
    </div>
    <div class="ml-auto">
      <button class="bg-sky-500 hover:bg-sky-700 text-white font-bold py-1 px-2 rounded-md" @click="logout()">logout</button>
   
    </div>

  </div>
 <div class="mt-3 bg-slate-400 px-3 w-3/4 py-2 rounded-md mr-3">
  <div >
        <input
        type="text"
        v-model="searchTerm"
        @input="filterItems"
        placeholder="Search..."
        class="border border-gray-100 rounded-md px-4 py-2 w-full"
      />
      </div>

 </div>
  <div class="mt-5">
    <div class="mr-4">
     
      <ul v-if="filteredItems.length > 0" class="mt-4">
        <li v-for="(item, index) in filteredItems" :key="index" class="border rounded-md mr-2 border-gray-50 mb-3 px-4 py-2">
          <div
            class="flex items-center space-x-1 w-full px-4 py-2 rounded-md cursor-pointer"
            :class="{ 'bg-white': selectedUser === item.username }"
            @click="selectUser(item.username)"
          >
            <img
              :src="item.user_user_avatar"
              alt=""
              class="mr-2 h-8 w-8 bg-white p-2 rounded-full"
            />
            <span class="mb-2" :class="{ 'font-bold': selectedUser === item.username }">{{ item.username }}</span>
          </div>
        </li>
      </ul>
      <p v-else-if="searchTerm" class="mt-2">No results found.</p>
      <p v-else class="mt-2">Type to search.</p>
    </div>
  </div>
    </div>
      <!-- Main content -->
          <div class="h-screen w-full overflow-y-auto">
            <div  v-if="selectedUser" class="mb-18">
              <nav  class="bg-slate-400 py-4 px-4 overflow-y-auto flex items-center justify-between fixed top-0 lg:left-1/4 lg:w-3/4 w-full border-l border-gray-200">
                <!-- Navigation content -->
                <div class="flex items-center">
                <img :src="getUserImage(selectedUser)" alt="" class="h-8 w-8 rounded-full mr-2">
                <span v-if="selectedUser">{{ selectedUser }}</span>
              </div>

              </nav>


              <div :class="{ 'bg-gray-50': selectedUser, 'bg-slate-300': !selectedUser }" class="flex flex-col min-h-screen">
            
                <div v-if="chatItems.length > 0" class="px-4 mt-20 py-8">
                  <div v-for="(item, index) in chatItems" :key="index" class="mt-4">
                    <div v-if="item.sender === userStore.user.username" class="bg-white ml-5 rounded-md shadow-md px-4 py-4 w-1/2">
                      <span>me :</span>
                      <span class="ml-3">{{ item.message }}</span>
                    </div>
                    <div v-else class="flex  justify-end">
                      <div class="bg-green-200 rounded-md w-1/2 shadow-md px-16 py-4">
                        <span>{{ item.sender }} :</span>
                        <span class="ml-3">{{ item.message }}</span>
                      </div>
                    </div>
                  </div>
               
              </div>

          
            <div class="flex-grow"></div> <!-- Add this div to push the footer to the bottom -->

            <div v-if="selectedUser" class="fixed bottom-0 mb-3 bg-slate-400 p-4 w-full">
          <div  class="flex items-center rounded-md px-10">
            <textarea  v-model="message"  type="text"  class="w-1/2 rounded-md py-1 px-4" placeholder="Type here..."></textarea>
            <button @click="sendMessage" class="ml-3 focus:outline-none bg-white p-3 rounded-md">
              <i class="fas fa-paper-plane text-gray-600 hover:text-gray-800"></i>
            </button>
          </div>
        </div>
          </div>

            </div>

        <!-- <footer class="bg-white-200 w-full py-4">
          <div class="container mx-auto text-center">
            <p class="text-gray-600 dark:text-white">&copy; 2023 Your Company. All rights reserved.</p>
          </div>
        </footer> -->

        <toast></toast>
      </div>
    </div>
    <router-view v-else></router-view>
  </div>
</template>

<script>
import axios from 'axios';
import { useUserStore } from '@/stores/user';

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
    selectUser(username) {
      this.selectedUser = username;
      const user = this.items.find(item => item.username === username);
      if (user) {
        this.selectedUserImage = user.user_user_avatar;
        this.recipient = user.username; // Store the recipient's name
      }
      // Perform any additional logic when a user is selected
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

        try {
          // Create a WebSocket connection and send the message
          const connection = new WebSocket("ws://localhost:8000//chat/");

          connection.onopen = () => {
            console.log("WebSocket connection opened.");

            // Construct the message payload
            const payload = JSON.stringify({
              message: message,
              username: username,
              recipient: recipient,
            });

            // Send the payload through the WebSocket connection
            connection.send(payload);
          };

          connection.onmessage = async (event) => {
            console.log('Received message:', event);

            // Handle the received message from the WebSocket
            const data = JSON.parse(event.data);
            await this.saveMessage(data.username, data.recipient, data.message);
            this.fetchChatMessages(recipient); // Update chat messages after saving the new message
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
          const response = await axios.get(`/chat/api/v1/fetch-chat-messages/${senderUsername}/${recipientUsername}/`);
          console.log('Response:', response);
          this.chatItems = response.data;
          console.log('Chat Messages:', this.chatItems);
        } catch (error) {
          console.error('Error fetching chat messages:', error);
        }
    }


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