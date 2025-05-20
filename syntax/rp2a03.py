"""
Ricoh 2a03/2a07

6502 valiant used on the Famicom/NES
- decimal mode is disabled
- contains several memory-mapped registers
- contains an internal soundchip
- contains an I/O port
- can perform DMA to the NES PPU chip (expected to be mapped at $2000)
"""
from syntax.mos6502 import *

macro+="""
    # 2a03/NES Registers
    .val SQ1_VOL     $4000
    .val SQ1_SWEEP   $4001
    .val SQ1_LO      $4002
    .val SQ1_HI      $4003
    
    .val SQ2_VOL     $4004
    .val SQ2_SWEEP   $4005
    .val SQ2_LO      $4006
    .val SQ2_HI      $4007
    
    .val TRI_LINEAR  $4008
    
    .val TRI_LO      $400A
    .val TRI_HI      $400B
    
    .val NOISE_VOL   $400C
    
    .val NOISE_LO    $400E
    .val NOISE_HI    $400F

    .val DMC_FREQ    $4010
    .val DMC_RAW     $4011
    .val DMC_START   $4012
    .val DMC_LEN     $4013

    .val OAM_DMA     $4014
    .val SND_CHN     $4015
    .val APU_STATUS  $4015
    .val JOY1        $4016
    .val JOY2        $4017
    .val APU_FRAME   $4017

    .val PPU_CTRL    $2000
    .val PPU_MASK    $2001
    .val PPU_STATUS  $2002
    .val OAM_ADDR    $2003
    .val OAM_DATA    $2004
    .val PPU_SCROLL  $2005
    .val PPU_ADDR    $2006
    .val PPU_DATA    $2007
"""