"""Build H3 symbol from Allwinner H3 datasheet v1.2 Table 3-1 text extraction."""
import re, json, csv
from pathlib import Path

source = Path('/tmp/h3-v12.txt').read_text()
table = source[source.index('Table 3-1. Pin Characteristics'):source.index('3.2. GPIO Multiplexing Functions', source.index('Table 3-1. Pin Characteristics'))]
pins = {}
for line in table.splitlines():
    m = re.match(r'^\s*([A-Z]{1,2}\d+)\s+(\S+)\s+(?:DRAM|GPIO|POWER|Power|-)\s+(I/O|I|O|A|P|G|-)\s+', line)
    if m:
        ball, name, typ = m.groups()
        pins[ball] = [name, typ]

power = {
 'VCC-DRAM':'L16 M16 N16 P16 P17 R16 T12 T13 T14 T15 U11',
 'VCC_IO':'G13 G14 G15 H13 H14 J14',
 'VDD_CPUX':'N8 P6 P7 P8 P9 R6 R7 R8 T6 T7 T8 U6 U9',
 'VDD_CPUS':'J7 J8',
 'VDD-SYS':'H10 J10 J11 J12 K10 K11 K12 L10 L11 L12 L13 L14',
 'GND':'A21 AA1 G8 H12 H15 J13 J16 J9 K13 K14 K15 K16 K7 K8 K9 L15 L8 L9 M10 M11 M12 M13 M14 M15 M7 M8 M9 N10 N11 N12 N13 N14 N15 N7 N9 P10 P11 P12 P13 P14 P15 R10 R11 R12 R13 R14 R9 T11',
}
for name, balls in power.items():
    for ball in balls.split():
        assert ball not in pins
        pins[ball] = [name, 'G' if name == 'GND' else 'P']
# Five table rows have their type displaced onto the following line by the watermark.
for ball,name,typ in [('V20','SA3','I/O'),('Y16','SDQ18','I/O'),('B20','PD2','I/O'),('G18','PF6','I/O'),('A2','EPHY_LINK_LED','A')]:
    assert ball not in pins
    pins[ball] = [name,typ]
assert len(pins) == 347, len(pins)

titles = ['DDR3 address and control','DDR3 data - 32 bit','eMMC - SDC2','SD card - SDC0','Ethernet PHY and MAC','Wi-Fi SDIO and Bluetooth UART PCM','USB0 OTG and USB1-3 host','HDMI','Audio codec and TV','Clocks reset and boot','GPIO UART SPI I2C','Camera CSI and GPIO E','Always-on GPIO L','Power supplies','Ground']
units = [[] for _ in titles]
emmc = {5:'CLK',6:'CMD',**{i+8:f'D{i}' for i in range(8)},16:'RST'}
sd = ['D1','D0','CLK','CMD','D3','D2','DET']
pg = ['SDC1_CLK','SDC1_CMD','SDC1_D0','SDC1_D1','SDC1_D2','SDC1_D3','UART1_TX','UART1_RX','UART1_RTS','UART1_CTS','PCM1_SYNC','PCM1_CLK','PCM1_DOUT','PCM1_DIN']
pd = ['RGMII_RXD3','RGMII_RXD2','RGMII_RXD1','RGMII_RXD0','RGMII_RXCK','RGMII_RXCTL','MII_RXERR','RGMII_TXD3','RGMII_TXD2','RGMII_TXD1','RGMII_TXD0','MII_CRS','RGMII_TXCK','RGMII_TXCTL','MII_TXERR','RGMII_CLKIN','MDC','MDIO']
pa = ['UART2_TX','UART2_RX','UART2_RTS','UART2_CTS','UART0_TX','UART0_RX/PWM0','SIM_PWREN','SIM_CLK','SIM_DATA','SIM_RST','SIM_DET','TWI0_SCK','TWI0_SDA','SPI1_CS/UART3_TX','SPI1_CLK/UART3_RX','SPI1_MOSI/UART3_RTS','SPI1_MISO/UART3_CTS','OWA_OUT','PCM0_SYNC/TWI1_SCK','PCM0_CLK/TWI1_SDA','PCM0_DOUT','PCM0_DIN']
pl = ['S_TWI_SCK','S_TWI_SDA','S_UART_TX','S_UART_RX','S_JTAG_MS','S_JTAG_CK','S_JTAG_DO','S_JTAG_DI','','','S_PWM','S_CIR_RX']
audio = 'LINEINL LINEINR LINEOUTL LINEOUTR MBIAS MICIN1N MICIN1P MICIN2N MICIN2P VRA1 VRA2 VRP TVOUT'.split()
for ball,(name,typ) in pins.items():
    label = name
    if typ == 'G': u=14
    elif typ == 'P': u=13
    elif name.startswith(('SDQ','SDM')): u=1
    elif name.startswith('S') and not name.startswith(('SPI',)): u=0
    elif re.fullmatch(r'PC\d+',name) and int(name[2:]) in emmc:
        u=2; label=f'{name}/SDC2_{emmc[int(name[2:])]}'
    elif name.startswith('PF'):
        u=3; label=f'{name}/SDC0_{sd[int(name[2:])]}'
    elif name.startswith('EPHY_') or name.startswith('PD'):
        u=4
        if name.startswith('PD'): label=f'{name}/{pd[int(name[2:])]}'
    elif name.startswith('PG'):
        u=5; label=f'{name}/{pg[int(name[2:])]}'
    elif name.startswith('USB_'): u=6
    elif name.startswith('H'): u=7
    elif name in audio: u=8
    elif name.startswith('PA'):
        u=10; label=f'{name}/{pa[int(name[2:])]}'
    elif name.startswith('PC'):
        u=10
        if int(name[2:])<4: label += '/'+['SPI0_MOSI','SPI0_MISO','SPI0_CLK','SPI0_CS'][int(name[2:])]
    elif name.startswith('PE'):
        u=11; i=int(name[2:]); f= ['CSI_PCLK','CSI_MCLK','CSI_HSYNC','CSI_VSYNC']+[f'CSI_D{k}' for k in range(8)]+['CSI_SCK/TWI2_SCK','CSI_SDA/TWI2_SDA','','']
        if f[i]: label += '/'+f[i]
    elif re.fullmatch(r'PL\d+',name):
        u=12
        if pl[int(name[2:])]: label += '/'+pl[int(name[2:])]
    else: u=9
    electrical={'I/O':'bidirectional','I':'input','O':'output','A':'passive','P':'power_in','G':'power_in','-':'no_connect'}[typ]
    if name in ['LINEINL','LINEINR','MICIN1N','MICIN1P','MICIN2N','MICIN2P','HHPD','X24MIN','X32KIN','KEYADC']: electrical='input'
    if name in ['LINEOUTL','LINEOUTR','MBIAS','TVOUT','HTX0N','HTX0P','HTX1N','HTX1P','HTX2N','HTX2P','HTXCN','HTXCP']: electrical='output'
    units[u].append((ball,label,electrical,name))

q=json.dumps
def natural(s):
    return [int(t) if t.isdigit() else t for t in re.split(r'(\d+)',s)]
for index,group in enumerate(units):
    if index == 6:
        group.sort(key=lambda p:(int(p[3][-1]), 0 if '_DP' in p[3] else 1))
    else:
        group.sort(key=lambda p:(natural(p[3]), natural(p[0])))
# One DDR3 unit, with address/control on the left and data on the right.
ddr_left_count = len(units[0])
units[0].extend(units.pop(1))
titles.pop(1)
titles[0] = 'DDR3 memory'
out=['(kicad_symbol_lib (version 20241209) (generator "h3_symbol_builder")', '(symbol "H3" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)', '(property "Reference" "U" (at 0 5.08 0) (effects (font (size 1.27 1.27))))', '(property "Value" "H3" (at 0 2.54 0) (effects (font (size 1.27 1.27))))']
for key,value in [('Footprint',''),('Datasheet','${KIPRJMOD}/dss/Allwinner_H3_Datasheet_V1.2.pdf'),('Description','Allwinner H3 quad Cortex-A7, FBGA347 14x14mm pitch 0.65mm; 14 functional units')]:
    out.append(f'(property {q(key)} {q(value)} (at 0 0 0) (effects (font (size 1.27 1.27)) hide))')
rows=[]
def function_group(unit, raw):
    if unit == 1:
        if raw.startswith('SDQ'):
            lane = int(re.search(r'\d+',raw).group())
            return ('data', lane//8 if re.fullmatch(r'SDQ\d+',raw) else lane)
        for prefix in ['SA','SBA','SCKE','SCK','SCS','SODT']:
            if raw.startswith(prefix): return ('control',prefix)
        return ('control','commands' if raw in ['SCAS','SRAS','SWE','SRST'] else raw)
    if unit in [2,3]:
        if raw in ['PC5','PF2']: return 'clock'
        if raw in ['PC6','PF3']: return 'command'
        if raw in ['PC16','PF6']: return 'reset_detect'
        return 'data'
    if unit == 4:
        if raw.startswith('PD'):
            i=int(raw[2:]); return 'MAC_RX' if i<=6 else 'MAC_TX' if i<=15 else 'MAC_management'
        if raw in ['EPHY_RXN','EPHY_RXP']: return 'PHY_RX'
        if raw in ['EPHY_TXN','EPHY_TXP']: return 'PHY_TX'
        return 'PHY_LED' if 'LED' in raw else 'PHY_bias'
    if unit == 5:
        i=int(raw[2:]); return 'SDIO' if i<6 else 'UART' if i<10 else 'PCM'
    if unit == 6: return raw[-1]  # Keep each USB differential pair together.
    if unit == 7:
        if raw.startswith('HTX'): return raw[:4]
        return 'DDC' if raw in ['HSCL','HSDA'] else raw
    if unit == 8:
        for prefix in ['LINEIN','LINEOUT','MICIN1','MICIN2']:
            if raw.startswith(prefix): return prefix
        return 'references' if raw in ['VRA1','VRA2','VRP'] else raw
    if unit == 9:
        if raw.startswith('X24'): return '24MHz'
        if raw.startswith('X32'): return '32kHz'
        if raw.startswith('JTAG'): return 'JTAG'
        if raw in ['UBOOT','TEST']: return 'boot_test'
        if raw in ['RESET','NMI']: return 'reset_interrupt'
        return raw
    if unit == 10:
        if raw.startswith('PC'): return 'SPI0' if int(raw[2:])<4 else 'GPIO_C'
        i=int(raw[2:]); return 'UART2' if i<4 else 'UART0' if i<6 else 'SIM' if i<11 else 'TWI0' if i<13 else 'SPI1_UART3' if i<17 else 'OWA' if i==17 else 'PCM0_TWI1'
    if unit == 11:
        i=int(raw[2:]); return 'timing' if i<4 else 'data' if i<12 else 'I2C' if i<14 else 'GPIO'
    if unit == 12:
        i=int(raw[2:]); return 'TWI' if i<2 else 'UART' if i<4 else 'JTAG' if i<8 else 'GPIO' if i<10 else raw
    return raw  # Supplies and grounds stay grouped by rail/domain.

for unit,group in enumerate(units,1):
    functional={}
    for pin in group:
        functional.setdefault(function_group(unit,pin[3]),[]).append(pin)
    blocks=list(functional.values())
    if unit == 1:
        sides=[[b for k,b in functional.items() if k[0]=='control'],
               [b for k,b in functional.items() if k[0]=='data']]
    elif unit == 14:
        # Balance ground pins across both sides, splitting the common GND rail.
        split = len(group) // 2
        sides = []
        for side_pins in [group[:split], group[split:]]:
            domains = {}
            for pin in side_pins:
                domains.setdefault(pin[3], []).append(pin)
            sides.append(list(domains.values()))
    else:
        # Split only between functional groups, keeping pairs and buses intact.
        split=min(range(len(blocks)+1),key=lambda i:abs(sum(len(b)+1 for b in blocks[:i])-sum(len(b)+1 for b in blocks[i:])))
        sides=[blocks[:split],blocks[split:]]
    placements=[]
    for side,side_blocks in enumerate(sides):
        row=2
        for block in side_blocks:
            for pin in block:
                placements.append((side,row,pin)); row+=1
            row+=1  # Next group's first pin is 200 mil from the previous pin.
    last_row=max(row for side,row,pin in placements)
    half= max(15.24, round((max(len(p[1]) for p in group)*0.64+3)/2.54)*2.54)
    top=0; bottom=round(-(last_row+2)*2.54,3)
    out.append(f'(symbol "H3_{unit}_1" (unit_name {q(titles[unit-1])})')
    out.append(f'(rectangle (start {-half} {top}) (end {half} {bottom}) (stroke (width 0.254) (type default)) (fill (type background)))')
    out.append(f'(text {q(titles[unit-1])} (at 0 -2.54 0) (effects (font (size 1.016 1.016))))')
    for side,row,(ball,label,typ,raw) in placements:
        y=round(-row*2.54,3); x=half+5.08 if side else -half-5.08; angle=180 if side else 0
        out.append(f'(pin {typ} line (at {x} {y} {angle}) (length 5.08) (name {q(label)} (effects (font (size 1.016 1.016)))) (number {q(ball)} (effects (font (size 1.016 1.016)))))')
        rows.append([ball,raw,label,unit,titles[unit-1],typ])
    out.append(')')
out += [')',')']
from library_tools import save_symbol
save_symbol('H3', '\n'.join(out[1:-1]))
with open('h3-pin-map.csv','w') as f:
    w=csv.writer(f); w.writerow(['Ball','Datasheet name','Symbol label','Unit','Function','Electrical type']); w.writerows(rows)
print(f'Created {len(rows)} unique pins in {len(units)} units')
