# Copyright (c) 2025 TR-Supowe，MIT License

import sys
import os
import re
import subprocess
import tempfile
import shutil
import random
import string
from collections import deque


# --- 配置区 ---
def get_application_path():
    """获取程序可执行文件所在的目录。"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


def get_7z_executable_path():
    """确定7z.exe的路径。"""
    # 优先使用捆绑的7z
    bundled_7z = os.path.join(get_application_path(), '7z', '7z.exe')
    if os.path.exists(bundled_7z):
        return bundled_7z
    # 然后在系统PATH中寻找
    if shutil.which("7z"):
        return "7z"
    return None


# --- 密码库功能模块 ---
def setup_password_library():
    """检查并创建密码库文件夹及初始文件。"""
    lib_path = os.path.join(get_application_path(), 'passwords')
    if not os.path.isdir(lib_path):
        print("[INFO] 未发现密码库目录，正在创建 'passwords' 文件夹...")
        os.makedirs(lib_path)

    default_files = ['0_temp.txt', '1_all.txt']
    for f in default_files:
        f_path = os.path.join(lib_path, f)
        if not os.path.exists(f_path):
            print(f"[INFO] 正在创建初始密码本: {f}")
            open(f_path, 'w').close()
    return lib_path


def load_passwords_from_file(file_path: str) -> list[str]:
    """从.txt文件中读取密码列表。"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            passwords = [line.strip() for line in f if line.strip()]
            print(f"[INFO] 成功从 '{os.path.basename(file_path)}' 加载 {len(passwords)} 个密码。")
            return passwords
    except Exception as e:
        print(f"[ERROR] 读取密码文件 '{os.path.basename(file_path)}' 时出错: {e}")
        return []


def save_password_to_library(password: str):
    """将成功的密码自动保存到主密码库(1_all.txt)。"""
    if not password:  # 不保存空密码
        return

    lib_path = setup_password_library()
    main_lib_file = os.path.join(lib_path, '1_all.txt')

    try:
        # 先检查密码是否存在，避免重复
        with open(main_lib_file, 'r+', encoding='utf-8') as f:
            existing_passwords = {line.strip() for line in f}
            if password not in existing_passwords:
                f.seek(0, 2)  # 移动到文件末尾
                f.write(f"\n{password}")
                print(f"[INFO] 新密码 '***' 已自动保存到 '1_all.txt'。")
    except Exception as e:
        print(f"[ERROR] 自动保存密码时出错: {e}")


def select_password_from_library() -> list[str]:
    """显示密码库菜单并让用户选择。"""
    lib_path = setup_password_library()
    print("\n--- 密码库选择 ---")
    try:
        txt_files = sorted([f for f in os.listdir(lib_path) if f.lower().endswith('.txt')])
        if not txt_files:
            print("[WARN] 密码库为空，没有任何 .txt 文件。")
            return []

        print("发现以下密码本:")
        for i, filename in enumerate(txt_files):
            if i >= 10:  # 最多只显示10个
                print(f"      ... (及其他 {len(txt_files) - 10} 个文件)")
                break
            print(f"  [{i}] {filename}")

        while True:
            choice = input(f"请输入要使用的密码本编号 (0-{min(len(txt_files) - 1, 9)}): ")
            if choice.isdigit() and 0 <= int(choice) < min(len(txt_files), 10):
                selected_file = os.path.join(lib_path, txt_files[int(choice)])
                return load_passwords_from_file(selected_file)
            else:
                print("[ERROR] 输入无效，请输入列表中的正确编号。")

    except Exception as e:
        print(f"[ERROR] 访问密码库时出错: {e}")
        return []


# --- 核心分析与解压模块 ---

def normalize_split_archive_names(directory: str):
    """通过上下文推断，规范化被伪装的分卷压缩包文件名。"""
    print("[DEBUG] 开始分卷文件名规范化...")
    try:
        files_in_dir = os.listdir(directory)
        split_pattern = re.compile(r'(\.(?:part\d{1,3}(?:\.rar)?|[zr]\d{2,3}|00[1-9]\d*))$', re.IGNORECASE)
        file_groups = {}
        for filename in files_in_dir:
            match = split_pattern.search(filename)
            base_name = match.string[:match.start()] if match else os.path.splitext(filename)[0]
            group = file_groups.setdefault(base_name, {'split_parts': [], 'other_parts': []})
            if match:
                group['split_parts'].append(filename)
            else:
                if filename != '.DS_Store': group['other_parts'].append(filename)
        for base_name, group in file_groups.items():
            if not group['split_parts'] or not group['other_parts']: continue
            if len(group['other_parts']) > 1:
                print(f"[WARN] 发现多个可能的伪装文件，无法安全推断。主文件名: '{base_name}'。已跳过。")
                continue
            renamed_candidate_name, original_path = group['other_parts'][0], os.path.join(directory,
                                                                                          group['other_parts'][0])
            has_part_one = any(
                re.search(r'\.(?:part0*1(?:\.rar)?|[zr]01|001)$', f, re.IGNORECASE) for f in group['split_parts'])
            if not has_part_one:
                new_filename = base_name + ".001"
                print(f"[INFO] 推断 '{renamed_candidate_name}' 是缺失的第一分卷。")
            else:
                part_numbers = [int(re.search(r'(\d+)$', f).group(1)) for f in group['split_parts']]
                next_part_num = max(part_numbers) + 1
                ext_template_match, num_format = re.search(r'(\.\D*?)(\d+)$', group['split_parts'][
                    0]), f"{{:0{len(re.search(r'(\d+)$', group['split_parts'][0]).group(2))}}}d"
                new_filename = base_name + ext_template_match.group(1) + num_format.format(next_part_num)
                print(f"[INFO] 推断 '{renamed_candidate_name}' 是一个被伪装的后续分卷。")
            new_path = os.path.join(directory, new_filename)
            try:
                os.rename(original_path, new_path)
                print(f"[SUCCESS] 已将其重命名为 -> {new_filename}")
            except OSError as e:
                print(f"[ERROR] 重命名文件时出错: {e}")
    except Exception as e:
        print(f"[ERROR] 文件名规范化阶段出现意外错误: {e}")


def analyze_directory(directory: str, passwords: list[str]) -> list:
    """智能分析目录，创建任务列表。"""
    normalize_split_archive_names(directory)
    print(f"[DEBUG] 开始压缩包探测...")
    new_tasks, processed_files = [], set()
    try:
        all_files = [os.path.join(directory, f) for f in os.listdir(directory) if
                     os.path.isfile(os.path.join(directory, f))]
    except FileNotFoundError:
        return []
    split_pattern = re.compile(r'\.(?:part\d{1,3}(?:\.rar)?|[zr]\d{2,3}|00[1-9]\d*)$', re.IGNORECASE)
    file_groups = {}
    for f_path in all_files:
        match, base_name = split_pattern.search(f_path), os.path.splitext(f_path)[0]
        if match: base_name = f_path[:match.start()]
        file_groups.setdefault(base_name, []).append(f_path)
    for base_name, file_list in file_groups.items():
        parts = [f for f in file_list if split_pattern.search(f)]
        if not parts: continue
        first_part_pattern = re.compile(r'\.(?:part0*1(?:\.rar)?|[zr]01|001)$', re.IGNORECASE)
        entry_point = next((f for f in parts if first_part_pattern.search(f)), None)
        if entry_point:
            task = {'type': 'split', 'entry_path': entry_point, 'all_parts': parts}
            new_tasks.append(task)
            processed_files.update(parts)
            print(f"[DEBUG] 识别出分卷任务: {os.path.basename(entry_point)} (共 {len(parts)} 个部分)")
    remaining_files, passwords_to_try = [f for f in all_files if f not in processed_files], [""] + passwords
    for f_path in remaining_files:
        for password in passwords_to_try:
            probe_command = [SEVEN_ZIP_PATH, 'l', f_path, f'-p{password}']
            try:
                result = subprocess.run(probe_command, capture_output=True, text=True, encoding='utf-8',
                                        errors='ignore')
                if "Type =" in result.stdout:
                    task = {'type': 'single', 'path': f_path}
                    new_tasks.append(task)
                    print(f"[DEBUG] 识别出独立压缩包任务: {os.path.basename(f_path)}")
                    break
            except Exception:
                continue
    return new_tasks


def attempt_decompression(seven_zip_path: str, file_to_decompress: str, passwords: list[str], output_dir: str) -> tuple[
    str, str, str | None]:
    """尝试解压, 成功时返回(status, msg, successful_password)"""
    passwords_to_try = [""] + [p for p in passwords if p]
    last_error_output = ""
    for password in passwords_to_try:
        command = [seven_zip_path, 'x', file_to_decompress, f'-p{password}', f'-o{output_dir}', '-y']
        try:
            result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            if result.returncode == 0:
                return 'success', f"密码正确，成功解压: {os.path.basename(file_to_decompress)}", password
            last_error_output, error_text_lower = (result.stderr or result.stdout), (
                        result.stderr or result.stdout).lower()
            if "password" in error_text_lower:
                continue
            else:
                break
        except FileNotFoundError:
            return 'fatal_error', f"严重错误: 无法找到 7-Zip 程序: {seven_zip_path}", None
        except Exception as e:
            return 'fatal_error', f"未知子进程错误: {e}", None
    final_error_text_lower = last_error_output.lower()
    if "password" in final_error_text_lower:
        return 'password_failure', "密码错误: 所有密码均尝试失败。", None
    elif "cannot open" in final_error_text_lower and "as archive" in final_error_text_lower:
        return 'not_archive', "非压缩包: 文件不是有效压缩格式。", None
    else:
        return 'fatal_error', f"7-Zip致命错误: {last_error_output.strip()}", None


def run_decompression_engine(staging_dir: str, initial_tasks: list, passwords: list[str], seven_zip_path: str):
    task_queue, successful_tasks, failed_tasks = deque(initial_tasks), 0, 0
    while task_queue:
        print("\n" + "=" * 20 + f" 队列剩余任务: {len(task_queue)} " + "=" * 20)
        current_task = task_queue.popleft()
        task_entry_path = current_task.get('entry_path') or current_task.get('path')
        if not os.path.exists(task_entry_path):
            print(f"[WARN] 任务文件已不存在，跳过: {os.path.basename(task_entry_path)}")
            continue
        print(f"[INFO] 正在处理任务: {os.path.basename(task_entry_path)}")
        status, message, successful_password = attempt_decompression(seven_zip_path, task_entry_path, passwords,
                                                                     staging_dir)
        print(f"[{status.upper()}] {message}")
        if status == 'success':
            successful_tasks += 1
            print(f"[PASSWORD] {os.path.basename(task_entry_path)} 解压密码: {successful_password}")
            save_password_to_library(successful_password)  # 自动学习密码
            files_to_delete = current_task.get('all_parts') or [current_task.get('path')]
            if files_to_delete:
                print(f"[INFO] 准备清理已处理的压缩包共 {len(files_to_delete)} 个部分...")
                for f_path in files_to_delete:
                    try:
                        if os.path.exists(f_path): os.remove(f_path)
                    except OSError as e:
                        print(f"[WARN] 清理文件失败: {e}")
            new_tasks = analyze_directory(staging_dir, passwords)
            if new_tasks:
                current_task_paths = {t.get('entry_path') or t.get('path') for t in task_queue}
                unique_new_tasks = [t for t in new_tasks if
                                    (t.get('entry_path') or t.get('path')) not in current_task_paths]
                if unique_new_tasks:
                    task_queue.extend(unique_new_tasks)
                    print(f"[INFO] 分析完毕，发现并添加了 {len(unique_new_tasks)} 个新任务到队列。")
        else:
            failed_tasks += 1
            failed_dir = os.path.join(staging_dir, '_failed_archives')
            os.makedirs(failed_dir, exist_ok=True)
            try:
                shutil.move(task_entry_path, os.path.join(failed_dir, os.path.basename(task_entry_path)))
                print(f"[INFO] 已将失败的压缩包隔离到 _failed_archives 目录。")
            except Exception as e:
                print(f"[ERROR] 隔离失败的压缩包时出错: {e}")
    return successful_tasks, failed_tasks


def process_single_file(file_path: str, passwords: list[str]):
    """对单个文件执行完整的解压、分析、输出流程"""
    source_file_abspath, source_dir_path = os.path.abspath(file_path), os.path.dirname(os.path.abspath(file_path))
    base_name = os.path.splitext(os.path.basename(source_file_abspath))[0]
    try:
        with tempfile.TemporaryDirectory(prefix=f"{base_name}_temp_", dir=source_dir_path) as staging_dir:
            print(f"[INFO] 为 '{os.path.basename(file_path)}' 创建暂存区: {staging_dir}")
            print("\n--- 开始初始解压 ---")
            initial_status, initial_message, successful_password = attempt_decompression(SEVEN_ZIP_PATH,
                                                                                         source_file_abspath, passwords,
                                                                                         staging_dir)
            print(f"[{initial_status.upper()}] {initial_message}")
            if initial_status != 'success':
                print(f"[ERROR] 初始文件 '{os.path.basename(file_path)}' 解压失败，跳过此文件。")
                return
            save_password_to_library(successful_password)  # 初始密码也学习
            print("\n--- 开始扫描第一层解压产物 ---")
            initial_tasks = analyze_directory(staging_dir, passwords)
            if not initial_tasks:
                print("[INFO] 未在第一层产物中发现新的压缩包任务。")
            else:
                print(f"[INFO] 分析完成，发现 {len(initial_tasks)} 个待处理任务。")
            successful_tasks, failed_tasks = run_decompression_engine(staging_dir, initial_tasks, passwords,
                                                                      SEVEN_ZIP_PATH)
            random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
            final_dest_dir = os.path.join(source_dir_path, f"{base_name}_{random_suffix}")
            try:
                shutil.move(staging_dir, final_dest_dir)
                print("\n" + "-" * 15 + f" 文件 '{os.path.basename(file_path)}' 处理完成 " + "-" * 15)
                print(f"[INFO] 最终文件已输出到: {final_dest_dir}")
                print(f"[SUCCESS] 成功处理压缩包: {successful_tasks + 1} 个 (包含初始文件)")
                print(f"[ERROR]   解压失败压缩包: {failed_tasks} 个 (详情请见 _failed_archives 子目录)")
            except Exception as e:
                print(f"\n[FATAL] 最后移动暂存区时发生致命错误: {e}")
                print(f"[INFO] 您可以手动访问未被清理的暂存区获取文件: {staging_dir}")
    except Exception as e:
        print(f"\n[FATAL] 处理文件 '{os.path.basename(file_path)}' 时发生未预料的严重错误: {e}")


# --- 主程序入口 ---
def main():
    """主程序入口，支持文件和文件夹拖拽，并包含密码库功能"""
    print("=" * 60)
    print(" Power Unzip - 多层/加密/伪装压缩包一键解压工具 v2.0")
    print("=" * 60)
    if len(sys.argv) < 2:
        print("[ERROR] 使用方法: 请将一个或多个文件/文件夹拖拽到本程序的 .bat 启动脚本上。")
        input("按 Enter 键退出...")
        return

    global SEVEN_ZIP_PATH
    SEVEN_ZIP_PATH = get_7z_executable_path()
    if not SEVEN_ZIP_PATH:
        print(f"[ERROR] 7-Zip程序未找到，请检查配置或系统PATH环境变量。")
        input("按 Enter 键退出...")
        return
    print(f"[INFO] 使用 7-Zip 程序于: {SEVEN_ZIP_PATH}")

    passwords = []
    try:
        password_str = input("[INPUT] 请输入密码 (直接回车可使用密码库或空密码): ")
        if password_str:  # 用户直接输入了密码
            passwords = [password_str]
        else:  # 用户回车，进入二级菜单
            choice = input(" -> 请选择操作: [1] 使用空密码解压 [2] 从密码库选择密码 (默认1): ")
            if choice == '2':
                passwords = select_password_from_library()
            else:  # 包括输入1或直接回车等其他情况
                passwords = [""]

    except Exception as e:
        print(f"[ERROR] 获取密码时发生错误: {e}")
        input("按 Enter 键退出...")
        return

    source_paths = sys.argv[1:]
    print(f"\n[INFO] 检测到 {len(source_paths)} 个拖拽项目，开始处理...")

    for i, path in enumerate(source_paths):
        print("\n" + "#" * 20 + f" 总任务 {i + 1}/{len(source_paths)}: {os.path.basename(path)} " + "#" * 20)
        if os.path.isfile(path):
            process_single_file(path, passwords)
        elif os.path.isdir(path):
            print(f"[INFO] 项目为文件夹，开始处理其内含的所有文件...")
            top_level_files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            if not top_level_files:
                print(f"[WARN] 文件夹 '{os.path.basename(path)}' 为空，跳过。")
                continue
            for j, file_in_dir in enumerate(top_level_files):
                print(
                    "\n" + "-" * 15 + f" 子任务 {j + 1}/{len(top_level_files)} of '{os.path.basename(path)}' " + "-" * 15)
                process_single_file(file_in_dir, passwords)
        else:
            print(f"[WARN] 路径 '{path}' 不是有效的文件或文件夹，已跳过。")

    print("\n" + "#" * 25 + " 所有任务处理完毕 " + "#" * 25)
    input("按 Enter 键退出...")


if __name__ == '__main__':
    main()