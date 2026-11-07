"""Samsung K4B4G1646B Rev 1.0, page 6, top-view ball map."""
import csv
import json
from pathlib import Path
from library_tools import save_symbol

part = 'K4B4G1646B-HCH9'
# Columns 4, 5 and 6 are unpopulated. Negative signals retain their bars.
matrix = {
 'A':'VDDQ DQU5 DQU7 DQU4 VDDQ VSS',
 'B':'VSSQ VDD VSS DQSU DQU6 VSSQ',
 'C':'VDDQ DQU3 DQU1 ~{DQSU} DQU2 VDDQ',
 'D':'VSSQ VDDQ DMU DQU0 VSSQ VDD',
 'E':'VSS VSSQ DQL0 DML VSSQ VDDQ',
 'F':'VDDQ DQL2 DQSL DQL1 DQL3 VSSQ',
 'G':'VSSQ DQL6 ~{DQSL} VDD VSS VSSQ',
 'H':'VREFDQ VDDQ DQL4 DQL7 DQL5 VDDQ',
 'J':'NC VSS ~{RAS} CK VSS NC',
 'K':'ODT VDD ~{CAS} ~{CK} VDD CKE',
 'L':'NC ~{CS} ~{WE} A10/AP ZQ NC',
 'M':'VSS BA0 BA2 NC VREFCA VSS',
 'N':'VDD A3 A0 A12/BC BA1 VDD',
 'P':'VSS A5 A2 A1 A4 VSS',
 'R':'VDD A7 A9 A11 A6 VDD',
 'T':'VSS ~{RESET} A13 A14 A8 VSS',
}
pins = {f'{r}{c}':n for r,ns in matrix.items() for c,n in zip([1,2,3,7,8,9],ns.split(),strict=True)}
assert len(pins)==96
left = [f'A{i}' for i in range(15)]
left[10]='A10/AP'; left[12]='A12/BC'
left += ['BA0','BA1','BA2','CK','~{CK}','CKE','~{CS}','~{RAS}','~{CAS}','~{WE}','~{RESET}','ODT','VREFCA','VREFDQ','ZQ']
right = [f'DQL{i}' for i in range(8)]+['DQSL','~{DQSL}','DML']
right += [f'DQU{i}' for i in range(8)]+['DQSU','~{DQSU}','DMU']
supplies = [(b,n) for b,n in pins.items() if n in ['VDD','VDDQ']]
grounds = [(b,n) for b,n in pins.items() if n in ['VSS','VSSQ']]
nc = [(b,n) for b,n in pins.items() if n=='NC']
q=json.dumps
def signals(names):
    return [(next(b for b,n in pins.items() if n==name),name) for name in names]

# 100 mil pitch within a group; 200 mil between groups, on two sides only.
left_groups = [signals(left[:15]), signals(left[15:18]),
               signals(['CK','~{CK}','CKE']),
               signals(['~{CS}','~{RAS}','~{CAS}','~{WE}','~{RESET}','ODT']),
               signals(['VREFCA','VREFDQ']), signals(['ZQ']),
               [(b,n) for b,n in supplies if n=='VDD'],
               [(b,n) for b,n in supplies if n=='VDDQ']]
right_groups = [signals(right[:11]), signals(right[11:]), nc,
                [(b,n) for b,n in grounds if n=='VSS'],
                [(b,n) for b,n in grounds if n=='VSSQ']]
height = (max(sum(map(len,g))+len(g)-1 for g in [left_groups,right_groups])+3)*2.54
out=[f'(symbol {q(part)} (pin_names (offset 1.016)) (in_bom yes) (on_board yes)']
for name,value,y,hide in [('Reference','U',15.24,False),('Value',part,12.7,False),('Footprint','',0,True),('Datasheet','${KIPRJMOD}/dss/Samsung_K4B4G1646B_Rev1.0.pdf',0,True),('Description','Samsung 4Gbit (512MiB) 256Mx16 DDR3-1333, 1.5V, 96-FBGA 10x13.3mm pitch 0.8mm',0,True)]:
    out.append(f'(property {q(name)} {q(value)} (at 0 {y} 0) (effects (font (size 1.27 1.27)){" hide" if hide else ""}))')
half_width = 15.24  # Match the H3 DDR3 unit's 30.48 mm body width.
out += [f'(symbol "{part}_1_1"', f'(rectangle (start {-half_width} 0) (end {half_width} {-height:.3f}) (stroke (width 0.254) (type default)) (fill (type background)))']
seen=set(); inventory=[]
def pin(ball,name,x,y,angle):
    assert ball not in seen
    seen.add(ball)
    typ = 'input'
    if name.startswith(('DQL','DQU','DQSL','DQSU','~{DQS')): typ='bidirectional'
    if name in ['VDD','VDDQ','VSS','VSSQ']: typ='power_in'
    if name=='ZQ': typ='passive'
    if name=='NC': typ='no_connect'
    out.append(f'(pin {typ} line (at {x} {y} {angle}) (length 5.08) (name {q(name)} (effects (font (size 1.016 1.016)))) (number {q(ball)} (effects (font (size 1.016 1.016)))))')
    inventory.append([ball,name,typ])
for side,groups in enumerate([left_groups,right_groups]):
    row=2
    for group in groups:
        for b,n in group:
            pin(b,n,half_width+5.08 if side else -half_width-5.08,round(-row*2.54,3),180 if side else 0)
            row+=1
        row+=1
assert seen==set(pins)
out += [')',')']
save_symbol(part,'\n'.join(out))
with open('ddr3-pin-map.csv','w') as f:
    w=csv.writer(f); w.writerow(['Ball','Signal','Electrical type']); w.writerows(inventory)
print(f'Added {part}: single unit, {len(seen)} unique balls; existing symbols preserved.')
