@echo off
setlocal

:: 动态创建临时的卸载.reg文件
(
    echo Windows Registry Editor Version 5.00
    echo.
    echo [-HKEY_CLASSES_ROOT\*\shell\complex-unzip-tool]
    echo.
    echo [-HKEY_CLASSES_ROOT\Directory\shell\complex-unzip-tool]
) > "%~dp0_temp_uninstall.reg"

:: 导入注册表以删除键值
echo [INFO] Removing registry entries...
reg import "%~dp0_temp_uninstall.reg"

if %errorlevel% equ 0 (
    echo [SUCCESS] Right-click menu removed successfully!
) else (
    echo [ERROR] Failed to remove from registry.
    echo         Please try running this script as an Administrator.
)

:: 清理临时文件
del "%~dp0_temp_uninstall.reg"

:end
echo.
pause