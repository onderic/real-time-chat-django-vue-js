<template>
  <div class="tracking-wider flex flex-col min-h-screen">
    <div class="relative flex min-h-screen" v-if="userStore.user.isAuthenticated">
      <!-- Sidebar content -->
      <div class="bg-white dark:text-white w-1/3 space-x-6 shadow-lg border border-gray-300 px-0 py-4 absolute inset-y-0 left-0 md:relative md:-translate-x-0 transform -translate-x-full transition duration-200 ease-in-out">
        <!-- Sidebar content -->
        <div class="bg-gray-100 py-9 px-4 overflow-y-auto flex items-center justify-between fixed top-0 w-full border border-b-0">
        </div>

        <div class="mt-20">
          <div>
            <input
              type="text"
              v-model="searchTerm"
              @input="filterItems"
              placeholder="Search"
              class="border border-gray-300 rounded-md px-4 py-2 w-64"
            />

            <ul v-if="filteredItems.length > 0" class="mt-2">
              <li
                v-for="(item, index) in filteredItems"
                :key="index"
                class="border border-gray-300 rounded-md px-4 py-2"
              >
                {{ item }}
              </li>
            </ul>

            <p v-else-if="searchTerm" class="mt-2">No results found.</p>
            <p v-else class="mt-2">Type to search.</p>
          </div>
        </div>
      </div>

      <!-- Main content -->
      <div class="h-screen w-full overflow-y-auto">
        <div class="mb-20">
          <nav class="bg-gray-100 py-6 px-4 overflow-y-auto flex items-center justify-between fixed top-0 lg:left-1/4 lg:w-3/4 w-full border-l border-gray-200">
            <!-- Navigation content -->
            <h1>hfhfhf</h1>
          </nav>
        </div>

        <!-- Main content -->
        <div class="flex flex-col min-h-screen px-4 lg:px-8">
          <div>
            <router-view />
          </div>
        </div>

        <div class="border-t border-gray-300 w-full"></div>

        <footer class="bg-white-200 w-full py-4">
          <div class="container mx-auto text-center">
            <p class="text-gray-600 dark:text-white">&copy; 2023 Your Company. All rights reserved.</p>
          </div>
        </footer>

        <toast></toast>
      </div>
    </div>
    <router-view v-else></router-view>
  </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { ref, onMounted } from 'vue'

export default {
  setup() {
    const userStore = useUserStore()
    const searchTerm = ref('')
    const items = ref([])
    const filteredItems = ref([])

    const filterItems = () => {
      filteredItems.value = items.value.filter((item) =>
        item.toLowerCase().includes(searchTerm.value.toLowerCase())
      )
    }

    // Function to initialize the filtered items on page load
    const initializeFilteredItems = () => {
      filterItems()
    }

    // Fetch users from the backend API and update the items array
    const fetchUsers = () => {
      axios.get('api/v1/chat')
        .then(response => {
          console.log(response.data); // Log the response data
          const responseData = response.data.users; // Assuming users array is inside a "users" property
          items.value = responseData.map(user => user.username);
          filterItems(); // Initialize filteredItems with the complete list of users
        })
        .catch(error => {
          console.error('Error fetching users:', error);
        });
    };


    // Call fetchUsers() before the component is created
    onMounted(() => {
      fetchUsers()
    })

    // Call initializeFilteredItems() on page load
    onMounted(initializeFilteredItems)

    return {
      searchTerm,
      items,
      filteredItems,
      userStore,
      filterItems,
    }
  },

  created() {
    this.userStore.initStore()

    const token = this.userStore.user.access

    if (token) {
      axios.defaults.headers.common['Authorization'] = 'Bearer ' + token
    } else {
      axios.defaults.headers.common['Authorization'] = ''
    }
  },
}


</script>
