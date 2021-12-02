#!/usr/bin/perl

use warnings;
use strict;

print "The file to load: ";
my $filename = <STDIN>;
chomp $filename;

my $aim = 0;
my $depth = 0;
my $distance = 0;
my @directions;

open my $f_in, '<', $filename;
chomp(my @lines = <$f_in>);

do {
	@directions = split(' ', shift(@lines));

	if (($directions[0] eq "forward") == 1) {
		$distance += int($directions[1]);
		$depth += int($directions[1]) * $aim;
	} elsif (($directions[0] eq "up") == 1) {
		$aim -= int($directions[1]);
	} elsif (($directions[0] eq "down") == 1) {
		$aim += int($directions[1]);
	} else {
		print "Oh no...";
	}
} until(!scalar @lines > 0);

print "Total Distance: ".$distance."\n";
print "Total Depth: ".$depth."\n";
print "Product: ".($depth * $distance)."\n";

close($f_in);