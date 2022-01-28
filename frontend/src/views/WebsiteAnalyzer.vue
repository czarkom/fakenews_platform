<template>
  <div :style="{'background-image' : 'url(../assets/resources/background.jpg)'}"
       class="my-4 flex flex-col items-center ml-4">
    <div class="w-full flex justify-center text-3xl font-semibold my-8">
      Wpisz adres URL wybranej strony
    </div>
    <div class="flex">
      <div class="mx-2">
        <input
            class="input"
            style="width: 400px !important;"
            type="text"
            v-model="url"
            placeholder="https://breakingnews.com/very-IMPORTANT-info"
            @keyup.enter="submit">
      </div>
      <div class="mx-2">
        <div @click="submit" class="button">
          <span class="mr-2">Wyślij</span>
          <span class="ml-2"><i class="fas fa-paper-plane"></i></span>
        </div>
      </div>
    </div>
    <div v-if="loading" class="my-8 text-3xl mt-36">
      <div class="la-ball-circus text-7xl">
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>
    <div class="w-11/12 border-2 rounded my-8 border-gray-400 p-4" v-if="websiteData">
      <div class="flex items-center justify-center py-4">
        <div class="font-semibold text-xl p-2 mr-8">
          Ocena Twojej strony:
        </div>
        <CircleProgress :percent="percent"
                        :show-percent="true"
                        :viewport="true"
                        :transition="5000"
                        :size="100"
                        :border-width="20"
                        :fill-color="description.color"
                        class="font-semibold text-lg"
        />
        <div class="p-2 mx-2 text-3xl font-extrabold" style="-webkit-text-stroke: 1px black;"
             :style="{ color: description.color }">
          {{ description.text }}
        </div>
      </div>
      <div class="flex items-center justify-center border-b-2 mx-2 border-gray-400">
        <div class="p-4 font-semibold text-center text-lg flex">
          Szczegółowe dane pozyskane ze strony:
          <div class="hover:text-blue-700 italic ml-4 cursor-pointer">
            <i class="fas fa-link mr-1"></i>
            <a :href="url" target="_blank">
              {{ formatUrl(websiteData.url, 50) }}
            </a>
          </div>
        </div>
      </div>
      <div class="m-2">
        <div class="mt-2 flex items-center mb-4">
          <div class="font-semibold mr-4">
            Legenda:
          </div>
          <div class="flex font-semibold items-center ml-2">
            <div class="mx-4 flex">
              <i class="fas fa-long-arrow-alt-up" style="color: #3690c0"></i>
              <i class="fas fa-long-arrow-alt-down" style="color:#045a8d"></i>
            </div>
            <div class="mr-1 text-xs">
              Blisko mediany
            </div>
            <img src="@/assets/resources/colorscale.png" class="h-6">
            <div class="ml-1 text-xs">
              Daleko od mediany
            </div>
          </div>
        </div>
        <div class="grid grid-cols-3" v-if="statistics">
          <div v-for="(value, name) in filteredWebsiteData" :key="name" class="text-sm my-1">
            <div v-if="!['url','rating'].includes(name)">
              <span class="font-semibold">{{ name }}: </span>
              <span class="font-medium">{{ value }}</span>
              <i class="fas fa-long-arrow-alt-up ml-2"
                 v-if="getArrowDirection(name) === 'up'"
                 :style="{ color: calculateArrowColor(name) }"></i>
              <i class="fas fa-long-arrow-alt-down ml-2"
                 v-if="getArrowDirection(name) === 'down'"
                 :style="{ color: calculateArrowColor(name) }"></i>
              <i class="fas fa-equals ml-2"
                 v-if="getArrowDirection(name) === 'even'"></i>
              <span class="ml-4">(Mediana: {{statistics[name]['50%']}})</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import 'load-awesome/css/ball-circus.css'
import {nextTick} from "vue";
import "vue3-circle-progress/dist/circle-progress.css";
import CircleProgress from "vue3-circle-progress";
import {RATING_WORDS} from "@/assets/utils/rating_words"

export default {
  name: 'websiteAnalyzer',
  components: {
    CircleProgress: CircleProgress
  },
  data() {
    return {
      url: null,
      websiteData: null,
      loading: false,
      percent: 0,
      description: null,
      statistics: null
    }
  },
  computed: {
    filteredWebsiteData() {
      const notAllowed = ['url', 'rating', 'statistics'];

      return Object.keys(this.websiteData)
          .filter(key => !notAllowed.includes(key))
          .reduce((obj, key) => {
            obj[key] = this.websiteData[key];
            return obj;
          }, {});
    }
  },
  methods: {
    async submit() {
      this.websiteData = null;
      this.percent = 0;
      this.loading = true;
      await nextTick();
      axios.post('analyze', {
        url: this.url
      }).then(response => {
        this.websiteData = response.data;
        this.statistics = JSON.parse(this.websiteData.statistics)
        this.percent = (this.websiteData.rating) / 5 * 100;
        this.description = RATING_WORDS[Math.round(this.percent / 10)]
      }).finally(() => {
            this.loading = false
          }
      )
    },
    formatUrl(url, length) {
      if (url.length > length) {
        return (url.substring(0, length) + "...");
      } else {
        return url;
      }
    },
    calculateArrowColor(column) {
      return this.calculateArrowColorUtil(column, this.websiteData, this.statistics)
    },
    getArrowDirection(column) {
      return this.getArrowDirectionUtil(column, this.websiteData, this.statistics)
    }
  }
}
</script>

<style>
.la-ball-circus {
  color: black;
}
</style>
