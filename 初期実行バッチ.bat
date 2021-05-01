@echo off
chcp 65001
set ps_command=`powershell "(Get-Date).AddDays(1).ToString('yyyy/MM/dd')"`
FOR /F "usebackq delims=" %%A IN (%ps_command%) DO set tomorrow=%%A

echo "nicoLiveReserver初期実行バッチ"

set /p JKCH="放送予約するチャンネル(ex.jk101):"

echo "%~dp0nicoLiveReserver.exe -ch %JKCH% -d %tomorrow% -t 04:00 -ho 144"

%~dp0nicoLiveReserver.exe -ch %JKCH% -d %tomorrow% -t 04:00 -ho 144

pause