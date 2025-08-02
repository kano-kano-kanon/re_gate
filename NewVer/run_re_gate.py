#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
re_gate 起動スクリプト
複数のバージョンから選択して実行
"""

import sys
import os
import subprocess
import webbrowser
from pathlib import Path

def main():
    print("=" * 60)
    print("  re_gate - 論理回路シミュレーター v2.0")
    print("=" * 60)
    print()
    print("実行方法を選択してください:")
    print()
    print("1. GUI版 (Tkinter) - クロスプラットフォーム対応")
    print("2. Web版 (HTML/JavaScript) - ブラウザで実行")
    print("3. コマンドライン版 (Python) - 元のスクリプト")
    print("4. 終了")
    print()
    
    while True:
        try:
            choice = input("選択 (1-4): ").strip()
            
            if choice == '1':
                run_gui_version()
                break
            elif choice == '2':
                run_web_version()
                break
            elif choice == '3':
                run_commandline_version()
                break
            elif choice == '4':
                print("終了します。")
                break
            else:
                print("無効な選択です。1-4の数字を入力してください。")
                
        except KeyboardInterrupt:
            print("\n終了します。")
            break
        except Exception as e:
            print(f"エラーが発生しました: {e}")

def run_gui_version():
    """GUI版を実行"""
    print("\nGUI版を起動しています...")
    script_path = Path(__file__).parent / "re_gate_gui.py"
    
    try:
        subprocess.run([sys.executable, str(script_path)], check=True)
    except FileNotFoundError:
        print("エラー: re_gate_gui.py が見つかりません。")
    except subprocess.CalledProcessError as e:
        print(f"エラー: GUI版の実行に失敗しました。{e}")
    except Exception as e:
        print(f"予期しないエラー: {e}")

def run_web_version():
    """Web版を実行"""
    print("\nWeb版をブラウザで開いています...")
    html_path = Path(__file__).parent / "re_gate_web.html"
    
    if html_path.exists():
        file_url = f"file://{html_path.absolute()}"
        webbrowser.open(file_url)
        print(f"ブラウザで {file_url} を開きました。")
        print("ブラウザが開かない場合は、以下のURLを手動で開いてください:")
        print(file_url)
    else:
        print("エラー: re_gate_web.html が見つかりません。")

def run_commandline_version():
    """コマンドライン版を実行"""
    print("\nコマンドライン版を起動しています...")
    script_path = Path(__file__).parent.parent / "re_gate_ver1.2.py"
    
    if script_path.exists():
        try:
            subprocess.run([sys.executable, str(script_path)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"エラー: コマンドライン版の実行に失敗しました。{e}")
        except Exception as e:
            print(f"予期しないエラー: {e}")
    else:
        print("エラー: re_gate_ver1.2.py が見つかりません。")

if __name__ == "__main__":
    main()
