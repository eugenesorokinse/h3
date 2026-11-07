"""Three-unit Kingston eMMC symbol; ball map from M06U datasheet v1.2 p13."""
import csv
import json
from collections import defaultdict
from library_tools import save_symbol

part='EMMC04G-M627-M06U'
# Dashes denote unpopulated locations, not NC balls. Top view, columns 1..14.
matrix={
 'A':'NC NC DAT0 DAT1 DAT2 VSS RFU NC NC NC NC NC NC NC',
 'B':'NC DAT3 DAT4 DAT5 DAT6 DAT7 NC NC NC NC NC NC NC NC',
 'C':'NC VDDI NC VSSQ NC VCCQ NC NC NC NC NC NC NC NC',
 'D':'NC NC NC NC - - - - - - - NC NC NC',
 'E':'NC NC NC - RFU VCC VSS VSF VSF VSF - NC NC NC',
 'F':'NC NC NC - VCC - - - - VSF - NC NC NC',
 'G':'NC NC RFU - VSS - - - - VSF - NC NC NC',
 'H':'NC NC NC - DS - - - - VSS - NC NC NC',
 'J':'NC NC NC - VSS - - - - VCC - NC NC NC',
 'K':'NC NC NC - ~{RST_n} RFU RFU VSS VCC VSF - NC NC NC',
 'L':'NC NC NC - - - - - - - - NC NC NC',
 'M':'NC NC NC VCCQ CMD CLK NC NC NC NC NC NC NC NC',
 'N':'NC VSSQ NC VCCQ VSSQ NC NC NC NC NC NC NC NC NC',
 'P':'NC NC VCCQ VSSQ VCCQ VSSQ RFU NC NC RFU NC NC NC NC',
}
pins={}
for r,ns in matrix.items():
    names=ns.split(); assert len(names)==14
    for c,n in enumerate(names,1):
        if n!='-': pins[f'{r}{c}']=n
assert len(pins)==153
def signal(name):return [(b,n) for b,n in pins.items() if n==name]
left=[signal('CLK'),signal('CMD'),signal('~{RST_n}'),signal('VDDI'),signal('VCC'),signal('VCCQ')]
right=[[p for i in range(8) for p in signal(f'DAT{i}')],signal('DS'),signal('VSS'),signal('VSSQ')]
# Keep unused balls visible, grouped by function and package row.
unused=defaultdict(list)
for b,n in pins.items():
    if n in ['NC','RFU','VSF']:unused[(n,b[0])].append((b,n))
def length(groups):return sum(len(g)+1 for g in groups)
unused_sides=[[],[],[],[]]
for group in sorted(unused.values(),key=len,reverse=True):
    min(unused_sides,key=length).append(group)
# Balance height without splitting package-row groups, then restore row order.
row_order={row:i for i,row in enumerate(matrix)}
for side in unused_sides:
    side.sort(key=lambda g:(row_order[g[0][0][0]],g[0][1]))
layouts=[('Signals and power',[left,right]),
         ('Unconnected balls 1',unused_sides[:2]),
         ('Unconnected balls 2',unused_sides[2:])]
half=15.24
q=json.dumps
out=[f'(symbol {q(part)} (pin_names (offset 1.016)) (in_bom yes) (on_board yes)']
props=[('Reference','U',5.08,False),('Value',part,2.54,False),('Footprint','',0,True),('Datasheet','${KIPRJMOD}/dss/Kingston_EMMC04G-M627.pdf',0,True),('Description','Kingston 4GB eMMC, 8-bit interface, 153-ball FBGA; M06U datasheet v1.2',0,True)]
for name,value,y,hide in props:
    out.append(f'(property {q(name)} {q(value)} (at 0 {y} 0) (effects (font (size 1.27 1.27)){" hide" if hide else ""}))')
inventory=[]
for unit,(title,sides) in enumerate(layouts,1):
    height=(max(length(g) for g in sides)+3)*2.54
    out += [f'(symbol \"{part}_{unit}_1\" (unit_name {q(title)})',f'(rectangle (start {-half} 0) (end {half} {-height:.3f}) (stroke (width 0.254) (type default)) (fill (type background)))']
    for side,groups in enumerate(sides):
        row=2
        for group in groups:
            for b,n in group:
                typ='bidirectional' if n.startswith('DAT') or n=='CMD' else 'input'
                if n=='DS':typ='output'
                if n=='VDDI':typ='passive' # Internal regulator capacitor node, not a supply input.
                if n in ['VCC','VCCQ','VSS','VSSQ']:typ='power_in'
                if n in ['NC','RFU','VSF']:typ='no_connect'
                x=half+5.08 if side else -half-5.08
                out.append(f'(pin {typ} line (at {x} {-row*2.54:.3f} {180 if side else 0}) (length 5.08) (name {q(n)} (effects (font (size 1.016 1.016)))) (number {q(b)} (effects (font (size 1.016 1.016)))))')
                inventory.append([b,n,typ,unit]); row+=1
            row+=1
    out.append(')')
assert len(inventory)==153 and len({p[0] for p in inventory})==153
out+=[')']
save_symbol(part,'\n'.join(out))
with open('emmc-pin-map.csv','w') as f:
    w=csv.writer(f);w.writerow(['Ball','Signal','Electrical type','Unit']);w.writerows(inventory)
print(f'Added {part}: three units, 153 unique balls.')
