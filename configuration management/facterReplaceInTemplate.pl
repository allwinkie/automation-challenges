#!/usr/bin/perl -w
use Cwd;
use POSIX qw(strftime);
my $date = strftime "%m-%d-%Y", localtime;
print "$date\n";

$targetIP=$ARGV[0];

my $pwd = `pwd` ;
chomp($pwd);
$templateWithFile = $pwd.'/template.file';
$templateWithFileout = $pwd."/template".$targetIP."-".$date.".txt";

my $file=$templateWithFile;
my $outfilename = $templateWithFileout;

open( $fh, '>', $templateWithFileout) or die "Could not open file '$templateWithFileout' $!";
open(INFO, $file) or die("Could not open  file.");

$f1 = "sshpass -p 'testme' ssh ".$targetIP." -l simpletest -o StrictHostKeyChecking=no 'facter -p'";
$f2 =`$f1`;
#$search = "# widget_type (output from facter -p widget)";

foreach $line (<INFO>)  {
     if ($line =~ /# widget_type/)
	{
       print $fh $f2;
     }   
    elsif($line =~ /#/)
	{
#print  "caught another";
	}
   else
	{
   print $fh $line;
	} 

}
close(INFO);
close ($fh);
