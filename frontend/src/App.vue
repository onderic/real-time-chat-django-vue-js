<template>
  <div class="tracking-wider  flex flex-col min-h-screen">
    <div class="relative flex min-h-screen" v-if="userStore.user.isAuthenticated">
      <!-- Sidebar content -->
      <div class="bg-slate-300  dark:text-white w-1/3 space-x-6 shadow-lg border border-gray-300 px-0 py-4 absolute inset-y-0 left-0 md:relative md:-translate-x-0 transform -translate-x-full transition duration-200 ease-in-out">
        <!-- Sidebar content -->
        <div class="bg-slate-400 py-2 px-4 overflow-y-auto flex items-center justify-between fixed top-0 w-full border border-b-0">
          <div class="flex items-center">
            <img :src="userStore.user.user_avatar" alt="logo" class="mr-2 h-12 w-12 rounded-full border-2 border-green-400">
          </div>
          <div class="ml-auto">
            <button class="bg-sky-500 hover:bg-sky-700 text-white font-bold py-1 px-2 rounded-md" @click="logout()">logout</button>
          </div>
        </div>


        <div class="mt-20">
          <div class="mr-4">
            
            <input
              type="text"
              v-model="searchTerm"
              @input="filterItems"
              placeholder="Search..."
              class="border border-gray-100 bg-white rounded-md px-4 py-2 w-full pl-10"
            />
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
            </div>

            <div :class="{ 'bg-gray-100': selectedUser, 'bg-white': !selectedUser }" class="flex flex-col min-h-screen">
            <div class="px-4 mt-20 py-8">
              <div class="w-1/4">
                <h2 v-if="selectedUser" class="bg-white px-4 py-4">Selected User: {{ selectedUser }}</h2>
              </div>
            </div>
            <div class="w-1/4 relative flex items-center">
                <h2 v-if="selectedUser" class="bg-green-400 px-4 py-4">Selected User: {{ selectedUser }}</h2>
              </div>
            <div class="flex-grow"></div> <!-- Add this div to push the footer to the bottom -->

            <div v-if="selectedUser" class="mb-3 bg-slate-400 p-4">
              <div class="flex items-center rounded-md px-10">
                <textarea class="w-full rounded-md py-1 px-4 " placeholder="Type here..."></textarea>
                <button class="ml-2 focus:outline-none bg-white p-3 rounded-md">
                <i class="fas fa-paper-plane text-gray-600 hover:text-gray-800"></i>
              </button>
              </div>
            </div>

          </div>

          


        <div class="border-t border-gray-300 w-full"></div>

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
import axios from 'axios'
import { useUserStore } from '@/stores/user'


export default {
  setup() {
      const userStore = useUserStore()
      return {
          userStore
      }
  },

  data() {
    return {
      searchTerm: '',
      items: [],
      filteredItems: [],
      selectedUser: null,
  
    };
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
      this.filteredItems = this.items.filter((item) => {
        const lowercaseItem = item.username.toLowerCase();
        return lowercaseItem.includes(this.searchTerm.toLowerCase());
      });
    },
    initializeFilteredItems() {
      this.filterItems();
    },
    fetchUsers() {
      axios.get('api/v1/chat')
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
  },
  created() {
    this.userStore.initStore();

    const token = this.userStore.user.access;

    if (token) {
      axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;
    } else {
      axios.defaults.headers.common['Authorization'] = '';
    }

    this.fetchUsers();
    this.initializeFilteredItems();
  },
};

</script>