# Tagalog Version / タガログ語版

\=======================================
Programa para sa Digital Logic Circuit Simulation
=================================================

Ang programang ito ay nagsasagawa ng simulation ng digital circuit gamit ang mga pangunahing logic gates at flip-flops (FF) sa Python.

---

■ Nilalaman ■

1. Pangkalahatang-ideya
2. Paggamit at Estruktura ng Klase ng “Raw Gate Version”
3. Paggamit at Estruktura ng Klase ng “easyer.Circuit Version”
4. Mga Katangian at Inirekomendang Paggamit
5. Iba pang mga Tampok
6. Lisensya at Impormasyon sa Pakikipag-ugnayan

---

\=======================================

1. Pangkalahatang-ideya
   \=======================================

* Sinusuportahan ang mga pangunahing logic gates (AND, OR, NOT, NAND, NOR, XOR, XNOR)
* Modele ang mga estado ng flip-flops (T, D, JK, RS)
* Sinusuportahan ang multi-input gates (and\_n, or\_n, atbp.)
* Representasyon ng delay circuits
* Simpleng analog elements tulad ng power supply (VCC) at resistor
* Paggawa ng clock signal (`time_function` class)
* Konstruksyon ng circuit gamit ang Nodes
* May error detection (tinatanggap lamang ang input na 0 o 1)

---

\=======================================
2\. Paggamit at Estruktura ng Klase ng “Raw Gate Version”
=========================================================

■ Pangunahing Klase

* `d_gate`: Logic gate class. Dito naka-defina lahat ng basic gates.

  * Halimbawa: `And(a,b)`, `Not(inp)`, `fa(a,b,cin)` (full adder) atbp.
* `ff_gate`: Flip-flop class

  * Mga method: `t(clk_edge)`, `d(d_val, clk_edge)`, `jk(j,k,clk_edge)`, `rs(r,s)`
* `analog_element`: Mga analog elements tulad ng power supply at resistor

  * Subclass: `VCC`, `Resistor`
* `time_function`: Clock signal generation
* `Node`: Klase para pagdugtungin ang mga input at gates bilang nodes para gumawa ng circuit

■ Simpleng halimbawa (code)

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

■ Halimbawa ng konstruksyon ng circuit

```python
n_and = Node(func=d.And, name="AND")
n_not = Node(func=d.Not, name="NOT")
n_and.inputs = [1, 0]
n_not.inputs = [n_and]

out_and = n_and.eval()
out_not = n_not.eval()
print(f"AND output: {out_and}, NOT output: {out_not}")
```

■ Katangian

* Low-level API na mataas ang flexibility pero mahirap i-manage ang komplikadong circuit
* Kailangan i-manage ang input validation at delays nang sarili

---

\=======================================
3\. Paggamit at Estruktura ng Klase ng “easyer.Circuit Version”
===============================================================

■ Pangunahing Klase at Estruktura

* Nakapaloob sa `easyer` namespace
* Pangunahing klase: `easyer.Circuit`

  * Gumawa ng input terminals: `add_input(name)`
  * Magdagdag ng logic gates: `add_gate(gate_name, input_nodes, name=None)`

    * Sinusuportahan ang mga gate\_name tulad ng 'AND', 'OR', 'NOT', 'XOR', 'NAND', 'NOR', 'XNOR', 'HA', 'FA', 'MUX', atbp.
  * Mag-set ng input values: `set_inputs({name: value, ...})`
  * Patakbuhin ang simulation step: `step()`
  * I-output ang resulta bilang string: `to_string()`
  * Ipakita ang waveform history: `wave_dump()`

■ Simpleng halimbawa (code)

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

■ Internal na estruktura

* Ang `Circuit` ay nagma-manage ng Nodes internally
* Bawat Node ay nage-evaluate gamit ang mga gate functions (methods ng `d_gate`)
* Pinapangalanan ang mga input para sa madaling simulation gamit ang iba't ibang input values
* Tinatala ang waveform history para sa visualization ng


mga signal change sa nakalipas na steps

■ Katangian

* Napakadaling gumawa ng circuit
* Angkop para sa prototyping ng maliit hanggang katamtamang laki ng circuit
* May internal error check para sa kaligtasan
* Sumusuporta sa multi-step simulation (may history)

---

\=======================================
4\. Mga Katangian at Inirekomendang Gamit
=========================================

| Bersyon                | Katangian                                                               | Inirekomendang Gamit                                     |
| ---------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------- |
| Raw Gate Version       | Mataas ang flexibility, malapit sa low-level, maganda para sa pag-aaral | Detalyadong verification ng sariling circuit, pang-aaral |
| easyer.Circuit Version | Madaling gamitin para sa mabilisang prototyping at testing              | Prototyping, medium-scale circuit design                 |

---

\=======================================
5\. Iba pang Tampok
===================

* `time_function` para gumawa ng arbitrary clock waveform
* Simpleng kalkulasyon ng current at voltage gamit ang analog elements (VCC, Resistor)
* Humihinto ang program sa maling input dahil sa error detection
* Maaaring gumawa ng komplikadong combinational circuit gamit ang `Node` class

---

\=======================================
6\. Lisensya at Impormasyon sa Pakikipag-ugnayan
================================================

* Lahat ay pag-aari ng may-akda.
* Para sa mga tanong o bug report: Twitter: @kano\_nandesu, keik: @kano.keik.info

---

\=======================================
Dagdag: Glossary
================

* Input terminal: Node kung saan pumapasok ang mga external na values sa circuit
* Logic gate: Pangunahing yunit ng lohikal na operasyon tulad ng AND, OR, NOT
* Flip-flop: 1-bit memory element na may estado
* Delay: Clock cycles na pagitan ng input change at output change
* Waveform history: Tala ng signal changes sa paglipas ng panahon

---

Ito ang detalyadong paliwanag at paggamit ng programang ito.
Huwag mag-atubiling magtanong kung may katanungan.

---