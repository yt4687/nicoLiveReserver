@echo off
echo "nicoLiveReserver自動実行ツール"

set /p TIME="実行する時間(ex.09:00):"

schtasks /Create /SC Daily /TN nicoLiveReserver /TR "%~dp0nicoLiveReser.exe -a" /ST %TIME%

pause