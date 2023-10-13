<template>
  <div class="custom-tooltip" v-if="isVisibleTooltip && localTooltipData !== null" 
    :class="isTooltipExtended ? 'custom-tooltip-extended' : 'custom-tooltip'" 
    @mouseover="isVisibleTooltip = true"
  >

    <div class="icon-wrapper">
      <i class="fa-solid fa-expand" v-if="!isTooltipExtended" @click="isTooltipExtended=true" 
        title="maximize">
      </i>
      <i class="fa-solid fa-compress" v-if="isTooltipExtended" @click="isTooltipExtended=false" 
        title="minimize">
      </i>
      <i class="fa-solid fa-circle-xmark" title="close"
        @click="isTooltipClicked=false; isVisibleTooltip=false; isTooltipExtended=false">
      </i>
    </div>

    <div class="pred-date" v-if="localTooltipData.datetime">{{localTooltipData.datetime}}</div>
    <div class="words"><span>{{localTooltipData.keywords}}</span></div>

    <div class="sentence-wrapper" v-if="localTooltipData.contentWithDate" 
      v-for="item in localTooltipData.contentWithDate.sentences" :key="item" 
    >
      <TooltipSentence :item="item"/>
    </div>

    <div class="sent-without-date-wrapper" 
      v-if="localTooltipData.contentWithoutDate && 
            (!localTooltipData.contentWithDate || showSentsWithoutDate)"
    >
      <div class="line-container">
        <hr class="line">
        <span class="text">Sentences WITHOUT Temporal Expressions</span>
        <hr class="line">
      </div>

      <div class="sentence-wrapper" v-for="item in localTooltipData.contentWithoutDate.sentences" :key="item">
        <TooltipSentence :item="item"/>
      </div>

    </div>

    <div v-if="localTooltipData !== null 
               && localTooltipData.contentWithoutDate 
               && localTooltipData.contentWithDate">
      <button class="show-more-btn"  v-if="!showSentsWithoutDate" @click="showSentsWithoutDate=true">
        Content Without Date
      </button>
      <button class="show-less-btn" v-else @click="showSentsWithoutDate=false">
        Only Content With Date
      </button>
    </div>
  </div>
</template>

<script>
import TooltipSentence from './TooltipSentence.vue';

export default {
  components: {
    TooltipSentence
  },

  props: {
    tooltipData: {
      type: [Object, null],
      default: null,
      deep: true
    },
  },

  data() {
    return {
      isVisibleTooltip: false,
      isTooltipClicked: false,
      showSentsWithoutDate: false,
      isTooltipExtended: false,
      localTooltipData: null,
    } // return
  }, // data

  methods: {
    showTooltip() {
      if(this.isSelected) return;
      this.isVisibleTooltip = true;
    },

    hideTooltip() {
      if(!this.isTooltipClicked) this.isVisibleTooltip = false;
    },

    selectTooltip() {
      this.isVisibleTooltip = true;
    },

    clickTooltip() {
      this.isTooltipClicked = true;
    },

    sentsWithDateTooltip(data) {
      console.log(data);
      this.localTooltipData = {
             'datetime': new Date(data.contentWithDate.datetime).toLocaleDateString('en-GB'),
             'keywords': data.keywords.toUpperCase(),
             'contentWithDate': data.contentWithDate,
             'contentWithoutDate': data.contentWithoutDate
            };

      this.isVisibleTooltip = true;
      console.log(this.localTooltipData);
      return "";
    },

    sentsWithoutDateTooltip(topic) {
      let isTooltipClicked = topic.isTooltipClicked;
      if(this.isTooltipClicked && !isTooltipClicked) return;

      this.localTooltipData = {
                               'datetime': null,
                               'keywords': topic.keywords.toUpperCase(),
                               'contentWithDate': null,
                               'contentWithoutDate': topic.contentWithoutDate[0]
                              };

      if(isTooltipClicked) this.isTooltipClicked = true;
      this.isVisibleTooltip = true;
    },

  }, // methods

  watch: {
    tooltipData: {
      deep: true,
      handler(newVal) {
        if(newVal.contentWithDate !== null)
          this.sentsWithDateTooltip(newVal);
        else
          this.sentsWithoutDateTooltip(newVal);
      } // handler
    } // tooltipData
  } // watch

};
</script>

<style>
.custom-tooltip {
  position: fixed;
  z-index: 9999;
  border: 2px solid white;
  padding: 8px;
  font-size: 14px;
  left: 50%;
  transform: translate(-50%, 0%);
  color: white;
  font-weight: bold;
  background: #499082c4;
  min-width: 70%;
  max-height: 40%;
  overflow: scroll;
  backdrop-filter: blur(10px) !important;
  box-shadow: 0px 69px 89px 119px #000000b5 !important;
  bottom: 5px !important;
  border-radius: 10px !important;
  box-sizing: border-box;
}

.custom-tooltip-extended{
  top: 0;
  bottom: 0;
  margin: auto;
  width: 90%;
  min-width: 30%;
  max-width: 1200px;
  height: fit-content;
  max-height: 90%;
}

.icon-wrapper {
  float: right; 
  display: flex; 
  justify-content: right; 
  align-items: center; 
  gap: 10px;
  font-size: 20px; 
  cursor: pointer;
}

.pred-date {
  background: #2e4353;
  padding: 8px;
  border-radius: 10px;
  color: white;
  display: inline-block;
  float: left;
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

.sentence-wrapper {
  display: flex;
  align-items: center;
  gap: 5px;
  width: 100%;
  margin-bottom: 8px;
}

.sent-without-date-wrapper {
  margin-top: 20px;
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
</style>
