******************************************************
* SemEval-2016 Task 4: Sentiment Analysis on Twitter *
*                                                    *
*               TRAINING + DEV + DEVTEST DATA        *
*                                                    *
* http://alt.qcri.org/semeval2016/task4/             *
* semevaltweet@googlegroups.com                      *
*                                                    *
******************************************************


TRAINING + DEV + DEVTEST dataset for SemEval-2016 Task 4

Version 1.2: November 5, 2015


Task organizers:

* Preslav Nakov, Qatar Computing Research Institute, HBKU
* Alan Ritter, The Ohio State University
* Sara Rosenthal, Columbia University
* Fabrizio Sebastiani, Qatar Computing Research Institute, HBKU
* Veselin Stoyanov, Facebook


LIST OF VERSIONS

  v1.2 [2015/11/05]: clarified that the test data is actually devtest, i.e., development time testing dataset

  v1.1 [2015/10/31]: swapped the first columns of the datasets for subtasks B, C, D, E due to an issue with the download script (otherwise the data is the same)

  v1.0 [2015/10/15]: initial distribution of the data


NOTES

1. Please note that by downloading the Twitter data you agree to abide by the Twitter terms of service (https://twitter.com/tos), and in particular you agree not to redistribute the data and to delete tweets that are marked deleted in the future.

2. The distribution consists of a set of Twitter status IDs with annotations for Subtasks A, B, C, D, and E: topic polarity and trends toward a topic. There are exactly 100 tweets provided per topic and a total of 100 topics. You should use the downloading script to obtain the corresponding tweets: https://github.com/aritter/twitter_download

3. The "neutral" label in the annotations stands for objective_OR_neutral.

4. The devtest dataset is a development time test set; this is not the actual test dataset for the task.

5. Even though we provide a default split of the data into training, development and development-time testing datasets, participants are free to use this data in any way they find useful when training and tuning their systems, e.g., use a different split, perform cross-validation, train on all three datasets, etc.


FILES

gold/train/100_topics_100_tweets.sentence-three-point.subtask-A.train.gold.txt -- training data for subtask A with gold annotations
gold/train/100_topics_XXX_tweets.topic-two-point.subtask-BD.train.gold.txt -- training data for subtasks B and D with gold annotations
gold/train/100_topics_100_tweets.topic-five-point.subtask-CE.train.gold.txt -- training data for subtasks C and E with gold annotations

gold/dev/100_topics_100_tweets.sentence-three-point.subtask-A.dev.gold.txt -- dev data for subtask A with gold annotations
gold/dev/100_topics_XXX_tweets.topic-two-point.subtask-BD.dev.gold.txt -- dev data for subtasks B and D with gold annotations
gold/dev/100_topics_100_tweets.topic-five-point.subtask-CE.dev.gold.txt -- dev data for subtasks C and E with gold annotations

gold/devtest/100_topics_100_tweets.sentence-three-point.subtask-A.devtest.gold.txt -- devtest data for subtask A with gold annotations
gold/devtest/100_topics_XXX_tweets.topic-two-point.subtask-BD.devtest.gold.txt -- devtest data for subtasks B and D with gold annotations
gold/devtest/100_topics_100_tweets.topic-five-point.subtask-CE.devtest.gold.txt -- devtest data for subtasks C and E with gold annotations

input/devtest/100_topics_100_tweets.sentence-three-point.subtask-A.devtest.input.txt -- devtest data for subtask, input only
input/devtest/100_topics_XXX_tweets.topic-two-point.subtask-BD.devtest.input.txt -- devtest data for subtasks B and D, input only
input/devtest/100_topics_100_tweets.topic-five-point.subtask-CE.devtest.input.txt -- devtest data for subtasks C and E, input only



DATA FORMAT FOR *GOLD* FILES


-----------------------SUBTASK A-----------------------------------------

The format for the training/dev/devtest *gold* file is as follows:

	id<TAB>label

where "label" can be 'positive', 'neutral' or 'negative'.


-----------------------SUBTASKS B,D--------------------------------------

The format for the training/dev/devtest *gold* file is as follows:

	id<TAB>topic<TAB>label

where "label" can be 'positive' or 'negative' (note: no 'neutral'!).

There are up to 100 tweets per topic (less than 100, as neutral tweets are excluded).

-----------------------SUBTASKS C,E--------------------------------------

The format for the training/dev/devtest *gold* file is as follows:

	id<TAB>topic<TAB>label

where "label" can be -2, -1, 0, 1, or 2,
corresponding to "strongly negative", "negative", "negative or neutral", "positive", and "strongly positive".

There are exactly 100 tweets per topic.



DATA FORMAT FOR *INPUT* FILES


-----------------------SUBTASK A-----------------------------------------

The format for the devtest *input* file is as follows (i.e., just one ID per line):

  id


-----------------------SUBTASKS B,C,D,E----------------------------------

The format for the devtest *input* file is as follows:

  id<TAB>topic

For subtasks B and D, there are up to 100 tweets per topic (less than 100, as neutral tweets are excluded).

For subtasks C and E, there are exactly 100 tweets per topic.



LICENSE

The accompanying dataset is released under a Creative Commons Attribution 3.0 Unported License (http://creativecommons.org/licenses/by/3.0/).



CITATION

You can cite the following paper when referring to the dataset (new citation will be provided when it will be available):

@InProceedings{Rosenthal-EtAl:2015:SemEval,
  author    = {Sara Rosenthal and Alan Ritter and Veselin Stoyanov and Svetlana Kiritchenko and Saif Mohammad and Preslav Nakov},
  title     = {{SemEval}-2015 Task 10: Sentiment Analysis in Twitter},
  booktitle = {Proceedings of the 9th International Workshop on Semantic Evaluation},
  series    = {SemEval'~15},
  year      = {2015},
  month     = {June},
  address   = {Denver, Colorado, USA},
  publisher = {Association for Computational Linguistics},
  pages     = {451--463},
  url       = {http://www.aclweb.org/anthology/S15-2078}}


USEFUL LINKS:

Google group: semevaltweet@googlegroups.com
SemEval-2016 Task 4 website: http://alt.qcri.org/semeval2016/task4/
SemEval-2016 website: http://alt.qcri.org/semeval2016/
