#!/usr/bin/env perl
use strict;
use warnings;

unless ($ARGV[0]) {die "provide sorted frag file at command line\n"}


open IN,$ARGV[0];
open GOOD,">".$ARGV[0].".good";
open BAD,">".$ARGV[0].".bad";

my $a = next_2_lines(); 
process($a);

sub process {
	my $two_lines = shift;
	unless ($two_lines->[0]) {exit;} # exits if no more data fed in
	unless ($two_lines->[1]) { # process last line of file fed in
		print GOOD $two_lines->[0]; 
		exit;
	}  
	my ($reads,$species) = interpret_lines($two_lines);
	if ($reads->[0] eq $reads->[1]) {
		if ($species->[0] eq $species->[1]) {
			print GOOD "",join("\n",@$two_lines),"\n";
		} else {
			print BAD "",join("\n",@$two_lines),"\n";
		}
		process(next_2_lines());
	} else {
		print GOOD $two_lines->[0],"\n";
		process(shift_1_line($two_lines));
	}
}

sub next_2_lines {
	my $a;
	$a->[0] = <IN>;
	$a->[1] = <IN>;
	return $a;
}

sub shift_1_line {
	my $a = shift; 
	$a->[0] = $a->[1];
	$a->[1] = <IN>;
	return $a;
}

sub interpret_lines {
	my $lines = shift;
	my ($reads,$species);
	foreach my $line (@$lines) {
		$line =~ s/[\n\r]//g;
		my @a = split /\t/,$line;
		push @$reads,pop @a;
		my @b = split /\|/,$line;
		push @$species,$b[2];
	}
	return ($reads,$species);
}
