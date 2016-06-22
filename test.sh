#!/bin/sh

PY=python
PROGRAMNAME=javimp.py
TESTFILE=TestJava.java
TESTFILEBACKUP=TestJava.java~
T1=ArrayList
T2="Ellipse2D LastOwnerException FileCacheImageInputStream"
T3="Activity Bundle OnClickListener"
HL="highlight -O ansi"
PYGM="pygmentize -g"

printf "\nTESTING BASIC OUTPUT \n"
printf "${PY} ${PROGRAMNAME} ${T1}\n\n"
printf "OUTPUT: \n"
${PY} ${PROGRAMNAME} ${T1} 2>/dev/null
printf "\n\nTESTING MULTIPLE ARGUMENTS FROM STANDARD LIBRARY \n"
printf "${PY} ${PROGRAMNAME} ${T2} \n\n"
printf "OUTPUT: \n"
${PY} ${PROGRAMNAME} ${T2} 2>/dev/null
printf "\n\nTESTING OUTPUT FOR ANDROID API \n"
printf "${PY} ${PROGRAMNAME} ${T3} \n\n"
printf "OUTPUT: \n"
${PY} ${PROGRAMNAME} ${T3} 2>/dev/null
printf "\n\nTESTING -a OPTION \n"
printf "${PY} ${PROGRAMNAME} -a ${T3} \n\n"
printf "OUTPUT: \n"
${PY} ${PROGRAMNAME} -a ${T3} 2>/dev/null
printf "\n\nTESTING -c OPTION \n"
printf "If successful, you should check the content of your clipboard afterwards \n\n"
${PY} ${PROGRAMNAME} -c ${T2} 2>/dev/null
printf "\n\nTESTING -o OPTION \n"
printf "${PY} ${PROGRAMNAME} -o ${T3} \n\n"
printf "CONTENT AFTER: \n"
${PY} ${PROGRAMNAME} -o ${T3} 2>/dev/null
cat import_statements.txt
rm import_statements.txt
printf "\n\nTESTING -i OPTION WITH ${TESTFILE} \n"
printf "${PY} ${PROGRAMNAME} -i ${TESTFILE} \n\n"
printf "CONTENT BEFORE: \n"
${PYGM} ${TESTFILE} || ${HL} ${TESTFILE} || cat ${TESTFILE}
printf "\nCONTENT AFTER: \n"
${PY} ${PROGRAMNAME} -i ${TESTFILE} 2>/dev/null
${PYGM} ${TESTFILE} || ${HL} ${TESTFILE} || cat ${TESTFILE}
cp ${TESTFILEBACKUP} ${TESTFILE}
printf "\n\nTESTING -a OPTION WITH OTHER OPTIONS \n\n"
printf "${PY} ${PROGRAMNAME} -a -o ${T3} \n\n"
printf "CONTENT AFTER: \n"
${PY} ${PROGRAMNAME} -a -o ${T3} 2>/dev/null
cat import_statements.txt
rm import_statements.txt
printf "\n\n${PY} ${PROGRAMNAME} -a -i ${TESTFILE} \n\n"
printf "CONTENT BEFORE: \n"
${PYGM} ${TESTFILE} || ${HL} ${TESTFILE} || cat ${TESTFILE}
printf "\nCONTENT AFTER: \n"
${PY} ${PROGRAMNAME} -a -i ${TESTFILE} 2>/dev/null
${PYGM} ${TESTFILE} || ${HL} ${TESTFILE} || cat ${TESTFILE}
cp ${TESTFILEBACKUP} ${TESTFILE}
printf "\n\nALL TESTS COMPLETED\n\n"
