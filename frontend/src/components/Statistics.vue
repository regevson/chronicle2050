<template>
  <div class="stats-wrapper">
    <apexchart class="stats-chart" type="donut" :options="dateSentsOptions" :series="dateSentsSeries" />
    <apexchart class="stats-chart" type="donut" :options="numClustersOptions"
      :series="numClustersSeries" 
    />
    <apexchart class="stats-chart" type="donut" :options="avgClusterSentsOptions" 
      :series="avgClusterSentsSeries"
    />
  </div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts';

export default {
  components: {
    apexchart: VueApexCharts
  },

  props: {
    stats: {
      type: [Object, null],
      default: null,
    },
  },

  data() {
    return {
      dateSentsSeries: [],
      dateSentsOptions: {
        chart: {type: 'pie', background: '#1b2730'},
        colors: ['#499082', '#8c8c8c'],
        legend: {show: false},
        title: {text: "% Sentences with Dates", align: "center"},
        theme: {mode: "dark", palette: 'palette2'},
      },

      numClustersSeries: [],
      numClustersOptions: {
        chart: {type: 'pie', background: '#1b2730'},
        colors: ['#499082'],
        legend: {show: false},
        title: {text: "#Clusters", align: "center"},
        theme: {mode: "dark", palette: 'palette2'},
        dataLabels: {enabled: false},
        plotOptions: {
          pie: {
            donut: {
              labels: {
                show: true,
                name: {show: false},
                total: {showAlways: true, show: true}
              }
            }
          }
        },
      },

      avgClusterSentsSeries: [],
      avgClusterSentsOptions: {
        chart: {type: 'pie', background: '#1b2730'},
        colors: ['#499082'],
        legend: {show: false},
        title: {text: "Ø Sentences Per Cluster", align: "center"},
        theme: {mode: "dark", palette: 'palette2'},
        dataLabels: {enabled: false},
        plotOptions: {
          pie: {
            donut: {
              labels: {
                show: true,
                name: {show: false},
                total: {showAlways: true, show: true}
              }
            }
          }
        },
      },

    } // return
  }, // data

  watch: {
    stats(stats) {
      this.calcChartData();
    }
  },

  methods: {
    calcChartData() {
      let numSents = this.stats.numSentsWithDate + this.stats.numSentsWithoutDate;
      this.dateSentsSeries = [Math.round(100/numSents*this.stats.numSentsWithoutDate), 
                              Math.round(100/numSents*this.stats.numSentsWithDate)];
      this.numClustersSeries[0] = this.stats.numClusters;
      this.avgClusterSentsSeries[0] = Math.round(numSents / this.stats.numClusters);
    }
  },
};
</script>

<style>
.stats-wrapper {
  display: flex; 
  justify-content: center; 
  gap: 10px; 
  box-sizing: border-box; 
  width: 95%; 
  margin: 0 auto;
}

.stats-chart {
  min-width: 100px;
}

@media (max-width: 658px) {
  .apexcharts-title-text {
    font-size: 10px;
  }
}
</style>

