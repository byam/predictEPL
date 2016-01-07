#!/usr/bin/perl
#
#  Authors: Preslav Nakov, Veselin Stoyanov
#  
#  Description: Checks the file format for subtask B of SemEval-2015 Task 10.
#
#  Version: 1.0
#
#  Last modified: December 20, 2014
#
#  Use:
#     perl format-check-semeval2015-task10-subtaskB.pl <INPUT_FILE> <PREDICTIONS_FILE>
#
#  Example use:
#
#     perl format-check-semeval2015-task10-subtaskB.pl SemEval2015-task10-test-B-input.txt sample/SemEval2015-task10-test-B-candidate-good.txt
#     perl format-check-semeval2015-task10-subtaskB.pl SemEval2015-task10-test-B-input.txt sample/SemEval2015-task10-test-B-candidate-bad.txt
#
#     perl format-check-semeval2015-task10-subtaskB.pl SemEval2015-task10-test-B-input-progress.txt sample/SemEval2015-task10-test-B-candidate-progress-good.txt
#     perl format-check-semeval2015-task10-subtaskB.pl SemEval2015-task10-test-B-input-progress.txt sample/SemEval2015-task10-test-B-candidate-progress-bad.txt
#
#  Description:
#     The format checker performs format checking for the predictions file given the input file.
##		
#		The format for the test input file is as follows:
#		id1<TAB>id2<TAB>unknwn<TAB>tweet_text
#		
#		for example:
#		NA      15115101       unknwn  amoure wins oscar
#		NA      15115101       unknwn  who's a master brogramer now?
#		
#		--System Output--
#		We expect the following format for the prediction file:
#		id1<TAB>id2<TAB>predicted_sentiment_4_tweet<TAB>tweet_text
#		
#		where tweet_text is optional,
#		and predicted_sentiment_4_tweet can be "positive", "negative" or "neutral".
#		For example:
#		NA      15115101        positive  amoure wins oscar
#		NA      15115101        neutral  who's a master brogramer now?#		


use warnings;
use strict;
use utf8;


########################
###   MAIN PROGRAM   ###
########################

### 1. Check the parameters
die "Usage: $0 <INPUT_FILE> <PREDICTIONS_FILE>\nThe input file should be SemEval2015-task10-test-B-input.txt\n" if ($#ARGV != 1);
my $INPUT_FILE       = $ARGV[0];
my $PREDICTIONS_FILE = $ARGV[1];


### 1. Read the files and get the statsitics
open INPUT,       '<:encoding(UTF-8)', $INPUT_FILE       or die "Cannot open $INPUT_FILE";
open PREDICTIONS, '<:encoding(UTF-8)', $PREDICTIONS_FILE or die "Cannot open $PREDICTIONS_FILE";

for (; <INPUT>; ) {
	s/[ \t\n\r]+$//;

 	### 1.1	. Check the input file format
	#NA      T15113803       unknwn  I just cut a 25 second audio clip of Aaron Rodgers.
	die "Wrong input file format!" if (!/^NA\t([^\t]+)\tunknwn\t[^\t]+$/);
	my $tid = $1;
	
	### 1.2. Check the predictions file format
	#NA      T15113803       negative  I just cut a 25 second audio clip of Aaron Rodgers.
	$_ = <PREDICTIONS>;
	s/[\n\r]+$//;
	die "Wrong predictions file format!" if (!/^NA\t([^\t]+)\t([^\t]+)(\t[^\t]+)?$/);
	my ($pid, $plabel) = ($1, $2);

	### 1.3. Check for ID mismatches
	die "IDs mismatch: expected $tid, but found $pid" if ($pid ne $tid);

	### 1.4. Check the label value
	die "Wrong label value: $plabel" if ($plabel !~ /^(positive|negative|neutral)$/);
}

close(INPUT) or die;
close(PREDICTIONS) or die;

print "The predictions file format looks OK.\n";
