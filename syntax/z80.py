"""
-- 8bit loads --

LD r,r'
LD r,n

LD r,(HL)
LD r,(IX+d)

LD r,(IY+d)

LD (HL),r
LD (IX+d),r

LD (IY+d),r

LD (HL),n
LD (IX+d),n

LD (IY+d),n

LD A,(BC)
LD A,(DE)
LD A,(nn)

LD (BC),A
LD (DE),A
LD (nn),A

LD A,I
LD A,R
LD I,A
LD R,A

-- 16bit loads --
LD dd,nn
LD IX, nn
LD IY, nn
LD HL, (nn)
LD dd, (nn)

LD IX,(nn)
LD IY,(nn)
LD (nn),HL
LD (nn),dd
LD (nn),IX
LD (nn),IY

LD SP,HL
LD SP,IX
LD SP,IY

PUSH qq
PUSH IX
PUSH IY

POP qq
POP IX
POP IY

-- EXCHANGE, BLOCK TRANSFER, BLOCK SEARCH GROUPS --
EX DE, HL
EX AF, AF`
EXX

EX (SP),HL
EX (SP),IX
EX (SP),IY

LDI

LDIR
LDD
LDDR

CPI
CPIR
CPD
CPDR

-- 8bit arithmetic and logic --
ADD A,r
ADD A,n

ADD A,(HL)
ADD A,(IX+d)

ADD A,(IY+d)

ADC A,s
SUB s
SBC A,s
AND s
OR s
XOR s
CP s

INC r
INC (HL)

INC (IX+d)
INC (IY+d)

DEC m

-- GENERAL-PURPOSE ARITHMETIC AND CPU CONTROL --
DAA
CPL
NEG

CCF

SCF

NOP

HALT

DI *
EI *
IM 0
IM 1
IM 2

-- 16bit arithmetic --
ADD HL, ss
ADC HL, ss
SBC HL, ss

ADD IX, pp
ADD IY, rr

INC ss
INC IX
INC IY

DEC ss
DEC IX
DEC IY

-- rotate and shift --
RLCA
RLA
RRCA
RRA

RLC r
RLC (HL)
RLC (IX+d)
RLC (IY+d)

RL m
RRC m
RR m
SLA m
SRA m
SRL m
RLD
RRD

-- bit set, reset and test --
BIT b,r
BIT b,(HL)
BIT b,(IX+d)
BIT b,(IY+d)
SET b,r
SET b,(HL)
SET b,(IX+d)
SET b,(IY+d)

RES b,m

-- jump --

JP nn
JP cc,nn
JR e
JR C,e
JR NC,e
JP Z,e
JR NZ,e

JP (HL)
JP (IX)
JP (IY)

DJNZ e

CALL nn
CALL cc,nn
RET
RET cc
RETI
RETN
RST p

-- input and output --
IN A,(n)
IN r,(C)
INI
INIR
IND
INR

OUT (n),A
OUT (C),r
OUTI
OTIR
OUTD
OTDR
"""