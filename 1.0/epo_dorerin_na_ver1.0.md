# Nauruan Version / ナウル語版

\=======================================
E Diigitāl Lojiik Saraamot Cirkit Sisimuleshon Proguraam
========================================================

Proguraam e sisimuleet diigitāl cirkit e keriden, menan basic lojiik geet menan flip-flop (FF) e Python.

---

■ Diigon ■

1. Obeerviuw
2. Uusij menan Klass Stakichoa e “Ro Gwate Vershon”
3. Uusij menan Klass Stakichoa e “easyer.Circuit Vershon”
4. Feachoor menan Rekoomended Uusij
5. Adishiniil Fankshon
6. Laisens menan Kontekt Infomeeshon

---

\=======================================

1. Obeerviuw
   \=======================================

* Sapoot menan basic lojiik geet (AND, OR, NOT, NAND, NOR, XOR, XNOR)
* Modil steit transishon menan flip-flop (T, D, JK, RS)
* Sapoot menan multi-input geet (and\_n, or\_n, etc.)
* Represin delai cirkit
* Simpol analog elemen menan paawa (VCC) menan resisitor
* Klok sigin jenenreshon (`time_function` klass)
* Cirkit konstukshen yuusij Nodes
* Eror detekshon (i o 1 nom ae innput valiu e alleweed)

---

\=======================================
2\. Uusij menan Klass Stakichoa e “Ro Gwate Vershon”
====================================================

■ Meen Klass

* `d_gate`: Lojiik geet klass. Ol basic geet e defin.

  * Eksampol: `And(a,b)`, `Not(inp)`, `fa(a,b,cin)` (ful adaer) etc.
* `ff_gate`: Flip-flop klass

  * Metod: `t(clk_edge)`, `d(d_val, clk_edge)`, `jk(j,k,clk_edge)`, `rs(r,s)`
* `analog_element`: Analog elemen menan paawa menan resisitor

  * Subklass: `VCC`, `Resistor`
* `time_function`: Klok sigin jenenreshon
* `Node`: Klass e kombain innput menan geet yuusij cirkit bilding

■ Simpol eksampol (kood)

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

■ Cirkit konstukshen eksampol

```python
n_and = Node(func=d.And, name="AND")
n_not = Node(func=d.Not, name="NOT")
n_and.inputs = [1, 0]
n_not.inputs = [n_and]

out_and = n_and.eval()
out_not = n_not.eval()
print(f"AND output: {out_and}, NOT output: {out_not}")
```

■ Feachoor

* Lo-liivul API menan haif fleksibiliti but komplek cirkit manidjmen
* Nid yuusij self menan innput valideshon menan delai

---

\=======================================
3\. Uusij menan Klass Stakichoa e “easyer.Circuit Vershon”
==========================================================

■ Meen Klass menan Stakichoa

* Grup e yuusij `easyer` namespace
* Meen klass: `easyer.Circuit`

  * Mek innput terminol: `add_input(name)`
  * Ad geet: `add_gate(gate_name, input_nodes, name=None)`

    * gate\_name sapoot: 'AND', 'OR', 'NOT', 'XOR', 'NAND', 'NOR', 'XNOR', 'HA', 'FA', 'MUX' etc.
  * Set innput valiu: `set_inputs({name: value, ...})`
  * Run simiuleeshon step: `step()`
  * Output risolt az string: `to_string()`
  * Show waveform history: `wave_dump()`

■ Simpol eksampol (kood)

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

■ Internol strakture

* `Circuit` e manidj Nodes internally
* Ol Node e eval yuusij geet funksion (d\_gate metod)
* Innput e nemd for easy simiuleshon usin difren innput valiu
* Waveform history rekod ol signal change fo past step

■ Feachoor

* Simpol menan izi cirkit konstrakshen
* Gud fo prototayping smol to mediyum cirkit
* Internal eror chek fo sefuriti
* Sapoot multi-step simiuleshon (history)

---

\=======================================
4\. Feachoor menan Rekoomended Uusij
====================================

| Vershon          | Feachoor                                            | Rekoomended Yusij                         |
| ---------------- | --------------------------------------------------- | ----------------------------------------- |
| Ro Gwate Vershon | Haif fleksibiliti, klos to lo-liivul, gud fo lernin | Detailyed self-meid cirkit chek, lernin   |
| easyer.Circuit   | Izi opreshon fo fast prototyping menan testin       | Prototayping, mediyum-skeil cirkit design |

---

\=======================================
5\. Adishiniil Fankshon
=======================

* `time_function` klas fo meik arbitrare klok waveform
* Simpol current menan voltage kalkuleshon yuusij analog elemen (VCC, Resistor)
* Program stop on invalid innput by eror detekshon
* Komplek combinational cirkit bilding posibol yuusij `Node` klas

---

\=======================================
6\. Laisens menan Kontekt Infomeeshon
=====================================

* Ol raet riserv baimen ol autor.
* Kontak o bug report: Twitter: @kano\_nandesu, keik: @kano.keik.info

---

\=======================================
Supplement: Glossari
====================

* Innput terminol: Node wea external valiu e go to cirkit
* Lojiik geet: Basic lojiik opreshon unit olsem AND, OR, NOT
* Flip-flop: 1-bit memori elemen menan steit
* Delai: Klok saikel betwin innput change menan output change
* Waveform history: Rekod signal change long taim

---

Dis is da detailyed eksplaneshon menan uusij fo dis proguraam.
Plis ask if yu hav eni kwestshon.
---------------------------------