@echo off
setlocal

:: 获取当前批处理文件所在的目录，从而定位到complex-unzip-tool.exe
set "EXE_PATH=%~dp0complex-unzip-tool.exe"

:: 检查EXE是否存在
if not exist "%EXE_PATH%" (
    echo [ERROR] complex-unzip-tool.exe not found in the same directory!
    echo         Please make sure this script is in the same folder as the exe.
    goto :end
)

:: 准备用于注册表文件的路径 (将单个'\'替换为'\\')
set "REG_PATH=%EXE_PATH:\=\\%"

echo [INFO] Generating registry script for:
echo        %EXE_PATH%

:: 动态创建临时的.reg文件
(
    echo Windows Registry Editor Version 5.00
    echo.
    echo ; --- Add to Right-Click Menu for ALL FILES ---
    echo.
    echo [HKEY_CLASSES_ROOT\*\shell\complex-unzip-tool]
    echo @="unzip by complex-unzip-tool"
    echo "Icon"="\"%REG_PATH%\",0"
    echo.
    echo [HKEY_CLASSES_ROOT\*\shell\complex-unzip-tool\command]
    echo @="\"%EXE_PATH%\" \"%%1\""
    echo.
    echo ; --- Add to Right-Click Menu for FOLDERS ---
    echo.
    echo [HKEY_CLASSES_ROOT\Directory\shell\complex-unzip-tool]
    echo @="unzip by complex-unzip-tool"
    echo "Icon"="\"%REG_PATH%\",0"
    echo.
    echo [HKEY_CLASSES_ROOT\Directory\shell\complex-unzip-tool\command]
    echo @="\"%EXE_PATH%\" \"%%1\""
) > "%~dp0_temp_install.reg"

:: 导入注册表
echo [INFO] Importing to registry...
reg import "%~dp0_temp_install.reg"

:: 检查导入是否成功
if %errorlevel% equ 0 (
    echo [SUCCESS] Right-click menu added successfully!
) else (
    echo [ERROR] Failed to add to registry.
    echo         Please try running this script as an Administrator.
)

:: 清理临时文件
del "%~dp0_temp_install.reg"

:end
echo.
pause