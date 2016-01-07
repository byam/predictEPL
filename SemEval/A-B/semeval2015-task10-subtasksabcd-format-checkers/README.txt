*** SUMMARY ***

Official format checkers for SemEval-2015 Task 10: Sentiment Analysis in Twitter, subtasks A, B, C and D.
These scripts should be used to check the output of systems that participate in the task.
See http://alt.qcri.org/semeval2015/task10/ for more detail.

Version 1.0: Dec. 16, 2015.


Organizers:
Sara Rosenthal          Columbia University
Alan Ritter             The Ohio State University
Veselin Stoyanov        Facebook
Svetlana Kiritchenko    NRC Canada
Saif Mohammad           NRC Canada
Preslav Nakov           Qatar Computing Research Institute

Checkers written by Preslav Nakov and Veselin Stoyanov.


This software is released under a Creative Commons Attribution 3.0 Unported License
        http://creativecommons.org/licenses/by/3.0/


To use it, run the following command:
perl format-check-semeval2015-task10-subtask<SUBTASK>.pl <input> <your-system-output>

Where <SUBTASK> is one of A, B, C, or D
and <your-system-output> is the file containing the output of your system.

NOTE: The script should be run in a directory containing the "input" files!
The script should then output:

	The predictions file format looks OK.


Details follow below.


------- SUBTASK A -------

  Use:
     perl format-check-semeval2015-task10-subtaskA.pl <INPUT_FILE> <PREDICTIONS_FILE>

  Example use:

     perl format-check-semeval2015-task10-subtaskA.pl SemEval2015-task10-test-A-input.txt sample/SemEval2015-task10-test-A-candidate-good.txt
     perl format-check-semeval2015-task10-subtaskA.pl SemEval2015-task10-test-A-input.txt sample/SemEval2015-task10-test-A-candidate-bad.txt

     perl format-check-semeval2015-task10-subtaskA.pl SemEval2015-task10-test-A-input-progress.txt sample/SemEval2015-task10-test-A-candidate-progress-good.txt
     perl format-check-semeval2015-task10-subtaskA.pl SemEval2015-task10-test-A-input-progress.txt sample/SemEval2015-task10-test-A-candidate-progress-bad.txt

  Description:
     The format checker performs format checking for the predictions file given the input file.
		
		The format for the test input file is as follows:
		id1<TAB>id2<TAB>start_token<TAB>end_token<TAB>unknwn<TAB>tweet_text
		
		for example:
		NA      15115101        2       2       unknwn  amoure wins oscar
		NA      15115101        3       4       unknwn  who's a master brogramer now?
		
		--System Output--
		We expect the following format for the prediction file:
		id1<TAB>id2<TAB>start_token<TAB>end_token<TAB>predicted_sentiment_4_phrase<TAB>tweet_text
		
		where tweet_text is optional,
		and predicted_sentiment_4_phrase can be "positive", "negative" or "neutral".
		For example:
		NA      15115101        2       2       positive  amoure wins oscar
		NA      15115101        3       4       neutral  who's a master brogramer now?


------- SUBTASK B -------

  Use:
     perl format-check-semeval2015-task10-subtaskB.pl <INPUT_FILE> <PREDICTIONS_FILE>

  Example use:

     perl format-check-semeval2015-task10-subtaskB.pl SemEval2015-task10-test-B-input.txt sample/SemEval2015-task10-test-B-candidate-good.txt
     perl format-check-semeval2015-task10-subtaskB.pl SemEval2015-task10-test-B-input.txt sample/SemEval2015-task10-test-B-candidate-bad.txt

     perl format-check-semeval2015-task10-subtaskB.pl SemEval2015-task10-test-B-input-progress.txt sample/SemEval2015-task10-test-B-candidate-progress-good.txt
     perl format-check-semeval2015-task10-subtaskB.pl SemEval2015-task10-test-B-input-progress.txt sample/SemEval2015-task10-test-B-candidate-progress-bad.txt

  Description:
     The format checker performs format checking for the predictions file given the input file.
		
		The format for the test input file is as follows:
		id1<TAB>id2<TAB>unknwn<TAB>tweet_text
		
		for example:
		NA      15115101       unknwn  amoure wins oscar
		NA      15115101       unknwn  who's a master brogramer now?
		
		--System Output--
		We expect the following format for the prediction file:
		id1<TAB>id2<TAB>predicted_sentiment_4_tweet<TAB>tweet_text
		
		where tweet_text is optional,
		and predicted_sentiment_4_tweet can be "positive", "negative" or "neutral".
		For example:
		NA      15115101        positive  amoure wins oscar
		NA      15115101        neutral  who's a master brogramer now?		


------- SUBTASK C -------

  Use:
     perl format-check-semeval2015-task10-subtaskC.pl <INPUT_FILE> <PREDICTIONS_FILE>

  Example use:
     perl format-check-semeval2015-task10-subtaskC.pl SemEval2015-task10-test-CD-input.txt sample/SemEval2015-task10-test-C-candidate-good.txt
     perl format-check-semeval2015-task10-subtaskC.pl SemEval2015-task10-test-CD-input.txt sample/SemEval2015-task10-test-C-candidate-bad.txt

  Description:
     The format checker performs format checking for the predictions file given the input file.

		--Test Data--
		
		The format for the test input file is as follows:
		id1<TAB>id2<TAB>unknwn<TAB>topic<TAB>tweet_text
		
		for example:
		NA      T15113803      unknwn     aaron rodgers       I just cut a 25 second audio clip of Aaron Rodgers talking about Jordy Nelson's grandma's pies. Happy Thursday.
		NA      T15113805      unknwn     aaron rodgers       Tough loss for the Dolphins last Sunday in Miami against Aaron Rodgers &amp; the Green Bay Packers: 27-24.
		
		--System Output--
		We expect the following format for the predictions file:
		id1<TAB>id2<TAB>predicted_sentiment_4_topic<TAB>topic<TAB>tweet_text
		
		where tweet_text is optional,
		and predicted_sentiment_4_topic can be "positive", "negative" or "neutral".
		For example:
		NA      T15113803      positive     aaron rodgers       I just cut a 25 second audio clip of Aaron Rodgers talking about Jordy Nelson's grandma's pies. Happy Thursday.
		NA      T15113805      neutral     aaron rodgers       Tough loss for the Dolphins last Sunday in Miami against Aaron Rodgers &amp; the Green Bay Packers: 27-24.


------- SUBTASK D -------

  Use:
     perl format-check-semeval2015-task10-subtaskD.pl <INPUT_FILE> <PREDICTIONS_FILE>

  Example use:
     perl format-check-semeval2015-task10-subtaskD.pl SemEval2015-task10-test-D-input.txt sample/SemEval2015-task10-test-D-candidate-good.txt
     perl format-check-semeval2015-task10-subtaskD.pl SemEval2015-task10-test-D-input.txt sample/SemEval2015-task10-test-D-candidate-bad.txt
     perl format-check-semeval2015-task10-subtaskD.pl SemEval2015-task10-test-D-input.txt sample/SemEval2015-task10-test-D-candidate-bad2.txt

  Description:
     The format checker performs format checking for the predictions file given the input file.

		--Test Input--
		
		The format for the test inout file is as follows:
		topic<TAB>unknwn
		
		for example:
		aaron rodgers	unknwn
		aaron samuels	unknwn
		
		--System Output--
		We expect the following format for the predictions file:
		topic<TAB>predicted_POS_to_POS+NEG_ratio
		
		Where predicted_POS_to_POS+NEG_ratio should be a number between 0 and 1,
		representing a prediction for the positive/(positive+negative) ratio
		for the sentiment of the tweets for the given topic.
		
		For example:
		aaron rodgers	0.8125
		aaron samuels	0.176470588
