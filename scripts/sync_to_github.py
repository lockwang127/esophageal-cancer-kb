#!/usr/bin/env python3
"""
GitHub同步脚本
将本地知识库推送到远程GitHub仓库
"""

import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# 路径配置
SCRIPT_DIR = Path(__file__).parent.parent

def run_command(cmd, cwd=None, check=True):
    """执行Shell命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(
        cmd, 
        shell=True, 
        cwd=cwd or SCRIPT_DIR,
        capture_output=True,
        text=True
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return result

def sync_to_github():
    """同步到GitHub"""
    print("=" * 50)
    print("食管癌知识库 - GitHub同步")
    print("=" * 50)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"仓库目录: {SCRIPT_DIR}\n")
    
    # 检查git是否可用
    try:
        run_command("git --version", check=True)
    except Exception as e:
        print(f"错误: git不可用 - {e}")
        return False
    
    # 检查是否是git仓库
    git_dir = SCRIPT_DIR / ".git"
    if not git_dir.exists():
        print("初始化Git仓库...")
        run_command("git init")
        run_command("git add .")
        run_command('git commit -m "Initial commit: 食管癌知识库 v1.0"')
        print("\n✓ 本地Git仓库初始化完成")
    else:
        print("已有Git仓库")
        # 检查远程
        result = subprocess.run(
            "git remote -v", 
            shell=True, 
            cwd=SCRIPT_DIR,
            capture_output=True,
            text=True
        )
        if not result.stdout.strip():
            print("\n尚未配置远程仓库")
            print("\n请按以下步骤操作:")
            print("1. 访问 https://github.com/new 创建名为 'esophageal-cancer-kb' 的仓库（Public）")
            print("2. 运行以下命令:")
            print(f"   git remote add origin git@github.com:lockwang127/esophageal-cancer-kb.git")
            print("   git push -u origin main")
            return False
        else:
            print(f"\n远程仓库已配置: {result.stdout.strip()}")
    
    # 推送前检查
    print("\n推送前检查:")
    
    # 检查状态
    result = subprocess.run(
        "git status", 
        shell=True, 
        cwd=SCRIPT_DIR,
        capture_output=True,
        text=True
    )
    print(result.stdout)
    
    # 检查远程
    result = subprocess.run(
        "git remote get-url origin", 
        shell=True, 
        cwd=SCRIPT_DIR,
        capture_output=True,
        text=True
    )
    remote_url = result.stdout.strip()
    
    if not remote_url:
        print("\n错误: 未配置远程仓库origin")
        print("\n请先创建GitHub仓库，然后运行:")
        print("  git remote add origin git@github.com:lockwang127/esophageal-cancer-kb.git")
        return False
    
    print(f"\n远程仓库: {remote_url}")
    
    # 检查分支
    result = subprocess.run(
        "git branch --show-current", 
        shell=True, 
        cwd=SCRIPT_DIR,
        capture_output=True,
        text=True
    )
    branch = result.stdout.strip() or "main"
    print(f"当前分支: {branch}")
    
    # 询问用户确认
    print("\n" + "=" * 50)
    print("准备推送")
    print("=" * 50)
    print(f"远程: {remote_url}")
    print(f"分支: {branch}")
    print("\n请确认是否推送? (按Enter继续，Ctrl+C取消)")
    input()
    
    # 推送
    print("\n推送中...")
    try:
        run_command(f"git push -u origin {branch}", check=True)
        print("\n✓ 推送成功！")
        return True
    except Exception as e:
        print(f"\n✗ 推送失败: {e}")
        return False

if __name__ == "__main__":
    sync_to_github()
