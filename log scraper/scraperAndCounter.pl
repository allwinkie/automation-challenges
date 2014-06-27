#!/usr/bin/perl
use strict;
use warnings;

my %count;
my $file = shift or die "usage: $0 fILE\n";

open my $fh, '<', $file or die "couldnt open '$file' $!";

while ( my $line = <$fh>) {
#        print $line;
	chomp $line;
        my @section = split / /, $line;
      #  print @section[0]."\n";
        my $ipaddress = $section[0];
        foreach my $str ( split /\s+/, $ipaddress) {
	$count{$str}++;
        }
}

foreach my $str (sort keys %count) {
printf "%-31s %s\n", $str, $count{$str};
}
