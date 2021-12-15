<template>
  <div>
    <div class="text-xl text-gray-800 font-bold p-4">
      Websites data overview
    </div>

    <template v-if="websitesData">
      <div class="mx-4 w-full">
        <table class="table">
          <thead>
          <tr>
            <th>
              No.
            </th>
            <th>
              Website url
            </th>
            <th>
              Exclamations
            </th>
            <th>
              Words to avoid
            </th>
            <th>
              Smart words
            </th>
            <th>
              View details
            </th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(website, index) in websitesData.data" :key="index">
            <td>{{ index + 1 }}.</td>
            <td>
              <a :href="website.url" target="_blank" class="hover:text-blue-700">
                {{ formatUrl(website.url) }}
              </a>
            </td>
            <td>{{ website.exclamation_count }}</td>
            <td>{{ website.words_to_avoid_count }}</td>
            <td>{{ website.smart_words_count }}</td>
            <td class="w-36">
              <div class="border-2 border-gray-600 rounded-xl cursor-pointer" @click="openWebsiteDataPreview(website)">
                Open<i class="ml-2 fas fa-envelope-open-text"></i>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
      <div class="m-8 p-12 rounded border-2 border-gray-500 text-gray-800" v-if="!websitesData.data.length">
        No entries in databse
      </div>
    </template>
    <template v-else-if="loading">
      <div class="alert mt-10 ml-6">
        <div class="text-xl flex items-center">
          <div>
            <i class="fas fa-spinner fa-pulse"></i>
          </div>
          <div class="ml-4">
            Loading websites data
          </div>
        </div>
      </div>
    </template>
    <div v-else-if="error" class="m-8 p-12 rounded border-2 border-red-500 text-red-500">
      Error occured during fetching data
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import 'load-awesome/css/ball-circus.css'

export default {
  name: 'dataOverview',
  components: {},
  data() {
    return {
      websitesData: null,
      error: null,
      loading: false,
      websiteDataPreviewOpened: false,
      previewWebsiteData: null
    }
  },
  mounted() {
    this.loading = true
    axios.get('data').then(
        response => {
          this.websitesData = response;
        },
        error => {
          this.error = error;
        }
    ).finally(
        () => this.loading = false
    )
  },
  methods: {
    openWebsiteDataPreview(website) {
      this.websiteDataPreviewOpened = true;
      this.previewWebsiteData = website;
    },
    formatUrl(url) {
      if (url.length > 10) {
        return (url.substring(0, 40) + "...");
      } else {
        return url;
      }
    }
  }
}
</script>