# Final Presentation


## Greetigs:
- Hello and Welcome to my final presentation. 
- I am working on a thesis with the title "Detecting and Visualizing Future-related Text Content" and today I would like to give you a short introduction into this project and show you what I've been working on.

## Introduction:
- so I will start off by saying that lots and lots of news articles are published every single day on the internet.
- and of course many of them contain information about the future
	- here we can see 4 such examples of headlines that tell us something about the future.
- this information could be about upcoming product releases, sports events, political announcements and plans and so on ...
- and it would be very useful to have some kind of system that could detect and extract those future-related sentences from the articles and visualize them to the user
- this would provide a great overview of what's in store for some country, some celebrity, or some company in the coming days, months, years or even decades

- So this was basically the goal of my work - to develop this kind of system where you can input some entity and it then extracts all future-related sentences it can find in news articles and presents them to you in a nice way.

- so let's explore the system step by step in more detail

## Sytem - Overview
- first of all, the user has to provide some keyword - for example elon musk
- then a lot of articles are downloaded from the internet, that are about this topic
- the articles are split up into sentences
- and these sentences are fed into a neural network
- this network has been trained to classify sentences as either future-related (positives) or non-future-related (negatives)
- so it classifies the sentences into 2 different groups
- and we only take the group with sentences about the future
- those sentences then get clustered into different topics
- which then are presented to the user - for every topic the most dominant keywords are extracted and used as topic-headings
- so for example in topic1 we have all sentences that contain some future information about a the spacex starship rocket launch
- in the last part, we identify all senteces that have some kind of temporal expression inside of them (like *next week*) and map them onto a timeline
- so now I want to talk a bit about this NN and the data it was trained on

## Create Multi-Source Dataset
- so next we'll look at the classification phase
- there our goal was to create a dataset of future-related and non-future-related sentences
- these sentences should be from different sources, they should have diverse structure, they should have different words inside of them and should be about a variety of different topics
- this is important so the neural network later on learns to generalize from the training set
- and the more diverse this training set is, the better it will generalize

- so the first source of our dataset is a website called 'longbets'
- this is a site where users can submit predictions and bet money on them
	- other users can then bet against those predictions
	- the winner gets the money
- the predictions there span over years and even decades, they are about different topics and written by different users
- so they were perfect for our dataset and therefore 448 predictions were scraped and added to the dataset

- the next source is a website that is mainly about future technology
- X positives and Y negatives where scraped from there

- then also ChatGPT was used to generate sentences
	- the nice thing about ChatGPT is that you can create prompts where you exactly specify what kind of data you want and you immediately get it
	- data gathering with chatgpt generally becomes more and more common now
- so 300 positives and negatives were generated in this way

- as in the end, the system has to classify sentences from news articles, it made sense collect the most amount of sentences from actual news articles, so 2.5k positives and 3k negatives were collected and manually labelled from NY-Times articles

- in total we managed to gather 6.8k sentences, where about half contain future information

## Classification
- so this data was then used to train a neural network
- and a very popular approach here is to take some pretrained model and finetune it for a downstream task - in our case for the task of detecting future-related sentences
- in the following I want to very quickly give you a short idea on how these models are pre trained 
- so in our case we used a variation of a transformer-encoder called BERT which was pretrained by doing MLM
- So basically some sentence from the training set is taken and randomly a word is replaced with the word 'MASK'
- This sentence is then fed into a transformer encoder model which creates for each word an embedding-vector. 
- The vector embedding of the masked word is then fed into a fully connected neural network. 
- Then a softmax activation function is applied to get a probability distribution 
- and then we have for every word in our dictionary a probability as we can see here
- and the goal is to maximize the probability for our masked word which in our case is the word 'is'
- and as in this case the network seems to have already been trained on this task and it correctly outputs for the word 'is' the highest probability
- so it turns out that if you do this for a huge amount of sentences, the model learns to understand language and you can use those vector embeddings it outputs here for downstream tasks

- so as already said, we want a model that takes a sentece as input and then determines if it contains future information or not
- so we have a binary classification problem
- so we append a fully connected network here that takes the word-embeddings from the pretrained model and that's how the NN is trained to do binary classification.

## System - Overview (1)
- so we've now looked at the NN-part, next we're going to take a look at the clustering-part

## Goal #3: Clustering into Topics
- so goal here is to take all the future-related sentences and group them into specific topics
- this is done by converting the sentences into vector-embeddings and then doing clustering on those vectors
- for a query like *Elon Musk* there could be formed topic-clusters like these: …

## Goal #4: Identify Sentences with Temporal Expressions
- once this is done, the clusters are taken and analyzed
- the goal here is to identify sentences that contain temporal expressions
- so here *'coming days'*, *'next week'*, *'next few weeks'*, *'six months'* would be temporal expressions
- those sentences are then extracted and visualized on a timeline

## Goal #5: Visualize Sentences on Timeline
- this works as follows
- we have the sentences we want to visualize, for example: …
- for every sentence we also have its publication-date
- we extract the temporal-expression and map it to a date
  - so here we map *coming days* to **05.04**, by adding a value that represents *coming days* eg. **3** to the publication date **02.04**
- here we have *next few weeks*, we map this to 17.04, as we map 2 weeks to *next few weeks*
- here we have *six-months*, we map this to 02.10, as this date is 6 months away from the publication date
- and that's it, we have our timeline that gives us a great overview of the future-related sentences for every topic
