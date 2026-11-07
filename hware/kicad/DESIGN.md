# H3 board design

## Purpose

Build a low-cost first board around the Allwinner H3. Use Orange Pi One as
a general reference, with bootable eMMC and external Wi-Fi/Bluetooth added.
This document records agreed requirements; component choices marked pending
are not yet fixed.

## Agreed requirements

| Block | Requirement |
| --- | --- |
| Processor | Allwinner H3 |
| Memory | One DDR3-family chip, 512 MiB total, 16-bit bus |
| Normal boot storage | Bootable eMMC on SDC2 |
| Removable storage | SD card on SDC0 |
| Wired network | 10/100 Mbps Ethernet using the H3 internal PHY |
| Wireless | External Wi-Fi and Bluetooth module |
| USB | Expose all H3 USB interfaces: USB0 OTG and USB1–3 host |
| Video | HDMI output |
| Audio | Stereo analog output and microphone input |

## Memory

Use one **4-Gbit ×16 device (256M ×16), providing 512 MiB**. Exact part
number, speed grade and DDR3 versus DDR3L operating voltage remain pending
cost and availability checks. Match the memory supply, reference network and
bootloader initialization to the selected device and 16-bit bus.

Prefer a short, point-to-point connection with on-die termination and minimal
external termination parts, following a proven H3 single-chip reference.
Avoid a large VTT termination resistor bank where the validated topology
allows. This does not eliminate supply decoupling, VREF generation/filtering,
ZQ calibration resistors or any required clock termination.

Reference candidate: Samsung K4B4G1646B-HCH9, shown as the single DDR3 device
on the NanoPi NEO Core DDR3 sheet. This is a reference candidate, not a final
BOM selection; check exact organization, availability, price and package
before choosing it or a compatible alternative.

The reference candidate now has a single-unit symbol in the local library
and its Samsung datasheet is saved under `dss/`. Its specified supply
is 1.5 V. Exact substitutes must be checked against their own pinout and
mechanical drawing; the same nominal ball count does not establish compatibility.
Sourcing check (2026-11-06): WIN SOURCE lists the exact part, while JLCPCB
lists zero stock. Treat seller stock as provisional and retain the RAM BOM
choice as pending a suitable price and supply source.

This board is fixed at 512 MiB. Do not add a second RAM footprint or upgrade
provisions. A future 1 GiB or 2 GiB product will be a separate board design.

Keep the complete H3 memory interface in the reusable symbol. For this board,
connect only the lanes required for the 16-bit configuration and handle unused
pins according to the H3 reference requirements. The combined DDR3 symbol
unit contains address/control on the left and data on the right.

## Storage and boot

Use SDC2 in 8-bit mode for eMMC, including its reset signal. eMMC capacity
and part number are pending. eMMC is the intended normal boot device, but
the Boot ROM checks for a bootable SD card on SDC0 first. Normal eMMC boot
therefore assumes no bootable SD card is inserted; retain SD for removable
storage and recovery.

The local library includes a three-unit **Kingston EMMC04G-M627-M06U**
4 GB reference component, based on its v1.2 datasheet saved in `dss/`.
This establishes a concrete pinout for schematic work; the final capacity,
supplier and purchasing choice remain pending. Use the H3-supported bus
modes and a matching 3.3 V VCCQ supply, rather than HS400 or 1.8 V modes.
Provide VCC/VCCQ decoupling, required pull-ups and the VDDI capacitor network;
the latter must be checked against Kingston's design guidelines. VDDI is
not a supply input. DS is unused with H3. Leave RFU/VSF/NC unconnected.
The eMMC's unconnected balls are divided between units B and C; unit A holds signals
and power. This split applies to eMMC only.

## Ethernet

Use the integrated **10/100 Mbps PHY**. This is a 100-megabit interface,
not gigabit Ethernet. Provide its required external analog components,
magnetics, RJ45 connection and protection. Connector and magnetics parts
remain pending. An external gigabit PHY is outside the current requirements.

## Wi-Fi and Bluetooth

H3 does not integrate a Wi-Fi or Bluetooth radio. Select an external combo
module with suitable software support and cost. The intended interfaces are
SDC1 for Wi-Fi and UART1 with flow control for Bluetooth; PCM1 is available
if the selected module needs it. Final module, antenna, supplies and
enable/reset/wake GPIO assignments remain pending.

## USB

Provide connectivity for USB0 OTG and all three USB host controllers.
Connector types and arrangement remain pending. Design the VBUS supplies,
host power switches, protection and OTG sensing around the chosen connectors.

## Video and audio

Provide HDMI output, stereo analog line output and microphone input. HDMI
connector, protection, audio connector and microphone configuration remain
pending. Include the required codec reference capacitors, bias and coupling
networks. Analog output is line level; direct speaker drive would require an
additional amplifier, which has not been requested.

## Power, clocks and PCB

Input supply, regulators, rail sequencing, clock components, reset circuit,
PCB dimensions and layer stack remain pending. Select these with the H3 and
chosen memory's electrical and routing requirements in view.

H3 package reference: FBGA347, 14 × 14 mm, 0.65 mm pitch. Verify the actual
H3 ball pattern and land dimensions before assigning a footprint.

## KiCad organization and current status

Work in this directory. Use `h3.kicad_pro`, the local `sym-lib-table` and
`h3.kicad_sym`; the symbol identifier is `h3:H3`.

The H3 symbol contains all 347 balls in 14 functional units, including
separate power and ground units. KiCad CLI loading and SVG export passed.
`h3-pin-map.csv` provides the pin inventory and `preview/` contains unit
previews. See `README.md` for the unit list and symbol details.

The board circuitry and PCB have not yet been implemented. Next, select the
RAM device and supply voltage, then eMMC, the wireless module and power parts
before completing the schematic and verified footprints.

## References

- [Allwinner H3 datasheet v1.2](https://cdn.hackaday.io/files/1872678012031328/Allwinner_H3_Datasheet_V1.2.pdf)
- [Bootable eMMC notes](https://linux-sunxi.org/Bootable_eMMC)
- [NanoPi NEO Core schematic, DDR3 sheet](https://wiki.friendlyelec.com/wiki/images/f/f0/NanoPi_NEO_Core-V1.0_1705.pdf)
