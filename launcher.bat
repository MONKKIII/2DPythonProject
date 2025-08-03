@echo off
echo ===============================
echo   RPG Multijoueur - Launcher
echo ===============================
echo.
echo Que voulez-vous faire ?
echo 1. Demarrer le serveur
echo 2. Lancer un client (localhost)
echo 3. Lancer un client (IP personnalisee)
echo 4. Quitter
echo.

set /p choice="Votre choix (1-4): "

if "%choice%"=="1" (
    echo.
    echo Demarrage du serveur...
    echo Appuyez sur Ctrl+C pour arreter le serveur
    echo.
    "%~dp0.venv\Scripts\python.exe" "%~dp0server.py"
    pause
) else if "%choice%"=="2" (
    echo.
    echo Lancement du client (connexion locale)...
    echo.
    "%~dp0.venv\Scripts\python.exe" "%~dp0client.py"
    pause
) else if "%choice%"=="3" (
    echo.
    set /p server_ip="Entrez l'adresse IP du serveur: "
    echo.
    echo Connexion au serveur !server_ip!...
    echo.
    "%~dp0.venv\Scripts\python.exe" "%~dp0client.py" !server_ip!
    pause
) else if "%choice%"=="4" (
    echo Au revoir !
    exit /b
) else (
    echo Choix invalide !
    pause
    goto :start
)

:start
goto :EOF
