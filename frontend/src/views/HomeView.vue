<template>
  <img class="logo" src="@/assets/img/logo.svg">
  <Settings @startEvent="startProcess" />

  <Statistics id="target-div" :stats="stats" />

  <Timeline :topics-with-datetime="topicsWithDatetime" :key="userProvidedEntity"/>

  <WordCloud :topics-without-datetime="topicsWithoutDatetime" />
</template>

<script>
import VueApexCharts from 'vue3-apexcharts';
import axios from 'axios'
import Settings from '../components/Settings.vue';
import Statistics from '../components/Statistics.vue';
import Tooltip from '../components/Tooltip.vue';
import Timeline from '../components/Timeline.vue';
import WordCloud from '../components/WordCloud.vue';

export default {
  components: {
    apexchart: VueApexCharts, Settings, Statistics, Tooltip, Timeline, WordCloud,
  },

  data() {
    return {
      userProvidedEntity: '',
      topicsWithDatetime: [],
      topicsWithoutDatetime: [],
      stats: null,
    } // return
  }, // data

  methods: {
    startProcess(configData) {
      if(this.userProvidedEntity === configData.entity) return; // same entity was inserted/clicked
      this.userProvidedEntity = configData.entity;
      this.scrollToStats();
      this.downloadData(configData);
    },

    scrollToStats() {
      const element = document.getElementById('target-div');
      if(element) element.scrollIntoView({ behavior: 'smooth' });
    },

    async downloadData(configData) {
      let allData = {};
      try {
        const params = {
          'entity': configData.entity,
          'from_date': configData.fromDate,
          'to_date': configData.toDate,
          'num_articles': configData.numArticles
        };

        const response = await axios.get('/api/all/', { params });
        allData = response.data;
      } catch(error) {
        console.error(error);
      }

      let topicsWithDatetime = [];
      let topicsWithoutDatetime = [];
      this.stats = allData.stats;

      allData.data.forEach(topic => {
        if(topic.contentWithDate.length > 0)
          topicsWithDatetime.push(topic);
        else {
          topic.contentWithDate = null;
          topicsWithoutDatetime.push(topic);
        }
      });

      topicsWithDatetime.sort((a, b) => a.avgTotalMentions - b.avgTotalMentions);

      this.topicsWithDatetime = topicsWithDatetime;
      this.topicsWithoutDatetime = topicsWithoutDatetime;
    },
  }, // methods
}
</script>

<style>
body {
  background: #1b2730;
  padding: 10px;
  font-family: 'Roboto', sans-serif;
  height: fit-content;
  padding-bottom: 400px;
}

div {
  color: white;
}

a {
  color: #640000;
  text-decoration: none;
}

.logo {
  width: 100%; 
  max-width: 800px;
  margin-bottom: 15px;
}

.downloadData-button {
  position: fixed;
  bottom: 30px;
  right: 50px;
  background-color: red;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  font-size: 18px;
  animation: wiggle 1s ease-in-out infinite;
}

@keyframes wiggle {
  0% { transform: rotate(0); }
  20% { transform: rotate(-2deg); }
  40% { transform: rotate(2deg); }
  60% { transform: rotate(-2deg); }
  80% { transform: rotate(2deg); }
  100% { transform: rotate(0); }
}

h1 {
  color: white;
  margin: 0;
  margin-bottom: 30px;
}

.log-window {
  position: fixed;
  bottom: 10px;
  right: 20px;
  background: #383b3d;
  width: 300px;
  height: 400px;
  border-radius: 10px;
  color: white;
  text-align: left;
  padding: 15px 10px 15px 10px;
  font-size: 17px;
  z-index: 9999999;
}

.log-preview {
  position: fixed;
  bottom: 10px;
  right: 20px;
  background: #383b3d;
  width: 70px;
  height: 30px;
  font-weight: bold;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 10px;
  color: white;
  text-align: left;
  padding: 10px 10px 10px 10px;
  font-size: 17px;
}

.log-window textarea {
  background: black;
  border: none;
  border-radius: 4px;
  resize: none;
  color: white;
}

.collapse {
  float: right;
  font-size: 30px;
  margin-top: -14px;
  cursor: pointer;
}

@media (max-width: 658px) {
  .custom-tooltip {
    min-width: 95%;
  }

  .words {
    font-size: 12px;
    min-width: 220px;
    width: 220px;
    padding: 5px 5px 5px 5px;
  }
  .text, .pred-date, .pub-date, .sentence {
    font-size: 12px;
  }
  .mention a {
    font-size: 13px;
  }

}
</style>

