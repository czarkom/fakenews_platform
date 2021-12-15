<template>
  <div>
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
                <div class="flex justify-center">
                  <span>Exclamations</span>
                  <div class="ml-2 text-xl cursor-pointer flex flex-col">
                    <i :class="{'invisible': !showExclamationsOrderAsc }" @click="sortDescending('exclamation_count')"
                       class="-mb-3 fas fa-sort-up"></i>
                    <i :class="{'invisible': !showExclamationsOrderDesc }" @click="sortAscending('exclamation_count')"
                       class="-mt-1 fas fa-sort-down"></i>
                  </div>
                </div>
              </th>
              <th>
                <div class="flex justify-center">
                  <span>Words to avoid</span>
                  <div class="ml-2 text-xl cursor-pointer flex flex-col">
                    <i :class="{'invisible': !showWordsToAvoidOrderAsc }"
                       @click="sortDescending('words_to_avoid_count')"
                       class="-mb-3 fas fa-sort-up"></i>
                    <i :class="{'invisible': !showWordsToAvoidOrderDesc }"
                       @click="sortAscending('words_to_avoid_count')"
                       class="-mt-1 fas fa-sort-down"></i>
                  </div>
                </div>
              </th>
              <th>
                <div class="flex justify-center">
                  <span>Smart words</span>
                  <div class="ml-2 text-xl cursor-pointer flex flex-col">
                    <i :class="{'invisible': !showSmartWordsOrderAsc }" @click="sortDescending('smart_words_count')"
                       class="-mb-3 fas fa-sort-up"></i>
                    <i :class="{'invisible': !showSmartWordsOrderDesc }" @click="sortAscending('smart_words_count')"
                       class="-mt-1 fas fa-sort-down"></i>
                  </div>
                </div>
              </th>
              <th>
                View details
              </th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(website, index) in websitesData" :key="index">
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
                <div class="border-2 border-gray-600 bg-gray-200 rounded-xl cursor-pointer shadow-xl shadow-inner"
                     @click="openWebsiteDataPreview(website)">
                  Open<i class="ml-2 fas fa-envelope-open-text"></i>
                </div>
              </td>
            </tr>
            </tbody>
          </table>
        </div>
        <div class="m-8 p-12 rounded border-2 border-gray-500 text-gray-800" v-if="!websitesData.length">
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
    <div class="modal" v-if="websiteDataPreviewOpened">
      <div class="rounded-lg overflow-hidden w-3/4">
        <div class="bg-gray-300 p-4 font-semibold text-center">
          Detailed data scrapped from
          <a :href="previewWebsiteData.url" target="_blank" class="hover:text-blue-700 italic">
            {{ formatUrl(previewWebsiteData.url) }}
          </a>
        </div>
        <div class="bg-white p-4">
          <div class="grid grid-cols-3">
            <div v-for="(column, index) in previewWebsiteDataToDisplay" :key="index">
              {{ column }}: {{previewWebsiteData[column]}}
            </div>
          </div>
        </div>
        <div class="bg-gray-300 p-2 font-semibold text-right">
          <div class="button button-danger" @click="closeMessagePreview">Close</div>
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
  name: 'dataOverview',
  components: {},
  data() {
    return {
      websitesData: null,
      error: null,
      loading: false,
      websiteDataPreviewOpened: false,
      previewWebsiteData: null,
      sortingOrder: {
        exclamation_count: undefined,
        smart_words_count: undefined,
        words_to_avoid_count: undefined
      },
      hiddenColumns: ['url', 'id']
    }
  },
  mounted() {
    this.loading = true
    axios.get('data').then(
        response => {
          this.websitesData = response.data;
        },
        error => {
          this.error = error;
        }
    ).finally(
        () => this.loading = false
    )
  },
  computed: {
    showExclamationsOrderAsc() {
      return this.sortingOrder.exclamation_count === 'asc' || this.sortingOrder.exclamation_count === undefined
    },
    showExclamationsOrderDesc() {
      return this.sortingOrder.exclamation_count === 'desc' || this.sortingOrder.exclamation_count === undefined
    },
    showWordsToAvoidOrderAsc() {
      return this.sortingOrder.words_to_avoid_count === 'asc' || this.sortingOrder.words_to_avoid_count === undefined
    },
    showWordsToAvoidOrderDesc() {
      return this.sortingOrder.words_to_avoid_count === 'desc' || this.sortingOrder.words_to_avoid_count === undefined
    },
    showSmartWordsOrderAsc() {
      return this.sortingOrder.smart_words_count === 'asc' || this.sortingOrder.smart_words_count === undefined
    },
    showSmartWordsOrderDesc() {
      return this.sortingOrder.smart_words_count === 'desc' || this.sortingOrder.smart_words_count === undefined
    },
    previewWebsiteDataToDisplay() {
      return Object.keys(this.previewWebsiteData).filter(el => !this.hiddenColumns.includes(el))
    }
  },
  methods: {
    openWebsiteDataPreview(website) {
      this.websiteDataPreviewOpened = true;
      this.previewWebsiteData = website;
    },
    closeMessagePreview() {
      this.websiteDataPreviewOpened = false;
    },
    formatUrl(url) {
      if (url.length > 10) {
        return (url.substring(0, 40) + "...");
      } else {
        return url;
      }
    },
    sortAscending(column) {
      let setAll = (obj, val) => Object.keys(obj).forEach(k => obj[k] = val);
      setAll(this.sortingOrder, undefined)
      console.log("Sorting asc", column)
      this.sortingOrder[column] = 'asc';
      this.websitesData.sort((a, b) => {
        if (a[column] > b[column]) {
          return 1;
        }
        if (a[column] < b[column]) {
          return -1;
        }
        return 0;
      });
    },

    sortDescending(column) {
      let setAll = (obj, val) => Object.keys(obj).forEach(k => obj[k] = val);
      setAll(this.sortingOrder, undefined)
      console.log("Sorting desc", column)
      this.sortingOrder[column] = 'desc';
      this.websitesData.sort((a, b) => {
        if (a[column] < b[column]) {
          return 1;
        }
        if (a[column] > b[column]) {
          return -1;
        }
        return 0;
      });
    },
  }
}
</script>