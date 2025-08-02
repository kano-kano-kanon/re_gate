#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
re_gate GUI版 - 論理回路ビジュアルエディタ
直感的なドラッグ＆ドロップ操作で論理回路を設計・シミュレーション
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import math
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple

class GateType(Enum):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    NAND = "NAND"
    NOR = "NOR"
    XOR = "XOR"
    XNOR = "XNOR"
    BUFFER = "BUFFER"

@dataclass
class Pin:
    x: int
    y: int
    canvas_id: int
    connected_wires: List[int]
    
@dataclass
class Gate:
    gate_type: GateType
    x: int
    y: int
    name: str
    canvas_rect: int
    canvas_text: int
    input_pins: List[Pin]
    output_pins: List[Pin]
    value: int = 0
    user_value: int = 0  # INPUT用の手動設定値

@dataclass
class Wire:
    canvas_id: int
    from_gate_id: int
    from_pin_idx: int
    to_gate_id: int
    to_pin_idx: int

class LogicSimulator:
    """論理演算エンジン"""
    
    @staticmethod
    def evaluate_gate(gate_type: GateType, inputs: List[int]) -> int:
        if gate_type == GateType.INPUT:
            return inputs[0] if inputs else 0
        elif gate_type == GateType.OUTPUT:
            return inputs[0] if inputs else 0
        elif gate_type == GateType.AND:
            return int(all(inputs)) if inputs else 0
        elif gate_type == GateType.OR:
            return int(any(inputs)) if inputs else 0
        elif gate_type == GateType.NOT:
            return 1 - inputs[0] if inputs else 1
        elif gate_type == GateType.NAND:
            return 1 - int(all(inputs)) if inputs else 1
        elif gate_type == GateType.NOR:
            return 1 - int(any(inputs)) if inputs else 1
        elif gate_type == GateType.XOR:
            return sum(inputs) % 2 if inputs else 0
        elif gate_type == GateType.XNOR:
            return (sum(inputs) + 1) % 2 if inputs else 1
        elif gate_type == GateType.BUFFER:
            return inputs[0] if inputs else 0
        else:
            return 0

class VisualGateEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("re_gate - 論理回路ビジュアルエディタ v2.0")
        self.master.geometry("1200x800")
        
        # データ構造
        self.gates: Dict[int, Gate] = {}
        self.wires: Dict[int, Wire] = {}
        self.gate_counter = 0
        self.wire_counter = 0
        
        # UI状態
        self.selected_gate = None
        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.connection_mode = False
        self.temp_wire = None
        self.connecting_from = None
        
        # シミュレーター
        self.simulator = LogicSimulator()
        
        self.setup_ui()
        self.create_sample_circuit()

    def setup_ui(self):
        """UI要素を作成"""
        # メインフレーム
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ツールバー
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # ゲート追加ボタン群
        ttk.Label(toolbar, text="ゲート:").pack(side=tk.LEFT, padx=5)
        
        gate_buttons = [
            ("INPUT", GateType.INPUT), ("OUTPUT", GateType.OUTPUT),
            ("AND", GateType.AND), ("OR", GateType.OR), ("NOT", GateType.NOT),
            ("NAND", GateType.NAND), ("NOR", GateType.NOR),
            ("XOR", GateType.XOR), ("XNOR", GateType.XNOR)
        ]
        
        for text, gate_type in gate_buttons:
            btn = ttk.Button(toolbar, text=text, width=6,
                           command=lambda gt=gate_type: self.add_gate_mode(gt))
            btn.pack(side=tk.LEFT, padx=2)
        
        # 操作ボタン群
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        ttk.Button(toolbar, text="接続", command=self.toggle_connection_mode).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="実行", command=self.simulate).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="リセット", command=self.reset_simulation).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="保存", command=self.save_circuit).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="読込", command=self.load_circuit).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="クリア", command=self.clear_all).pack(side=tk.LEFT, padx=5)
        
        # キャンバスフレーム
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # キャンバス（スクロール対応）
        self.canvas = tk.Canvas(canvas_frame, bg="white", width=1000, height=600)
        
        # スクロールバー
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # 配置
        self.canvas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        
        # ステータスバー
        self.status_bar = ttk.Label(main_frame, text="論理回路エディタ準備完了", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # イベントバインド
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<Double-Button-1>", self.on_double_click)
        
        # キーボードショートカット
        self.master.bind("<Delete>", self.delete_selected)
        self.master.bind("<Control-s>", lambda e: self.save_circuit())
        self.master.bind("<Control-o>", lambda e: self.load_circuit())
        self.master.bind("<F5>", lambda e: self.simulate())
        
        self.master.focus_set()  # キーボードフォーカス設定

    def get_gate_color(self, gate_type: GateType) -> str:
        """ゲートタイプに応じた色を返す"""
        colors = {
            GateType.INPUT: "#87CEEB",    # スカイブルー
            GateType.OUTPUT: "#FFB6C1",   # ライトピンク
            GateType.AND: "#98FB98",      # ペールグリーン
            GateType.OR: "#DDA0DD",       # プラム
            GateType.NOT: "#F0E68C",      # カーキ
            GateType.NAND: "#90EE90",     # ライトグリーン
            GateType.NOR: "#DA70D6",      # オーキッド
            GateType.XOR: "#FFE4B5",      # モカシン
            GateType.XNOR: "#FFDAB9",     # ピーチパフ
            GateType.BUFFER: "#E0E0E0"    # ライトグレー
        }
        return colors.get(gate_type, "#FFFFFF")

    def get_pin_count(self, gate_type: GateType) -> Tuple[int, int]:
        """ゲートタイプに応じた入力・出力ピン数を返す"""
        pin_configs = {
            GateType.INPUT: (0, 1),
            GateType.OUTPUT: (1, 0),
            GateType.NOT: (1, 1),
            GateType.BUFFER: (1, 1),
            GateType.AND: (2, 1),
            GateType.OR: (2, 1),
            GateType.NAND: (2, 1),
            GateType.NOR: (2, 1),
            GateType.XOR: (2, 1),
            GateType.XNOR: (2, 1)
        }
        return pin_configs.get(gate_type, (2, 1))

    def add_gate_mode(self, gate_type: GateType):
        """ゲート追加モードに設定"""
        self.status_bar.config(text=f"{gate_type.value}ゲートを配置するためにキャンバスをクリックしてください")
        self.canvas.config(cursor="crosshair")
        self.canvas.bind("<Button-1>", lambda e: self.add_gate(gate_type, e.x, e.y))

    def add_gate(self, gate_type: GateType, x: int, y: int):
        """ゲートを追加"""
        gate_id = self.gate_counter
        self.gate_counter += 1
        
        # ゲート名
        name = f"{gate_type.value}{gate_id}"
        
        # サイズとピン情報
        width, height = 80, 50
        input_count, output_count = self.get_pin_count(gate_type)
        
        # ゲート本体描画
        color = self.get_gate_color(gate_type)
        rect_id = self.canvas.create_rectangle(
            x, y, x + width, y + height, 
            fill=color, outline="black", width=2
        )
        
        text_id = self.canvas.create_text(
            x + width//2, y + height//2, 
            text=gate_type.value, font=("Arial", 10, "bold")
        )
        
        # ピン作成
        input_pins = []
        output_pins = []
        
        # 入力ピン
        for i in range(input_count):
            pin_y = y + height * (i + 1) / (input_count + 1)
            pin_id = self.canvas.create_oval(
                x - 8, pin_y - 4, x + 2, pin_y + 4,
                fill="red", outline="darkred", width=2
            )
            input_pins.append(Pin(x - 3, int(pin_y), pin_id, []))
        
        # 出力ピン
        for i in range(output_count):
            pin_y = y + height * (i + 1) / (output_count + 1)
            pin_id = self.canvas.create_oval(
                x + width - 2, pin_y - 4, x + width + 8, pin_y + 4,
                fill="blue", outline="darkblue", width=2
            )
            output_pins.append(Pin(x + width + 3, int(pin_y), pin_id, []))
        
        # ゲートオブジェクト作成
        gate = Gate(
            gate_type=gate_type,
            x=x, y=y, name=name,
            canvas_rect=rect_id,
            canvas_text=text_id,
            input_pins=input_pins,
            output_pins=output_pins,
            value=0,
            user_value=0 if gate_type == GateType.INPUT else 0
        )
        
        self.gates[gate_id] = gate
        
        # キャンバスアイテムにゲートIDをタグ付け
        self.canvas.addtag_withtag(f"gate_{gate_id}", rect_id)
        self.canvas.addtag_withtag(f"gate_{gate_id}", text_id)
        for pin in input_pins + output_pins:
            self.canvas.addtag_withtag(f"gate_{gate_id}", pin.canvas_id)
        
        # 通常モードに戻る
        self.canvas.config(cursor="")
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.status_bar.config(text=f"{gate_type.value}ゲートを追加しました")

    def toggle_connection_mode(self):
        """接続モードのオン/オフ"""
        self.connection_mode = not self.connection_mode
        if self.connection_mode:
            self.canvas.config(cursor="hand2")
            self.status_bar.config(text="接続モード: 出力ピンから入力ピンへドラッグしてください")
        else:
            self.canvas.config(cursor="")
            self.status_bar.config(text="通常モード")
            if self.temp_wire:
                self.canvas.delete(self.temp_wire)
                self.temp_wire = None
            self.connecting_from = None

    def on_canvas_click(self, event):
        """キャンバスクリック処理"""
        clicked_item = self.canvas.find_closest(event.x, event.y)[0]
        
        if self.connection_mode:
            self.handle_connection_click(event, clicked_item)
        else:
            self.handle_normal_click(event, clicked_item)

    def handle_connection_click(self, event, clicked_item):
        """接続モードでのクリック処理"""
        # ピンクリックの検出
        gate_id, pin_type, pin_idx = self.find_pin_at_item(clicked_item)
        
        if gate_id is not None:
            if pin_type == "output" and self.connecting_from is None:
                # 出力ピンクリック - 接続開始
                self.connecting_from = (gate_id, pin_idx)
                gate = self.gates[gate_id]
                pin = gate.output_pins[pin_idx]
                self.temp_wire = self.canvas.create_line(
                    pin.x, pin.y, event.x, event.y,
                    fill="red", width=3, dash=(5, 5)
                )
                self.status_bar.config(text="入力ピンをクリックして接続を完了してください")
                
            elif pin_type == "input" and self.connecting_from is not None:
                # 入力ピンクリック - 接続完了
                from_gate_id, from_pin_idx = self.connecting_from
                self.create_wire(from_gate_id, from_pin_idx, gate_id, pin_idx)
                
                if self.temp_wire:
                    self.canvas.delete(self.temp_wire)
                    self.temp_wire = None
                self.connecting_from = None
                self.status_bar.config(text="接続が完了しました")

    def handle_normal_click(self, event, clicked_item):
        """通常モードでのクリック処理"""
        # ゲート選択
        gate_id = self.find_gate_at_item(clicked_item)
        if gate_id is not None:
            self.select_gate(gate_id)
            self.drag_data = {"x": event.x, "y": event.y, "item": clicked_item, "gate_id": gate_id}

    def find_pin_at_item(self, item) -> Tuple[Optional[int], Optional[str], Optional[int]]:
        """アイテムIDからピン情報を検索"""
        for gate_id, gate in self.gates.items():
            for i, pin in enumerate(gate.input_pins):
                if pin.canvas_id == item:
                    return gate_id, "input", i
            for i, pin in enumerate(gate.output_pins):
                if pin.canvas_id == item:
                    return gate_id, "output", i
        return None, None, None

    def find_gate_at_item(self, item) -> Optional[int]:
        """アイテムIDからゲートIDを検索"""
        for gate_id, gate in self.gates.items():
            if item in [gate.canvas_rect, gate.canvas_text]:
                return gate_id
        return None

    def create_wire(self, from_gate_id: int, from_pin_idx: int, to_gate_id: int, to_pin_idx: int):
        """配線を作成"""
        from_gate = self.gates[from_gate_id]
        to_gate = self.gates[to_gate_id]
        from_pin = from_gate.output_pins[from_pin_idx]
        to_pin = to_gate.input_pins[to_pin_idx]
        
        # 既存接続をチェック
        for wire in self.wires.values():
            if wire.to_gate_id == to_gate_id and wire.to_pin_idx == to_pin_idx:
                messagebox.showwarning("接続エラー", "この入力ピンは既に接続されています")
                return
        
        # 配線描画
        wire_id = self.canvas.create_line(
            from_pin.x, from_pin.y, to_pin.x, to_pin.y,
            fill="black", width=2, arrow=tk.LAST
        )
        
        # 配線オブジェクト作成
        wire_obj = Wire(
            canvas_id=wire_id,
            from_gate_id=from_gate_id,
            from_pin_idx=from_pin_idx,
            to_gate_id=to_gate_id,
            to_pin_idx=to_pin_idx
        )
        
        wire_counter_id = self.wire_counter
        self.wire_counter += 1
        self.wires[wire_counter_id] = wire_obj
        
        # ピンの接続リストに追加
        from_pin.connected_wires.append(wire_counter_id)
        to_pin.connected_wires.append(wire_counter_id)

    def select_gate(self, gate_id: int):
        """ゲートを選択"""
        # 前の選択を解除
        if self.selected_gate is not None:
            prev_gate = self.gates[self.selected_gate]
            self.canvas.itemconfig(prev_gate.canvas_rect, width=2)
        
        # 新しい選択
        self.selected_gate = gate_id
        gate = self.gates[gate_id]
        self.canvas.itemconfig(gate.canvas_rect, width=4, outline="orange")
        
        self.status_bar.config(text=f"選択: {gate.name} ({gate.gate_type.value})")

    def on_canvas_drag(self, event):
        """ドラッグ処理"""
        if self.connection_mode and self.temp_wire:
            # 接続線の更新
            coords = self.canvas.coords(self.temp_wire)
            self.canvas.coords(self.temp_wire, coords[0], coords[1], event.x, event.y)
        elif self.drag_data["item"] and "gate_id" in self.drag_data:
            # ゲートの移動
            self.move_gate(self.drag_data["gate_id"], 
                          event.x - self.drag_data["x"], 
                          event.y - self.drag_data["y"])
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def move_gate(self, gate_id: int, dx: int, dy: int):
        """ゲートを移動"""
        gate = self.gates[gate_id]
        
        # ゲート本体移動
        self.canvas.move(gate.canvas_rect, dx, dy)
        self.canvas.move(gate.canvas_text, dx, dy)
        
        # ピン移動
        for pin in gate.input_pins + gate.output_pins:
            self.canvas.move(pin.canvas_id, dx, dy)
            pin.x += dx
            pin.y += dy
            
            # 接続されている配線も更新
            for wire_id in pin.connected_wires:
                wire = self.wires[wire_id]
                from_gate = self.gates[wire.from_gate_id]
                to_gate = self.gates[wire.to_gate_id]
                from_pin = from_gate.output_pins[wire.from_pin_idx]
                to_pin = to_gate.input_pins[wire.to_pin_idx]
                
                self.canvas.coords(wire.canvas_id, 
                                 from_pin.x, from_pin.y, 
                                 to_pin.x, to_pin.y)
        
        # 座標更新
        gate.x += dx
        gate.y += dy

    def on_canvas_release(self, event):
        """ドラッグ終了処理"""
        self.drag_data = {"x": 0, "y": 0, "item": None}

    def on_right_click(self, event):
        """右クリックメニュー"""
        clicked_item = self.canvas.find_closest(event.x, event.y)[0]
        gate_id = self.find_gate_at_item(clicked_item)
        
        if gate_id is not None:
            self.show_gate_menu(event, gate_id)

    def show_gate_menu(self, event, gate_id: int):
        """ゲート用コンテキストメニュー"""
        gate = self.gates[gate_id]
        menu = tk.Menu(self.master, tearoff=0)
        
        if gate.gate_type == GateType.INPUT:
            menu.add_command(label=f"値を設定 (現在: {gate.user_value})", 
                           command=lambda: self.set_input_value(gate_id))
        
        menu.add_separator()
        menu.add_command(label="削除", command=lambda: self.delete_gate(gate_id))
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def set_input_value(self, gate_id: int):
        """入力ゲートの値を設定"""
        gate = self.gates[gate_id]
        new_value = 1 - gate.user_value  # トグル
        gate.user_value = new_value
        gate.value = new_value
        
        # 表示更新
        self.canvas.itemconfig(gate.canvas_text, text=f"IN={new_value}")
        self.status_bar.config(text=f"入力値を {new_value} に設定しました")

    def on_double_click(self, event):
        """ダブルクリック処理"""
        clicked_item = self.canvas.find_closest(event.x, event.y)[0]
        gate_id = self.find_gate_at_item(clicked_item)
        
        if gate_id is not None:
            gate = self.gates[gate_id]
            if gate.gate_type == GateType.INPUT:
                self.set_input_value(gate_id)

    def simulate(self):
        """シミュレーション実行"""
        try:
            # トポロジカルソートによる評価順序決定
            evaluation_order = self.topological_sort()
            
            # 各ゲートを順番に評価
            for gate_id in evaluation_order:
                gate = self.gates[gate_id]
                
                if gate.gate_type == GateType.INPUT:
                    gate.value = gate.user_value
                else:
                    # 入力値収集
                    inputs = []
                    for i, pin in enumerate(gate.input_pins):
                        input_value = 0
                        for wire_id in pin.connected_wires:
                            wire = self.wires[wire_id]
                            if wire.to_gate_id == gate_id and wire.to_pin_idx == i:
                                from_gate = self.gates[wire.from_gate_id]
                                input_value = from_gate.value
                                break
                        inputs.append(input_value)
                    
                    # ゲート評価
                    gate.value = self.simulator.evaluate_gate(gate.gate_type, inputs)
                
                # 表示更新
                self.update_gate_display(gate_id)
            
            self.status_bar.config(text="シミュレーション完了")
            
        except Exception as e:
            messagebox.showerror("シミュレーションエラー", f"エラーが発生しました: {str(e)}")

    def topological_sort(self) -> List[int]:
        """トポロジカルソート（評価順序決定）"""
        # 入力ゲートから開始
        visited = set()
        order = []
        
        def dfs(gate_id):
            if gate_id in visited:
                return
            visited.add(gate_id)
            
            gate = self.gates[gate_id]
            
            # 依存ゲートを先に処理
            for pin in gate.input_pins:
                for wire_id in pin.connected_wires:
                    wire = self.wires[wire_id]
                    if wire.to_gate_id == gate_id:
                        dfs(wire.from_gate_id)
            
            order.append(gate_id)
        
        for gate_id in self.gates:
            dfs(gate_id)
        
        return order

    def update_gate_display(self, gate_id: int):
        """ゲート表示更新"""
        gate = self.gates[gate_id]
        
        if gate.gate_type == GateType.INPUT:
            text = f"IN={gate.value}"
        elif gate.gate_type == GateType.OUTPUT:
            text = f"OUT={gate.value}"
        else:
            text = f"{gate.gate_type.value}={gate.value}"
        
        self.canvas.itemconfig(gate.canvas_text, text=text)
        
        # 値に応じて色変更
        if gate.value == 1:
            color = self.lighten_color(self.get_gate_color(gate.gate_type))
        else:
            color = self.get_gate_color(gate.gate_type)
        
        self.canvas.itemconfig(gate.canvas_rect, fill=color)

    def lighten_color(self, color: str) -> str:
        """色を明るくする"""
        # 簡単な実装：固定の明るい色に変更
        light_colors = {
            "#87CEEB": "#E0F6FF",  # スカイブルー -> 薄いブルー
            "#FFB6C1": "#FFE4E1",  # ライトピンク -> 薄いピンク
            "#98FB98": "#F0FFF0",  # ペールグリーン -> 薄いグリーン
            "#DDA0DD": "#F8F8FF",  # プラム -> 薄い紫
            "#F0E68C": "#FFFFF0",  # カーキ -> 薄い黄色
        }
        return light_colors.get(color, "#FFFFFF")

    def reset_simulation(self):
        """シミュレーション結果をリセット"""
        for gate in self.gates.values():
            if gate.gate_type != GateType.INPUT:
                gate.value = 0
            self.update_gate_display(gate.no_id if hasattr(gate, 'no_id') else 0)
        
        self.status_bar.config(text="シミュレーション結果をリセットしました")

    def delete_selected(self, event=None):
        """選択されたゲートを削除"""
        if self.selected_gate is not None:
            self.delete_gate(self.selected_gate)

    def delete_gate(self, gate_id: int):
        """ゲートを削除"""
        if gate_id not in self.gates:
            return
        
        gate = self.gates[gate_id]
        
        # 接続されている配線を削除
        wires_to_delete = []
        for pin in gate.input_pins + gate.output_pins:
            wires_to_delete.extend(pin.connected_wires)
        
        for wire_id in set(wires_to_delete):
            if wire_id in self.wires:
                self.canvas.delete(self.wires[wire_id].canvas_id)
                del self.wires[wire_id]
        
        # キャンバスアイテム削除
        self.canvas.delete(gate.canvas_rect)
        self.canvas.delete(gate.canvas_text)
        for pin in gate.input_pins + gate.output_pins:
            self.canvas.delete(pin.canvas_id)
        
        # ゲート削除
        del self.gates[gate_id]
        
        if self.selected_gate == gate_id:
            self.selected_gate = None
        
        self.status_bar.config(text=f"ゲート {gate.name} を削除しました")

    def clear_all(self):
        """全てクリア"""
        if messagebox.askyesno("確認", "全ての回路をクリアしますか？"):
            self.canvas.delete("all")
            self.gates.clear()
            self.wires.clear()
            self.gate_counter = 0
            self.wire_counter = 0
            self.selected_gate = None
            self.status_bar.config(text="回路をクリアしました")

    def save_circuit(self):
        """回路を保存"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                circuit_data = {
                    "gates": {
                        str(gate_id): {
                            "gate_type": gate.gate_type.value,
                            "x": gate.x, "y": gate.y,
                            "name": gate.name,
                            "user_value": gate.user_value
                        }
                        for gate_id, gate in self.gates.items()
                    },
                    "wires": {
                        str(wire_id): {
                            "from_gate_id": wire.from_gate_id,
                            "from_pin_idx": wire.from_pin_idx,
                            "to_gate_id": wire.to_gate_id,
                            "to_pin_idx": wire.to_pin_idx
                        }
                        for wire_id, wire in self.wires.items()
                    }
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(circuit_data, f, indent=2, ensure_ascii=False)
                
                self.status_bar.config(text=f"回路を保存しました: {filename}")
                
            except Exception as e:
                messagebox.showerror("保存エラー", f"保存に失敗しました: {str(e)}")

    def load_circuit(self):
        """回路を読み込み"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    circuit_data = json.load(f)
                
                # クリア
                self.clear_all()
                
                # ゲート復元
                for gate_id_str, gate_data in circuit_data["gates"].items():
                    gate_id = int(gate_id_str)
                    gate_type = GateType(gate_data["gate_type"])
                    
                    # ゲート追加（簡略版）
                    self.add_gate(gate_type, gate_data["x"], gate_data["y"])
                    
                    # IDと値を復元
                    current_id = self.gate_counter - 1
                    if current_id in self.gates:
                        gate = self.gates[current_id]
                        gate.name = gate_data["name"]
                        gate.user_value = gate_data.get("user_value", 0)
                        
                        # IDを調整
                        if current_id != gate_id:
                            self.gates[gate_id] = gate
                            del self.gates[current_id]
                
                # 配線復元
                for wire_data in circuit_data["wires"].values():
                    self.create_wire(
                        wire_data["from_gate_id"], wire_data["from_pin_idx"],
                        wire_data["to_gate_id"], wire_data["to_pin_idx"]
                    )
                
                self.status_bar.config(text=f"回路を読み込みました: {filename}")
                
            except Exception as e:
                messagebox.showerror("読み込みエラー", f"読み込みに失敗しました: {str(e)}")

    def create_sample_circuit(self):
        """サンプル回路を作成"""
        # 入力ゲート
        self.add_gate(GateType.INPUT, 50, 100)
        input1_id = self.gate_counter - 1
        
        self.add_gate(GateType.INPUT, 50, 200)
        input2_id = self.gate_counter - 1
        
        # ANDゲート
        self.add_gate(GateType.AND, 250, 150)
        and_id = self.gate_counter - 1
        
        # 出力ゲート
        self.add_gate(GateType.OUTPUT, 450, 150)
        output_id = self.gate_counter - 1
        
        # 配線
        self.create_wire(input1_id, 0, and_id, 0)
        self.create_wire(input2_id, 0, and_id, 1)
        self.create_wire(and_id, 0, output_id, 0)
        
        self.status_bar.config(text="サンプル回路を作成しました。入力ゲートをダブルクリックして値を変更できます。")

def main():
    """メイン関数"""
    root = tk.Tk()
    app = VisualGateEditor(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("終了します")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
