# Symbol library rules

These rules apply to components created or edited in this project's local
`h3.kicad_sym` library. Keep the generators consistent with the saved symbols.

## Layout

- Place pins on **two sides only: left and right**. Do not place supply,
  ground or other pins on the top or bottom edges.
- Use **100 mil (2.54 mm)** pin pitch within each functional group.
- Use **200 mil (5.08 mm)** between the last pin of one group and the first
  pin of the next group on the same side. This is double the normal pitch,
  equivalent to leaving one unused pin position between groups.
- Group pins by function. Keep differential pairs, byte lanes, buses and
  supply/ground domains together; split sides only between complete groups.
- Preserve numeric order within buses and logical order within byte lanes.
- Size each body to fit its pin groups and readable labels without overlap.
- Use visible pin names and ball numbers. Show individual supply and ground
  balls; do not stack or hide them.

## Component structure

- Keep the H3 processor divided into functional units. Its DDR3 address,
  control and data interface stays in one unit, with address/control on the
  left and data byte lanes on the right.
- Keep the DDR3 memory device as **one unit**, including power and ground.
- For eMMC, use unit A for functional signals and power, and divide NC,
  RFU and VSF balls between units B and C with balanced heights. Keep all
  balls visible and individually numbered.
- Match the DDR3 memory symbol's body width to the H3 DDR3 unit: currently
  **1200 mil (30.48 mm)**.
- Preserve ball identifiers, electrical types and all existing components
  when changing layout or regenerating a symbol.
- Check ball maps against the exact device datasheet. Mark NC balls explicitly.
- Assign footprints only after checking package dimensions and ball patterns.

## Project files and verification

- Store project components in this directory's `h3.kicad_sym`, registered
  through the local `sym-lib-table` as `h3`.
- Update pin inventories and SVG previews when symbols change.
- Verify pin counts, unique ball identifiers, two-side placement, spacing,
  and successful KiCad loading/export after layout edits.
