#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
re_gate 実行可能ファイル作成スクリプト
PyInstallerを使用してスタンドアロン実行ファイルを生成
"""

import subprocess
import sys
import os
from pathlib import Path

def check_pyinstaller():
    """PyInstallerがインストールされているかチェック"""
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__} が見つかりました")
        return True
    except ImportError:
        print("❌ PyInstallerがインストールされていません")
        return False

def install_pyinstaller():
    """PyInstallerをインストール"""
    print("PyInstallerをインストールしています...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstallerのインストールが完了しました")
        return True
    except subprocess.CalledProcessError:
        print("❌ PyInstallerのインストールに失敗しました")
        return False

def create_executable():
    """実行可能ファイルを作成"""
    script_path = Path(__file__).parent / "re_gate_gui.py"
    
    if not script_path.exists():
        print(f"❌ {script_path} が見つかりません")
        return False
    
    print("実行可能ファイルを作成しています...")
    print("この処理には数分かかる場合があります...")
    
    # PyInstallerコマンド構築
    cmd = [
        "pyinstaller",
        "--onefile",                    # 単一ファイル
        "--windowed",                   # Windowsでコンソールウィンドウを非表示
        "--name", "re_gate_gui",        # 出力ファイル名
        "--icon", "NONE",               # アイコンなし（必要に応じて追加）
        str(script_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, cwd=script_path.parent)
        print("✅ 実行可能ファイルの作成が完了しました")
        
        # 出力ファイルの場所を表示
        dist_path = script_path.parent / "dist"
        if sys.platform == "win32":
            exe_path = dist_path / "re_gate_gui.exe"
        else:
            exe_path = dist_path / "re_gate_gui"
        
        if exe_path.exists():
            print(f"📁 実行ファイル: {exe_path}")
            print(f"📏 ファイルサイズ: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 実行可能ファイルの作成に失敗しました: {e}")
        return False

def create_installer_script():
    """インストーラースクリプトを作成"""
    installer_content = '''#!/bin/bash
# re_gate インストールスクリプト

echo "=================================="
echo "  re_gate インストーラー"
echo "=================================="

# Python 3 チェック
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 がインストールされていません"
    echo "Python 3.7以上をインストールしてください"
    exit 1
fi

echo "✅ Python 3 が見つかりました"

# ディレクトリ作成
mkdir -p ~/re_gate
cd ~/re_gate

# ファイルダウンロード（実際の運用では適切なURLに変更）
echo "ファイルをダウンロードしています..."
# curl -O https://example.com/re_gate_gui.py
# curl -O https://example.com/re_gate_web.html
# curl -O https://example.com/run_re_gate.py

echo "✅ インストール完了"
echo "実行方法:"
echo "  python3 ~/re_gate/run_re_gate.py"

# デスクトップショートカット作成（Linux）
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    cat > ~/Desktop/re_gate.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=re_gate
Comment=論理回路シミュレーター
Exec=python3 $HOME/re_gate/run_re_gate.py
Icon=applications-electronics
Terminal=false
Categories=Education;Science;
EOF
    chmod +x ~/Desktop/re_gate.desktop
    echo "🖥️  デスクトップショートカットを作成しました"
fi
'''
    
    installer_path = Path(__file__).parent / "install.sh"
    with open(installer_path, 'w', encoding='utf-8') as f:
        f.write(installer_content)
    
    installer_path.chmod(0o755)  # 実行権限付与
    print(f"✅ インストーラースクリプトを作成しました: {installer_path}")

def create_batch_launcher():
    """Windows用バッチランチャーを作成"""
    batch_content = '''@echo off
title re_gate - 論理回路シミュレーター
echo ================================
echo   re_gate 起動中...
echo ================================
python "%~dp0run_re_gate.py"
pause
'''
    
    batch_path = Path(__file__).parent / "run_re_gate.bat"
    with open(batch_path, 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    print(f"✅ Windows用バッチファイルを作成しました: {batch_path}")

def main():
    print("=" * 60)
    print("  re_gate 配布版作成ツール")
    print("=" * 60)
    print()
    
    # PyInstallerチェック・インストール
    if not check_pyinstaller():
        if input("PyInstallerをインストールしますか？ (y/N): ").lower() == 'y':
            if not install_pyinstaller():
                return
        else:
            print("実行可能ファイルの作成をスキップします")
    
    print("\n作成する配布版を選択してください:")
    print("1. 実行可能ファイル (.exe/.bin)")
    print("2. インストーラースクリプト")
    print("3. バッチランチャー (Windows)")
    print("4. 全て")
    print("5. 終了")
    
    choice = input("\n選択 (1-5): ").strip()
    
    if choice == '1':
        create_executable()
    elif choice == '2':
        create_installer_script()
    elif choice == '3':
        create_batch_launcher()
    elif choice == '4':
        create_executable()
        create_installer_script()
        create_batch_launcher()
        print("\n✅ 全ての配布版を作成しました")
    elif choice == '5':
        print("終了します")
        return
    else:
        print("無効な選択です")
        return
    
    print("\n🎉 配布版の作成が完了しました！")
    print("\n📦 配布方法:")
    print("  - 実行ファイル: そのまま配布・実行")
    print("  - インストーラー: Unix系OSでの自動セットアップ")
    print("  - バッチファイル: Windows環境での簡単起動")

if __name__ == "__main__":
    main()
