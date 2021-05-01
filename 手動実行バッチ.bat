@echo off
chcp 65001

echo nicoLiveReserver初期実行バッチ

set /p JKCH="放送予約するチャンネル(ex.jk101):"
set /p YDATE="予約日(ex.2021/05/01):"
set /p YTIME="予約時刻(ex.11:00):"
set /p BTIME="放送時間(ex.24):"

%~dp0nicoLiveReserver.exe -ch %JKCH% -d %YDATE% -t %YTIME% -ho %BTIME%

pause