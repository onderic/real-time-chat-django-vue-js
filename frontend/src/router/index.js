import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

import SignupView from '../views/Registration/SignupView.vue'
import LoginView from '../views/Registration/LoginView.vue'

import { useUserStore } from '@/stores/user';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },

     // Authentication
     {
      path: '/signup',
      name: 'signup',
      component: SignupView,
      meta: { requiresAuth: false },
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },

    
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
});

router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  const isAuthenticated = userStore.user.isAuthenticated;

  if (to.meta.requiresAuth && !isAuthenticated) {
    // Route requires authentication but user is not logged in, redirect to login
    next({ name: 'login', query: { to: to.path } });
  } else {
    // User is logged in or route doesn't require authentication, proceed with navigation
    next();
  }
});

export default router