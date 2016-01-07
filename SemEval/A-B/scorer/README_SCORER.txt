Scorer for SemEval-2013 Task #2: Sentiment Analysis on Twitter

Task organizers:
Theresa Wilson   Johns Hopkins University, HLTCOE
Zornitsa Kozareva  University of Southern California, ISI
Preslav Nakov  Qatar Computing Research Institute, Qatar Foundation
Sara Rosenthal  Columbia University
Veselin Stoyanov Johns Hopkins University 
Alan Ritter  University of Washington

Scorer written by Veselin Stoyanov.

This software is released under a Creative Commons Attribution 3.0 Unported License (http://creativecommons.org/licenses/by/3.0/).

Version 1.0: March 6, 2013.

DIRECTORY CONTENT

The following files can be found in the directory:

scorer.py --> the official verifier and scorer for taskX
taskX.test --> an example of the format in which the test data is released
taskX.pred --> an example system response file produced by a (hypothetical) task participant
taskX.gs --> an example of the gold standard format

USAGE

To verify the format of a submission file (for task A or B respectively) use the following command:
python scorer.py A taskA.pred
python scorer.py B taskB.pred

To score the made up example response use:
python scorer.py A taskA.pred taskA.gs
python scorer.py B taskB.pred taskB.gs

FORMATS

-----------------------TASK A-----------------------------------------
--Test Data--

The format for the test file is as follows:
id1<TAB>id2<TAB>start_token<TAB>end_token<TAB>unknwn<TAB>tweet_text

for example:
418381654813081609      15115101        2       2       unknwn  amoure wins oscar
418381654813081610      15115101        3       4       unknwn  who's a master brogramer now?

--System Output--
We expect the following format for the prediction file is:
id1<TAB>id2<TAB>start_token<TAB>end_token<TAB>pred_class<TAB>tweet_text

where the text field is optional. For example:
418381654813081609      15115101        2       2       positive  amoure wins oscar
418381654813081610      15115101        3       4       neutral  who's a master brogramer now?


--Gold Standard--
The gold standard following the same format as the system output above 

-----------------------TASK B-----------------------------------------
(Task B uses the same format as Task A, but it excludes the start and end token fields.)
--Test Data--

The format for the test file is as follows:
id1<TAB>id2<TAB>unknwn<TAB>tweet_text

for example:
418381654813081609      15115101       unknwn  amoure wins oscar
418381654813081610      15115101       unknwn  who's a master brogramer now?

--System Output--
We expect the following format for the prediction file is:
id1<TAB>id2<TAB>pred_class<TAB>tweet_text

where the text field is optional. For example:
418381654813081609      15115101        positive  amoure wins oscar
418381654813081610      15115101        neutral  who's a master brogramer now?


--Gold Standard--
The gold standard following the same format as the system output above 

