# Begrüßung:
- Hello and Welcome to my initial presentation. 
- I am working on a thesis with the title "Detecting and Visualizing Future-related Text Content" and I would like to give you a short introduction into this topic and show you what I've been working on and what I am planning to do in the coming months.

# Introduction:
- so I will start off by saying that lots and lots of news articles are published every day.
- and of course many of them contain information about the future
- so here we have 4 such examples of such future-related content in news articles
- this information could be about upcoming product releases, sports matches, political announcements and plans and so on ...
- if we had some kind of system that given some entity could extract these future-related sentences from articles, this could be very useful
- because it would provide a great overview of what's in store for this entity it them coming days, months, years or even decades

- and yeah that's basically the goal of my work, to develop this kind of system where you can input some entity and it then extracts all future-related sentences it can find in news articles and presents to you what it has found in a nice way.

- but now I want to talk about this system step by step and in a bit more detail

# Sytem - Overview
- first of all, the use has to provide some keyword - for example elon musk
- then a lot of articles are downloaded from the internet, that are about this topic
- the articles are split up into sentences
- and these sentences are fed into a neural network that has been trained to classify sentences as either future-related (positives) or non-future-related (negatives)
- so the NN classifies the sentences into 2 different groups
- and we only take the group with sentences about the future
- those sentences then get clustered into different topics
- which then are presented to the user - for every topic the most dominant keywords are extracted and used as topic-headings
- so for example in topic1 we have all sentences that contain some future information about …
- in the last part, we identify all senteces that have some kind of temporal expression inside of them (like *next week*) and map them onto a timeline
- so now I want to talk a bit about this NN and the data it was trained on

# Goal #1 - Create Multi-Sourced Dataset
- the first goal of the project is to create a dataset of future-related-sentences.
- these sentences should be from different sources and they should have different words inside them with different structure
- this data is then used to train a classifier

# Goal #2 - Fine-tune RoBERTa
- so as already said, we want a model that takes a sentece as input and then determines if it contains future information or not
- so we have a binary classification problem
- a popular approach to solve these kinds of problems is to take some pretrained language model like bert, that has already been trained on a huge amount of data and has already learned to *understand* text and then finetune it.
- so we append a fully connected network here that takes the word-embeddings from the pretrained model and that's how the NN is trained to do binary classification.

# System - Overview (1)
- so we've now looked at the NN-part, next we're going to take a look at the clustering-part

# Goal #3: Clustering into Topics
- so goal here is to take all the future-related sentences and group them into specific topics
- this is done by converting the sentences into vector-embeddings and then doing clustering on those vectors
- for a query like *Elon Musk* there could be formed topic-clusters like these: …

# Goal #4: Identify Sentences with Temporal Expressions
- once this is done, the clusters are taken and analyzed
- the goal here is to identify sentences that contain temporal expressions
- so here *'coming days'*, *'next week'*, *'next few weeks'*, *'six months'* would be temporal expressions
- those sentences are then extracted and visualized on a timeline

# Goal #5: Visualize Sentences on Timeline
- this works as follows
- we have the sentences we want to visualize, for example: …
- for every sentence we also have its publication-date
- we extract the temporal-expression and map it to a date
  - so here we map *coming days* to **05.04**, by adding a value that represents *coming days* eg. **3** to the publication date **02.04**
- here we have *next few weeks*, we map this to 17.04, as we map 2 weeks to *next few weeks*
- here we have *six-months*, we map this to 02.10, as this date is 6 months away from the publication date
- and that's it, we have our timeline that gives us a great overview of the future-related sentences for every topic

# Current Progress
- so as my initial presentation is quite late, I've already managed to do some work
- most of the components are already implemented
  - I have a dataset from 4 different sources of about 1k sentences
  - I have trained the classifier
  - I have implemented the sentence-clustering and temporal-expression-extraction
  - and I have written the frontend code to visualize the sentences on a timeline

# What's still to do
- however there is still a lot to do
- first of all I have yet to significantly increase the dataset to ~4k sentences
- then I want to output the statistics, like:
  - #articles downloaded
  - % future-nonfuture sentences
  - #clusters and avg-cluster-size
  - % sentences with temporal expressions
- also the user has to be able to put in a query, so the whole system to allow this has to be built
  - basically the frontend has yet to be connected to the backend
- finally the thesis should be written, so I can hand it in and present it in the end of June
