<template>
    <div :style="{'background-image' : 'url(../assets/resources/background.jpg)'}"
         class="my-4 flex flex-col items-center">
      <div class="w-full flex justify-center text-3xl font-semibold my-4">
        Enter your URL for analysis
      </div>
      <div class="flex">
        <div class="mx-2">
          <input class="input" type="text" v-model="query" placeholder="https://fronda.pl/farmazon">
        </div>
        <div class="mx-2">
          <div @click="submit" class="button">
            <span class="mr-2">Wyślij</span>
            <span class="ml-2"><i class="fas fa-paper-plane"></i></span>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';

export default {
  name: 'Home',
  components: {
  },
  data() {
    return {
      query: null
    }
  },
  mounted() {
    console.log(axios.defaults.baseURL);
  },
  methods: {
    submit(){
      axios.post('search', {
        url: this.query
      })
    }
  }
}
</script>
