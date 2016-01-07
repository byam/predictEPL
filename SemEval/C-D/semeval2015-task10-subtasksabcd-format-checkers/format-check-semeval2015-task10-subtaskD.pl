#!/usr/bin/perl
#
#  Authors: Preslav Nakov, Veselin Stoyanov
#  
#  Description: Checks the file format for subtask D of SemEval-2015 Task 10.
#
#  Version: 1.0
#
#  Last modified: December 20, 2014
#
#  Use:
#     perl format-check-semeval2015-task10-subtaskD.pl <INPUT_FILE> <PREDICTIONS_FILE>
#
#  Example use:
#     perl format-check-semeval2015-task10-subtaskD.pl SemEval2015-task10-test-D-input.txt sample/SemEval2015-task10-test-D-candidate-good.txt
#     perl format-check-semeval2015-task10-subtaskD.pl SemEval2015-task10-test-D-input.txt sample/SemEval2015-task10-test-D-candidate-bad.txt
#     perl format-check-semeval2015-task10-subtaskD.pl SemEval2015-task10-test-D-input.txt sample/SemEval2015-task10-test-D-candidate-bad2.txt
#
#  Description:
#     The format checker performs format checking for the predictions file given the input file.
#
#		--Test Input--
#		
#		The format for the test inout file is as follows:
#		topic<TAB>unknwn
#		
#		for example:
#		aaron rodgers	unknwn
#		aaron samuels	unknwn
#		
#		--System Output--
#		We expect the following format for the predictions file:
#		topic<TAB>predicted_POS_to_POS+NEG_ratio
#		
#		Where predicted_POS_to_POS+NEG_ratio should be a number between 0 and 1,
#		representing a prediction for the positive/(positive+negative) ratio
#		for the sentiment of the tweets for the given topic.
#		
#		For example:
#		aaron rodgers	0.8125
#		aaron samuels	0.176470588
#	


use warnings;
use strict;
use utf8;


########################
###   MAIN PROGRAM   ###
########################

### 1. Check the parameters
die "Usage: $0 <INPUT_FILE> <PREDICTIONS_FILE>\nThe input file should be SemEval2015-task10-test-D-input.txt\n" if ($#ARGV != 1);
my $INPUT_FILE       = $ARGV[0];
my $PREDICTIONS_FILE = $ARGV[1];


### 1. Read the files and get the statsitics
open INPUT,       '<:encoding(UTF-8)', $INPUT_FILE       or die "Cannot open $INPUT_FILE";
open PREDICTIONS, '<:encoding(UTF-8)', $PREDICTIONS_FILE or die "Cannot open $PREDICTIONS_FILE";

for (; <INPUT>; ) {
	s/^[ \t]+//;
	s/[ \t\n\r]+$//;

 	### 1.1	. Check the input file format
	#aaron rodgers	unknwn
	die "Wrong input file format!" if (!/([^\t]+)\tunknwn/);
	my $ttopic = $1;
	

	### 1.2. Check the predictions file format
	#aaron rodgers	0.8125
	$_ = <PREDICTIONS>;
	die "Wrong predictions file format!" if (!/([^\t]+)\t([0-9\.]+)/);
	my ($ptopic, $pscore) = ($1, $2);

	### 1.3. Check for mismatches in the topics
	die "IDs mismatch: expected '$ttopic', but found '$ptopic'" if ($ptopic ne $ttopic);

	### 1.4. Make sure the score is in [0;1]
	die "The score should be in [0;1]: found a value of $pscore" if (($pscore < 0.0) || ($pscore > 1.0));

}

close(INPUT) or die;
close(PREDICTIONS) or die;

print "The predictions file format looks OK.\n";
