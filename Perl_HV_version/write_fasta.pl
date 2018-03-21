#!/usr/bin/env perl
use strict;
use warnings;

unless ($ARGV[0]) {die "provide fully processed frag file at command line\n"}

my $outdir = $ARGV[0].".fasta_files";
if (-e $outdir) {die "error -- output directory $outdir already exist -- remove and try again\n";}
mkdir($outdir);

my $output;
my $species_counters;
open FH,$ARGV[0];
while (my $line = <FH>) {
	my $a = interpret_line($line);
	if (defined $species_counters->{$a->{species}}) {++$species_counters->{$a->{species}}} else {$species_counters->{$a->{species}} = 1}
	$output->{$a->{species}} .= ">seq".$species_counters->{$a->{species}}."|".$a->{read}."\n".$a->{seq}."\n";
}
close FH;

foreach my $species (keys %$output) {
	open OUT,">>$outdir\/".$species.".fa";
	print OUT $output->{$species};
	close OUT;
}

sub interpret_line {
	my $line = shift;
	my $out;
	$line =~ s/[\n\r]//g;
	my @a = split /\t/,$line;
	$out->{read} = pop @a;
	$out->{species} = $a[5];
	$out->{seq} = $a[0];
	return $out
}

