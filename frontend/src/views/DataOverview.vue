<template>
  <div class="ml-4">
    <div class="mx-4">
      <div class="text-xl text-gray-800 font-bold my-4">
        Websites data overview
      </div>
      <div class="flex justify-center" v-if="websitesData">
        <div class="w-full border-2 rounded-md border-gray-400 text-center text-gray-700">
          <div class="bg-gray-200 rounded-t-md font-semibold text-gray-900 py-1 border-b-2 border-gray-400">
            <span>
              Choose columns to display (max 4)
            </span>
            <span>
              <i class="fas fa-filter"></i>
            </span>
          </div>
          <div class="flex items-center my-2">
            <div class="mx-2 font-semibold">Chosen columns:</div>
            <div v-for="(column, index) in chosenColumns" :key="index" class="font-semibold">
              <div class="text-sm mx-2 rounded-xl p-1 px-2 border-gray-800 border-2 shadow bg-gray-200">
                {{ column }}
              </div>
            </div>
          </div>
          <div class="grid grid-cols-3 p-2">
            <div v-for="column in columnNames" :key="column" class="text-left">
              <label class="cursor-pointer" :class="{'cursor-not-allowed': checkIfMaxChosen(column)}">
                 <input :value="column"
                     type="checkbox"
                     v-model="chosenColumns"
                     :disabled="checkIfMaxChosen(column)"
                     class="cursor-pointer"
                     :class="{'cursor-not-allowed': checkIfMaxChosen(column)}">
                 <span class="ml-2 text-sm">{{ column }}</span>
              </label>
            </div>
          </div>
        </div>
      </div>
      <template v-if="websitesData">
        <div class="w-full">
          <table class="table">
            <thead>
            <tr>
              <th>
                No.
              </th>
              <th>
                <i class="fas fa-link mr-2"></i>Website url
              </th>
              <th v-for="(column, index) in chosenColumns" :key="index">
                <div class="flex justify-center">
                  <span>{{ column }}</span>
                  <div class="ml-2 text-xl cursor-pointer flex flex-col">
                    <i :class="checkAscVisibility(column)"
                       @click="sortDescending(column)"
                       class="-mb-3 fas fa-sort-up"></i>
                    <i :class="checkDescVisibility(column)"
                       @click="sortAscending(column)"
                       class="-mt-1 fas fa-sort-down"></i>
                  </div>
                </div>
              </th>
              <th>
                <i class="fas fa-info-circle mr-2"></i>View details
              </th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(website, index) in websitesData" :key="index">
              <td>{{ index + 1 }}.</td>
              <td class="text-left">
                <a :href="website.url" target="_blank" class="hover:text-blue-700">
                  {{ formatUrl(website.url, 30) }}
                </a>
              </td>
              <td v-for="column in chosenColumns" :key="column">
                {{ website[column] }}
              </td>
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
      <div class="rounded-lg overflow-hidden w-3/4 bg-gray-300">
        <div class="p-4 font-semibold text-center text-lg flex justify-center">
          Detailed data scrapped from
          <div class="hover:text-blue-700 italic ml-4 cursor-pointer">
            <i class="fas fa-link mr-1"></i>
            <a :href="previewWebsiteData.url" target="_blank">
              {{ formatUrl(previewWebsiteData.url, 50) }}
            </a>
          </div>
        </div>
        <div class="mt-2 flex items-center mb-4 ml-4">
          <div class="font-semibold mr-4">
            Legend:
          </div>
          <div class="flex font-semibold items-center ml-2">
            <div class="mx-4 flex">
              <i class="fas fa-long-arrow-alt-up" style="color: #3690c0"></i>
              <i class="fas fa-long-arrow-alt-down" style="color:#045a8d"></i>
            </div>
            <div class="mr-1 text-xs">
              Near median
            </div>
            <img src="@/assets/resources/colorscale.png" class="h-6">
            <div class="ml-1 text-xs">
              Far from median
            </div>
          </div>
        </div>
        <div class="bg-white p-4">
          <div class="grid grid-cols-3">
            <div v-for="(column, index) in previewWebsiteDataToDisplay" :key="index" class="text-sm my-1">
              <span class="font-semibold">{{ column }}: </span>
              <span class="font-medium">{{ previewWebsiteData[column] }}</span>
              <i class="fas fa-long-arrow-alt-up ml-2"
                 v-if="getArrowDirection(column) === 'up'"
                 :style="{ color: calculateArrowColor(column) }"></i>
              <i class="fas fa-long-arrow-alt-down ml-2"
                 v-if="getArrowDirection(column) === 'down'"
                 :style="{ color: calculateArrowColor(column) }"></i>
              <i class="fas fa-equals ml-2"
                 v-if="getArrowDirection(column) === 'even'"></i>
              <span class="ml-4">(Median: {{statistics[column]['50%']}})</span>
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
      sortingOrder: {},
      hiddenColumns: ['url', 'id','binary_rating'],
      chosenColumns: ['exclamation_count', 'words_to_avoid_count', 'smart_words_count'],
      columnNames: [],
      statistics: null
    }
  },
  mounted() {
    this.loading = true
    axios.get('data').then(
        response => {
          this.websitesData = response.data['db_data'];
          this.statistics = JSON.parse(response.data['statistics'])
          const columnNames = Object.keys(this.websitesData[0]).filter(el => !this.hiddenColumns.includes(el));
          columnNames.forEach((col) => {
            this.sortingOrder[col] = undefined;
          });
          this.columnNames = columnNames;
        },
        error => {
          this.error = error;
        }
    ).finally(
        () => this.loading = false
    )
  },
  computed: {
    previewWebsiteDataToDisplay() {
      return Object.keys(this.previewWebsiteData).filter(el => !this.hiddenColumns.includes(el))
    }
  },
  methods: {
    checkAscVisibility(column) {
      return this.sortingOrder[column] === 'asc' || this.sortingOrder[column] === undefined ? '' : 'invisible';
    },
    checkDescVisibility(column) {
      return this.sortingOrder[column] === 'desc' || this.sortingOrder[column] === undefined ? '' : 'invisible';
    },
    checkIfMaxChosen(value) {
      return this.chosenColumns.length === 4 && !(this.chosenColumns.includes(value));
    },
    openWebsiteDataPreview(website) {
      this.websiteDataPreviewOpened = true;
      this.previewWebsiteData = website;
    },
    closeMessagePreview() {
      this.websiteDataPreviewOpened = false;
    },
    formatUrl(url, length) {
      if (url.length > length) {
        return (url.substring(0, length) + "...");
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
    calculateArrowColor(column) {
      return this.calculateArrowColorUtil(column, this.previewWebsiteData, this.statistics)
    },
    getArrowDirection(column) {
      return this.getArrowDirectionUtil(column, this.previewWebsiteData, this.statistics)
    }
  }
}
</script>