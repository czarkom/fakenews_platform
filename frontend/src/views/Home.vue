<template>
    <div :style="{'background-image' : 'url(../assets/resources/background.jpg)'}"
         class="my-4 flex flex-col items-center">
      <div class="w-full flex justify-center text-3xl font-semibold my-4">
        Enter your URL for analysis
      </div>
      <div class="flex">
        <div class="mx-2">
          <input
              class="input"
              style="width: 400px !important;"
              type="text"
              v-model="query"
              placeholder="https://fronda.pl/farmazon"
              @keyup.enter="submit">
        </div>
        <div class="mx-2">
          <div @click="submit" class="button">
            <span class="mr-2">Wyślij</span>
            <span class="ml-2"><i class="fas fa-paper-plane"></i></span>
          </div>
        </div>
      </div>
      <div v-if="loading" class="my-8 text-3xl">
        <div class="la-ball-circus text-3xl">
          <div></div>
          <div></div>
          <div></div>
        </div>
      </div>
      <div class="w-2/3 border-4 rounded my-8 border-black" v-if="websiteData">
        <div class="flex items-center justify-center border-b-2 mx-2 border-black">
          <div class="font-semibold text-center text-2xl my-2">
            Website's data
          </div>
        </div>
        <div class="m-2">
          <div class="my-2">
            div elements: {{websiteData.div}}
          </div>
          <div class="my-2">
            a elements: {{websiteData.a}}
          </div>
          <div class="my-2">
            span elements: {{websiteData.span}}
          </div>
          <div class="my-2">
            iframe elements: {{websiteData.iframe}}
          </div>
          <div class="my-2">
            button elements: {{websiteData.button}}
          </div>
        </div>
      </div>
    </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import 'load-awesome/css/ball-circus.css'

export default {
  name: 'Home',
  components: {
  },
  data() {
    return {
      query: null,
      websiteData: null,
      loading: false,
    }
  },
  mounted() {
    console.log(axios.defaults.baseURL);
  },
  methods: {
    submit(){
      this.websiteData = null;
      this.loading = true;
      axios.post('search', {
        url: this.query
      }).then( response => {
        this.websiteData = response.data;
      }).finally( () => {
        this.loading = false
      }
      )
    }
  }
}
</script>

<style>
 .la-ball-circus {
    color: black;
}
</style>
