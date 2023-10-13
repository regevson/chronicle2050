<template>

  <div class="search">
    <img src="@/assets/img/logo.png" style="width: 70%; margin-bottom: 50px;"><br>

    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 30px">

    <input type="number" min="1000" placeholder="#articles to download" style="width: 180px; font-weight: 600 !important; text-align: center"/>

    <input type="date" min="1000" placeholder="#articles to download" style="width: 180px; font-weight: 600 !important; text-align: center"/>

    <input @click="enable_updates" type="text" min="1000" value="automatic updates" :style="{width: '180px', fontWeight: '600 !important', textAlign: 'center', cursor: 'pointer', backgroundColor: updates_enabled ? 'red' : 'white', outline: 'none'}" readonly/>

  </div>

    <input type="text" placeholder="explore the future of..." style="margin-bottom: 20px; font-weight: bold !important; text-align: center"/><br>
    <input @click="isCollapsed = false" class="search-button" type="submit" value="Explore">

  </div>

  <div v-if="showTooltip && tooltipData.length > 0" class="custom-tooltip">
    <div v-if="tooltipData[0]" class="pred-date">{{tooltipData[0]}}</div>
    <div class="words"><span>{{tooltipData[1]}}</span></div>

      <div v-if="tooltipData[0]" v-for="item in tooltipData[3]" :key="item" class="sentence-wrapper">
        <div class="pub-date">pub. {{new Date(item.timestamp).toLocaleDateString('en-GB')}}:</div>
        <div class="sentence" style="background: #60a698 !important"><a :href="item.link" target="_blank">{{item.sentence}}</a></div>
      </div>

    <div v-if="tooltipData[5] > 0" style="color: #ffffff82">
      <p style="margin-top: 10px; margin-bottom: 0">{{tooltipData[5]}} more</p>
      <p style="margin-top: 0; font-size: 12px"><i>(removed due to lack of new info)</i></p>
    </div>




    <div v-if="showNonTimex || !tooltipData[0]" style="margin-top: 50px">

      <div class="line-container">
        <hr class="line">
        <span class="text">Sentences WITHOUT Temporal Expressions</span>
        <hr class="line">
      </div>

      <div v-for="item in tooltipData[4]" :key="item" class="sentence-wrapper">
        <div class="pub-date">pub. {{new Date(item.timestamp).toLocaleDateString('en-GB')}}:</div>
        <div class="sentence"><a :href="item.link" target="_blank">{{item.sentence}}</a> <span style="color: #1b2730c7">[{{Math.floor(item.importance)}} mention(s)]</span></div>
      </div>

    </div>

    <div v-if="tooltipData[0]">
      <button v-if="!showNonTimex && tooltipData[4].length > 0" class="show-more-btn" @click="showNonTimex = true">Content Without Date</button>
      <button v-if="showNonTimex" class="show-less-btn" @click="showNonTimex = false">Only Content With Date</button>
    </div>
  </div>


  
  <div style="display: flex; justify-content: center; gap: 80px;">
    <apexchart type="donut" :options="opt" :series="ser" height="200" width="230" />
    <apexchart type="donut" :options="opt2" :series="ser2" height="200" width="230" />
    <apexchart type="donut" :options="opt3" :series="ser3" height="200" width="230" />
  </div>

  <div style="margin-top: 20px">
    <apexchart ref="chart" type="scatter" :options="chartOptions" :series="series" height="700" @mounted="onChartReady"/>
  </div>

  

  <div v-if="cloud" style="margin-top: 50px; display: flex; flex-wrap: wrap">
    <div @click="showNonTempTooltip(group, true)" @mouseover="showNonTempTooltip(group, false)" @mouseleave="hide()" v-for="[topicNum, group] in Object.entries(cloud)" :key="topicNum" class="topic" style="display: flex; padding: 8px">
      <div class="words-no-temp" :style="sizes(group)">{{cut(group.sentences[0].keywords).toUpperCase()}}</div>
    </div>
  </div>



  <div v-if="!isCollapsed" class="log-window">
    <i @click="isCollapsed = true" class="collapse fa-solid fa-caret-down"></i>
    <span style="">#articles left:</span> <b>{{articlesLeft}}</b><br>
    <span>#articles downloaded:</span> <b>{{articlesDownloaded}}</b><br>
    <br>
    <span>#updates left:</span><b> {{updatesLeft}}</b><br>
    <span>#updates done:</span><b> {{updatesDone}}</b><br>
    <br>
    <span style="font-weight: bold; font-size: 18px">LOG:</span><br>
    <textarea style="width:100%; height:220px" readonly>{{log}}</textarea>
    <button v-if="showRefresh" class="refresh-button" @click="refresh()">Refresh</button>
  </div>

  <div v-else class="log-preview">
    <span>LOG</span>
    <i @click="isCollapsed = false" style="margin: 0" class="collapse fa-solid fa-caret-up"></i>
  </div>



</template>

<script>
import VueApexCharts from 'vue3-apexcharts';
import axios from 'axios'


export default {
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      isSelected: false,
      showTooltip: false,
      showNonTimex: false,
      isOverlayVisible: false,
      showRefresh: false,
      isCollapsed: true,

      clickThres: 0,
      tooltipData: [],
      topicKeywords: [],
      timeline: {},
      timelineNo: {},
      cloud: {},

      numClusters: 0,
      numSents: 0,
      avgSentencesPerCluster: 0,
      numTemporal: 0,

      maxSameTimex: 0,
      maxTimexDistance: 0,
      maxMentions: 0,

      articlesLeft: 0,
      articlesDownloaded: 0,
      updatesLeft: 0,
      updatesDone: 0,
      log: "",

      updates_enabled: false,


      ser: [],
      opt: {
        chart: {
          type: 'pie',
          background: '#1b2730',
        },
        legend: {
          show: false
        },
        title: {
          text: "Sentences with/without Timexes"
        },
        theme: {
          mode: "dark",
          palette: 'palette2'
        },
      },

      ser2: [],
      opt2: {
        chart: {
          type: 'pie',
          background: '#1b2730',
        },
        legend: {
          show: false
        },
        title: {
          text: "Number of Clusters"
        },
        theme: {
          mode: "dark",
          palette: 'palette2'
        },
        dataLabels: {
          enabled: false
        },
        plotOptions: {
          pie: {
            donut: {
              labels: {
                show: true,
                name: {
                  show: false
                },
                total: {
                  showAlways: true,
                  show: true
                }
              }
            }
          }
        },
      },

      ser3: [],
      opt3: {
        chart: {
          type: 'pie',
          background: '#1b2730',
        },
        legend: {
          show: false
        },
        title: {
          text: "Avg Sentences Per Cluster"
        },
        theme: {
          mode: "dark",
          palette: 'palette2'
        },
        dataLabels: {
          enabled: false
        },
        plotOptions: {
          pie: {
            donut: {
              labels: {
                show: true,
                name: {
                  show: false
                },
                total: {
                  showAlways: true,
                  show: true
                }
              }
            }
          }
        },
      },




      series: [{
        name: 'Sample Data',
        data: [[]],
      }],
      chartOptions: {
        theme: {
          mode: 'dark',
        },

        legend: {
          show: false
        },


        chart: {
          events: {
          },
          background: '#1b2730',
          zoom: {
            enabled: true
          }
        },
        xaxis: {
          type: 'datetime',
          labels: {
            formatter: function(val) {
              let d = new Date(val);
              d.setHours(0, 0, 0, 0);
              return new Date(d).toLocaleDateString('en-GB');
            }
          }
        },
        yaxis: {
          type: 'numeric',
          labels: {
            maxWidth: 400,
          }
        },
        tooltip: {
        }
      }
    }

  },

  methods: {

    enable_updates() {
      this.updates_enabled = !this.updates_enabled;
    },

    form(v) {
      if(v < 1) v = 0;
      return this.timeline[v][0][0].keywords;
    },

    show() {
      if(this.isSelected) return;
      this.showTooltip = true;
    },

    hide() {
      if(this.isSelected) return;
      this.showTooltip = false;
    },

    select() {
      this.showTooltip = true;
      this.isSelected = true;
      this.clickThres = 2;
    },

    click() {
      this.clickThres -= 1;
      if(this.clickThres <= 0) {
        this.isSelected = false;
        this.hide();
      }
    },

    showNonTempTooltip(data, clicked) {
      console.log(data);
      let arr = [null,
                 data.sentences[0].keywords.toUpperCase(),
                 data.sentences[0].cluster_id,
                 null,
                 data.sentences
                ];
      this.tooltipData = arr;
      if(clicked)
        this.select();
      else
        this.show();
    },

    tooltip({ seriesIndex, dataPointIndex, w }) {
      let data = w.config.series[seriesIndex].data[dataPointIndex];
      let arr = [new Date(data[0]).toLocaleDateString('en-GB'),
                 data[2][0].keywords.toUpperCase(),
                 data[2][0].cluster_id,
                 data[2],
                 this.timelineNo[data[2][0].cluster_id]
                ];
      let diff = data[2][0].numSameTimex-data[2].length;
      arr.push(diff)
      this.tooltipData = arr;
      return "";
    },

    sizes(group) {
      let mentions = group.totalMentions;
      const minMentions = 1;
      const range = this.maxMentions - minMentions;
      const normalizedValue = (mentions - minMentions) / range;
      const lowestPx = 9;
      const pxDiff = 13;
      const output = (normalizedValue * pxDiff) + lowestPx;
      return {'font-size': output + 'px'};
    },

    colors(maxSameTimex) {
      return function({value, seriesIndex, w}) {
        const data = w.config.series[seriesIndex].data;
        if(data[0] === undefined || data[0].length == 0)
          return "";

        /*let diffTime = Math.abs(new Date(data[0][2][0].timestamp) - new Date(data[0][2][0].datetime));*/
        /*let distance = Math.ceil(diffTime / (1000 * 60 * 60 * 24));*/

        let sameTimex = parseFloat(data[0][2][0].numSameTimex);

        /*// TODO: calc average (could be multiple sentences)*/
        /*let mentions = parseFloat(data[0][2][0].importance);*/

        /*let p1 = 1 - distance/maxTimexDistance;*/
        let p2 = sameTimex/maxSameTimex;
        /*let p3 = mentions/maxMentions;*/
        /*value = 0*p1 + 1*p2 + 0*p3;*/
        value = p2;

        const maxValue = 1;
        let green = Math.round(255 * (maxValue - value));
        let blue = Math.round(255 * (maxValue - value));

        // Convert RGB values to hexadecimal format
        let redHex = "FF";
        let greenHex = green.toString(16).padStart(2, "0");
        let blueHex = blue.toString(16).padStart(2, "0");

        return "#" + redHex + greenHex + blueHex;
      }
    },

    cut(w) {
      w = w.split(" "); // split the string into an array of words
      let firstFourWords = w.slice(0, 4); // get the first four elements of the array
      let result = firstFourWords.join(" "); // join the first four elements back into a string
      return result;
    },

    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    },

    async onChartReady() {
      console.log("second");
      this.submitQuery();
      let old_checksum = 0;
      await axios.post('/api/submit/?query=Justin Bieber');
      this.showRefresh = true;
      /*while(true) {*/
        /*try {*/
          /*const response = await axios.get('/api/status/');*/
          /*let new_checksum = response.data[0];*/
          /*this.articlesLeft = response.data[1][0]; */
          /*this.articlesDownloaded = response.data[1][1];*/
          /*this.updatesLeft = response.data[1][2];*/
          /*this.updatesDone = response.data[1][3];*/
          /*this.log = response.data[1][4];*/
          /*if(new_checksum != old_checksum) {*/
            /*old_checksum = new_checksum;*/
            /*this.showRefresh = true;*/
          /*}*/
        /*} */
        /*catch(error) { console.error(error); }*/

        /*let secs = 0;*/
        /*await this.sleep(secs*1000);*/
      /*}*/
    },

    async submitQuery() {
      try {
        await axios.post('/api/submit/?query=Justin Bieber');
      } catch(error) { console.error(error); }
    },

    async refresh() {
      this.$refs.chart.updateSeries([{
                name: 'Series A',
                data: [[]]
            }]);
      /*this.$refs.chart.updateOptions({});*/


      this.showRefresh = false;
      let full = null;
      try {
        const response = await axios.get('/api/all/?query=Justin Bieber');
        full = response.data;
      } catch(error) {
        console.error(error);
      }

      this.numSents = full.length;

      let all = {};
      full.forEach(item => {
        if(!all[item.cluster_id]) {
          all[item.cluster_id] = {"hasTemp": false, "totalMentions": 0, "sentences": []};
          this.numClusters += 1;
        }

        if(item.datetime) {
          all[item.cluster_id].hasTemp = true;
          all[item.cluster_id].totalMentions += parseInt(item.importance) + parseInt(item.numSameTimex) // is floored
        }
        else
          all[item.cluster_id].totalMentions += parseInt(item.importance) // is floored
        all[item.cluster_id].sentences.push(item);
      });


      this.timeline = {};
      this.timelineNo = {};
      this.cloud = {};
      Object.entries(all).forEach(([key, value]) => {
        if(value.hasTemp) {
          let w = [];
          let wo = [];
          for(let i = 0; i < value.sentences.length; i++) {
            let sent = value.sentences[i];
            if(sent.datetime)
              w.push(sent);
            else
              wo.push(sent);
          }
          this.timeline[key] = w;
          this.timelineNo[key] = wo;
        }
        else {
          this.cloud[key] = {"sentences": value.sentences, "totalMentions": value.totalMentions};
          if(value.totalMentions > this.maxMentions) this.maxMentions = value.totalMentions;
        }

      });

      this.timeline = Object.values(this.timeline);
      this.timeline.sort((a, b) => a.totalMentions - b.totalMentions);

      for(let t = 0; t < this.timeline.length; t++) {
        let sents = this.timeline[t];
        let arr = [];
        let dates = [];
        for(let i = 0; i < sents.length; i++) {
          let sent = sents[i];
          if(sent.numSameTimex > this.maxSameTimex) this.maxSameTimex = sent.numSameTimex;
          let idx = dates.indexOf(sent.datetime);
          if(idx == -1) {
            arr.push([sent]);
            dates.push(sent.datetime);
          }
          else {
            arr[idx].push(sent);
          }
        }
        this.timeline[t] = arr;
      }

      this.series = [];
      for(let t = 0; t < this.timeline.length; t++) {
        let sents = this.timeline[t];
        for(let i = 0; i<sents.length; i++) {
          let sent = sents[i];
          let series = [[new Date(sent[0].datetime), t, sent]];
          series = {data: series};
          this.series.push(series);
          this.numTemporal += 1;
        }
      }

      let chartOptions = {
        theme: {
          mode: 'dark',
        },

        legend: {
          show: false
        },


        chart: {
          events: {
          },
          background: '#1b2730',
          zoom: {
            enabled: true
          }
        },
        xaxis: {
          type: 'datetime',
          labels: {
            formatter: function(val) {
              let d = new Date(val);
              d.setHours(0, 0, 0, 0);
              return new Date(d).toLocaleDateString('en-GB');
            }
          }
        },
        yaxis: {
          type: 'numeric',
          labels: {
            maxWidth: 400,
          }
        },
        tooltip: {
        }
      };

      chartOptions.tooltip.custom = this.tooltip;
      chartOptions.chart.events.dataPointMouseEnter = this.show;
      chartOptions.chart.events.dataPointMouseLeave = this.hide;
      chartOptions.chart.events.dataPointSelection = this.select;
      chartOptions.chart.events.click = this.click;
      chartOptions.yaxis.tickAmount = Object.keys(this.timeline).length-1;
      chartOptions.yaxis.max = Object.keys(this.timeline).length-1;
      chartOptions.yaxis.labels.formatter = this.form;
      chartOptions.colors = [this.colors(this.maxSameTimex)];
      this.$refs.chart.updateOptions(chartOptions);

      let nonTemp = this.numSents - this.numTemporal;
      this.ser = [Math.round(100/this.numSents*nonTemp), Math.round(100/this.numSents*this.numTemporal)];
      this.ser2[0] = this.numClusters;
      this.ser3[0] = Math.round(this.numSents / this.numClusters);
    },

  }

}
</script>

<style>

body {
  background: #1b2730;
  padding: 10px;
  font-family: 'Roboto', sans-serif;
}

.custom-tooltip {
  backdrop-filter: blur(10px) !important;
  box-shadow: 0px 69px 89px 119px #000000b5 !important;
  position: fixed;
  z-index: 9999;
  top: 10px;
  max-width: 1000px;
  border: 2px solid white;
  padding: 8px;
  font-size: 14px;
  font-family: Arial, sans-serif;
  white-space: normal !important;
  left: 50%;
  transform: translate(-50%, 0%);
  color: white;
  font-weight: bold;
  background: #499082c4;
  width: fit-content;
  margin: 0 auto;
  border-radius: 10px;
  margin-bottom: 10px;
  max-height: 620px;
  overflow: scroll;
}

.topic {
  color: white;
  background: #499082;
  padding: 10px;
  text-align: left;
  border-radius: 10px;
  max-width: 960px;
  margin: 0 auto;
  margin-bottom: 50px;
}

.sentence {
  font-size: 15px;
  background: #225349 !important;
  font-weight: bold;
  padding: 7px;
  border-radius: 5px;
  color: white;
  text-align: left;
}

.words {
  text-align: center;
  min-width: 70%;
  font-weight: bold;
  font-size: 15px;
  background: #2e4353;
  padding: 8px;
  border-radius: 10px;
  width: fit-content;
  margin: 0 auto;
  margin-bottom: 30px;
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

a {
  color: white;
  text-decoration: none;
}

.pred-date {
  background: #2e4353;
  padding: 8px;
  border-radius: 10px;
  border: 2px solid #499082;
  color: white; 
  display: inline-block; 
  float: left; 
  margin-top: -1px;
}

.show-more-btn {
  background: transparent;
  border: 2px solid #1b2730;
  font-weight: bold;
  padding: 6px;
  border-radius: 8px;
  color: #1b2730;
  cursor: pointer;
}

.show-less-btn {
  background: transparent;
  border: 2px solid #510101;
  font-weight: bold;
  padding: 6px;
  border-radius: 8px;
  color: #510101;
  cursor: pointer;
}

.show-more-btn:hover {
  background: #1b2730;
  color: white;
  transition: 0.4s all ease-in-out;
}

.show-less-btn:hover {
  background: #510101;
  color: white;
  transition: 0.4s all ease-in-out;
}


.sentence-wrapper {
  display: flex; 
  align-items: center; 
  gap: 5px; 
  width: 100%; 
  margin-bottom: 8px;
}

.pub-date {
  font-weight: normal; 
  white-space: nowrap;
  background: #60a698;
  padding: 3px;
  border-radius: 5px;
}


.line-container {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.line {
  flex-grow: 1;
  height: 3px;
  border: none;
  background-color: #2e4353;
}

.text {
  margin: 0 10px;
  font-size: 15px;
  color: #2e4353;
}

.refresh-button {
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

.search {
  background: #2a3e4d;
  border-radius: 8px;
  width: fit-content;
  min-width: 700px;
  margin: 0 auto;
  margin-bottom: 70px;
  padding: 30px 50px 30px 50px;
}

h1 {
  color: white; 
  margin: 0;
  margin-bottom: 30px;
}

.search input {
  height: 25px;
  border-radius: 5px;
  border: none;
  padding: 5px;
  margin-right: 10px;
}

.search-button {
  background-color: #499082;
  color: white;
  padding: 10px;
  height: 35px !important;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  font-size: 18px;
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

</style>
