<template>
  <div class="flex mx-0" v-if="statistics">
    <div class="w-1/3">
      <div class="text-xl text-gray-800 font-bold my-4 text-center">
        Statystyki dla poszczególnych cech
      </div>
      <div style="max-height: 82vh" class="overflow-y-scroll">
        <div v-for="column_name in columnNamesToChoose"
             :key="column_name"
             class="py-4 border-gray-400 cursor-pointer"
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
    </div>
    <div class="w-3/4 pt-8 overflow-y-scroll" style="max-height: 90vh" ref="data_section">
      <div class="grid grid-cols-2 py-4">
        <div v-for="(value, stat_name) in filteredWebsiteData"
             class="my-4 flex items-center justify-center text-lg"
             :key="stat_name">
          <div>
            <span class="font-semibold">{{ stat_name }}:</span> {{ statistics[chosenColumn][stat_name] }}
          </div>
        </div>
      </div>
      <div class="flex w-full items-center justify-center">
        <div class="w-1/2 flex flex-col mx-16">
          <div class="font-semibold text-lg my-2 text-center">
            Wykres skrzypcowy<br>(wartości rzeczywiste)
          </div>
          <img :src="require('@/assets/resources/violinplots/dist_violinplot_' + chosenColumn + '.png')"
               class="mb-4">
        </div>
        <div class="w-1/2 flex flex-col mx-16 text-center">
          <div class="font-semibold text-lg my-2">
            Wykres skrzypcowy przy kategoryzacji binarnej<br>(wartości normalizowane)
          </div>
          <img :src="require('@/assets/resources/violins_split/dist_violinplot_split_' + chosenColumn + '.png')"
               class="mb-4">
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
  },
  computed: {
    filteredWebsiteData() {
      const notAllowed = ['0%', '8.3%', '16.7%', '33.3%', '41.7%', '58.3%', '66.7%', '83.3%', '91.7%', '100%', 'count'];
      return Object.keys(this.statistics[this.chosenColumn])
          .filter(key => !notAllowed.includes(key))
          .reduce((obj, key) => {
            obj[key] = this.statistics[key];
            return obj;
          }, {});
    },
    columnNamesToChoose() {
      const notAllowed = ['categorical_rating', 'binary_rating']
      return Object.keys(this.statistics).filter(k => !notAllowed.includes(k))
    }
  },
  watch: {
    chosenColumn() {
      this.$refs.data_section.scrollTo({top: 0, behavior: 'smooth'})
    }
  }
}
</script>

<style scoped>

</style>