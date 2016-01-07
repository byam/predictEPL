TEST dataset for SemEval-2014 Task #9: Sentiment Analysis on Twitter

SemEval-2014 Task 10 organizers:

- Sara Rosenthal, Columbia University
- Alan Ritter, University of Washington
- Veselin Stoyanov, Johns Hopkins University 
- Preslav Nakov, Qatar Computing Research Institute


NOTE

Please note that by downloading the Twitter data you agree to abide
by the Twitter terms of service (https://twitter.com/tos),
and in particular you agree not to redistribute the data
and to delete tweets that are marked deleted in the future.
You MUST NOT re-distribute the tweets, the annotations or the corpus obtained,
as this violates the Twitter Terms of Use.


Version 1.1: September 20, 2014


SUMMARY

TASK A:
SemEval2014-task9-test-A-gold-NEED-TWEET-DOWNLOAD.txt -- test data for Subtask A

TASK B:
SemEval2014-task9-test-B-gold-NEED-TWEET-DOWNLOAD.txt -- test data for Subtask B


IMPORTANT NOTE 1:

To use this test dataset, one should download (1), and most likely also (2) and (3):

1. the official scorer and format checker
2. the training dataset
3. the dev dataset

You can find them here: http://alt.qcri.org/semeval2014/task9/index.php?id=data-and-tools


IMPORTANT NOTE 2: The data is *NOT READY* to be used as input directly.

You need to do the following two steps first:

1. Download the missing Tweets (SMS and Live Journal messages are already included, but Tweets are missing)

2. Reformat it to be usable as input:

For Subtask A this can be done using the following two commands:

	python download_tweets_api.py --dist=SemEval2014-task9-test-A-gold-NEED-TWEET-DOWNLOAD.txt > SemEval2014-task9-test-A-gold.txt

	generate-taskB-test-input.pl < SemEval2014-task9-test-A-gold.txt > SemEval2014-task9-test-A-input.txt

And similarly for Subtask B:

	python download_tweets_api.py --dist=SemEval2014-task9-test-B-gold-NEED-TWEET-DOWNLOAD.txt > SemEval2014-task9-test-B-gold.txt

	generate-taskB-test-input.pl < SemEval2014-task9-test-B-gold.txt > SemEval2014-task9-test-B-input.txt



INPUT DATA FORMAT (AFTER THE ABOVE STEPS)

-----------------------TASK A-----------------------------------------
--Test Data--

The format for the test file is as follows:
id1<TAB>id2<TAB>start_token<TAB>end_token<TAB>unknwn<TAB>tweet_text

for example:
NA      15115101        2       2       unknwn  amoure wins oscar
NA      15115101        3       4       unknwn  who's a master brogramer now?

--System Output--
We expect the following format for the prediction file is:
id1<TAB>id2<TAB>start_token<TAB>end_token<TAB>pred_class<TAB>tweet_text

where the text field is optional. For example:
NA      15115101        2       2       positive  amoure wins oscar
NA      15115101        3       4       neutral  who's a master brogramer now?


--Gold Standard--
The gold standard will follow the same format as the example system output above.

-----------------------TASK B-----------------------------------------
(Task B uses the same format as Subtask A, but it excludes the start and end token fields.)
--Test Data--

The format for the test file is as follows:
id1<TAB>id2<TAB>unknwn<TAB>tweet_text

for example:
NA      15115101       unknwn  amoure wins oscar
NA      15115101       unknwn  who's a master brogramer now?

--System Output--
We expect the following format for the prediction file is as follows:
id1<TAB>id2<TAB>pred_class<TAB>tweet_text

where the text field is optional. For example:
NA      15115101        positive  amoure wins oscar
NA      15115101        neutral  who's a master brogramer now?

--Gold Standard--
The gold standard will follow the same format as the example system output above.



INPUT DATA FORMAT NOTES

1. For subtask A, the annotations are at the token level, where the tokenization is on a single " " (space). Note that in the case of two consecutive spaces, this creates an empty token, which is counted! Also, token counting starts from zero.

2. Some punctuation characters are escaped, e.g.

@BarackObama\u002c Clinton\u002c Panetta\u002c Petraeus we will not #StandDown on Nov 6 or Nov 7 or Nov 8th. Do the right thing now. #WeWillNotLetThisGo



EVALUATION

The metric for evaluating the participants' systems is average F-measure (averaged F-positive and F-negative, and ignoring F-neutral; note that this does not make the task binary!), as well as F-measure for each class (positive, negative, neutral), which can be illuminating when comparing the performance of different systems.

See also the scorer for details on scoring the output.


DATASET USE

The development dataset is intended to be used as a development-time evaluation dataset as the participants develop their systems. However, the participants are free to use the dataset in any way they like, e.g., they can add it to their training dataset as well.



USEFUL LINKS:

Google group: semevaltweet@googlegroups.com

SemEval-2014 Task 9 website: http://alt.qcri.org/semeval2014/task9/
SemEval-2014 website: http://alt.qcri.org/semeval2014/

SemEval-2015 Task 10 website: http://alt.qcri.org/semeval2015/task10/
SemEval-2015 website: http://alt.qcri.org/semeval2015/



REFERENCES:

If you use the above datasets, please cite the following paper:

@InProceedings{rosenthal-EtAl:2014:SemEval,
  author    = {Rosenthal, Sara  and  Ritter, Alan  and  Nakov, Preslav  and  Stoyanov, Veselin},
  title     = {SemEval-2014 Task 9: Sentiment Analysis in Twitter},
  booktitle = {Proceedings of the 8th International Workshop on Semantic Evaluation (SemEval 2014)},
  month     = {August},
  year      = {2014},
  address   = {Dublin, Ireland},
  publisher = {Association for Computational Linguistics and Dublin City University},
  pages     = {73--80},
  url       = {http://www.aclweb.org/anthology/S14-2009}
}

For the 2013 datasets, you could also refer to the following paper:

@InProceedings{nakov-EtAl:2013:SemEval-2013,
  author    = {Nakov, Preslav  and  Rosenthal, Sara  and  Kozareva, Zornitsa  and  Stoyanov, Veselin  and  Ritter, Alan  and  Wilson, Theresa},
  title     = {SemEval-2013 Task 2: Sentiment Analysis in Twitter},
  booktitle = {Second Joint Conference on Lexical and Computational Semantics (*SEM), Volume 2: Proceedings of the Seventh International Workshop on Semantic Evaluation (SemEval 2013)},
  month     = {June},
  year      = {2013},
  address   = {Atlanta, Georgia, USA},
  publisher = {Association for Computational Linguistics},
  pages     = {312--320},
  url       = {http://www.aclweb.org/anthology/S13-2052}
}
