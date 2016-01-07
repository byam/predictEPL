#!/usr/bin/perl
#
#  Authors: Preslav Nakov, Veselin Stoyanov
#  
#  Description: Checks the file format for subtask C of SemEval-2015 Task 10.
#
#  Version: 1.0
#
#  Last modified: December 20, 2014
#
#  Use:
#     perl format-check-semeval2015-task10-subtaskC.pl <INPUT_FILE> <PREDICTIONS_FILE>
#
#  Example use:
#     perl format-check-semeval2015-task10-subtaskC.pl SemEval2015-task10-test-CD-input.txt sample/SemEval2015-task10-test-C-candidate-good.txt
#     perl format-check-semeval2015-task10-subtaskC.pl SemEval2015-task10-test-CD-input.txt sample/SemEval2015-task10-test-C-candidate-bad.txt
#
#  Description:
#     The format checker performs format checking for the predictions file given the input file.
#
#		--Test Data--
#		
#		The format for the test input file is as follows:
#		id1<TAB>id2<TAB>unknwn<TAB>topic<TAB>tweet_text
#		
#		for example:
#		NA      T15113803      unknwn     aaron rodgers       I just cut a 25 second audio clip of Aaron Rodgers talking about Jordy Nelson's grandma's pies. Happy Thursday.
#		NA      T15113805      unknwn     aaron rodgers       Tough loss for the Dolphins last Sunday in Miami against Aaron Rodgers &amp; the Green Bay Packers: 27-24.
#		
#		--System Output--
#		We expect the following format for the predictions file:
#		id1<TAB>id2<TAB>predicted_sentiment_4_topic<TAB>topic<TAB>tweet_text
#		
#		where tweet_text is optional,
#		and predicted_sentiment_4_topic can be "positive", "negative" or "neutral".
#		For example:
#		NA      T15113803      positive     aaron rodgers       I just cut a 25 second audio clip of Aaron Rodgers talking about Jordy Nelson's grandma's pies. Happy Thursday.
#		NA      T15113805      neutral     aaron rodgers       Tough loss for the Dolphins last Sunday in Miami against Aaron Rodgers &amp; the Green Bay Packers: 27-24.
#		

use warnings;
use strict;
use utf8;


########################
###   MAIN PROGRAM   ###
########################

### 1. Check the parameters
die "Usage: $0 <INPUT_FILE> <PREDICTIONS_FILE>\nThe input file should be SemEval2015-task10-test-CD-input.txt\n" if ($#ARGV != 1);
my $INPUT_FILE       = $ARGV[0];
my $PREDICTIONS_FILE = $ARGV[1];


### 1. Read the files and get the statsitics
open INPUT,       '<:encoding(UTF-8)', $INPUT_FILE       or die "Cannot open $INPUT_FILE";
open PREDICTIONS, '<:encoding(UTF-8)', $PREDICTIONS_FILE or die "Cannot open $PREDICTIONS_FILE";

for (; <INPUT>; ) {
	s/[ \t\n\r]+$//;

 	### 1.1	. Check the input file format
	#NA      T15113803       unknwn  aaron rodgers   I just cut a 25 second audio clip of Aaron Rodgers.
	die "Wrong input file format!" if (!/^NA\t([^\t]+)\tunknwn\t([^\t]+)\t[^\t]+$/);
	my ($tid, $ttopic) = ($1, $2);
	
	### 1.2. Check the predictions file format
	#NA      T15113803       negative  aaron rodgers   I just cut a 25 second audio clip of Aaron Rodgers.
	$_ = <PREDICTIONS>;
	s/[\n\r]+$//;
	die "Wrong predictions file format!" if (!/^NA\t([^\t]+)\t([^\t]+)\t([^\t]+)(\t[^\t]+)?$/);
	my ($pid, $plabel, $ptopic) = ($1, $2, $3);

	### 1.3. Check for ID mismatches
	die "IDs mismatch: expected $tid, but found $pid" if ($pid ne $tid);

	### 1.4. Check for topic mismatches
	die "Topic mismatch: expected '$ttopic', but found '$ptopic'" if ($ttopic ne $ptopic);

	### 1.5. Check for label value
	die "Wrong label value: $plabel" if ($plabel !~ /^(positive|negative|neutral)$/);
}

close(INPUT) or die;
close(PREDICTIONS) or die;

print "The predictions file format looks OK.\n";
