**********************************************************
* SemEval-2015 Task 10: Training Data for Subtasks C & D *
*                                                        *
* http://alt.qcri.org/semeval2015/task10/index.php       *
* semevaltweet@googlegroups.com                          *
*                                                        *
* Sara Rosenthal, Columbia University                    *
* Alan Ritter, The Ohio State University                 *
* Veselin Stoyanov, Facebook                             *
* Svetlana Kiritchenko, NRC Canada                       *
* Saif Mohammad, NRC Canada                              *
* Preslav Nakov, Qatar Computing Research Institute      *
**********************************************************

The distribution consists of a set of Twitter status IDs with annotations for Subtask C and D:
topic polarity and trends toward a topic.
There are about 10 tweets provided per topic and a total of 44 topics.

You should use the downloading script for subtasks A and B to obtain the corresponding tweets:

	https://github.com/aritter/twitter_download

The data for Subtask C is formatted as follows (see twitter-train-B-topics.txt):

<ID><tab><TOPIC><tab><TOPIC polarity: positive|negative|neutral|off_topic><tab><TWITTER_MESSAGE>

Example:
105121481662541824	#dexter	neutral	I forgot how sad the first episode of the 5th season of Dexter is. #depressing #dexter #darkpassenger

Note: The annotation with respect to Subtask A would have been negative for this tweet (the overall polarity of the tweet is negative), but it is neutral for Subtask C (the negative sentiment is NOT towards the topic: #dexter).

This can be seen in the file twitter-train-B-tweet-and-topics.txt, which we have included to allow for such comparisons.


The data for Subtask D is simply computed through the ratio of polarity.

For your reference, here are the definitions of Subtasks C and D:

Subtask C: Topic-Based Message Polarity Classification: Given a message and a topic, classify whether the message is of positive, negative, or neutral sentiment towards the given topic. For messages conveying both a positive and negative sentiment towards the topic, whichever is the stronger sentiment should be chosen.

Subtask D: Detecting Trends Towards a Topic: Given a set of messages on a given topic from the same period of time, determine whether the dominant sentiment towards the target topic in these messages is (a) strongly positive, (b) weakly positive, (c) neutral, (d) weakly negative, or (e) strongly negative.
