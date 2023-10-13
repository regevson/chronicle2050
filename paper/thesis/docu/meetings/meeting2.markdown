# Meeting 2)

## Classifier:

### Architecture:
- Finetuned DistilRoberta
- Layers:
  - DistilRoberta Last Layer → **Mean Pooling Layer (512) → Dropout Layer → Finetuning Hidden Layer (512) → ReLU → Dropout Layer →  Output Layer (1)**

### Dataset:
![](/home/regevson/ComputerScience/cs/6_semester/Bachelor/docu/meetings/dataset.png)
- longbets-negatives are sentences from news articles with dates in them (as there are a lot of dates in longbets)
- *'reviewed'* are sentences from news articles that were classified by the model and reviewed
  - these contain a lot of sentences where the model wasn't sure
  - this part of the dataset could increase a lot
- *'horizons'*, *'chatgpt'* and *'reviewed'* I reviewed manually

## Temporal-Extraction:
- SUTime (similar to GUTime)
- extract timexes of type **DATE** that are in the future
- Problem with type **DURATION**:
  - *"After being postponed for 30 years, it will finally happen in 2 months."*
  - gives **'30 years'** and **'2 months'**
  - need system to decide if 30-years-context is before/after 2-months-context and then take the one that is **after**
    - **temporal-relation-extraction?** → no ready-to-use system found (or not available anymore)
  - therefore right now I'm discarding type **DURATION** and only use **DATE**
    - **DATE** works pretty good
    - also detects expressions like: *'in the next couple of days'* or *'next summer'*, …

## Clustering:
- downloaded ~2500 articles from internet with topic 'elon musk'
- classified them with the model
- fed into BERTopic:
  1) Sentence Embedding: **SBERT**
  2) Dimensionality Reduction: **UMAP**
  3) Clustering: **HDBSCAN**
  4) Generate Topic Candidates: **c-TF-IDF**
  5) Maximize Marginal Relevance: **MMR**

- all detected predictions are fed into BERTopic
  - generates pretty good clusters

- for the timeline I tried extracting sentences with timexes from the previously clustered topics
  - doesn't work that well, might need other approach
  - maybe separately clustering the timeline-sentences with different BERTopic configuration works better

- Intertopic Distance Plot:
![](/home/regevson/ComputerScience/cs/6_semester/Bachelor/docu/meetings/topic_distance_plot.png)

- Dominant Keywords Per Topic Plot:
![](/home/regevson/ComputerScience/cs/6_semester/Bachelor/docu/meetings/topic_keywords_plot.png)
