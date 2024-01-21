# Meeting 3:

## Postprocessing Clusters:
- clustering led to having very **similar** sentences in the same cluster
  - same sentence, only slightly different structure, other word, …
- this led to 'duplicate' info on the timeline or in the topic-section
- right now I use the SBERT embeddings that were fed to BERTopic and eliminate similar sentences like this:
  - [**0.7874, 0.77049**, 0.598494, **0.3454, 0.314950**] turns into
  - [**0.7874**, 0.598494, **0.3454**]

## Small Website to make Classification more convenient:
- can share with friends
- can do classification on my phone
- sentences are from news articles (requested without a specific topic)

## Structure of Thesis:

# Extraction And Visualization of Future-related Sentences from News Articles

## Abstract

## Table of Contents

## Introduction
### Background and motivation
### Research questions and objectives
### Overview of the thesis

## Literature Review
### Existing methods for future-related sentence extraction
### Current approaches to topic modeling
### Visualization techniques for temporal data

## Data collection and preprocessing
### Goal
- multi-sourced
- sentences should have different structure
### Sources of news articles
#### Longbets
- describe source and data scraped from there
#### Horizons
- describe source and data scraped from there
#### ChatGPT
- describe source and data scraped from there
#### News
- describe source and data scraped from there
### Data cleaning and preprocessing techniques
### Annotation of future-related sentences

## Methodology
### Overview of the proposed method
### Description of the BERT model and fine-tuning process
### Clustering of future-related sentences using BERTopic
### Temporal tagging of future-related sentences

## Results
### Evaluation metrics
### Analysis of the extracted future-related sentences and their topics

## Visualization
### Overview of the proposed visualization approach
### Interactive timeline visualization of future-related sentences and topics

## Conclusion and future work
### Summary of the contributions and achievements
### Limitations and future directions for research

## References

## Appendices


I have already started with the *Data collection and preprocessing* section


## Visualizing Stats to Frontend:
- fraction of sentences with(out) temporal expressions (timeline)
- num clusters
- average sentences per cluster
