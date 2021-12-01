#!/usr/bin/perl

use warnings;
use strict;

print "The file to load: ";
my $filename = <STDIN>;
chomp $filename;

open my $f_in, '<', $filename;
chomp(my @lines = <$f_in>);

my $total_increases = 0;
my $current_value = int($lines[0]);

do {
	my $next_value = int(shift(@lines));
	$total_increases += 1 if ($current_value < $next_value);
	$current_value = $next_value;
} until(!scalar @lines > 0);

print "Total Increases ".$total_increases;
print "\n";

close($f_in);