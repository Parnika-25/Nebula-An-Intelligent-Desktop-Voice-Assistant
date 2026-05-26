@echo off
cd apps/backend
call build_backend.bat
cd ../../apps/desktop
npm run build
pause
