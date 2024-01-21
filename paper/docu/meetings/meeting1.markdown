# Meeting 1)


### First dataset from site called: LongBets
- you can make predictions and bet and comment on them

### Another dataset is from a site called Horizon
- only took the first sentence of the paragraph, which contains the prediction
- then manually reviewed it

### ChatGPT
- I put in: "Give me a list of 30 predictions about the future and don't use the word will



## Questions:

### Are the big number of 'wills' a problem?
- 

### Should I generate more data - how much do I need?
- 

### Should I try to pretrain Roberta on this data?
- 

### How should I go about collecting sentences that are not predictions?
- chatgpt equal amount for negatives
- horizons 40 from top section
- longbets negatives → scrape news


- news that also contain dates
- current news - google news portal
- from beginning of article


- 50% from news (contain verb in past tense)
- 50% from news (present)


- not only past to non-past


- some should have date, some not
- present of dates


5k to 5k would be ideal


- collect prompts

- generate tricky examples with prompts to chatgpt




<hr>

connect to some news api
bing news

give keyword, in specific time-frame
- time estimation


- group them - clustering (affinitive propagation) density based (dp scan)
- cosine similary - roberta/esbert
- term cloud for each cluster
- what year fall into cluster

- feedback from users
- recall and presicion

- use gitlab for classifier
  - add adam as developer
