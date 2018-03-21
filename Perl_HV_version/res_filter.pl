#!/usr/bin/env perl
use strict;
use warnings;

unless ($ARGV[0] && $ARGV[1]) {die "provide res file and frag file at command line\n"}
unless (-e $ARGV[0]) {die "file not found $ARGV[0]\n"}
unless (-e $ARGV[1]) {die "file not found $ARGV[1]\n"}

my $taxids; {
	open FH,$ARGV[0];
	my $line = <FH>; #skip first line
	while ($line = <FH>) {
		my @a = split /\|/,$line;
		$taxids->{$a[2]} = 1;
	}
	close FH;
}
print "imported ",scalar(keys %$taxids)," valid taxa from res file\n";

my $cg = 0; my $cb = 0; # good/bad counters
open FH,$ARGV[1];
open GOOD,">".$ARGV[1].".filtered";
while (my $line = <FH>) {
	my @a = split /\|/,$line;
	if ($taxids->{$a[2]}) {
		print GOOD $line; ++$cg
	} else {
		++$cb
	}
}
close FH;
close GOOD;
print "filtered frag file: $cg retained, $cb removed\n";