"""
KITTY Homebrew Computer (65c02)
"""
from syntax.wdc65c02 import *

macro+="""
    # Video Memory
    .val CHR        $6800
    .val PAL        $6C00
    
    # IO Registers
    .val KEY1       $7000
    .val KEY2       $7010
    .val KEY3       $7020
    .val KEY4       $7030
    .val KEY5       $7040
    
    .val BANK       $70D0
    
    .val FREQ1      $70E0
    .val FREQ2      $70E1
    .val FREQ3      $70E2
    .val FREQCTRL   $70E3
    .val VOL1       $70F0
    .val VOL2       $70F1
    .val VOL3       $70F2
    .val VOL4       $70F3
    .val WAVE1      $70F4
    .val WAVE2      $70F5
    .val WAVE3      $70F6
    .val WAVE4      $70F7
    
    # Cartridge
    .val CART   $8000
"""