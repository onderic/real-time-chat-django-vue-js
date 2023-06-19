import { defineStore } from 'pinia';
import axios from 'axios';

export const useUserStore = defineStore({
  id: 'user',

  state: () => ({
    user: {
      isAuthenticated: false,
      id: null,
      username: null,
      email: null,
      phone_number: null,
      user_avatar: null,
      access: null,
      refresh: null,
    },
  }),

  actions: {
    initStore() {
      console.log('initStore', localStorage.getItem('user.access'));

      if (localStorage.getItem('user.access')) {
        console.log('User has access!');

        this.user.access = localStorage.getItem('user.access');
        this.user.refresh = localStorage.getItem('user.refresh');
        this.user.id = localStorage.getItem('user.id');
        this.user.username = localStorage.getItem('user.username');
        this.user.email = localStorage.getItem('user.email');
        this.user.user_avatar = localStorage.getItem('user.user_avatar');
        this.user.phone_number = localStorage.getItem('user.phone_number');
        this.user.isAuthenticated = true;

        this.refreshToken();

        console.log('Initialized user:', this.user);
      }
    },

    setToken(data) {
      console.log('setToken', data);

      this.user.access = data.access;
      this.user.refresh = data.refresh;
      this.user.isAuthenticated = true;

      localStorage.setItem('user.access', data.access);
      localStorage.setItem('user.refresh', data.refresh);

      console.log('user.access:', localStorage.getItem('user.access'));
    },

    removeToken() {
      console.log('removeToken');

      this.user.refresh = null;
      this.user.access = null;
      this.user.isAuthenticated = false;
      this.user.id = null;
      this.user.username = null;
      this.user.email = null;
      this.user.user_avatar = null;
      this.user.phone_number = null;

      localStorage.setItem('user.access', '');
      localStorage.setItem('user.refresh', '');
      localStorage.setItem('user.id', '');
      localStorage.setItem('user.username', '');
      localStorage.setItem('user.email', '');
      localStorage.setItem('user.user_avatar', '');
      localStorage.setItem('user.phone_number', '');
    },

    setUserInfo(user) {
      console.log('setUserInfo', user);
    
      this.user.id = user.id;
      this.user.username = user.username;
      this.user.email = user.email;
    
      // Fetch user avatar and phone number from backend and update the user object
      axios
        .get(`/api/v1/user/${this.user.id}/`)
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
    
      localStorage.setItem('user.id', this.user.id);
      localStorage.setItem('user.username', this.user.username);
      localStorage.setItem('user.email', this.user.email);
      localStorage.setItem('user.phone_number', this.user.phone_number);
    
      console.log('User:', this.user);
    },
    

    refreshToken() {
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

          this.removeToken();
        });
    },
  },
});
