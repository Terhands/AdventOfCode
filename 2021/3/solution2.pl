#!/usr/bin/perl

use warnings;
use strict;

print "The file to load: ";
my $filename = <STDIN>;
chomp $filename;

open my $f_in, '<', $filename;
chomp(my @lines = <$f_in>);

close($f_in);

# my %digits_map = ();
# my $num_digits = 0;
# # intitializing our big ugly hash based on the size of binary digit we're dealing with
# foreach my $char (split //, $lines[0]) {
# 	$digits_map{$num_digits} = 0;
# 	$num_digits++;
# }

# load up our initial lists
my @popular = @lines;
my @unpopular = @lines;

my $popular_string = "";
my $current_digit = 0;
do {
	my $popular_sum = 0;
	foreach (@popular) {
		my @chars = (split //, $_);
		$popular_sum += int($chars[$current_digit]);
	}

	my $check_value = 0;
	if ($popular_sum >= (@popular / 2)) {
		$check_value = 1;
	}
	$popular_string = $popular_string.$check_value;

	# print "Popular sum: $popular_sum\n";
	# print $current_digit."\n";
	# print "@popular\n--------\n";
	# print "Check: $check_value\n";
	# print "Current popular: $popular_string\n";


	@popular = grep { $_ =~ "^$popular_string" } @popular;
	$current_digit++;

	# print "@popular\n";

} until(scalar @popular == 1);

my $unpopular_string = "";
$current_digit = 0;
do {
	my $unpopular_sum = 0;
	foreach (@unpopular) {
		my @chars = (split //, $_);
		$unpopular_sum += int($chars[$current_digit]);
	}

	my $check_value = 0;
	if ($unpopular_sum < (@unpopular / 2)) {
		$check_value = 1;
	}
	$unpopular_string = $unpopular_string.$check_value;

	# print "Popular sum: $popular_sum\n";
	# print $current_digit."\n";
	# print "@popular\n--------\n";
	# print "Check: $check_value\n";
	# print "Current popular: $popular_string\n";


	@unpopular = grep { $_ =~ "^$unpopular_string" } @unpopular;
	$current_digit++;

	# print "@popular\n";

} until(scalar @unpopular == 1);

my $converted_popular = oct("0b" . $popular[0]);
my $converted_unpopular = oct("0b" . $unpopular[0]);
print "Popular: $popular[0] ($converted_popular)"."\n";
print "Unpopular: $unpopular[0] ($converted_unpopular)"."\n";
print "Total: ".($converted_popular * $converted_unpopular)."\n";



# my $unpopular_starting_digit = 1;





# do {
# 	my @power_bits = shift(@lines);
# 	my $index = 0;
# 	foreach (split //, $lines[0]) {
# 		# print "$index\n";
# 		# print int($_)."\n";
# 		$digits_map{$index} += int($_);
# 		$index++;
# 	}
# } until(!scalar @lines > 0);

# my $index = 0;
# my $gamma = "";
# my $epsilon = "";
# do{
# 	if ($digits_map{$index} > ($total_lines / 2)) {
# 		$gamma = $gamma."1";
# 		$epsilon = $epsilon."0";
# 	} else {
# 		$gamma = $gamma."0";
# 		$epsilon = $epsilon."1";
# 	}
# 	$index++;
# } until($index == $num_digits);

# my $converted_gamma = oct("0b" . $gamma);
# my $converted_epsilon = oct("0b" . $epsilon);
# print "Gamma: $gamma ($converted_gamma)\nEpsilon: $epsilon ($converted_epsilon)\nAnswer: ".($converted_gamma * $converted_epsilon)."\n";

