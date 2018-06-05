@echo off

title PEP8 Test Repeater

set /p pep8test_name="Enter name of file to test for PEP8 compliance: "
set /p pep8test_time="Enter the number of seconds you would like between each repeat: "

:repeat
cls
echo -----------------------------------------------------------------
(pep8 %pep8test_name%.py)

timeout /t %pep8test_time%

goto :repeat