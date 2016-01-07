#!/usr/bin/perl
#
#  Author: Preslav Nakov
#  
#  Description: Generates input for Subtask B
#
#  Last modified: September 20, 2014
#
#

use warnings;
use strict;
use utf8;
binmode (STDIN,  ":utf8");
binmode (STDOUT, ":utf8");

########################
###   MAIN PROGRAM   ###
########################

for (my $counter = 1; <>; $counter++) {
	
	### 249298288367525888	T14114531	positive	i'm done writing code for the week! Looks like we've developed a good a** game for the show Revenge on ABC Sunday, Premeres 09/30/12 9pm
	die "Wrong file format!" if (!/^[^\t]+\t[^\t]+\t(positive|negative|neutral)\t(.+)$/);
	my ($label, $message) = ($1, $2);

	print "NA\t$counter\tunknwn\t$message\n";
}
