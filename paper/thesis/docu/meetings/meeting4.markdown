# Meeting 4:

## Changed Timeline:
  - y-axis: topics
  - dot (x,y): contains (all) sentences of a cluster y that map to date x
      - should be same event as same cluster and same timex
      - show all sentences instead of one as they often provide additional information
  - color of dot: should represent relevance of the event
      - #sameDate: count #sentences of a cluster that map to this date
  - per dot not only the most representative sentence is shown, but others that have same date but differ a bit (based on cosine-sim) are shown too → can provide additional information
  - added publication date to sentences


## Remove Duplicates and Similar Sentences:
  - as there are lots of similar sentences (same content, slightly different words) those should not be shown to the user → they don't provide additional information
  - those sentences are removed
    - compare sentences based on their cosine-similarity
    - if it is too close, remove the sentence with the lower #mentions

## Cluster View under Timeline:
  - now every sentences contains a link to the article it was extracted from
  - #mentions is shown next to sentence
    - #mentions = #duplicates + #sentences with cosine-similarity ≥ 0.9
  - sentences are ordered by #mentions (descending)

## TODO:
- make content dynamic (query field)
  - should I run classifier and clustering on a normal server (RAM: 8GB, 4 vCPUS)
    - website would be up 24/7
  - or on GoogleColab
    - website would be up only when session is started

- write thesis

- improve frontend UI
