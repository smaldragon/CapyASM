from . import mos6502

registers = ["A","X","Y","P","C","D","I","V"]

macro = mos6502.macro+"""
    ; 2a03/NES Registers
    var SQ1_VOL     $4000
    var SQ1_SWEEP   $4001
    var SQ1_LO      $4002
    var SQ1_HI      $4003
    
    var SQ2_VOL     $4004
    var SQ2_SWEEP   $4005
    var SQ2_LO      $4006
    var SQ2_HI      $4007
    
    var TRI_LINEAR  $4008
    ;
    var TRI_LO      $400A
    var TRI_HI      $400B
    
    var NOISE_VOL   $400C
    ;
    var NOISE_LO    $400E
    var NOISE_HI    $400F

    var DMC_FREQ    $4010
    var DMC_RAW     $4011
    var DMC_START   $4012
    var DMC_LEN     $4013

    var OAM_DMA     $4014
    var SND_CHN     $4015
    var JOY1        $4016
    var JOY2        $4017

    var PPU_CTRL    $2000
    var PPU_MASK    $2001
    var PPU_STATUS  $2002
    var OAM_ADDR    $2003
    var OAM_DATA    $2004
    var PPU_SCROLL  $2005
    var PPU_ADDR    $2006
    var PPU_DATA    $2007
"""

opcodes = mos6502.opcodes