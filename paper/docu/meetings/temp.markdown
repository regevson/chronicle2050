## Solving The Duration-Problem Without Temporal Extraction:
- quite a few predictions with temporal expressions in them that could be displayed on timeline are lost
- When iteratively adding words to the sentence, you can see which part contributes most to the prediction
- if a timex is located in this area → choose it, descard the other
0 After
1 After being
2 After being posponed
3 After being posponed for
4 After being posponed for 30
5 After being posponed for 30 years
6 After being posponed for 30 years, it
7 After being posponed for 30 years, it will
8 After being posponed for 30 years, it will finally
9 After being posponed for 30 years, it will finally happen
10 After being posponed for 30 years, it will finally happen in
11 After being posponed for 30 years, it will finally happen in 2
12 After being posponed for 30 years, it **will finally happen in 2 years**
-> **use 2 years**
![](/home/regevson/ComputerScience/cs/6_semester/Bachelor/docu/meetings/nn_iter_1.png)

0 It
1 It might
2 It might, after
3 It might, after being
4 It might, after being planned
5 It might, after being planned for
6 It might, after being planned for 30
7 It might, after being planned for 30 years
8 It might, after being planned for 30 years, be
9 It might, after being planned for 30 years, be realized
10 It might, after being planned for 30 years, be realized in
11 It might, after being planned for 30 years, be realized in 5
12 It might, after being planned for 30 years, **be realized in 5 years**
-> **use 5 years**
![](/home/regevson/ComputerScience/cs/6_semester/Bachelor/docu/meetings/nn_iter_2.png)

### Problems, when relevant section is not towards the end of the sentence
- non-relevant section doesn't decrease confidence

0 The
1 The rockets
2 The rockets are
3 The rockets are going
4 The rockets are going to
5 The rockets are going to be
6 The rockets are going to be launched
7 The rockets are going to be launched in
8 The rockets are going to be launched in 2
9 The rockets are going to be launched in 2 years
10 The rockets are going to be launched in 2 years, following
11 The rockets are going to be launched in 2 years, following 5
12 The rockets are going to be launched in 2 years, following 5 years
13 The rockets are going to be launched in 2 years, following 5 years of
14 The rockets are going **to be launched in 2 years, following 5 years of discussions**
-> **use 2 years or 5 years?**
![](/home/regevson/ComputerScience/cs/6_semester/Bachelor/docu/meetings/nn_iter_3.png)

### Solution:
- extract those non-contributing sections of sentences and put them into negatives
- maybe this will lead towards confidence-reduction?
- In the case of *"The rockets are going to be launched in 2 years, following 5 years of discussions"*
  - *"The rockets are going to be launched in 2 years"* into POSITIVES
  - *"Following 5 years of discussions"* into NEGATIVES
  - *"The rockets are going to be launched in 2 years, following 5 years of discussions"* into POSITIVES
- this would further improve the classifier on its original task and could also make it detect the sections that contribute to the prediction most





## Postprocessing Clusters:
- clustering led to having very **similar** sentences in the same cluster
  - same sentence, only slightly different structure, other word, …
- this led to 'duplicate' info on the timeline or in the topic-section
- right now I use the SBERT embeddings that were fed to BERTopic and eliminate similar sentences like this:
  - [**0.7874, 0.77049**, 0.598494, **0.3454, 0.314950**] turns into
  - [**0.7874**, 0.598494, **0.3454**]
- works pretty good, but I will try to change the mmr-parameters
