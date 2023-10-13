<template>
<div class="pub-date">pub.<br>{{new Date(item.timestamp).toLocaleDateString('en-GB')}}:</div>
<div class="sentence">
  {{item.sentence}}
  <span class="mention">
    [{{Math.floor(item.mentions)}} mention{{Math.floor(item.mentions) > 1 ? 's' : ''}}]
    <a 
      :href="item.link" 
      style="background: #161e27 !important"
      target="_blank">1</a> 
    <a 
      :href="link" 
      v-for="(link, idx) in getLinks(item.links)"
      :key="link" 
      target="_blank">{{idx+2}}</a> 
    <span v-if="shouldShowDots(item.links)" style="font-weight: bold; font-size: 15px">...</span>
</span>
</div>
</template>

<script>

export default {
  props: {
    item: {
      type: [Object, null],
      default: null,
    },
  },

  data() {
    return {
    } // return
  }, // data

  methods: {
    getLinks(links) {
      return links.split(',').filter(item => item !== '').slice(0, 5);
    },

    shouldShowDots(links) {
      return links.split(',').filter(item => item !== '').length > 6;
    },
  }, // methods


};
</script>

<style>
.pub-date {
  text-align: left;
  font-weight: 500;
  white-space: nowrap;
  background: #31665b;
  padding: 3px;
  border-radius: 5px;
}

.sentence {
  font-size: 15px;
  background: #31665b !important;
  font-weight: bold;
  padding: 7px;
  border-radius: 5px;
  color: white;
  text-align: left;
}

.mention {
  color: #161e27;
}

.mention a {
  color: white !Important;
  background: cadetblue;
  border-radius: 100%;
  padding: 0px 5px 0px 5px;
  margin-right: 2px;
}

</style>
