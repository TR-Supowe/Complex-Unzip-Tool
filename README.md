# Complex-Unzip-Tool v1.0 🚀

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-brightgreen.svg)
![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)

**一款多层、加密、伪装压缩包批量解压工具，专为解决复杂解压场景而生。**

---

## 📖 项目简介 (About The Project)

在某些特定场景中，我们常常会遇到经过多层嵌套、设置了不同密码、修改了后缀名等方式进行伪装的压缩包。手动一层层解压、重命名、尝试密码非常繁琐且耗时。

**Complex-Unzip-Tool** 正是为了解决这一痛点而诞生的。它采用“任务队列”和“智能分析”引擎，致力于实现对各种复杂压缩包的“一键式”全自动深度解压。

<br>

---

## ✨ 主要功能 (Features)

- **全能批量处理**: 支持拖拽**单个文件**、**多个文件**、**单个文件夹**、**多个文件夹**进行批量解压。
- **深度递归解压**: 自动解压任意层数嵌套的压缩包，直至最内层。
- **密码库系统**:
  - 支持从`.txt`密码本中读取密码列表进行尝试。
  - **自动学习**: 任何成功解压的密码都会被自动、不重复地记录到主密码库 `1_all.txt` 中。
  - **临时密码库**: 提供`0_temp.txt`，方便用户临时粘贴密码使用，此文件不会被程序自动修改。
  - **用户自定义密码本**：用户可以自定义`2-9`号密码本，手动进行进一步的密码管理
- **智能反伪装**:
  - **后缀伪装识别**: 能识别被伪装成`.pdf`, `.txt`等其他格式的压缩文件。
  - **分卷智能补全**: 能够通过`.002`, `.003`等分卷线索，自动推断并修复被改名的第一分卷（`.001`）。
- **错误容忍机制**: 单个压缩包解压失败（如密码错误、文件损坏）不会中断整个流程，问题文件会被自动隔离到 `_failed_archives` 目录，程序继续处理其他任务。
- **控制台交互**: 提供详细的实时解压日志，整个过程完全透明。
- **开箱即用**: 以便携式软件包发布，内置7-Zip核心组件，无需用户安装任何依赖。

---

## 🚀 快速上手 (Getting Started)

本程序为Windows平台下的绿色便携版，无需安装。

1. **下载**
  
  - 前往本项目的 [GitHub Releases](https://github.com/TR-Supowe/Complex-Unzip-Tool/releases) 页面。
  - 下载最新版本的 `Complex-Unzip-Tool_vX.X.zip` 压缩包。
2. **解压**
  
  - 将下载的`.zip`文件解压到您希望的任意位置。
3. **使用**
  
  - **最简单的方式**: 将一个或多个需要解压的**文件/文件夹**，直接用鼠标**拖拽到 `complex-unzip-tool.exe` 文件上**。
  - 程序会自动弹出一个控制台窗口，并开始执行。
  - 执行后会提示输入密码，如果要使用单密码解压接下来的所有文件，则直接输入密码。如果文件无密码，则按下回车后，再按下1选择无密码解压。
  - 如果想要使用密码本中的多个密码解压，则在按下回车后再按下2选择使用密码本解压，然后再根据输出的密码本列表按下对应的数字编号即可。
4. **安装到Windows右键菜单**
  
  - 使用管理员权限运行`install.bat`将该程序安装到Windows右键菜单。
    
  - 使用管理员权限运行`uninstall.bat`卸载安装，删除对注册表的修改。
    

---

## 🔑 密码库配置 (Password Library)

密码库是本工具的核心功能之一，它位于程序目录下的 `passwords/` 文件夹中。

- `1_all.txt`: **主密码库**。所有被验证有效的密码都会被自动添加至此。
- `0_temp.txt`: **临时密码库**。用于存放临时的密码。如果你接下来的解压需要数个密码，而您也不准备长时间保存这些密码，您可以将密码临时添加到该密码库中（这些密码依然会被保存到主密码库中）。
- 使用**临时密码库**而不是遍历所有密码有助于您快速找到正确的密码解压文件。
- **自定义密码本**: 您可以在`passwords/`文件夹中创建自己的`.txt`文件（例如`my_pass.txt`），程序会自动识别并将其加入到密码库选择菜单中。

---

## 🤝 贡献 (Contributing)

欢迎任何形式的贡献！如果您有好的想法或发现了Bug，请随时提交 [Issues](https://github.com/TR-Supowe/Complex-Unzip-Tool/issues)。

但是抱歉由于时间问题，可能不会及时回复。

如果您希望贡献代码，请遵循以下步骤：

1. Fork 本项目
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交一个 Pull Request

---

## 📜 许可证 (License)

本项目使用 MIT 许可证。详情请见 `LICENSE` 文件。

---

## 🙏 致谢 (Acknowledgements)

- 本工具的核心解压功能依赖于强大的 **7-Zip**。在此向 **Igor Pavlov** 及所有7-Zip的贡献者致以诚挚的感谢。
- 感谢所有提出宝贵建议和进行测试的用户。

# Complex-Unzip-Tool v1.0 🚀

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-brightgreen.svg)
![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)

**A batch decompression tool for multi-layered, encrypted, and disguised archives, designed to handle complex extraction scenarios.**

---

## 📖 Project Introduction (About The Project)

In certain scenarios, we often encounter archives that are disguised through multi-layer nesting, different passwords, or modified file extensions. Manually decompressing each layer, renaming files, and trying passwords is tedious and time-consuming.

**Complex-Unzip-Tool** was born to solve this pain point. It utilizes a "task queue" and "intelligent analysis" engine to achieve fully automated, one-click deep decompression of various complex archives.

<br>

---

## ✨ Key Features (Features)

- **Comprehensive Batch Processing**: Supports drag-and-drop of **single files**, **multiple files**, **single folders**, and **multiple folders** for batch decompression.
- **Deep Recursive Extraction**: Automatically decompresses archives with any level of nesting until the innermost layer.
- **Password Library System**:
  - Supports reading password lists from `.txt` files for automated attempts.
  - **Auto-Learning**: Any successfully used password is automatically and non-redundantly recorded into the master password library `1_all.txt`.
  - **Temporary Password Library**: Provides `0_temp.txt` for temporary password storage; this file is not modified by the program.
  - **User-Defined Password Libraries**: Users can create custom password libraries (numbered `2-9`) for advanced password management.
- **Smart Anti-Disguise**:
  - **Extension Disguise Recognition**: Detects archives disguised as `.pdf`, `.txt`, or other formats.
  - **Split Archive Auto-Completion**: Intelligently identifies and repairs renamed first volumes (`.001`) using clues from split parts (`.002`, `.003`, etc.).
- **Error Tolerance**: Failed decompression (e.g., wrong password, corrupted file) won’t halt the entire process. Problem files are moved to `_failed_archives`, and processing continues.
- **Console Interaction**: Provides detailed real-time logs for full transparency.
- **Portable & Ready-to-Use**: Released as a portable package with embedded 7-Zip components—no dependencies required.

---

## 🚀 Quick Start (Getting Started)

This program is a portable green version for Windows—no installation needed.

1. **Download**
  
  - Visit the [GitHub Releases](https://github.com/TR-Supowe/Complex-Unzip-Tool/releases) page.
  - Download the latest `Complex-Unzip-Tool_vX.X.zip`.
2. **Extract**
  
  - Extract the downloaded `.zip` to any desired location.
3. **Usage**
  
  - **Simplest Method**: Drag one or more **files/folders** directly onto `complex-unzip-tool.exe`.
  - A console window will open and start processing.
  - If prompted for a password:
    - For a **single password** for all files: Enter the password directly.
    - For **passwordless** files: Press Enter, then press `1`.
    - For **multi-password** attempts: Press Enter, then press `2` to use a password library. Select a library by entering its number.
4. **Add to Windows Context Menu**
  
  - Run `install.bat` as **Administrator** to add to the right-click menu.
  - Run `uninstall.bat` as **Administrator** to remove registry modifications.

---

## 🔑 Password Library Configuration (Password Library)

The password library is a core feature located in the `passwords/` directory.

- `1_all.txt`: **Master Library**. All verified passwords are auto-added here.
- `0_temp.txt`: **Temporary Library**. Stores short-term passwords (these will still be added to `1_all.txt`).
- Using the **temporary library** instead of scanning all passwords speeds up the process.
- **Custom Libraries**: Create `.txt` files in `passwords/` (e.g., `my_pass.txt`). The program will auto-detect and add them to the menu.

---

## 🤝 Contributing (Contributing)

Contributions are welcome! Submit [Issues](https://github.com/TR-Supowe/Complex-Unzip-Tool/issues) for bugs or suggestions.

*Note: Responses may be delayed due to time constraints.*

To contribute code:

1. Fork the project.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit changes (`git commit -m 'Add some AmazingFeature'`).
4. Push the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📜 License (License)

Distributed under the MIT License. See `LICENSE` for details.

---

## 🙏 Acknowledgements (Acknowledgements)

- Core decompression relies on **7-Zip**. Sincere gratitude to **Igor Pavlov** and all contributors.
- Thanks to all users for valuable feedback and testing.
