# Project datasheets

All component datasheet fields in the local `h3` library point to this directory.

| File | Manufacturer document | Symbol reference |
| --- | --- | --- |
| `Allwinner_H3_Datasheet_V1.2.pdf` | Allwinner H3 v1.2 | H3 |
| `Samsung_K4B4G1646B_Rev1.0.pdf` | Samsung K4B4G1646B v1.0, January 2012 | K4B4G1646B-HCH9 |
| `Kingston_EMMC04G-M627.pdf` | Kingston EMMC04G-M627-M06U v1.2 | EMMC04G-M627-M06U |

Sources:

- [Allwinner H3](https://cdn.hackaday.io/files/1872678012031328/Allwinner_H3_Datasheet_V1.2.pdf)
- [Samsung DDR3](https://www.unikeyic.com/media/datasheet/49/53/3d5c/49/efcebae6f518c1cf560d3b6f628de334.pdf)
- [Kingston eMMC](https://www1.futureelectronics.com/doc/Kingston/EMMC04G-M627-M06U.pdf)

The Kingston document is the **M06U** variant; do not infer the properties of
another firmware/order suffix from this document. Page 13 contains the
153-ball top-view assignment, and pages 11–12 contain package drawings.
The document labels the interface eMMC 5.0 and explicitly states backwards
compatibility. Its VDDI pin is an internal regulator capacitor node, not a
board supply input. Its DS signal is for HS400 and is unused with the H3.
RFU, VSF and NC balls are not connected on this part; retain their labels
and leave them unconnected in the board design.
