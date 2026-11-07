# Allwinner H3 symbol

See [DESIGN.md](DESIGN.md) for board requirements and pending component choices.
See [RULES.md](RULES.md) for symbol layout and library editing rules.

Local library: `h3.kicad_sym`, symbol `h3:H3`. The project-local
`sym-lib-table` resolves the library in this directory, independently of the
global library of the same name in the older t113 project.
Open `h3.kicad_pro` to use this project-local library registration.

The same library also contains `h3:K4B4G1646B-HCH9`, a **single-unit**
Samsung 512 MiB x16 DDR3 symbol. All 96 balls, including the five NC balls,
are represented individually. Pins use the left and right sides only, with
100 mil pitch within functional groups and 200 mil between groups.
The ball map was checked against page 6 of
the [downloaded Samsung datasheet](dss/Samsung_K4B4G1646B_Rev1.0.pdf).
This part uses 1.5 V and a 10 × 13.3 mm, 0.8 mm pitch package. Its footprint
is pending verification. `ddr3-pin-map.csv` records the pins, and
`build_ddr3.py` regenerates this symbol while preserving the H3 component.
The H3 generator also preserves other library components.

Other x16 DDR3 devices may share this ball map, but substitutes require
checking the exact datasheet, supply voltage, package and timing settings.

`h3:EMMC04G-M627-M06U` is a three-unit Kingston 4 GB eMMC reference
component in the same library. Unit A contains signals and power; units B
and C share the NC, RFU and VSF balls. All 153 balls remain visible and individually
numbered. It follows the same two-side layout and 100/200 mil
spacing rules, with a 30.48 mm body width. `build_emmc.py` regenerates it;
`emmc-pin-map.csv` provides its ball inventory. The pinout was checked
against page 13 of the [Kingston datasheet](dss/Kingston_EMMC04G-M627.pdf).
Footprint and final purchasing part remain pending. Use a 3.3 V I/O supply
for the intended H3 SDC2 arrangement; do not assume HS400 operation on H3.

All three component datasheets are copied into the project-root `dss/`
directory, and the symbols' Datasheet properties reference those local PDFs.

All 347 package balls appear exactly once, with visible individual power and
ground pins. All H3 units use left/right pins only, 100 mil pitch within
functional groups and 200 mil spacing between groups. Package: FBGA347,
14 × 14 mm, 0.65 mm pitch. Footprint assignment
is intentionally empty pending a verified H3-specific ball-pattern footprint;
a generic 347-ball footprint should not be assumed compatible.

| Unit | Function |
| --- | --- |
| A | DDR3 address, control and 32-bit data |
| B | eMMC - SDC2 |
| C | SD card - SDC0 |
| D | Ethernet PHY and MAC / GPIO D |
| E | Wi-Fi SDIO and Bluetooth UART / PCM |
| F | USB0 OTG and USB1-3 host |
| G | HDMI |
| H | Audio codec and TV |
| I | Clocks, reset and boot |
| J | GPIO A and remaining GPIO C |
| K | Camera / GPIO E |
| L | Always-on GPIO L |
| M | Power supplies and DRAM reference |
| N | Ground |

## Design intent

First board memory target: **512 MiB using one 4-Gbit x16 DDR3-family chip**,
with a 16-bit memory bus. Exact part number and DDR3 versus DDR3L supply
voltage remain to be selected by cost and availability. Configure the
bootloader for the selected device and 16-bit bus. Keep the full H3 memory
interface in the reusable SoC symbol; unused upper byte lanes are handled
in the board schematic following the H3 reference requirements.

A separate future board targets 1 GiB or 2 GiB. Candidate configurations are two
4-Gbit x16 devices for 1 GiB or two 8-Gbit x16 devices for 2 GiB on the
32-bit bus, subject to checking exact device geometry and bootloader support.
That is a separate board design. This first board is fixed at one chip and
512 MiB, with no upgrade provision or extra RAM footprint required.

Use Orange Pi One as a general H3 reference, with eMMC and external wireless
added for this board. The symbol describes the SoC, not a complete Orange Pi
board or its connector wiring. No external memory, wireless module, Ethernet
magnetics, protection, regulators or decoupling are included yet.

- eMMC on SDC2 is the intended normal system storage. The Boot ROM checks SD
  (SDC0) before eMMC; a bootable SD card can take priority. This symbol does
  not change ROM boot policy. Keep SD nonbootable or absent for normal eMMC boot.
- Wi-Fi and Bluetooth require an external module. Unit E exposes the usual
  SDIO, UART with flow control, and PCM interfaces; enable/reset/wake signals
  can be allocated from remaining GPIO once a module is selected.
- Internal Ethernet PHY is for 10/100 operation and requires the external
  analog network and magnetics. GPIO D exposes the alternative external PHY
  MAC interface; multiplexed functions are alternatives on the same balls.
- USB OTG ID/VBUS sensing and host VBUS switching need board-level circuitry
  and GPIO allocation. The dedicated USB data pins are all present in unit F.
- Audio outputs are line level. Speakers need an amplifier; microphone bias,
  AC coupling and codec reference capacitors need external circuitry.
- GPIO labels show selected useful mux functions. They retain the port names;
  this is not an exhaustive listing of every mux choice. Digital GPIO pins
  use bidirectional ERC types because software selects their direction.
- Analog pins without an unambiguous fixed direction use passive ERC type.
  Analog support networks must be reviewed separately. All supply and ground
  balls use `power_in`; K4 is explicitly `no_connect`.

## Sources and verification

- [Allwinner H3 datasheet v1.2](https://cdn.hackaday.io/files/1872678012031328/Allwinner_H3_Datasheet_V1.2.pdf),
  Table 3-1 (printed pages 66–73), Table 3-2 (74–77), package appendix (613–614).
- [linux-sunxi bootable eMMC documentation](https://linux-sunxi.org/Bootable_eMMC).

`h3-pin-map.csv` lists ball, original datasheet name, displayed name, unit and
ERC type for review. KiCad 9 CLI successfully loads and exports all 14 units;
SVG previews are in `preview/`. This verifies format and pin coverage, not a
finished board design or PCB footprint.

`build_h3.py` reproduces the library using the datasheet's `pdftotext -layout`
output at `/tmp/h3-v12.txt`. It checks 347 unique balls and explicitly handles
the five rows interrupted by the PDF watermark and multiline supply lists.
