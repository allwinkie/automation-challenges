$CT="Content-Type:application\/json";
$errorTotal=0;
$successTotal=0;
$loop1=0;
# first two should pass , the last four should fail
@wordlist = ('tellme','BiGb0oDy','!@#$%^&*','but crack','DROP TABLE','ALL CAPS'); 
while ( $loop1 <= 6)
{
$RESTSTRING="curl -X PUT -H $CT -d '{\"word\":\"$wordlist[$loop1]\"}' http://localhost:8080/word/WORDNAME";
chomp($RESTSTRING);
print "$RESTSTRING\n";
$data=`$RESTSTRING`;
print $data;

if ($data ){ 
    print " error statement $data\n\n";
    if ($loop1 >= 2)
           {
        $successTotal++
            }
          }
else
{ print " didn't error\n\n";
 if ( $loop <= 1){
           $successTotal++; 
		   }
              };

       if (($loop <= 3)&&($data =~ /one word/)) {
        print "*******************************  multiword error caught \n";
                   };

$loop1++;
print " loop number is $loop1 \n";
}
;
print " section 1 - check for single words\n ";
print " two positive and four negative tests - total of 6 ";
print " $successTotal are the number of passes\n";
print "**************************************************************************************************************************";
print "***************************************************** END SECTION 1 ******************************************************";
print "**************************************************************************************************************************";

 

#$CT="Content-Type:application\/json";
$errorTotal=0;
$successTotal=0;
$loop1=0;
# first two should pass return a value pair , the last four should not
@wordlist = ('tellme','BiGb0oDy','!@#$%^&*','but crack','DROP TABLE','ALL CAPS'); 
while ( $loop1 <= 6)
{
$RESTSTRING="curl -X GET http://localhost:8080/words/@wordlist[$loop1]";
chomp($RESTSTRING);
print "$RESTSTRING\n";
$data=`$RESTSTRING`;
print $data;
print "@wordlist[$loop1] the value to get checked $loop1 \n";
if ($loop1 == 0) 
	{
	if($data =~ /tellme/)
		{
	$successTotal++;
        print "$wordlist[$loop1] succes in loop $loop1 \n";
		}
	};
 
if ($loop1 == 1) 
	{
	if($data =~ /\"BiGb0oDy\": 0/)
		{
	$successTotal++;
       print "$wordlist[$loop1] succes in loop $loop1 \n";
		}
	};

if ($loop1 == 2) 
	{
	if($data =~ /!@/)
		{
	$successTotal++;
       print "$wordlist[$loop1] succes in loop $loop1 \n";
		}
	};
 
if ($loop1 == 3) 
	{
	if($data =~ /but/)
		{
	$successTotal++;
       print "$wordlist[$loop1] succes in loop $loop1 \n";
		}
	};

if ($loop1 == 4) 
	{
	if($data =~ /DROP/)
		{
	$successTotal++;
	       print "$wordlist[$loop1] succes in loop $loop1 \n";
		}
	};
if ($loop1 == 5) 
	{
	if($data =~ /ALL/)
		{
	$successTotal++;
	       print "$wordlist[$loop1] succes in loop $loop1 \n";
		}
	};
if (($loop == 6)&&($data =~ /WORDNAME/)&&($data =~ /tellme/)) 
        {
        print "*******************************  dumps more than one word  \n";
        $successTotal++;
	       print "$wordlist[$loop1] succes in loop $loop1 \n";
        };
print " loop number is $loop1 \n";
$loop1++;

}
;
print " section 1 - check for single words\n ";
print " two positive and four negative tests - total of 6 ";
print " $successTotal are the number of passes\n";
print "**************************************************************************************************************************";
print "***************************************************** END SECTION 2 ******************************************************";
print "**************************************************************************************************************************";


