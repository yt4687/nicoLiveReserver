@echo off
echo "nicoLiveReserver�������s�c�[��"

set /p TIME="���s���鎞��(ex.09:00):"

schtasks /Create /SC Daily /TN nicoLiveReserver /TR "%~dp0nicoLiveReser.exe -a" /ST %TIME%

pause