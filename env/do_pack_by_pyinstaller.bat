pyinstaller.exe pyinstaller_pack_f.spec
copy .\dist\Area.exe ..\bin
rd /q /s .\build
rd /q /s .\dist