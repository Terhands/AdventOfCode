#!/usr/bin/perl

use warnings;

print "The file to load: ";
my $filename = <STDIN>;
chomp $filename;

open my $f_in, '<', $filename;
chomp(my @lines = <$f_in>);

my %digits_map = ();
my $num_digits = 0;
# intitializing our big ugly hash based on the size of binary digit we're dealing with
foreach my $char (split //, $lines[0]) {
	$digits_map{$num_digits} = 0;
	$num_digits++;
}
my $total_lines = @lines;

# print %digits_map."\n";

do {
	my @power_bits = shift(@lines);
	my $index = 0;
	foreach (split //, $lines[0]) {
		# print "$index\n";
		# print int($_)."\n";
		$digits_map{$index} += int($_);
		$index++;
	}
} until(!scalar @lines > 0);

my $index = 0;
my $gamma = "";
my $epsilon = "";
do{
	if ($digits_map{$index} > ($total_lines / 2)) {
		$gamma = $gamma."1";
		$epsilon = $epsilon."0";
	} else {
		$gamma = $gamma."0";
		$epsilon = $epsilon."1";
	}
	$index++;
} until($index == $num_digits);

my $converted_gamma = oct("0b" . $gamma);
my $converted_epsilon = oct("0b" . $epsilon);
print "Gamma: $gamma ($converted_gamma)\nEpsilon: $epsilon ($converted_epsilon)\nAnswer: ".($converted_gamma * $converted_epsilon)."\n";

close($f_in);