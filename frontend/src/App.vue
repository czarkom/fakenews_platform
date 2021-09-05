<template>
  <div class="w-full">
    <img style="filter: grayscale(100%)" class="h-auto grayscale-0 w-screen h-screen bg-black absolute top-0 left-0 opacity-60" src="@/assets/resources/background.jpg">
    <div class="h-16">
      <div class="absolute top-0 left-0 bg-gray-400 opacity-60 w-full h-16"></div>
      <div class="flex relative w-full items-center h-full">
        <div class="w-1/2 flex items-center mx-4 h-full justify-center">
          <img src="@/assets/resources/fakenews_logo.png" class="h-12">
          <span class="font-bold text-xl">Fakenews platform</span>
        </div>
        <div class="w-1/2 flex justify-between">
          <router-link :to="{name: 'home'}" class="nav-link w-1/3">Website analyser</router-link>
          <router-link :to="{name: 'statistics'}" class="nav-link w-1/3">Statistics</router-link>
          <router-link :to="{name: 'statistics'}" class="nav-link w-1/3">About project</router-link>
        </div>
      </div>
    </div>
    <router-view class="relative"/>
  </div>
</template>
