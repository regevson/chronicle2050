<template>
  <Tooltip ref="tooltip" :tooltip-data="tooltipData" />

  <div class="word-cloud-wrapper" v-if="topicsWithoutDatetime" @mouseover="$refs.tooltip.hideTooltip()">
    <div class="topic" @click="initTooltip(topic, true)" 
      @mouseover="initTooltip(topic, false)" v-for="topic in topicsWithoutDatetime" 
      @mousemove="initTooltip(topic, false)" :key="topic.clusterID"
    >
      <div class="words-no-temp" :style="sizes(topic)">{{cut(topic.keywords).toUpperCase()}}</div>
    </div>
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
    topicsWithoutDatetime: {
      type: [Object, null],
      default: null
    },
  },

  data() {
    return {
      cnt: 0,
      maxMentions: 0,
      tooltipData: null,
    } // return
  }, // data

  watch: {
    topicsWithoutDatetime(newVal) {
      this.prepareWordCloudData(newVal);
    },
  },

  methods: {
    cut(w) {
      w = w.split(" "); // split the string into an array of words
      let firstFourWords = w.slice(0, 4); // get the first four elements of the array
      let result = firstFourWords.join(" "); // join the first four elements back into a string
      return result;
    },

    initTooltip(topic, isTooltipClicked) {
      topic.isTooltipClicked = isTooltipClicked;
      topic.cnt = this.cnt;
      this.cnt += 1;
      this.tooltipData = topic;
    },

    sizes(topic) {
      let mentions = topic.avgTotalMentions;
      const minMentions = 1;
      const range = this.maxMentions - minMentions;
      const normalizedValue = (mentions - minMentions) / range;
      const lowestPx = 9;
      const pxDiff = 13;
      const output = (normalizedValue * pxDiff) + lowestPx;
      return {'font-size': output + 'px'};
    },

    prepareWordCloudData(topicsWithoutDatetime) {
      topicsWithoutDatetime.sort((a, b) => b.avgTotalMentions - a.avgTotalMentions);
      this.maxMentions = topicsWithoutDatetime[0].avgTotalMentions;
    },
  }, // methods
};
</script>

<style>
.word-cloud-wrapper {
  padding-top: 70px; 
  display: flex; 
  flex-wrap: wrap;
  /*background: red;*/
}

.topic {
  color: white;
  background: #499082;
  text-align: left;
  display: flex;
  border-radius: 7px;
  max-width: 960px;
  margin: 0 auto;
  margin-bottom: 50px;
  padding: 8px;
}

.words-no-temp {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-weight: bold;
  font-size: 15px;
  border-radius: 10px;
  cursor: pointer;
}
</style>
