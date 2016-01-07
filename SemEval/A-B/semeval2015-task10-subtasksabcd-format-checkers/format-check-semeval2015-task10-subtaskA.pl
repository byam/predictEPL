#!/usr/bin/perl
#
#  Authors: Preslav Nakov, Veselin Stoyanov
#  
#  Description: Checks the file format for subtask A of SemEval-2015 Task 10.
#
#  Version: 1.0
#
#  Last modified: December 20, 2014
#
#  Use:
#     perl format-check-semeval2015-task10-subtaskA.pl <INPUT_FILE> <PREDICTIONS_FILE>
#
#  Example use:
#
#     perl format-check-semeval2015-task10-subtaskA.pl SemEval2015-task10-test-A-input.txt sample/SemEval2015-task10-test-A-candidate-good.txt
#     perl format-check-semeval2015-task10-subtaskA.pl SemEval2015-task10-test-A-input.txt sample/SemEval2015-task10-test-A-candidate-bad.txt
#
#     perl format-check-semeval2015-task10-subtaskA.pl SemEval2015-task10-test-A-input-progress.txt sample/SemEval2015-task10-test-A-candidate-progress-good.txt
#     perl format-check-semeval2015-task10-subtaskA.pl SemEval2015-task10-test-A-input-progress.txt sample/SemEval2015-task10-test-A-candidate-progress-bad.txt
#
#  Description:
#     The format checker performs format checking for the predictions file given the input file.
#		
#		The format for the test input file is as follows:
#		id1<TAB>id2<TAB>start_token<TAB>end_token<TAB>unknwn<TAB>tweet_text
#		
#		for example:
#		NA      15115101        2       2       unknwn  amoure wins oscar
#		NA      15115101        3       4       unknwn  who's a master brogramer now?
#		
#		--System Output--
#		We expect the following format for the prediction file:
#		id1<TAB>id2<TAB>start_token<TAB>end_token<TAB>predicted_sentiment_4_phrase<TAB>tweet_text
#		
#		where tweet_text is optional,
#		and predicted_sentiment_4_phrase can be "positive", "negative" or "neutral".
#		For example:
#		NA      15115101        2       2       positive  amoure wins oscar
#		NA      15115101        3       4       neutral  who's a master brogramer now?
#		


use warnings;
use strict;
use utf8;


########################
###   MAIN PROGRAM   ###
########################

### 1. Check the parameters
die "Usage: $0 <INPUT_FILE> <PREDICTIONS_FILE>\nThe input file should be SemEval2015-task10-test-A-input.txt\n" if ($#ARGV != 1);
my $INPUT_FILE       = $ARGV[0];
my $PREDICTIONS_FILE = $ARGV[1];


### 1. Read the files and get the statsitics
open INPUT,       '<:encoding(UTF-8)', $INPUT_FILE       or die "Cannot open $INPUT_FILE";
open PREDICTIONS, '<:encoding(UTF-8)', $PREDICTIONS_FILE or die "Cannot open $PREDICTIONS_FILE";

for (; <INPUT>; ) {
	s/[ \t\n\r]+$//;

 	### 1.1	. Check the input file format
	# NA      15115101        2       2       unknwn  amoure wins oscar
	die "Wrong input file format!" if (!/^NA\t([^\t]+)\t(\d+)\t(\d+)\tunknwn\t[^\t]+$/);
	my ($tid, $tbegin, $tend) = ($1, $2, $3);
	
	### 1.2. Check the predictions file format
	# NA      15115101        2       2       positive  amoure wins oscar
	$_ = <PREDICTIONS>;
	s/[\n\r]+$//;
	die "Wrong predictions file format!" if (!/^NA\t([^\t]+)\t(\d+)\t(\d+)\t([^\t]+)(\t[^\t]+)?$/);
	my ($pid, $pbegin, $pend, $plabel) = ($1, $2, $3, $4);

	### 1.3. Check for ID mismatches
	die "IDs mismatch: expected $tid, but found $pid" if ($pid ne $tid);

	### 1.4. Check for position mismatches
	die "Positions mismatch: expected [$tbegin, $tend], but found [$pbegin, $pend]" if (($tbegin != $pbegin) || ($tend != $pend));

	### 1.5. Check the label value
	die "Wrong label value: $plabel" if ($plabel !~ /^(positive|negative|neutral)$/);
}

close(INPUT) or die;
close(PREDICTIONS) or die;

print "The predictions file format looks OK.\n";
