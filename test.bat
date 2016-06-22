@set PY=python
@set PROGRAMNAME=javimp.py
@set TESTFILE=TestJava.java
@set TESTFILEBACKUP=TestJava.java~
@set T1=ArrayList
@set T2=Ellipse2D LastOwnerException FileCacheImageInputStream
@set T3=Activity Bundle OnClickListener


@echo TESTING BASIC OUTPUT
@echo %PY% %PROGRAMNAME% %T1%
@echo.
@echo OUTPUT:
@%PY% %PROGRAMNAME% %T1% 2>nul
@echo.
@echo.
@echo TESTING MULTIPLE ARGUMENTS FROM STANDARD LIBRARY
@echo %PY% %PROGRAMNAME% %T2%
@echo.
@echo OUTPUT:
@%PY% %PROGRAMNAME% %T2% 2>nul
@echo.
@echo.
@echo TESTING OUTPUT FOR ANDROID API
@echo %PY% %PROGRAMNAME% %T3%
@echo.
@echo OUTPUT:
@%PY% %PROGRAMNAME% %T3% 2>nul
@echo.
@echo.
@echo TESTING -a OPTION
@echo %PY% %PROGRAMNAME% -a %T3%
@echo.
@echo OUTPUT:
@%PY% %PROGRAMNAME% -a %T3% 2>nul
@echo.
@echo.
@echo TESTING -c OPTION
@echo If successful, you should check the content of your clipboard afterwards
@echo.
@%PY% %PROGRAMNAME% -c %T2% 2>nul
@echo.
@echo.
@echo TESTING -o OPTION
@echo %PY% %PROGRAMNAME% -o %T3%
@echo.
@echo CONTENT AFTER:
@%PY% %PROGRAMNAME% -o %T3% 2>nul
@type import_statements.txt
@del import_statements.txt
@echo.
@echo.
@echo TESTING -i OPTION WITH %TESTFILE%
@echo %PY% %PROGRAMNAME% -i %TESTFILE%
@echo.
@echo CONTENT BEFORE:
@type %TESTFILE%
@echo.
@echo.
@echo CONTENT AFTER:
@%PY% %PROGRAMNAME% -i %TESTFILE% 2>nul
@type %TESTFILE%
@copy /Y %TESTFILEBACKUP% %TESTFILE% >nul
@echo.
@echo.
@echo.
@echo TESTING -a OPTION WITH OTHER OPTIONS
@echo.
@echo %PY% %PROGRAMNAME% -a -o %T3%
@echo.
@echo CONTENT AFTER:
@%PY% %PROGRAMNAME% -a -o %T3% 2>nul
@type import_statements.txt
@del import_statements.txt
@echo.
@echo.
@echo %PY% %PROGRAMNAME% -a -i %TESTFILE%
@echo.
@echo CONTENT BEFORE:
@type %TESTFILE%
@echo.
@echo.
@echo CONTENT AFTER:
@%PY% %PROGRAMNAME% -a -i %TESTFILE% 2>nul
@type %TESTFILE%
@copy /Y %TESTFILEBACKUP% %TESTFILE% >nul
@echo.
@echo.
@echo.
@echo ALL TESTS COMPLETED