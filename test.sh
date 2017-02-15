#!/usr/bin/bash
# simple test for snail.py
# as -xe is being used, dont echo messages just set random var to "messsage"


set -xe

test="++++    test1      ++++"
./snail.py -h &&
status="ok" || 
status"[ test 1 failed"
I=""

test="++++     test 1    ++++"
./snail.py --help &&
status="ok" ||
status="> test 1 failed"
echo""


test="++++     test 2    ++++"
./snail.py --test &&
status="ok" ||
status="> test 2 failed"
echo""


UTS=$(date +%s)

test="++++     test 3    ++++"
./snail.py --genlevel $UTS && 
status="ok" ||
status="> test 3 failed"
echo""


test="++++     test 3a    ++++"
[ -f $UTS ] &&
status="File exist" ||
status="> file does not exist" &&
status="> test 3a failed"
echo""


test="++++     test 4    ++++"
./snail.py --level $UTS &&
status="ok" ||
status="> test 4 failed"
echo""

rm $UTS


test="++++     test 4.a    ++++"
./snail.py --level"probably_not_existent" &&
status="ok" ||
status="> test 4.a failed"
echo""


test="++++     test 5    ++++"
./snail.py -h &&
status="ok" ||
status="> test 5 failed"
echo""
