<template>
  <Tooltip ref="tooltip" :tooltip-data="tooltipData" />

  <div id="target-div" style="margin-top: 20px">
    <apexchart ref="chart" type="scatter" :options="chartOptions" :series="series" @touchend="clickHandler" @mousedown="clickHandler" @touchmove="hasMoved=true" @updated="updateTimelineHeight" />
    <!--
    <apexchart ref="chart" type="scatter" :options="chartOptions" :series="series" height="700" @touchend="clickHandler" @mousedown="clickHandler" @touchmove="hasMoved=true" @mousemove="hasMoved=true"/>
    -->
  </div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts';
import Tooltip from '../components/Tooltip.vue';

export default {
  components: {
    apexchart: VueApexCharts, Tooltip
  },

  props: {
    topicsWithDatetime: {
      type: [Object, null],
      default: null
    },
  },

  data() {
    return {
      maxSumOfMentions: 0,
      tooltipData: null,

      maxDate: '',
      minDate: '',
      hasMoved: false,

      series: [{name: '', data: [[]]}],
      chartOptions: {
        theme: {mode: 'dark'},
        legend: {show: false},
        chart: {height: 'auto', events: {}, background: '#1b2730', zoom: {enabled: true}, offsetX: 0, offsetY: 20},
        grid: {borderColor: '#499082'},
        markers: {size: 9, strokeWidth: 0},
        xaxis: {
          position: 'top',
          axisBorder: {color: '#499082', height: 0.1},
          type: 'datetime',
          labels: {
            style: {fontWeight: '600'},
            formatter: function(val) {
              let d = new Date(val);
              d.setHours(0, 0, 0, 0);
              return new Date(d).toLocaleDateString('en-GB');
            }
          }
        },
        yaxis: {type: 'numeric', 
                labels: {maxWidth: 400, style: {fontWeight: 'bold', colors: '#499082'}}},
        tooltip: {}
      },

    }
  },

  watch: {
    topicsWithDatetime(newVal) {
      this.prepareTimelineData(newVal);
    },
  },

  methods: {
    clickHandler(event) {
      if(this.hasMoved) {
        this.hasMoved = false;
        return;
      }
      let x, y;

      if(event.touches) {
        if(event.touches.length < 1) return;
        let touch = event.touches[0];
        x = touch.clientX;
        y = touch.clientY;
      }
      else {
        x = event.clientX;
        y = event.clientY;
      }

      const markers = document.querySelectorAll('.apexcharts-series-markers');

      let minDist = 9999;
      let selectedIdx;
      for(let i = 0; i < markers.length; i++) {
        const rect = markers[i].getBoundingClientRect();
        let dist = Math.abs(rect.left-x) + Math.abs(rect.top-y);
        if(dist < minDist) {
          minDist = dist;
          selectedIdx = i;
        }
      }

      this.$refs.tooltip.clickTooltip();
      this.$refs.tooltip.showTooltip();
      this.tooltipData = this.series[selectedIdx].data[0][2];
    },

    calcDataPointColor(maxSumOfMentions) {
      return function({value, seriesIndex, w}) {
        const data = w.config.series[seriesIndex].data;
        if(data[0].length < 1) return "";

        let dataPoint = data[0][2];

        let sumOfMentions = parseFloat(dataPoint.contentWithDate.sumOfMentions);
        let frac = sumOfMentions/maxSumOfMentions;

        const maxValue = 1;
        let green = Math.round(255 * (maxValue - frac));
        let blue = Math.round(255 * (maxValue - frac));

        // Convert RGB values to hexadecimal format
        let redHex = "FF";
        let greenHex = green.toString(16).padStart(2, "0");
        let blueHex = blue.toString(16).padStart(2, "0");
        return "#" + redHex + greenHex + blueHex;
      }
    },

    formatYLabels(labelNum) {
      if(labelNum < 1) labelNum = 0;
      if(this.topicsWithDatetime[labelNum]) {
        let label = this.topicsWithDatetime[labelNum].keywords;
        return label.toString().split("-");
      }
    },

    initTooltip({ seriesIndex, dataPointIndex, w }) {
      /*if(this.hasMoved)*/
        /*this.hasMoved = false;*/
      /*else {*/
        let data = w.config.series[seriesIndex].data[dataPointIndex];
        this.tooltipData = data[2];
      /*}*/
      return "";
    },

    prepareTimelineData(topicsWithDatetime) {
      this.series = [];
      for(let i=0; i<topicsWithDatetime.length; i++) {
        let cwd = topicsWithDatetime[i].contentWithDate;
        let cwod = topicsWithDatetime[i].contentWithoutDate[0];
        let keywords = topicsWithDatetime[i].keywords;
        topicsWithDatetime[i].keywords = keywords.split('-').slice(0, 4).join('-');
        keywords = topicsWithDatetime[i].keywords;
        let clusterId = topicsWithDatetime[i].clusterID;
        for(let j=0; j<cwd.length; j++) {
          if(cwd[j].sumOfMentions > this.maxSumOfMentions) 
            this.maxSumOfMentions = cwd[j].sumOfMentions;
          if(new Date(cwd[j].datetime) > new Date(this.maxDate) || this.maxDate === '') 
            this.maxDate = cwd[j].datetime;
          if(new Date(cwd[j].datetime) < new Date(this.minDate) || this.minDate === '') 
            this.minDate = cwd[j].datetime;

          let payload = {'keywords': keywords, 
                         'contentWithDate': cwd[j], 
                         'contentWithoutDate': cwod
                        };
          let series = [[cwd[j].datetime, i, payload]];
          series = {data: series};
          this.series.push(series);
        }
      }

      this.setChartOptions();
    },

    setChartOptions() {
      this.chartOptions.tooltip.custom = this.initTooltip;
      this.chartOptions.chart.events.dataPointMouseEnter = this.$refs.tooltip.showTooltip;
      this.chartOptions.chart.events.dataPointMouseLeave = this.$refs.tooltip.hideTooltip;
      /*this.chartOptions.chart.events.dataPointSelection = this.$refs.tooltip.selectTooltip;*/
      /*this.chartOptions.chart.events.click = this.$refs.tooltip.clickTooltip;*/
      this.chartOptions.yaxis.tickAmount = this.topicsWithDatetime.length-1;
      this.chartOptions.yaxis.tickAmount = this.topicsWithDatetime.length-1;
      this.chartOptions.yaxis.max = this.topicsWithDatetime.length-1;
      this.chartOptions.yaxis.labels.formatter = this.formatYLabels;
      this.chartOptions.yaxis.labels.rotate = 0;
      this.chartOptions.colors = [this.calcDataPointColor(this.maxSumOfMentions)];
      this.chartOptions.chart.height = 70 * this.topicsWithDatetime.length;
      this.$refs.chart.updateOptions(this.chartOptions);
    },

    updateTimelineHeight() {
      const timelineHeight = document.getElementsByClassName('vue-apexcharts')[3].clientHeight;
      console.log(timelineHeight);
      document.getElementsByClassName('apexcharts-zoomable')[0].style.height = (timelineHeight + 30) + "px";
    }
  }, // methods
};
</script>

<style>
@media (max-width: 658px) {
  .apexcharts-text tspan {
    font-size: 9px;
  }
}
</style>
