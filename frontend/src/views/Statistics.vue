<template>
  <div class="flex mx-0" v-if="statistics">
    <div class="w-1/3">
      <div class="text-xl text-gray-800 font-bold my-4 text-center">
        Statistics for columns
      </div>
      <div v-for="(value, column_name) in statistics"
           :key="column_name"
           class="py-4 border-gray-400 rounded-r-lg cursor-pointer"
           :class="{ 'bg-gray-300': chosenColumn !== column_name,
            'font-semibold': chosenColumn === column_name}"
           :style="[chosenColumn === column_name ? {'text-shadow': '0px 0px 3px #07653e'} : {}]"
           @click="chooseColumn(column_name)">
        <div
            class="flex items-center justify-center text-semibold text-xl text-center">
          {{ column_name }}
        </div>
      </div>
    </div>
    <div class="w-3/4 p-4">
      <div class="grid grid-cols-2 my-4">
        <div v-for="(value, stat_name) in statistics[chosenColumn]"
             class="my-4 flex items-center justify-center text-lg"
             :key="stat_name">
          <div>
            <span class="font-semibold">{{ stat_name }}:</span> {{ value }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Statistics",
  mounted() {
    this.getStatistics();
  },
  data() {
    return {
      statistics: null,
      loading: false,
      chosenColumn: 'words_to_avoid_count'
    }
  },
  methods: {
    getStatistics() {
      this.loading = true
      axios.get('statistics').then(
          response => {
            this.statistics = JSON.parse(response.data)
          },
          error => {
            this.error = error;
          }
      ).finally(
          () => this.loading = false
      )
    },
    chooseColumn(columnName) {
      this.chosenColumn = columnName
    }
  }
}
</script>

<style scoped>

</style>