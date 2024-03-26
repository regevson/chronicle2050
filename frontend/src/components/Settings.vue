<template>
  <div class="search">

    <!-- Configurations Section -->

    <div class="settings-wrapper">
      <div class="config-text">download</div>
      <input type="number" min="1000" max="6000" :value="numArticles" 
        placeholder="#articles to download" readonly
      />
      <div class="config-text">articles, from:</div>
      <input type="date" :value="selectedQuery.from" title="from-date" readonly />
      <div class="config-text">to:</div>
      <input type="date" :value="selectedQuery.to" title="to-date" readonly />
    </div>

    <!-- Research Preview Banner -->

    <div class="preview" @click="testEntity()">
      <span style="color: white; font-weight: bold">
        This is a research preview. One of the seven queries can be selected.<br>
        Precomputed values are returned.
      </span>
    </div>

    <!-- Entity Selection -->

    <div>
      <button class="preview-btn" v-for="query in queries" :key="query" @click="entityButton(query)" 
        :class="{'preview-selected': selectedQuery.entity === query.entity}"
      >
          {{query.entity}}
      </button>
    </div>

    <!-- Start Button -->

    <input class="search-button" @click="emitConfig" type="submit" 
      :value="'Lay out ' + selectedQuery.entity + '\'s' + ' future'"
    >
    <!--
    <input type="text" placeholder="explore the future of..." 
      style="margin-bottom: 20px; font-weight: bold !important; text-align: center" disabled><br>
    -->
  </div>
</template>

<script>

export default {
  data() {
    return {
      queries: [
        {'entity': 'NASA', 'from': '2023-09-10', 'to': '2023-10-09'},
        {'entity': 'USA', 'from': '2023-09-10', 'to': '2023-10-09'},
        {'entity': 'Ukraine', 'from': '2023-09-10', 'to': '2023-10-09'},
        {'entity': 'Israel', 'from': '2023-09-10', 'to': '2023-10-09'},
        {'entity': 'Tennis', 'from': '2023-09-10', 'to': '2023-10-09'},
        {'entity': 'OpenAI', 'from': '2023-09-10', 'to': '2023-10-09'},
        {'entity': 'Elon Musk', 'from': '2023-09-10', 'to': '2023-10-09'}
      ],
      numArticles: 4000,
      selectedQuery: null,
    } // return
  }, // data

  created() {
    this.selectedQuery = this.queries[0];
    this.numArticles = 4000;
  },

  methods: {
    testEntity() {
      this.selectedQuery = {'entity': 'Test', 'from': '2023-09-10', 'to': '2023-10-09'};
    },

    entityButton(query) {
      this.selectedQuery = query;
    },

    emitConfig() {
      this.$emit('start-event', {
        'entity': this.selectedQuery.entity, 
        'fromDate': this.selectedQuery.from, 
        'toDate': this.selectedQuery.to,
        'numArticles': this.numArticles
      })
    }
  },
};
</script>

<style>
.search {
  background: #2a3e4d;
  border-radius: 8px;
  max-width: 800px;
  margin: 0 auto;
  margin-bottom: 90px;
  padding: 20px 10px 20px 10px;
  box-sizing: border-box;
}

.search input {
  height: 25px;
  border-radius: 5px;
  border: none;
  padding: 5px;
}

.settings-wrapper {
  display: flex; 
  align-items: center; 
  justify-content: center; 
  flex-wrap: wrap;
  margin-bottom: 30px;
  gap: 5px;
}

.settings-wrapper input {
  font-weight: normal !important; 
  text-align: center !important;
  width: 95px;
  font-family: 'Roboto', sans-serif;
  color: black;
}

.preview {
  display: flex;
  align-content: center;
  justify-content: center;
  background: #8a5050;
  margin: 0 auto;
  margin-bottom: 34px;
  padding: 10px;
  border-radius: 5px;
  font-size: calc(15px + 0.1vw);
  width: 90%;
}

.preview-btn {
  background-color: grey;
  color: white;
  margin: 5px;
  padding: 10px;
  border: none;
}

.preview-selected {
  background-color: #3b7368;
}

.search-button {
  background-color: #3b7368;
  color: white;
  padding: 10px;
  height: 35px !important;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  font-size: 16px;
  margin-top: 30px;
}

button {
  font-weight: 600;
  cursor: pointer;
  border-radius: 5px;
  font-size: 12px;
}

button:hover {
  /*background-color: #3b7368;*/
  transform: scale(1.04);
  transition: ease-in-out 0.2s all;
}

.config-text {
  font-weight: bold;
  font-size: 17px;
}

@media (max-width: 658px) {
  .search input {
    font-size: 12px;
  }

  .settings-wrapper {
    flex-direction: column;
  }
  .config-text, input[type="number"], input[type="date"] {
    font-size: 14px;
    flex: 0 0 100%;
  }
}

</style>

