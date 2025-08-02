# English Version / 英語版

\=======================================
Digital Logic Circuit Simulation Program
========================================

This program simulates the behavior of digital circuits using basic logic gates and flip-flops (FF) on Python.

---

■ Contents ■

1. Overview
2. Usage and Class Structure of “Raw Gate Version”
3. Usage and Class Structure of “easyer.Circuit Version”
4. Features and Recommended Usage Scenarios
5. Additional Functions
6. License and Contact Information

---

\=======================================

1. Overview
   \=======================================

* Supports basic logic gates (AND, OR, NOT, NAND, NOR, XOR, XNOR)
* Models state transitions of flip-flops (T, D, JK, RS)
* Supports multi-input gates (and\_n, or\_n, etc.)
* Representation of delay circuits
* Simple analog elements model like power supply (VCC) and resistor
* Clock signal generation (`time_function` class)
* Circuit construction using Nodes
* Error detection included (only 0 or 1 input values allowed)

---

\=======================================
2\. Usage and Class Structure of “Raw Gate Version”
===================================================

■ Main Classes

* `d_gate`: Logic gate class. All basic gates are defined here.

  * Examples: `And(a,b)`, `Not(inp)`, `fa(a,b,cin)` (full adder), etc.
* `ff_gate`: Flip-flop class

  * Methods: `t(clk_edge)`, `d(d_val, clk_edge)`, `jk(j,k,clk_edge)`, `rs(r,s)`
* `analog_element`: Analog elements like power supply and resistor

  * Subclasses: `VCC`, `Resistor`
* `time_function`: Clock signal generation
* `Node`: Class to combine inputs and gates as nodes for circuit building

■ Simple example (code)

```python
d = d_gate()
a, b = 1, 0
out_and = d.And(a, b)
out_not = d.Not(a)
print(f"AND({a},{b}) = {out_and}")
print(f"NOT({a}) = {out_not}")

ff = ff_gate()
clk_edge = 1
state_t = ff.t(clk_edge)
print(f"T-FF state: {state_t}")
```

■ Circuit construction example

```python
n_and = Node(func=d.And, name="AND")
n_not = Node(func=d.Not, name="NOT")
n_and.inputs = [1, 0]
n_not.inputs = [n_and]

out_and = n_and.eval()
out_not = n_not.eval()
print(f"AND output: {out_and}, NOT output: {out_not}")
```

■ Features

* Low-level API with high flexibility but complex circuit management
* Need to manually manage input validation and delays

---

\=======================================
3\. Usage and Class Structure of “easyer.Circuit Version”
=========================================================

■ Main Classes and Structure

* Grouped under the `easyer` namespace
* Main class: `easyer.Circuit`

  * Create input terminals: `add_input(name)`
  * Add logic gates: `add_gate(gate_name, input_nodes, name=None)`

    * gate\_name supports 'AND', 'OR', 'NOT', 'XOR', 'NAND', 'NOR', 'XNOR', 'HA', 'FA', 'MUX', etc.
  * Set input values: `set_inputs({name: value, ...})`
  * Execute simulation step: `step()`
  * Output results as string: `to_string()`
  * Display waveform history: `wave_dump()`

■ Simple example (code)

```python
import easyer

circuit = easyer.Circuit()
a = circuit.add_input('a')
b = circuit.add_input('b')

not_a = circuit.add_gate('NOT', [a], name='not_a')
and_gate = circuit.add_gate('AND', [not_a, b], name='and_gate')

circuit.set_inputs({'a': 0, 'b': 1})
circuit.step()

print(circuit.to_string())
print(circuit.wave_dump())
```

■ Internal structure

* `Circuit` manages Nodes internally
* Each Node evaluates by using gate functions (methods of `d_gate`)
* Inputs managed by name, allowing multiple simulations with different input values
* Waveform history accumulates signal changes over past steps for visualization

■ Features

* Very simple and easy circuit construction
* Suitable for prototyping small to medium circuits
* Internal error checks ensure high safety
* Supports multi-step simulation (keeps history)

---

\=======================================
4\. Features and Recommended Usage Scenarios
============================================

| Version                | Features                                                | Recommended Use Cases                             |
| ---------------------- | ------------------------------------------------------- | ------------------------------------------------- |
| Raw Gate Version       | High flexibility, close to low-level, good for learning | Detailed self-made circuit verification, learning |
| easyer.Circuit Version | Easy operation for fast prototyping and testing         | Prototyping, medium-scale circuit design          |

---

\=======================================
5\. Additional Functions
========================

* `time_function` class for arbitrary clock waveform creation
* Simple current and voltage calculations using analog elements (VCC, Resistor)
* Program stops on invalid inputs by error detection
* Complex combinational circuit construction possible using `Node` class

---

\=======================================
6\. License and Contact Information
===================================

* All rights reserved by the author.
* Contact or bug reports: Twitter: @kano\_nandesu, keik: @kano.keik.info

---

\=======================================
Supplementary: Glossary
=======================

* Input terminal: Node where external values are input to the circuit
* Logic gate: Basic logic operation unit such as AND, OR, NOT
* Flip-flop: 1-bit memory element, circuit with state
* Delay: Clock cycles delay from input change to output change
* Waveform history: Record of signal changes over time

---

This concludes the detailed explanation and usage of this program.
Feel free to contact us if you have any questions.

---