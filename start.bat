@echo off
chcp 65001 >nul
echo =======================================
echo    🔮 도사운세 서버 시작 🔮
echo =======================================
echo.
echo 서버를 시작합니다...
echo 브라우저에서 http://localhost:2222 로 접속하세요
echo.
echo 종료하려면 Ctrl+C 를 누르세요
echo =======================================
echo.

python app.py

pause

