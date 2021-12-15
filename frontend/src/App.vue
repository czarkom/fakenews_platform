<template>
  <div class="w-full">
    <div class="sticky top-0 z-10">
      <img style="filter: grayscale(100%)"
           class="h-auto z-20 grayscale-0 w-screen h-screen bg-black absolute top-0 left-0 opacity-60"
           src="@/assets/resources/background.jpg">
    </div>
    <div class="sticky top-0 z-30">
      <div class="flex top-0 bg-gray-400 w-full items-center relative z-30">
        <div class="w-1/2 flex items-center mx-4 justify-center">
          <img src="@/assets/resources/fakenews_logo.png" class="h-12">
          <span class="font-bold text-xl">Fakenews platform</span>
        </div>
        <div class="w-1/2 flex justify-between">
          <router-link :to="{name: 'websiteAnalyzer'}" class="nav-link w-1/3">Website analyser</router-link>
          <router-link :to="{name: 'dataOverview'}" class="nav-link w-1/3">Data overview</router-link>
          <router-link :to="{name: 'knowledgeBase'}" class="nav-link w-1/3">Knowledge base</router-link>
        </div>
      </div>
    </div>
    <router-view class="relative z-20 ml-4 mr-10 mb-10"/>
  </div>
</template>
