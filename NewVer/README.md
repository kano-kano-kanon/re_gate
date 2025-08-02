# re_gate v2.0 - UI版 論理回路シミュレーター

## 概要

re_gateは論理回路の設計とシミュレーションを行うツールです。v2.0では、従来のPythonライブラリに加えて、**直感的なUI操作**が可能なバージョンを提供します。

## 提供バージョン

### 1. GUI版 (re_gate_gui.py)
- **Tkinter**ベースのクロスプラットフォーム対応GUI
- ドラッグ&ドロップによる直感的な回路設計
- リアルタイムシミュレーション
- 回路の保存・読み込み機能

#### 特徴
- ✅ 視覚的な回路設計
- ✅ マウス操作による配線
- ✅ リアルタイム値表示
- ✅ 保存/読み込み機能
- ✅ Windows/Mac/Linux対応

### 2. Web版 (re_gate_web.html)
- **HTML/CSS/JavaScript**によるブラウザ実行
- インストール不要
- モバイルデバイス対応

#### 特徴
- ✅ ブラウザで即座に実行
- ✅ インストール不要
- ✅ レスポンシブデザイン
- ✅ クロスプラットフォーム

### 3. 元のPython版 (re_gate_ver1.2.py)
- プログラマブルな論理回路ライブラリ
- スクリプトによる自動化

## 使用方法

### 🚀 簡単起動
```bash
python run_re_gate.py
```
起動スクリプトが各バージョンを案内します。

### 個別起動

#### GUI版
```bash
python re_gate_gui.py
```

#### Web版
- `re_gate_web.html`をブラウザで開く
- または：
```bash
python -m http.server 8000
# http://localhost:8000/re_gate_web.html にアクセス
```

#### Python版
```bash
python ../re_gate_ver1.2.py
```

## 操作方法

### GUI版・Web版共通

#### 基本操作
1. **ゲート配置**: ツールバーのゲートボタン → キャンバスクリック
2. **接続**: 「接続」ボタン → 出力ピンから入力ピンへドラッグ
3. **移動**: ゲートをドラッグ
4. **削除**: 右クリック → 削除
5. **シミュレーション**: 「実行」ボタン

#### 利用可能なゲート
- **INPUT**: 入力ゲート（ダブルクリックで値変更）
- **OUTPUT**: 出力ゲート
- **AND**: 論理積ゲート
- **OR**: 論理和ゲート  
- **NOT**: 否定ゲート
- **NAND**: 否定論理積ゲート
- **NOR**: 否定論理和ゲート
- **XOR**: 排他的論理和ゲート
- **XNOR**: 否定排他的論理和ゲート

#### キーボードショートカット（GUI版）
- `F5`: シミュレーション実行
- `Ctrl+S`: 保存
- `Ctrl+O`: 読み込み
- `Delete`: 選択ゲート削除

## サンプル回路

起動時に基本的なAND回路が自動作成されます：
```
INPUT A ──┐
          ├─ AND ─── OUTPUT
INPUT B ──┘
```

## 高度な使用例

### フルアダー回路
1. INPUT A, B, Cin を配置
2. XOR, AND, OR ゲートで構成
3. Sum と Carry 出力を確認

### カウンター回路
1. D-フリップフロップ相当の回路を構築
2. クロック信号による状態変化をシミュレーション

## ファイル構成

```
NewVer/
├── run_re_gate.py          # 統合起動スクリプト
├── re_gate_gui.py          # GUI版メインファイル
├── re_gate_web.html        # Web版（単一ファイル）
├── README.md               # このファイル
└── examples/               # サンプル回路（予定）
```

## 必要環境

### GUI版
- Python 3.7+
- tkinter（通常Pythonに同梱）

### Web版
- モダンなWebブラウザ
- JavaScript有効

### Python版
- Python 3.7+
- numpy（オプション）

## トラブルシューティング

### GUI版が起動しない
```bash
# tkinterがインストールされているか確認
python -c "import tkinter; print('OK')"

# Ubuntu/Debianの場合
sudo apt-get install python3-tk

# macOS（Homebrew）の場合
brew install python-tk
```

### Web版で動作しない
- JavaScriptが有効になっているか確認
- モダンなブラウザを使用（Chrome 70+, Firefox 65+, Safari 12+）

## 開発者向け情報

### アーキテクチャ
- **GUI版**: Model-View-Controller パターン
- **Web版**: Component-based architecture
- **共通**: トポロジカルソートによる評価順序決定

### 拡張方法
1. 新しいゲートタイプを`GateType`列挙型に追加
2. `LogicSimulator.evaluate_gate`にロジック追加
3. UI側でピン設定とビジュアル要素追加

## ライセンス

MIT License - 自由に使用・改変・配布可能

## 更新履歴

### v2.0 (2025-08-02)
- GUI版とWeb版を追加
- 統合起動スクリプト
- ドラッグ&ドロップUI
- 保存/読み込み機能

### v1.2
- 元のPythonライブラリ版

## 貢献

バグ報告、機能要望、プルリクエストを歓迎します！

---

**re_gate** - 論理回路学習とプロトタイピングの最適なツール
