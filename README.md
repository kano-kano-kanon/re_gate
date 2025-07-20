# 実装関数の使い方ドキュメント

## 📘 目次

* [論理ゲート (`d_gate` / `easyer`)](#論理ゲート)
* [加算器 (`HalfAdder`, `FullAdder`)](#加算器)
* [メモリ系 / フリップフロップ (`ff_gate`)](#フリップフロップ)
* [ビットメモリ・ディレイ](#ビットメモリディレイ)
* [エンコーダ・デコーダ](#エンコーダデコーダ)
* [回路構築とシミュレーション (`Circuit`)](#回路構築とシミュレーション)
* [アナログ素子](#アナログ素子)
* [GUI エディタの使い方](#gui-エディタの使い方)

---

## 論理ゲート

すべて `easyer` 経由で簡単に使えます（`d_gate` を内部に持っています）。

```python
from re_gate_ver1.2 import easyer as g

g.And(1, 1)     # => 1
g.Or(0, 1)      # => 1
g.Not(1)        # => 0
g.Xor(1, 0)     # => 1
g.Nand(1, 1)    # => 0
g.Nor(0, 0)     # => 1
g.Xnor(1, 1)    # => 1
```

---

## 加算器

### 半加算器（Half Adder）

```python
sum_bit, carry = g.HalfAdder(1, 1)
print(sum_bit, carry)  # => 0 1
```

### 全加算器（Full Adder）

```python
sum_bit, carry = g.FullAdder(1, 1, 1)
print(sum_bit, carry)  # => 1 1
```

---

## フリップフロップ

### D フリップフロップ

```python
g.FF_D(d=1, clk=1)  # => 1
g.FF_D(d=0, clk=1)  # => 0
```

### T フリップフロップ（トグル）

```python
g.FF_T(1)  # トグルで 1 -> 0 -> 1 と反転していく
```

### JK フリップフロップ

```python
g.FF_JK(1, 0, 1)  # => 1
g.FF_JK(0, 1, 1)  # => 0
```

### RS フリップフロップ

```python
g.FF_RS(0, 1)  # => 1
g.FF_RS(1, 0)  # => 0
g.FF_RS(1, 1)  # エラー終了
```

---

## ビットメモリ・ディレイ

### 単ビットメモリ

```python
q = g.BitMemory(d=1, en=1, q=0)  # => 1
q = g.BitMemory(d=0, en=0, q=1)  # => 1（保持）
```

### 遅延回路（1クロック）

```python
g.Delay([1, 0, 1])  # 初回 => [0,0,0]
g.Delay([0, 1, 1])  # 次回 => [1,0,1]
```

---

## エンコーダ・デコーダ

### エンコーダ (n→m)

```python
g.Encoder([0, 0, 1, 0], 2)  # => [1, 0]（2進数で index=2）
```

### デコーダ (m→2ⁿ)

```python
g.Decoder([1, 0], 4)  # => [0, 0, 1, 0]
```

---

## 回路構築とシミュレーション

### ノード追加とシミュレーション実行

```python
from re_gate_ver1.2 import easyer

c = easyer.Circuit()
a = c.add("A", lambda: 1)
b = c.add("B", lambda: 0)
out = c.add("OUT", easyer.And, a, b)

c.step()
print(out.value)  # => 0
```

### 波形ダンプ

```python
c.wave_dump()
# 出力例：
#        A: ───
#        B:    
#      OUT:
```

---

## アナログ素子

```python
from re_gate_ver1.2 import VCC, Resistor, Series

vcc = VCC(voltage=5.0, in_ohm=10)
r1 = Resistor("R1", 10)
r2 = Resistor("R2", 20)

s = Series(r1, r2)
current = s.apply_voltage(vcc.get_voltage())  # 串連回路に電圧印加

print(r1.get_voltage())  # 電圧降下
print(r1.get_current())  # 電流
```

---

## GUI エディタの使い方

```bash
python re_gate_ver1.2.py
```

起動すると Tkinter GUI が表示されます：

* `IN1`, `IN2` をクリックで値を `0/1` に変更
* ANDゲート出力がリアルタイム表示
* 将来的に複数のゲート追加・配線可能性あり（現在ドラッグ未実装）

---

## ユーティリティ

### クロック信号生成

```python
from re_gate_ver1.2 import time_function

clk = time_function(cycles=3, high_duration=2, low_duration=2)
wave = clk.generate_clock_signal()
print(wave)  # => [1,1,0,0,1,1,0,0,...]

rising, falling = clk.detect_edges(wave)
print(rising)  # [0, 4, 8, ...]
```

---

## エラー処理

* `0` か `1` 以外の入力が来た場合、`quit()` で強制終了
* フリップフロップの禁止状態（RS = 1,1）は警告付き終了

---

## ライセンス

Copyright (c) 2025 kano-kano-kanon

本ソフトウェアおよび関連文書ファイル（以下「ソフトウェア」）のコピーを取得するすべての人に対し、無償で以下の条件のもとに、ソフトウェアの使用、複製、改変、統合、公開、配布、サブライセンスを行うことを許可します。

**条件：**

1. 上記の著作権表示および本許諾表示は、ソフトウェアのすべての複製または実質的な部分に含めるものとします。
2. 本ソフトウェアを改変または再配布する場合は、元のバージョンがkano-kano-kanonによって作成されたことを明示しなければなりません。
3. 改変の有無にかかわらず、本ソフトウェアの再配布は、配布されたコードのコピーまたはそれが公開されているURLをkano-kano-kanon,Twitter:@kano_nandesu,keik:@kano_keik.infoに送信することによって報告しなければなりません。
4. 本ソフトウェアは「現状のまま」提供され、明示的または黙示的な一切の保証を伴いません


---

## 作者

* バージョン: 1.2
* 作成者: kano-kano-kanon

---

## お問い合わせ

不具合・追加機能の要望などは Issue またはライセンス記載の連絡先でどうぞ。
