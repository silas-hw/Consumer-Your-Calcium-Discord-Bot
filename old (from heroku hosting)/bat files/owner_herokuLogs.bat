@echo off
cd /d "D:\silas\discord bots\Consumer Your Calcium Help"
heroku logs -n 1500 -a calciumconsumer --source app --tail
pause
