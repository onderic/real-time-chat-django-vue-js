<template>
    <div v-if="!userStore.user.isAuthenticated"  id="app"  class="dark:bg-slate-800 mt-8 rounded-lg mx-auto">
      <div class="mb-4 px-16 text-white  bg-gray-800 ">
          <!--Logo-->
        <div class="text-center">
                    <img
                      class="mx-auto w-48"
                      src="https://tecdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/lotus.webp"
                      alt="logo" />
                    <h4 class="mb-12 mt-1 pb-1  dark:text-white text-xl font-semibold">
                      We are The Lotus Team
                    </h4>
                  </div>
          <form  @submit.prevent="submitForm" class="max-w-md mx-auto p-4 shadow-md rounded-lg">
            <div class="mb-4">
              <label for="name" class="block text-gray-700  dark:text-white font-bold mb-2">Username:</label>
              <input v-model="form.username" type="username" id="username" class="w-full px-3 dark:bg-slate-700 dark:text-white py-2 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500" placeholder="Enter your username">
            </div>
            <div class="mb-4">
              <label for="email" class="block text-gray-700  dark:text-white font-bold mb-2">Email:</label>
              <input v-model="form.email" type="email" id="email" class="w-full px-3 dark:bg-slate-700 dark:text-white py-2 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500" placeholder="Enter your email">
            </div>
            <div class="mb-4">
              <label for="password" class="block text-gray-700  dark:text-white font-bold mb-2">Password:</label>
              <input v-model="form.password1" type="password" class="w-full px-3 dark:bg-slate-700 dark:text-white py-2 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500" placeholder="Enter password">
            </div>
            <div class="mb-4">
              <label for="password" class="block text-gray-700  dark:text-white font-bold mb-2">Repeat Password:</label>
              <input v-model="form.password2" type="password" class="w-full px-3 dark:bg-slate-700 dark:text-white py-2 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500" placeholder="Repeat password">
            </div>
            <template v-if="errors.length > 0">
                <div class="bg-red-400 text-white mb-3 rounded-lg p-6">
                    <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                </div>
            </template>
            <button type="submit" class="submitbtn">Register</button>
            <!--Register button-->
            <div class="flex items-center mt-6 justify-between pb-6">
                <p class="mb-0 mr-2  dark:text-white">Already have an account?</p>
                <button type="button" class="submitbtnsml"><RouterLink :to="{'name': 'login'}">Login</RouterLink>  </button>
              </div>
          </form>
        </div>
          
        </div>
        
  </template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'; 

export default {
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    userStore.initStore();
    const token = userStore.user.access;

    if (token) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    } else {
      axios.defaults.headers.common["Authorization"] = "";
    }

    return {
      userStore,
      toastStore,
    };
  },
  mounted() {
    if (this.userStore.user.isAuthenticated) {
      // User is already logged in, redirect to home page
      this.$router.push('/')
    }
  },

    data() {
        return {
            form: {
                email: '',
                username: '',
                password1: '',
                password2: ''
            },
            errors: [],
        }
    },

    methods: {
  submitForm() {
    this.errors = []

    if (this.form.email === '') {
      this.errors.push('E-mail is missing')
    }

    if (this.form.username === '') {
      this.errors.push('Name is missing')
    }

    if (this.form.password1 === '') {
      this.errors.push('Password is missing')
    } else if (this.form.password1.length < 8) {
      this.errors.push('Password should be at least 8 characters long')
    }

    if (this.form.password1 !== this.form.password2) {
      this.errors.push('The password does not match')
    }

    if (this.errors.length === 0) {
      axios
    .post('api/v1/signup/', this.form)
    .then(response => {
        if (response.data.message === 'success') {
            // Handle success case
            this.toastStore.showToast(5000, 'You have successfully registered. Please log in', 'bg-emerald-500')

            this.form.email = ''
            this.form.username = ''
            this.form.password1 = ''
            this.form.password2 = ''
            this.$router.push('/login');
            // Redirect to home page
        } else {
            // Handle error case
            if (response.data.error) {
                const errorMessage = response.data.error;
                this.toastStore.showToast(5000, errorMessage, 'bg-red-300');
            } else {
                this.toastStore.showToast(5000, 'Seems you already have an account try to login', 'bg-red-300');
            }
        }
    })
    .catch(error => {
        if (error.response && error.response.data && error.response.data.error) {
            const errorMessage = error.response.data.error;
            this.toastStore.showToast(5000, errorMessage, 'bg-red-300');
        } else {
            console.log('error', error);
        }
    });

    }
  }
}

}
</script>