#!/usr/bin/perl

use warnings;
use strict;

print "The file to load: ";
my $filename = <STDIN>;
chomp $filename;

open my $f_in, '<', $filename;
chomp(my @lines = <$f_in>);

my $length = @lines;
my $total_increases = 0;
my $index = 0;
my $current_value = int($lines[0]) + int($lines[1]) + int($lines[2]);


print $length;

do {

	
	my $next_value = int($lines[$index + 1]) + int($lines[$index + 2]) + int($lines[$index + 3]);
	# print "Current value: ".$current_value."\n";
	# print "Next value: ".$next_value."\n";

	$total_increases += 1 if ($current_value < $next_value);
	$current_value = $next_value;

	$index = $index + 1;
	# print $index."\n";

} while($index + 3 < $length);

print "Total Increases ".$total_increases."\n";

close($f_in);