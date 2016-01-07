#!/usr/bin/perl
#
#  Author: Preslav Nakov
#  
#  Description: Generates input for Subtask A
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
	
	### 269437682537594881	T14115502	25	26	positive	@GMA My daughter @jordynking17 will be 14 on December 17th! We r going to see Buddy @ The Kirby Center in WB on December 14th. So excited!
	die "Wrong file format!" if (!/^[^\t]+\t[^\t]+\t([0-9]+\t[0-9]+)\t(positive|negative|neutral)\t(.+)$/);
	my ($spans, $label, $message) = ($1, $2, $3);

	print "NA\t$counter\t$spans\tunknwn\t$message\n";
}
