set gender=%1
set store=steam

venv\Scripts\python.exe -c "from src.stanleydemo.install_unattended import %store%_uninstall;%store%_uninstall()"
venv\Scripts\python.exe -c "from src.stanleydemo.install_unattended import %store%_%gender%;%store%_%gender%()"