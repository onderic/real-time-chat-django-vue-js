<script setup>
import { RouterLink, RouterView } from 'vue-router'

</script>

<template>
<div class="flex  bg-white  h-screen">
  <div class="w-1/4 h-screen  bg-gray-100">
    <div class="bg-gray-100 py-10 px-4   w-full border-b border-gray-200 flex items-center justify-between fixed top-0">
      
    </div>
    <!-- Sidebar content -->
    
  </div>
  <div class="">
    <nav class=" bg-gray-100 py-6 px-4  flex items-center justify-between fixed top-0 left-1/4 w-3/4  border-l border-gray-200">
      <div class="flex items-center">
        <img src="logo.png" alt="Logo" class="w-8 h-8 mr-2">
        <span class="text-gray-800 font-bold text-lg">Chat</span>
      </div>
      <ul class="flex items-center space-x-4">
      
        <li><a href="#" class="text-gray-800">Services</a></li>
        <li><a href="#" class="text-gray-800">Contact</a></li>
      </ul>
    </nav>
   
  </div>
  <div class=" mt-20 px-8 text-white py-8 w-3/4">
      <!-- Main content -->
      <h1 class="text-2xl font-bold">Welcome to the Chat App!</h1>
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam malesuada erat ut nunc consectetur, ut finibus mi eleifend. Suspendisse efficitur ligula id volutpat sagittis. Duis sed interdum turpis.</p>
    </div>
  <div>
    
  </div>
</div>

 
  <!-- <RouterView /> -->
</template>

<style>
</style>