<template>
  <div class="flex flex-col items-center justify-center h-screen">
    <h1 class="text-4xl mb-8">Hello, Welcome to my chat site! {{ userStore.user.username }}</h1>

    <div v-if="isAuthenticated" class="bg-white">
      <select v-model="recipient" class="mb-4">
        <option value="">Select a recipient</option>
        <option v-for="user in users" :value="user.username" :key="user.id" class="bg-white">{{ user.username }}</option>
      </select>

      <input v-model="message" type="text" id="id_message_send_input" class="mr-4">
      <button @click="sendMessage" id="id_message_send_button" class="px-4 py-2 bg-blue-500 text-white">Send Message</button>

      <div v-if="chatItems.length > 0">
        <div v-for="(item, index) in chatItems" :key="index" class="mt-4 bg-gray-400">
          {{ item.sender }}: {{ item.message }}
        </div>
      </div>
      <div v-else class="mt-4">No messages yet.</div>
    </div>
  </div>
  <router-view></router-view>
</template>



<script>
import { useUserStore } from '@/stores/user';
import axios from 'axios';

export default {
  name: 'ChatComponent',
  data() {
    return {
      users: [],
      recipient: '',
      message: '',
      chatItems: [],
      searchTerm: '',
      items: [],
      filteredItems: [],
      selectedUser: null,
      selectedUserImage: null
    };
  },
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },
  watch: {
  recipient: {
    immediate: true,
    handler(value) {
      if (value) {
        this.fetchChatMessages(value);
      } else {
        this.chatItems = [];
      }
    },
  },
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
    async fetchUsers() {
      try {
        const response = await axios.get('/api/v1/users/');
        console.log('Response:', response);
        this.users = response.data.users.map(user => ({
          ...user,
          user_avatar: `http://127.0.0.1:8000${user.user_avatar}`
        }));
        console.log('Users:', this.users);
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    },

    async sendMessage() {
        const username = this.userStore.user.username;
        const recipient = this.recipient;
        const message = this.message;

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
        const senderUsername = this.userStore.user.username; // Get the sender's username from the userStore

        const response = await axios.get(`/chat/api/v1/fetch-chat-messages/${senderUsername}/${recipientUsername}/`);
        console.log('Response:', response);
        this.chatItems = response.data;
        console.log('Chat Messages:', this.chatItems);
      } catch (error) {
        console.error('Error fetching chat messages:', error);
      }
    },


  },
  computed: {
    isAuthenticated() {
      return this.userStore.user.isAuthenticated;
    },
  },
  beforeCreate() {
    this.userStore.initStore();

    const token = this.userStore.user.access;

    if (token) {
      axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;
    } else {
      axios.defaults.headers.common['Authorization'] = '';
    }
  },
};
</script>

<style scoped>

</style>
