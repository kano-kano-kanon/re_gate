#re_gate_ver1.2.py
#import math
#import random
import time
import numpy as np
# self = no（内部で「番号」扱いしたいなら self.no_id などで持つ）

class BaseElement:
    _counter = 0#class 変数 (全体で共有)
    def __init__(no):
        no.no_id=BaseElement._counter
        BaseElement._counter += 1

class analog_element:
    class VCC(BaseElement):
        def __init__(no,voltage,in_ohm,name="VCC"):
            super().__init__()
            no.name=name
            no.inohm=in_ohm
            no.voltage=voltage
            if not in_ohm == 0:
                no.Pmax_with_ohm=in_ohm
        def get_voltage(no):
            return no.voltage
        def get_resistance(no):
            return no.inohm
        
    class Resistor(BaseElement):
        def __init__(no,name,resistance_ohm):
            super().__init__()
            no.name=name
            no.resistance=resistance_ohm
            no.voltage=0
            no.current=0
        def apply_voltage(no,voltage):
            no.voltage=voltage
            no.current=voltage / no.resistance
            return no.current
        
        def get_voltage(no):
            return no.voltage
        def get_current(no):
            return no.current
        def get_resistance(no):
            return no.resistance
        
ele = analog_element  # クラスの名前空間として使う
VCC = ele.VCC
Resistor = ele.Resistor

class Series:
    def __init__(no,*elements):
        no.elements=elements
    def sum_resistance(no):
        return sum(e.get_resistance() for e in no.elements)
    def apply_voltage(no,sum_voltage):
        R_sum =no.sum_resistance()
        I_sum =sum_voltage / R_sum
        for e in no.elements:
            v_drop = I_sum * e.get_resistance()
            e.apply_voltage(v_drop)
        return I_sum

class time_function:
    def __init__(no,cycles,high_duration,low_duration):
        no.cycles=cycles
        no.high_duration=high_duration
        no.low_duration=low_duration
    
    def generate_clock_signal(no):
        clock = []
        for _ in range(no.cycles):
            clock.extend([1] * no.high_duration)
            clock.extend([0] * no.low_duration)
        return clock
    
    def detect_edges(no, clock_signal):
        rising_edges = []
        falling_edges = []
        for i in range(1, len(clock_signal)):
            if clock_signal[i] == 1 and clock_signal[i - 1] == 0:
                rising_edges.append(i)
            elif clock_signal[i] == 0 and clock_signal[i - 1] == 1:
                falling_edges.append(i)
        return rising_edges, falling_edges

def Error(on):
    if on == 1:
        print(f"不正な結果が入力層もしくは中間層で発生しました。")
        quit()

class BaseGate:
    _counter = 0
    def __init__(no, name=None):
        BaseGate._counter += 1
        no.no_id = BaseGate._counter
        no.name = name if name else f"{no.__class__.__name__}_{no.no_id}"
    def error(no, *inputs):
        for i in inputs:
            if i not in (0, 1):
                print(f"[{no.name}] 入力値が不正: {inputs}")
                quit()
    def __repr__(no):
        return f"<{no.__class__.__name__} #{no.no_id} '{no.name}'>"
class d_gate(BaseGate):
    def __init__(no, name=None,delay_len=1):
        super().__init__(name)
        no.delay_state = None
        no.delay_len = delay_len
        no._delay_buffer = None  # 遅延バッファ（キュー）
    #単入力ゲート
    def Buffer(no,inp):no.error(inp);return inp
    def Not(no,inp):
        no.error(inp)
        if inp==0:
            out = 1
        elif inp==1:
            out=0
        return out
    def Inverter(no,inp):#eireace
        no.error(inp)
        out = no.Not(inp)
        return out 
    # 基本2入力ゲート
    def And(no, a, b): no.error(a, b); return a & b
    def OR(no, a, b): no.error(a, b); return a | b
    def nand(no, a, b): return 1 - no.And(a, b)
    def nor(no, a, b): return 1 - no.OR(a, b)
    def xor(no, a, b): no.error(a, b); return a ^ b
    def xnor(no, a, b): return 1 - no.xor(a, b)
    # 多入力ゲート
    def and_n(no, *args): no.error(*args); return int(all(args))
    def or_n(no, *args):  no.error(*args); return int(any(args))
    def nand_n(no, *args): return 1 - no.and_n(*args)
    def nor_n(no, *args):  return 1 - no.or_n(*args)
    def xor_n(no, *args):  no.error(*args); return sum(args) % 2
    def xnor_n(no, *args): return 1 - no.xor_n(*args)
    # 複合ロジック
    def mux(no, sel, a, b):
        no.error(sel, a, b)
        return int(not sel) * a + sel * b

    def maj(no, a, b, c):
        return no.majority_n(a, b, c)

    def majority_n(no, *args):
        no.error(*args)
        ones = sum(args)
        return int(ones > len(args) // 2)

    def parity(no, *args):
        no.error(*args)
        return sum(args) % 2

    def all_1(no, *args):
        no.error(*args)
        return int(all(args))

    def any_1(no, *args):
        no.error(*args)
        return int(any(args))

    def onehot(no, *args):
        no.error(*args)
        return int(sum(args) == 1)
    #半加算と全加算
    def ha(no, a, b):
        s = no.xor(a, b)
        c = no.And(a, b)
        return s, c

    def fa(no, a, b, cin):
        s1, c1 = no.ha(a, b)
        s2, c2 = no.ha(s1, cin)
        cout = no.OR(c1, c2)
        return s2, cout
    #組み合わせ回路
    def bit_memory(no, d, enable, prev_q=0):
        no.error(d, enable, prev_q)
        if enable == 1:
            return d
        else:
            return prev_q

    def nbit_memory(no, d_list, enable, prev_q_list):
        if len(d_list) != len(prev_q_list):
            raise ValueError("d_list と prev_q_list の長さが違います")
        no.error(enable)
        return [no.bit_memory(d, enable, prev_q) for d, prev_q in zip(d_list, prev_q_list)]

    def tristate_buffer_n(no, input_list, enable_list):
        if len(input_list) != len(enable_list):
            raise ValueError("input_list と enable_list の長さが違います")
        for val, en in zip(input_list, enable_list):
            no.error(val, en)
        # 高インピーダンスは None で表現
        return [val if en == 1 else None for val, en in zip(input_list, enable_list)]

    def delay(no, input_list):
        # 入力の検証
        for val in input_list:
            no.error(val)
        
        # 初回呼び出しなら内部状態を0で初期化
        if no._delay_state is None:
            no._delay_state = [0]*len(input_list)
        
        # 現在のdelay_stateを出力として返す（遅延）
        output = no._delay_state.copy()

        # 入力を内部状態に保存しておく（次回の出力になる）
        no._delay_state = input_list.copy()

        return output
    def delay_n(no, input_list):
        no.error(*input_list)
        if no._delay_buffer is None:
            # delay_len分の0入力を用意
            no._delay_buffer = [[0]*len(input_list) for _ in range(no.delay_len)]

        # 出力はバッファの先頭（最も古いデータ）
        output = no._delay_buffer.pop(0)

        # 新しい入力をバッファ末尾に追加
        no._delay_buffer.append(input_list.copy())

        return output
    def encoder_n_to_m(no, inputs, output_bits):
        n = len(inputs)
        m = output_bits
        no.error(*inputs)
        for i in reversed(range(n)):
            if inputs[i] == 1:
                # 出力は i を mビット2進数で表現
                return [(i >> bit) & 1 for bit in reversed(range(m))]
        # どれも1でなければ0を返す
        return [0]*m

    def decoder_n_to_m(no, inputs, output_bits):
        n = len(inputs)
        m = output_bits
        no.error(*inputs)
        index = 0
        for bit in inputs:
            if bit not in (0,1):
                no.error(*inputs)
        for i, val in enumerate(reversed(inputs)):
            index |= (val << i)
        return [1 if i == index else 0 for i in range(m)]

#フリップフロップ
class ff_gate(BaseGate):
    def __init__(no, name=None):
        super().__init__(name)
        no.state = 0  # Qの状態

    def t(no, clk_edge):
        if clk_edge == 1:
            no.state ^= 1
        return no.state

    def d(no, d_val, clk_edge):
        if clk_edge == 1:
            if d_val not in (0, 1):
                no.error(d_val)
            no.state = d_val
        return no.state

    def jk(no, j, k, clk_edge):
        no.error(j, k)
        if clk_edge == 1:
            if j == 0 and k == 0:
                pass  # 保持
            elif j == 0 and k == 1:
                no.state = 0
            elif j == 1 and k == 0:
                no.state = 1
            elif j == 1 and k == 1:
                no.state ^= 1
        return no.state

    def rs(no, r, s):
        no.error(r, s)
        if r == s == 1:
            print(f"[{no.name}] RS-FFで禁止状態")
            quit()
        elif r == 1:
            no.state = 0
        elif s == 1:
            no.state = 1
        return no.state
    
def detect_edge(prev_clk,curr_clk):
    if prev_clk == 0 and curr_clk==1:
        return 1 #rising / positive
    elif prev_clk==1 and curr_clk== 0:
        return -1 #falling / negative
    else:
        return 0

class Node:
    def __init__(no, func, name):
        no.func = func
        no.name = name
        no.inputs = []
        no.value = 0

    def eval(no):
        args = [i.value if isinstance(i, Node) else i for i in no.inputs]
        no.value = no.func(*args)
        return no.value

class easyer:
    d = d_gate()
    ff = ff_gate()

    @staticmethod
    def And(a, b): return easyer.d.And(a, b)
    @staticmethod
    def Or(a, b): return easyer.d.OR(a, b)
    @staticmethod
    def Not(a): return easyer.d.Not(a)
    @staticmethod
    def Xor(a, b): return easyer.d.xor(a, b)
    @staticmethod
    def Nand(a, b): return easyer.d.nand(a, b)
    @staticmethod
    def Nor(a, b): return easyer.d.nor(a, b)
    @staticmethod
    def Xnor(a, b): return easyer.d.xnor(a, b)
    @staticmethod
    def Mux(sel, a, b): return easyer.d.mux(sel, a, b)
    @staticmethod
    def Majority(*args): return easyer.d.majority_n(*args)
    @staticmethod
    def Parity(*args): return easyer.d.parity(*args)
    @staticmethod
    def HalfAdder(a, b): return easyer.d.ha(a, b)
    @staticmethod
    def FullAdder(a, b, cin): return easyer.d.fa(a, b, cin)
    @staticmethod
    def BitMemory(d, en, q): return easyer.d.bit_memory(d, en, q)
    @staticmethod
    def Delay(inputs): return easyer.d.delay(inputs)
    @staticmethod
    def Encoder(ins, bits): return easyer.d.encoder_n_to_m(ins, bits)
    @staticmethod
    def Decoder(ins, bits): return easyer.d.decoder_n_to_m(ins, bits)
    @staticmethod
    def FF_T(clk): return easyer.ff.t(clk)
    @staticmethod
    def FF_D(d, clk): return easyer.ff.d(d, clk)
    @staticmethod
    def FF_JK(j, k, clk): return easyer.ff.jk(j, k, clk)
    @staticmethod
    def FF_RS(r, s): return easyer.ff.rs(r, s)

    class Circuit:
        def __init__(no):
            no.nodes = []
            no.signals = {}
            no.history = []

        def add(no, name, func, *inputs):
            node = Node(func=func, name=name)
            node.inputs = list(inputs)
            no.nodes.append(node)
            no.signals[name] = node
            return node

        def step(no):
            snapshot = {}
            for n in no.nodes:
                val = n.eval()
                snapshot[n.name] = val
            no.history.append(snapshot)
            return snapshot

        def to_string(no):
            return "\n".join(" | ".join(f"{k}:{v}" for k, v in h.items()) for h in no.history)

        def wave_dump(no):
            if not no.history:
                print("[!] No simulation history.")
                return
            keys = list(no.history[0].keys())
            for k in keys:
                line = f"{k:>10}: " + "".join("─" if t[k] else " " for t in no.history)
                print(line)
import tkinter as tk

# --- Nodeクラス（論理ゲートインスタンス） ---
class Node:
    def __init__(no, gate_func, name):
        no.gate_func = gate_func
        no.name = name
        no.inputs = []  # Node or int (0/1)
        no.value = 0
    def eval(no):
        # 入力値を取得（Nodeならevalし値を取る）
        args = []
        for inp in no.inputs:
            if isinstance(inp, Node):
                args.append(inp.eval())
            else:
                args.append(inp)
        no.value = no.gate_func(*args)
        return no.value
    def __repr__(no):
        return f"<Node {no.name} value={no.value}>"

# --- GUI層 ---

class VisualGateEditor(tk.Frame):
    def __init__(no, master):
        super().__init__(master)
        no.master = master
        no.pack()
        no.master.title("論理回路ビジュアルエディタ")

        no.canvas = tk.Canvas(no, width=900, height=600, bg="white")
        no.canvas.pack()

        no.gates = []  # GUI上のゲート情報リスト
        no.nodes = []  # Nodeインスタンスの管理リスト
        no.wires = []  # 配線リスト: ((from_gate, from_pin), (to_gate, to_pin), canvas_line_id)

        no.selected_pin = None  # 接続中のピン情報 (gate, pin_index, canvas_id)

        # ドラッグ＆ドロップ用
        no.drag_data = {"x":0, "y":0, "item":None, "gate":None}

        # GUIイベントバインド
        no.canvas.bind("<ButtonPress-1>", no.on_canvas_press)
        no.canvas.bind("<B1-Motion>", no.on_canvas_drag)
        no.canvas.bind("<ButtonRelease-1>", no.on_canvas_release)

        # サンプルで2入力とANDゲートを配置
        no.input1 = no.create_input_gate(50, 100, init_value=0, name="IN1")
        no.input2 = no.create_input_gate(50, 200, init_value=1, name="IN2")
        no.and_gate = no.create_logic_gate(300, 150, d.And, name="AND")

        # 配線はドラッグで行う（出力→入力）

        # 実行ボタン
        no.btn = tk.Button(no, text="▶ 評価", command=no.evaluate_circuit)
        no.btn.pack(pady=10)

    def create_input_gate(no, x, y, init_value=0, name=None):
        gate = {"kind": "INPUT", "x": x, "y": y, "value": init_value, "name": name or "IN"}
        gate["rect"] = no.canvas.create_rectangle(x, y, x+60, y+40, fill="lightblue")
        gate["text"] = no.canvas.create_text(x+30, y+20, text=gate["name"])
        gate["out_pin"] = no.canvas.create_oval(x+55, y+15, x+65, y+25, fill="blue")

        # Nodeとしても管理
        # 入力は恒等関数 lambda x: x として値は gate["value"]で保持
        node = Node(gate_func=lambda val=gate["value"]: val, name=gate["name"])
        node.value = gate["value"]
        gate["node"] = node
        no.nodes.append(node)

        # クリックでトグル
        def toggle_gate(event, g=gate):
            g["value"] = 1 - g["value"]
            g["node"].value = g["value"]
            no.canvas.itemconfigure(g["text"], text=f"{g['name']}={g['value']}")

        no.canvas.tag_bind(gate["rect"], "<Button-1>", toggle_gate)
        no.canvas.tag_bind(gate["text"], "<Button-1>", toggle_gate)
        no.canvas.tag_bind(gate["out_pin"], "<Button-1>", toggle_gate)

        no.gates.append(gate)
        return gate

    def create_logic_gate(no, x, y, gate_func, name=None):
        gate = {"kind": "LOGIC", "x": x, "y": y, "name": name or "LOGIC"}
        gate["rect"] = no.canvas.create_rectangle(x, y, x+60, y+40, fill="lightgreen")
        gate["text"] = no.canvas.create_text(x+30, y+20, text=gate["name"])
        # 出力ピン
        gate["out_pin"] = no.canvas.create_oval(x+55, y+15, x+65, y+25, fill="green")
        # 入力ピンを2個（例として）
        gate["in_pins"] = [
            no.canvas.create_oval(x-10, y+10, x, y+20, fill="red"),
            no.canvas.create_oval(x-10, y+30, x, y+40, fill="red")
        ]

        node = Node(gate_func=gate_func, name=gate["name"])
        node.value = 0
        gate["node"] = node
        no.nodes.append(node)

        no.gates.append(gate)
        return gate

    def evaluate_circuit(no):
        # 入力ノードの値はGUIの値に連動させる
        for gate in no.gates:
            if gate["kind"] == "INPUT":
                gate["node"].value = gate["value"]

        # 入力接続はここで補完するべき（配線情報からnode.inputs設定）

        # 例: and_gateノードにinput1, input2のnodeを接続
        no.and_gate["node"].inputs = [no.input1["node"], no.input2["node"]]

        # 評価して結果表示
        result = no.and_gate["node"].eval()
        print(f"ANDゲートの出力: {result}")

        # 結果を画面に反映
        no.canvas.itemconfigure(no.and_gate["text"], text=f"{no.and_gate['name']}={result}")
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = VisualGateEditor(root)
        root.mainloop()
    except ValueError as e:
        print(f"エラー: {e}")