import { defineStore } from 'pinia';
import axios from 'axios';

export const useUserStore = defineStore({
  id: 'user', // Unique identifier for the store instance

  state: () => ({
    user: {
      // Initial state of the user object
      isAuthenticated: false,
      id: null,
      name: null,
      email: null,
      phone_number: null,
      user_avatar: null,
      access: null,
      refresh: null,
    },
  }),

  actions: {
    initStore() {
      // Action to initialize the store's state from localStorage
      console.log('initStore', localStorage.getItem('user.access'));

      if (localStorage.getItem('user.access')) {
        console.log('User has access!');

        // Retrieve user data from localStorage and update the state
        this.user.access = localStorage.getItem('user.access');
        this.user.refresh = localStorage.getItem('user.refresh');
        this.user.id = localStorage.getItem('user.id');
        this.user.name = localStorage.getItem('user.name');
        this.user.email = localStorage.getItem('user.email');
        this.user.user_avatar = localStorage.getItem('user.user_avatar');
        this.user.phone_number = localStorage.getItem('user.phone_number');
        this.user.isAuthenticated = true;

        // Call refreshToken action to update the access token
        this.refreshToken();

        console.log('Initialized user:', this.user);
      }
    },

    setToken(data) {
      // Action to set the access and refresh tokens in the store's state and localStorage
      console.log('setToken', data);

      this.user.access = data.access;
      this.user.refresh = data.refresh;
      this.user.isAuthenticated = true;

      localStorage.setItem('user.access', data.access);
      localStorage.setItem('user.refresh', data.refresh);

      console.log('user.access:', localStorage.getItem('user.access'));
    },

    removeToken() {
      // Action to remove tokens and user data from the store's state and localStorage
      console.log('removeToken');

      this.user.refresh = null;
      this.user.access = null;
      this.user.isAuthenticated = false;
      this.user.id = null;
      this.user.name = null;
      this.user.email = null;
      this.user.user_avatar = null;
      this.user.phone_number = null;

      localStorage.setItem('user.access', '');
      localStorage.setItem('user.refresh', '');
      localStorage.setItem('user.id', '');
      localStorage.setItem('user.name', '');
      localStorage.setItem('user.email', '');
      localStorage.setItem('user.user_avatar', '');
      localStorage.setItem('user.phone_number', '');
    },

    setUserInfo(user) {
      // Action to set user information in the store's state and localStorage
      console.log('setUserInfo', user);

      this.user.id = user.id;
      this.user.name = user.name;
      this.user.email = user.email;

      // Fetch additional user data from the backend and update the user object
      axios
        .get(`/api/v1/users/${this.user.id}/`)
        .then(response => {
          const userData = response.data;
          this.user.user_avatar = `http://127.0.0.1:8000${userData.user_avatar}`;
          this.user.phone_number = userData.phone_number ? userData.phone_number : null;
          localStorage.setItem('user.user_avatar', this.user.user_avatar);
          localStorage.setItem('user.phone_number', this.user.phone_number);
          console.log('User:', this.user);
        })
        .catch(error => {
          console.error('Error fetching user data:', error);
        });

      // Update user information in localStorage
      localStorage.setItem('user.id', this.user.id);
      localStorage.setItem('user.name', this.user.name);
      localStorage.setItem('user.email', this.user.email);
      localStorage.setItem('user.phone_number', this.user.phone_number);

      console.log('User:', this.user);
    },

    refreshToken() {
      // Action to refresh the access token
      axios
        .post('/api/v1/refresh/', {
          refresh: this.user.refresh,
        })
        .then(response => {
          this.user.access = response.data.access;

          localStorage.setItem('user.access', response.data.access);

          axios.defaults.headers.common['Authorization'] = 'Bearer ' + response.data.access;
        })
        .catch(error => {
          console.log(error);

          // If token refresh fails, remove tokens and user data
          this.removeToken();
        });
    },
  },
});
