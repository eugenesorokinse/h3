# DDR3 schematic

`hware/startup/h3-startup/ddr3.kicad_sch` implements one Samsung
K4B4G1646B-HCH9, 512 MiB, x16, at 1.5 V. See [PDF preview](ddr3.pdf).

Three separate KiCad bus aliases group the interface:

- `DDR_ADDR`: SA0–SA14 and SBA0–SBA2.
- `DDR_DATA`: SDQ0–SDQ15, both byte masks, and both differential strobes.
- `DDR_CTRL`: command, reset, differential clock, CKE0, CS0 and ODT0.

Each alias has a labeled bus and individual wire entries at both devices.
DQ bits connect in numeric order within their byte lanes. SA15, the upper two
H3 byte lanes, second-rank controls, and the RAM's five NC balls are marked NC.
Bootloader initialization must select the x16 memory configuration.

Support circuitry follows the NanoPi NEO Core rev 1705 DDR3 sheet (sheet 4):
240 ohm 1% calibration resistors for H3 and RAM, 100 ohm differential clock
termination, a 2k/2k 1% VREF divider, VREF filtering and local bypass capacitors,
and DRAM supply decoupling. Place calibration and clock termination components
at their respective devices and decoupling close to the supply balls.

Global VDD_DRAM, SVREF and GND interfaces connect to the H3 power sheet.
The power sheet must still supply regulated 1.5 V. The RAM purchasing choice,
verified footprints, PCB placement/routing and signal integrity remain pending.

Validation with KiCad 9.0.2 on 2026-11-08:

- SVG and PDF export passed; the page was visually inspected.
- Exported netlist checked all 49 H3-to-RAM signals, all 18 RAM supply balls,
  all 21 RAM ground balls, all 11 H3 DRAM supply balls, shared SVREF,
  and isolation of the unused H3 lanes and rank controls.
- DDR3 sheet ERC has no violations, including bus membership checks.
- Full project ERC reports 322 violations after the text style review. Other
  sheets remain unfinished; undriven VDD_DRAM/GND/SVREF are reported on the
  CPU power sheet. No power flags were added to conceal these pending supplies.

Reference: https://wiki.friendlyelec.com/wiki/images/f/f0/NanoPi_NEO_Core-V1.0_1705.pdf

Text style review: component references, values, net labels and annotations use
1.27 mm (50 mil) text; the page caption uses 2.54 mm (100 mil). Embedded
symbol pin text is preserved. Passive field offsets were tightened to fit the
existing component rows. Netlist connectivity is unchanged by these edits.
