<template>
  <div id="app" class="container bg-white dark:bg-slate-800 mt-8 pb-8 px-4 mb-8 rounded-lg mx-auto">
      <div class="mb-4">
        <!--Logo-->
      <div class="text-center">
                  <img
                    class="mx-auto w-48"
                    src="https://tecdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/lotus.webp"
                    alt="logo" />
                  <h4 class="mb-12 mt-1 pb-1  dark:text-white  text-xl font-semibold">
                    We are The Lotus Team
                  </h4>
                </div>
        <form v-on:submit.prevent="submitForm" class="max-w-md mx-auto p-4 shadow-md dark:shadow-xl rounded-lg">
          <div class="mb-4">
            <label for="email" class="block text-gray-700 dark:text-white font-bold mb-2">Email:</label>
            <input v-model="form.email" type="email" id="email" class="w-full px-3 py-2  dark:bg-slate-700 dark:text-white border border-gray-300 rounded-md focus:outline-none focus:border-blue-500" placeholder="Enter your email">
          </div>
          <div class="mb-4">
            <label for="password" class="block text-gray-700 dark:text-white font-bold mb-2">Password:</label>
            <input v-model="form.password" type="password" id="password" class="w-full px-3 py-2  dark:bg-slate-700 dark:text-white border border-gray-300 rounded-md focus:outline-none focus:border-blue-500" placeholder="Enter your name">
          </div>

          <template v-if="errors.length > 0">
            <div class="bg-red-500 text-white mb-3 rounded-lg p-6">
                <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
            </div>
        </template>

          <button type="submit" class="submitbtn">Login</button>

          <!--Forgot password link-->
          <div class="mt-3  dark:text-white " >
            <a  href="#!">Forgot password?</a>
          </div>

          <!--Register button-->
          <div class="flex items-center mt-6 justify-between pb-6">
                    <p class="mb-0 mr-2  dark:text-white ">Don't have an account?</p>
                    <button type="button" class="submitbtnsml"><RouterLink :to="{'name': 'signup'}">Register</RouterLink>  </button>
                  </div>
        </form>
      </div>
        
      </div>
      
</template>

<script>
import axios from 'axios';
import { useUserStore } from '@/stores/user';

export default {
  setup() {
    const userStore = useUserStore();

    return {
      userStore,
    };
  },

  data() {
    return {
      form: {
        email: '',
        password: '',
      },
      errors: [],
    };
  },

  methods: {
    async submitForm() {
      this.errors = [];

      if (this.form.email === '') {
        this.errors.push('Your e-mail is missing');
      }

      if (this.form.password === '') {
        this.errors.push('Your password is missing');
      }

      if (this.errors.length === 0) {
        try {
          const response = await axios.post('api/v1/login/', this.form);
          this.userStore.setToken(response.data);
          axios.defaults.headers.common['Authorization'] = 'Bearer ' + response.data.access;

          const response2 = await axios.get('api/v1/me/');
          this.userStore.setUserInfo(response2.data);

        // Redirect the user to the intended page or home ('/')
         const intendedPage = this.$route.query.to || '/';
          this.$router.push(intendedPage);

          // Trigger a full home page reload
          location.reload();
        } catch (error) {
          this.errors.push('Invalid email or password');
          console.log('error', error);
        }
      }
    },
  },
};
</script>
